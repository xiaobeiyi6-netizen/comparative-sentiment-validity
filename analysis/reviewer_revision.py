# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""Retrospective reviewer-requested diagnostics on existing archive labels.

No new human observations or transformer inference. Requires the same four
lawfully obtained local inputs as the original statistical audit. Public
outputs contain group/replicate aggregates only, never text or account strings.
"""
import argparse
import copy
import hashlib
import json
import platform
import re
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from revision_sensitivity import get_data, norm, rates, budget_sensitivity

SEED = 20261017
REPEATS = 200
K = 100


def metrics(reference, estimate):
    pairs = np.array(list(combinations(range(len(reference)), 2)))
    a, b = pairs.T
    gap = reference[a] - reference[b]
    predicted = estimate[a] - estimate[b]
    gap[np.abs(gap) < 1e-12] = 0
    predicted[np.abs(predicted) < 1e-12] = 0
    eligible = gap != 0
    reversal = (gap * predicted < 0) & eligible
    tied = (predicted == 0) & eligible
    den = int(eligible.sum())
    return dict(MAE_pp=float(100 * np.mean(np.abs(estimate - reference))),
                strict_pct=float(100 * reversal.sum() / den) if den else np.nan,
                half_penalty_pct=float(100 * (reversal.sum() + .5 * tied.sum()) / den) if den else np.nan,
                predicted_ties=int(tied.sum()), eligible_pairs=den,
                reference_ties=int((~eligible).sum()))


def counts(calibration, column):
    result = []
    for x in calibration:
        y, prediction = x[:, 0].astype(bool), x[:, column].astype(bool)
        result.append([(y & prediction).sum(), (y & ~prediction).sum(),
                       (~y & prediction).sum(), (~y & ~prediction).sum()])
    return np.asarray(result, float)


def estimate_methods(calibration, evaluated, column, rule):
    c = counts(calibration, column)
    pooled = c.sum(axis=0)
    pt = (pooled[0] + .5) / (pooled[0] + pooled[1] + 1)
    pf = (pooled[2] + .5) / (pooled[2] + pooled[3] + 1)
    pos, neg = c[:, 0] + c[:, 1], c[:, 2] + c[:, 3]
    jt, jf = (c[:, 0] + .5) / (pos + 1), (c[:, 2] + .5) / (neg + 1)
    if rule == 'blend_Jeffreys':
        st, sf = (pos * jt + K * pt) / (pos + K), (neg * jf + K * pf) / (neg + K)
    elif rule == 'augmented_Jeffreys':
        st = (c[:, 0] + .5 + K * pt) / (pos + 1 + K)
        sf = (c[:, 2] + .5 + K * pf) / (neg + 1 + K)
    else:
        raise ValueError(rule)
    q = np.array([x[:, column].mean() for x in evaluated])
    human = np.array([x[:, 0].mean() for x in calibration])

    def adjust(t, f):
        denominator = t - f
        bad = np.abs(denominator) < .10
        adjusted = np.clip((q - f) / np.where(bad, 1, denominator), 0, 1)
        return np.where(bad, q, adjusted), int(np.sum(bad))

    ep, fp = adjust(np.repeat(pt, len(q)), np.repeat(pf, len(q)))
    eg, fg = adjust(st, sf)
    return {'CC': (q, 0), 'Pooled ACC': (ep, fp),
            'Group ACC': (eg, fg), 'Human-only': (human, 0)}


def run_budget(data, corpus, mode, repeats=REPEATS):
    """Common nested sampling, tie rules, correction and fallback for both corpora."""
    groups = sorted(data.group.unique())
    arrays = [data[data.group == g][['human_negative', 'VADER', 'RoBERTa']].to_numpy(int) for g in groups]
    full = np.array([x[:, 0].mean() for x in arrays])
    budgets = [25, 50, 100, 200, 400] if corpus == 'Airline' and mode != 'account_holdout' else [25, 50, 100]
    rng = np.random.default_rng(SEED)
    all_accounts = pd.unique(data.account)
    account_index = pd.Index(all_accounts)
    account_codes = [account_index.get_indexer(data.loc[data.group == g, 'account']) for g in groups]
    assert not data.account.isna().any()
    rows, allocations, skipped = [], [], []
    for repeat in range(repeats):
        held, pool = [], []
        if mode == 'account_holdout':
            selected_codes = rng.permutation(len(all_accounts))[:int(np.ceil(.2 * len(all_accounts)))]
            selected_mask = np.zeros(len(all_accounts), bool)
            selected_mask[selected_codes] = True
            for x, ac in zip(arrays, account_codes):
                hold_mask = selected_mask[ac]
                held.append(x[hold_mask])
                candidates = x[~hold_mask]
                pool.append(candidates[rng.permutation(len(candidates))])
            # Same account never appears on both sides anywhere in a corpus.
            assert all(not selected_mask[ac[~selected_mask[ac]]].any() for ac in account_codes)
        elif mode == 'message_holdout':
            for x in arrays:
                ix = rng.permutation(len(x)); nt = int(np.ceil(.2 * len(x)))
                held.append(x[ix[:nt]]); pool.append(x[ix[nt:]])
        elif mode == 'finite_archive':
            pool = [x[rng.permutation(len(x))] for x in arrays]
        else:
            raise ValueError(mode)
        for budget in budgets:
            if any(len(x) < budget for x in pool) or (mode != 'finite_archive' and any(len(x) == 0 for x in held)):
                skipped.append(dict(corpus=corpus, mode=mode, repeat=repeat, budget=budget))
                continue
            cal = [x[:budget] for x in pool]
            evaluation = [x[budget:] for x in pool] if mode == 'finite_archive' else held
            assert all(len(x) > 0 for x in evaluation)
            target = full if mode == 'finite_archive' else np.array([x[:, 0].mean() for x in evaluation])
            for g, original, p, ev in zip(groups, arrays, pool, evaluation):
                allocations.append(dict(corpus=corpus, mode=mode, repeat=repeat, budget=budget, group=g,
                    archive_n=len(original), calibration_pool_n=len(p), evaluation_n=len(ev),
                    labeled_archive_pct=100 * budget / len(original), labeled_pool_pct=100 * budget / len(p)))
            rules = ['blend_Jeffreys', 'augmented_Jeffreys'] if mode == 'message_holdout' else ['augmented_Jeffreys']
            for column, model in [(1, 'VADER'), (2, 'RoBERTa')]:
                for rule in rules:
                    estimates = estimate_methods(cal, evaluation, column, rule)
                    for method, (estimate, fallback) in estimates.items():
                        if mode == 'finite_archive' and method != 'Human-only':
                            # Paid labels are used exactly; correct only unlabeled remainder.
                            n = np.array([len(x) for x in arrays])
                            h = np.array([x[:, 0].mean() for x in cal])
                            estimate = (budget * h + (n - budget) * estimate) / n
                            method = 'Label-assisted CC' if method == 'CC' else method
                        rows.append(dict(corpus=corpus, mode=mode, repeat=repeat, budget=budget,
                            model=model, rule=rule, method=method, fallback_groups=fallback,
                            **metrics(target, estimate)))
                    if mode == 'finite_archive':
                        q = np.array([x[:, column].mean() for x in arrays])
                        rows.append(dict(corpus=corpus, mode=mode, repeat=repeat, budget=budget,
                            model=model, rule=rule, method='Raw CC (no labels)', fallback_groups=0,
                            **metrics(full, q)))
    return pd.DataFrame(rows), pd.DataFrame(allocations), skipped


def summarize(runs):
    keys = ['corpus', 'mode', 'budget', 'model', 'rule', 'method']
    agg = {'repetitions': ('repeat', 'nunique')}
    for col in ['MAE_pp', 'strict_pct', 'half_penalty_pct', 'predicted_ties', 'eligible_pairs', 'reference_ties', 'fallback_groups']:
        agg[col + '_mean'] = (col, 'mean')
        agg[col + '_q025'] = (col, lambda x: x.quantile(.025))
        agg[col + '_q975'] = (col, lambda x: x.quantile(.975))
    return runs.groupby(keys, as_index=False).agg(**agg)


def paired_bootstrap(data, out):
    """Fresh paired within-candidate bootstrap with a fully specified seed."""
    groups=sorted(data.group.unique())
    arrays=[data[data.group==g][['human_negative','VADER','RoBERTa']].to_numpy(int) for g in groups]
    pairs=np.array(list(combinations(range(len(groups)),2)));aa,bb=pairs.T
    full=np.array([x[:,0].mean() for x in arrays]);original=full[aa]-full[bb]
    sign_stable=np.zeros(len(pairs),int)
    rng=np.random.default_rng(SEED); rows=[]
    for repeat in range(5000):
        shares=np.stack([x[rng.integers(0,len(x),len(x))].mean(axis=0) for x in arrays])
        reference=shares[:,0];gap=reference[aa]-reference[bb]
        sign_stable += ((gap*original)>0)
        one={}
        for column,model in [(1,'VADER'),(2,'RoBERTa')]:
            one[model]=metrics(reference,shares[:,column])
            rows.append(dict(repeat=repeat,model=model,**one[model]))
        rows.append(dict(repeat=repeat,model='VADER minus RoBERTa',
            **{col:one['VADER'][col]-one['RoBERTa'][col] for col in one['VADER']}))
    runs=pd.DataFrame(rows); runs.to_csv(out/'gop_paired_bootstrap_replicates.csv',index=False)
    summary=[]
    for model,d in runs.groupby('model'):
        r={'model':model,'repetitions':5000,'seed':SEED}
        for col in ['MAE_pp','strict_pct','half_penalty_pct']:
            r[col+'_mean']=d[col].mean();r[col+'_q025']=d[col].quantile(.025);r[col+'_q975']=d[col].quantile(.975)
        summary.append(r)
    summary=pd.DataFrame(summary); summary.to_csv(out/'gop_paired_bootstrap_summary.csv',index=False)
    stable=pd.DataFrame({'a':[groups[a] for a in aa],'b':[groups[b] for b in bb],
        'original_reference_gap_pp':100*original,'reference_sign_agreement_pct':100*sign_stable/5000})
    stable.to_csv(out/'gop_bootstrap_reference_sign_stability.csv',index=False)
    return summary


def native_ties(air, gop, out):
    output = []
    for corpus, data in [('Airline', air), ('GOP', gop)]:
        budget_sensitivity(data, corpus, out)
        d = pd.read_csv(out / (corpus.lower() + '_sensitivity_splits.csv'))
        d = d[(d.k == -1) | ((d.method == 'Group ACC') & (d.k == 100))].copy()
        den = (15 - d.reference_ties) if corpus == 'Airline' else 45
        d['half_penalty_pct'] = 100 * (d.reversal_all + .5 * d.predicted_ties / den)
        for (budget, model, method), x in d.groupby(['budget', 'model', 'method']):
            output.append(dict(corpus=corpus, budget=budget, model=model, method=method,
                repetitions=x.repeat.nunique(), MAE_pp=x.MAE_pp.mean(), strict_pct=100*x.reversal_all.mean(),
                predicted_ties=x.predicted_ties.mean(), reference_ties=x.reference_ties.mean(),
                half_penalty_pct=x.half_penalty_pct.mean()))
        if corpus == 'Airline':
            p = d[(d.budget == 400) & (d.model == 'RoBERTa')].pivot(index='repeat', columns='method', values='reversal_all')
            a, b = p['Group ACC'], p['CC']
            (out / 'airline_roberta_paired_ranking_changes.json').write_text(json.dumps({
                'budget':400, 'repetitions':len(p), 'group_ACC_better_than_CC':int((a<b).sum()),
                'group_ACC_tied_with_CC':int((a==b).sum()),'group_ACC_worse_than_CC':int((a>b).sum())},indent=2))
    return pd.DataFrame(output)


def duplicate_audit(raw_airline, raw_gop, air):
    output = []
    candidate = raw_gop.candidate.fillna('').astype(str).str.strip()
    eligible = raw_gop[~candidate.str.casefold().isin({'no candidate mentioned', ''})].copy()
    for corpus, d, group, label in [('Airline',raw_airline,'airline','airline_sentiment'), ('GOP',eligible,'candidate','sentiment')]:
        z = d.copy(); z['normalized'] = z.text.map(norm)
        dup = z.groupby('normalized').agg(records=(label,'size'), labels=(label,'nunique'), groups=(group,'nunique'))
        tweet_dups = z.groupby('tweet_id').size()
        output.append(dict(corpus=corpus, records=len(z), unique_normalized_texts=len(dup),
            surplus_rows=int((dup.records-1).sum()), repeated_text_groups=int((dup.records>1).sum()),
            label_conflict_groups=int(((dup.records>1)&(dup.labels>1)).sum()),
            cross_group_texts=int((dup.groups>1).sum()), repeated_tweet_id_groups=int((tweet_dups>1).sum()),
            surplus_tweet_id_rows=int((tweet_dups-1).sum())))
    # First-occurrence airline counterpart uses existing labels/predictions, no inference.
    keep = ~raw_airline.text.map(norm).duplicated()
    variants = pd.DataFrame([dict(variant='Airline unique normalized texts',**r) for r in rates(air[keep])])
    return pd.DataFrame(output), variants


def vader_diagnostics(raw, archive, out):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    import vaderSentiment
    analyzer = SentimentIntensityAnalyzer()
    ablated = copy.deepcopy(analyzer); ablated.lexicon.pop('united')
    def placeholders(t):
        tokens=[]
        for w in t.split(' '):
            w = '@user' if w.startswith('@') and len(w)>1 else w
            w = 'http' if w.startswith('http') else w
            tokens.append(w)
        return ' '.join(tokens)
    variants = {
        'Original input':(lambda t:t,analyzer),
        'All mention placeholders':(lambda t:re.sub(r'@[A-Za-z0-9_]+','@user',t),analyzer),
        'URL placeholders':(lambda t:re.sub(r'https?://\S+','http',t),analyzer),
        'Model-card token placeholders':(placeholders,analyzer),
        'United handle only masked':(lambda t:re.sub(r'@united\b','@airline',t,flags=re.I),analyzer),
        'Bare United only masked':(lambda t:re.sub(r'(?<![\w@#])united\b','airline',t,flags=re.I),analyzer),
        'United lexicon entry removed':(lambda t:t,ablated),
    }
    y=(raw.airline_sentiment=='negative').to_numpy()
    details, total=[],[]
    original_prediction=None
    for name,(transform,v) in variants.items():
        q=np.array([v.polarity_scores(transform(t))['compound']<=-.05 for t in raw.text.astype(str)])
        if name=='Original input':
            assert np.array_equal(q,(archive.vader==0).to_numpy()),'New VADER did not match archived labels'
            original_prediction=q
        z=pd.DataFrame({'group':raw.airline,'human_negative':y.astype(int),'VADER':q.astype(int),'RoBERTa':q.astype(int)})
        total.append(dict(variant=name,**rates(z)[0],binary_changes_from_original=int((q!=original_prediction).sum())))
        for g, ix in raw.groupby('airline').groups.items():
            yy, pp=y[ix],q[ix]
            tp=int((yy&pp).sum());fn=int((yy&~pp).sum());fp=int((~yy&pp).sum());tn=int((~yy&~pp).sum())
            details.append(dict(variant=name,group=g,n=len(ix),TP=tp,FN=fn,FP=fp,TN=tn,
                reference_pct=100*yy.mean(),predicted_pct=100*pp.mean(),bias_pp=100*(pp.mean()-yy.mean()),
                negative_recall_pct=100*tp/(tp+fn),binary_accuracy_pct=100*(tp+tn)/len(ix),
                changed_predictions=int((pp!=original_prediction[ix]).sum()),
                recovered_original_false_negatives=int((yy&~original_prediction[ix]&pp).sum()),
                newly_missed_negatives=int((yy&original_prediction[ix]&~pp).sum())))
    united=raw.airline.eq('United').to_numpy()
    feature={
        'United handle':raw.text.str.contains(r'@united\b',case=False,regex=True).to_numpy(),
        'Bare United':raw.text.str.contains(r'(?<![\w@#])united\b',case=False,regex=True).to_numpy(),
        'Any leading mention':raw.text.str.contains(r'^\s*@',regex=True).to_numpy(),
        'URL':raw.text.str.contains(r'https?://',regex=True).to_numpy(),
        'Retweet text prefix':raw.text.str.contains(r'^\s*RT\s',case=False,regex=True).to_numpy(),
    }
    features=[]
    for name,mask in feature.items():
        for flag in [True,False]:
            ix=united&(mask==flag);npos=int((y&ix).sum());fn=int((y&ix&~original_prediction).sum())
            features.append(dict(feature=name,present=flag,n=int(ix.sum()),human_negatives=npos,
                original_false_negatives=fn,false_negative_rate_pct=100*fn/npos if npos else np.nan))
    return pd.DataFrame(details),pd.DataFrame(total),pd.DataFrame(features)


def main():
    p=argparse.ArgumentParser();p.add_argument('--inputs',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();out=args.out;out.mkdir(parents=True,exist_ok=True)
    air,gop,audit,_=get_data(args.inputs)
    raw=pd.read_csv(args.inputs/'Tweets.csv');rg=pd.read_csv(args.inputs/'GOP_REL_ONLY.csv');pred=pd.read_csv(args.inputs/'airline_predictions.csv')
    expected={'airline_predictions.csv':'5674f3e56dc3667344ab43c867ee8dd4f61126823950524c3f5cd54d92f9eda2',
              'gop_external_validation_results.zip':'8a93da7db63b6d2f5c0c2daec0faabdbab0b8cf7be415b1af30e3d49636968e7'}
    for f,h in expected.items():assert hashlib.sha256((args.inputs/f).read_bytes()).hexdigest()==h
    allocations=[]
    for corpus,d in [('Airline',air),('GOP',gop)]:
        for g,x in d.groupby('group'):
            n=len(x); nt=int(np.ceil(.2*n)) if corpus=='Airline' else round(.2*n)
            for b in ([25,50,100,200,400] if corpus=='Airline' else [25,50,100]):
                allocations.append(dict(corpus=corpus,group=g,archive_n=n,evaluation_n=nt,
                    calibration_pool_n=n-nt,budget=b,labeled_archive_pct=100*b/n,labeled_pool_pct=100*b/(n-nt)))
    pd.DataFrame(allocations).to_csv(out/'label_allocations.csv',index=False)
    duplicates,variant=duplicate_audit(raw,rg,air)
    duplicates.to_csv(out/'duplicate_provenance_diagnostics.csv',index=False);variant.to_csv(out/'airline_duplicate_sensitivity.csv',index=False)
    diag,glob,features=vader_diagnostics(raw,pred,out)
    diag.to_csv(out/'vader_input_diagnostics_groups.csv',index=False);glob.to_csv(out/'vader_input_diagnostics_summary.csv',index=False)
    features.to_csv(out/'united_false_negative_features.csv',index=False)
    print('VADER input diagnostics completed',flush=True)
    native_ties(air,gop,out).to_csv(out/'native_budget_ties.csv',index=False)
    print('Native budget tie audits completed',flush=True)
    paired_bootstrap(gop,out)
    print('Fresh 5,000 paired GOP bootstrap replicates completed',flush=True)
    all_summaries=[];all_skipped=[]
    for mode in ['message_holdout','finite_archive','account_holdout']:
        parts=[];alloc=[]
        for corpus,d in [('Airline',air),('GOP',gop)]:
            r,a,s=run_budget(d,corpus,mode);parts.append(r);alloc.append(a);all_skipped+=s
            print(corpus,mode,'completed',len(r),'aggregate replicate rows',flush=True)
        runs=pd.concat(parts,ignore_index=True);summary=summarize(runs);all_summaries.append(summary)
        runs.to_csv(out/(mode+'_replicates.csv'),index=False);summary.to_csv(out/(mode+'_summary.csv'),index=False)
        pd.concat(alloc,ignore_index=True).to_csv(out/(mode+'_allocations.csv'),index=False)
    summary=pd.concat(all_summaries,ignore_index=True);summary.to_csv(out/'all_common_budget_summaries.csv',index=False)
    metadata={'design':'retrospective reuse of released human labels; no new human annotation',
        'seed':SEED,'repetitions':REPEATS,'k':K,'nested_budgets':True,'holdout_rounding':'ceil(.2*n) in both corpora for common message protocol',
        'tie_rule':'exclude reference ties; report strict reversals and predicted ties; half penalty on ties',
        'account_split':'global 20% of observed distinct account names without replacement; all messages of a selected account held out across groups',
        'account_split_budgets':[25,50,100],'infeasible_split_budget_cells':all_skipped,
        'finite_archive_target':'known sampled labels enter exactly; corrections apply only to unlabeled complement; human-only is random-sample proportion',
        'primary_results_replaced':False,'new_transformer_inference':False,'python':platform.python_version(),
        'numpy':np.__version__,'pandas':pd.__version__,'source_checks':audit}
    (out/'reviewer_revision_protocol.json').write_text(json.dumps(metadata,indent=2))
    print('All diagnostics complete; infeasible cells:',len(all_skipped),flush=True)


if __name__=='__main__':main()
