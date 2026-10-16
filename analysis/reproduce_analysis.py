#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""Re-aggregate archived predictions: audit group-specific errors and simulate limited-label calibration
on already-human-annotated real GOP tweets, with leakage-free held-out evaluation.

Not a new participant study or newly collected manual labels. No model retraining.
"""
from __future__ import annotations
import hashlib, io, json, zipfile, pathlib, os
import numpy as np
import pandas as pd

ROOT = pathlib.Path(os.environ.get('SCIE_DATA_ROOT', str(pathlib.Path(__file__).resolve().parents[1] / 'private_inputs')))
OUT = pathlib.Path(os.environ.get('SCIE_OUTPUT_DIR', str(pathlib.Path(__file__).resolve().parents[1] / 'reproduced_outputs')))
OUT.mkdir(parents=True, exist_ok=True)
SEED = 20261016
REPS = 200
BUDGETS = [25, 50, 100]
HOLDOUT_FRACTION = 0.20
SHRINK_PSEUDOCOUNT = 100.0  # match airline reported protocol
MIN_ACC_CONTRAST = 0.10
JEFFREYS_CELL = 0.5

# Original source provenance; verified by the restoration and previous audits.
EXPECTED_SHA = {
    'Tweets.csv':'ea94b23f41892b290dec3330bb8cf9cb6b8bc669eaae5f3a84c40f7b0de8f15e',
    'GOP_REL_ONLY.csv':'413bae11a4b04a414baffb63407788a3231a06b8ab806caaf9f930b5e2acec86',
}
for fn, digest in EXPECTED_SHA.items():
    actual = hashlib.sha256((ROOT/fn).read_bytes()).hexdigest()
    if actual != digest:
        raise ValueError(f'Raw source integrity failure: {fn}: {actual} != {digest}')

# Verify the airline alignment at the individual row level.
raw_a = pd.read_csv(ROOT/'Tweets.csv', low_memory=False)
pa = pd.read_csv(ROOT/'airline_predictions.csv', low_memory=False)
assert len(raw_a)==len(pa)==14640
assert (raw_a['text'].astype(str).map(lambda x:hashlib.sha256(x.encode('utf-8')).hexdigest()).to_numpy() == pa['text_sha256'].to_numpy()).all()
label_map = {'negative':0,'neutral':1,'positive':2}
assert (raw_a['airline_sentiment'].map(label_map).to_numpy() == pa['reference'].to_numpy()).all()
airline = pd.DataFrame({
    'group':raw_a.airline.astype(str),
    'human_negative':(pa.reference==0).astype('int8'),
    'VADER':(pa.vader==0).astype('int8'),
    'RoBERTa':(pa.roberta==0).astype('int8'),
})

with zipfile.ZipFile(ROOT/'gop_external_validation_results.zip') as z:
    gpred = pd.read_csv(io.BytesIO(z.read('gop_external_validation_results/row_predictions_and_overlap_flags.csv')))
raw_g = pd.read_csv(ROOT/'GOP_REL_ONLY.csv',low_memory=False)
raw_g['sha_text'] = raw_g['text'].astype(str).map(lambda x:hashlib.sha256(x.encode('utf-8')).hexdigest())
raw_keys = set(zip(raw_g.candidate.astype(str),raw_g.sha_text,raw_g.sentiment.astype(str)))
assert len(gpred)==4483 and not gpred.text_sha256.duplicated().any()
assert all((c,h,s) in raw_keys for c,h,s in zip(gpred.candidate,gpred.text_sha256,gpred.sentiment))
gop = gpred[['candidate','human_negative','VADER','RoBERTa']].rename(columns={'candidate':'group'}).copy()
for col in ['human_negative','VADER','RoBERTa']:
    assert set(gop[col].unique()) <= {0,1}

# Observed group rates, full confusion tables and strict pairwise decomposition.
def group_mechanism(data:pd.DataFrame, corpus:str):
    group_rows=[]
    for group, d in data.groupby('group', sort=True):
        y=d.human_negative.to_numpy()
        p=y.mean()
        for model in ['VADER','RoBERTa']:
            hat=d[model].to_numpy()
            tp=int(((y==1)&(hat==1)).sum()); fn=int(((y==1)&(hat==0)).sum())
            fp=int(((y==0)&(hat==1)).sum()); tn=int(((y==0)&(hat==0)).sum())
            tpr=tp/(tp+fn); fpr=fp/(fp+tn); fnr=1-tpr
            q=hat.mean(); bias=q-p
            false_pos_component=(1-p)*fpr
            false_neg_component=-p*fnr
            assert abs(bias-(false_pos_component+false_neg_component)) < 1e-12
            group_rows.append(dict(corpus=corpus, group=group, model=model, n=len(d),
                                   TP=tp, FN=fn, FP=fp, TN=tn, gold_negative_prop=p,
                                   pred_negative_prop=q, bias_pp=bias*100,
                                   TPR=tpr,FPR=fpr,FNR=fnr,
                                   false_positive_component_pp=false_pos_component*100,
                                   false_negative_component_pp=false_neg_component*100,
                                   identity_error_pp=(q-p-false_pos_component-false_neg_component)*100))
    m=pd.DataFrame(group_rows)
    pair_rows=[]
    from itertools import combinations
    groups=sorted(m.group.unique())
    for a,b in combinations(groups,2):
        for model in ['VADER','RoBERTa']:
            aa=m[(m.group==a)&(m.model==model)].iloc[0]
            bb=m[(m.group==b)&(m.model==model)].iloc[0]
            gdiff=100*(aa.gold_negative_prop-bb.gold_negative_prop)
            pdiff=100*(aa.pred_negative_prop-bb.pred_negative_prop)
            bias_d=aa.bias_pp-bb.bias_pp
            assert abs(pdiff-(gdiff+bias_d)) < 1e-8
            rev=bool(gdiff*pdiff<0)
            pair_rows.append(dict(corpus=corpus,model=model,group_a=a,group_b=b,
                                  gold_diff_pp=gdiff,pred_diff_pp=pdiff,
                                  reference_abs_gap_pp=abs(gdiff),bias_difference_pp=bias_d,
                                  bias_a_pp=aa.bias_pp,bias_b_pp=bb.bias_pp,
                                  reversed=int(rev),
                                  fp_component_difference_pp=aa.false_positive_component_pp-bb.false_positive_component_pp,
                                  fn_component_difference_pp=aa.false_negative_component_pp-bb.false_negative_component_pp))
    pairs=pd.DataFrame(pair_rows)
    return m,pairs
am,ap = group_mechanism(airline,'Airline')
gm,gp = group_mechanism(gop,'GOP')
mech=pd.concat([am,gm],ignore_index=True); pairs=pd.concat([ap,gp],ignore_index=True)
mech.to_csv(OUT/'group_confusion_error_decomposition.csv',index=False)
pairs.to_csv(OUT/'pairwise_bias_reversal_mechanism.csv',index=False)
summary_pairs = pairs.groupby(['corpus','model']).agg(n_pairs=('reversed','size'),
    reversals=('reversed','sum'),large_gap_10pp_pairs=('reference_abs_gap_pp',lambda s:int((s>=10).sum()))).reset_index()
summary_pairs['large_gap_10pp_reversals']=[int(pairs[(pairs.corpus==r.corpus)&(pairs.model==r.model)&(pairs.reference_abs_gap_pp>=10)].reversed.sum()) for r in summary_pairs.itertuples()]
summary_pairs.to_csv(OUT/'observed_reversal_mechanism_summary.csv',index=False)

# Same-budget GOP-only calibration from already available human labels.
# Each repeated split takes 20% within each candidate as an untouched holdout.
# A *fixed* random permutation of the remaining texts yields nested 25/50/100 budgets.
# All rates and human-only estimates are from calibration labels, never holdout labels.
def confusion_counts(d, model):
    y=d.human_negative.to_numpy(); pred=d[model].to_numpy()
    return (int(((y==1)&(pred==1)).sum()),int(((y==1)&(pred==0)).sum()),
            int(((y==0)&(pred==1)).sum()),int(((y==0)&(pred==0)).sum()))

def jeffreys_rates(counts):
    tp,fn,fp,tn=counts
    return ((tp+JEFFREYS_CELL)/(tp+fn+2*JEFFREYS_CELL),
            (fp+JEFFREYS_CELL)/(fp+tn+2*JEFFREYS_CELL))

def acc(q,tpr,fpr):
    if abs(tpr-fpr) < MIN_ACC_CONTRAST:
        return q, True
    return float(np.clip((q-fpr)/(tpr-fpr),0,1)),False

rng=np.random.default_rng(SEED)
groups=sorted(gop.group.unique())
group_indices={name:gop.index[gop.group==name].to_numpy() for name in groups}
assert min(len(v) for v in group_indices.values())>=181
full_gold=gop.groupby('group').human_negative.mean()
from itertools import combinations
all_pairs=list(combinations(groups,2))
large_gap_pairs=[(a,b) for a,b in all_pairs if abs(full_gold[a]-full_gold[b]) >= .10]
assert len(all_pairs)==45

repeat_rows=[]; detail_rows=[]
for rep in range(REPS):
    cal_perm={}; hold_indices={}
    for name,ind in group_indices.items():
        perm=rng.permutation(ind)
        hold_n=round(len(ind)*HOLDOUT_FRACTION)
        hold_indices[name]=perm[:hold_n]
        cal_perm[name]=perm[hold_n:]
        assert len(cal_perm[name])>=max(BUDGETS)
    held={name:gop.loc[ind] for name,ind in hold_indices.items()}
    held_gold={name:float(d.human_negative.mean()) for name,d in held.items()}
    reference_sign_changes=sum(np.sign(held_gold[a]-held_gold[b]) != np.sign(full_gold[a]-full_gold[b]) for a,b in all_pairs)
    for budget in BUDGETS:
        cal={name:gop.loc[ind[:budget]] for name,ind in cal_perm.items()}
        for model in ['VADER','RoBERTa']:
            per_counts={name:confusion_counts(d,model) for name,d in cal.items()}
            pooled_counts=tuple(sum(v[k] for v in per_counts.values()) for k in range(4))
            pooled_tpr,pooled_fpr=jeffreys_rates(pooled_counts)
            preds={name:{} for name in groups}; fallbacks={method:0 for method in ['CC','ACC_pooled','ACC_group_shrunk','Human_only']}
            for name in groups:
                sample=cal[name]; test=held[name]
                q=float(test[model].mean()); human_only=float(sample.human_negative.mean())
                tp,fn,fp,tn=per_counts[name]
                # Shrink conditional rates using a fixed pseudocount mass of 100 for each denominator.
                g_tpr=(tp+JEFFREYS_CELL+SHRINK_PSEUDOCOUNT*pooled_tpr)/(tp+fn+2*JEFFREYS_CELL+SHRINK_PSEUDOCOUNT)
                g_fpr=(fp+JEFFREYS_CELL+SHRINK_PSEUDOCOUNT*pooled_fpr)/(fp+tn+2*JEFFREYS_CELL+SHRINK_PSEUDOCOUNT)
                pooled_est,f_pool=acc(q,pooled_tpr,pooled_fpr)
                shrink_est,f_shrink=acc(q,g_tpr,g_fpr)
                preds[name]={'CC':q,'ACC_pooled':pooled_est,'ACC_group_shrunk':shrink_est,'Human_only':human_only}
                fallbacks['ACC_pooled']+=int(f_pool);fallbacks['ACC_group_shrunk']+=int(f_shrink)
                if rep==0:
                    detail_rows.append(dict(rep=rep,budget_per_group=budget,model=model,group=name,
                                            n_calibration=len(sample),n_holdout=len(test),gold_holdout=held_gold[name],
                                            cal_human_rate=human_only,CC=q,ACC_pooled=pooled_est,
                                            ACC_group_shrunk=shrink_est,Human_only=human_only,
                                            cal_TP=tp,cal_FN=fn,cal_FP=fp,cal_TN=tn,
                                            pooled_TPR=pooled_tpr,pooled_FPR=pooled_fpr,
                                            shrunk_TPR=g_tpr,shrunk_FPR=g_fpr))
            for method in ['CC','ACC_pooled','ACC_group_shrunk','Human_only']:
                err=np.array([abs(preds[name][method]-held_gold[name])*100 for name in groups])
                reverse_pairs=[(a,b) for a,b in all_pairs if (held_gold[a]-held_gold[b])*(preds[a][method]-preds[b][method])<0]
                reverse_gap10=[(a,b) for a,b in large_gap_pairs if (held_gold[a]-held_gold[b])*(preds[a][method]-preds[b][method])<0]
                ties=sum(preds[a][method]==preds[b][method] and held_gold[a]!=held_gold[b] for a,b in all_pairs)
                ties_strong=sum(preds[a][method]==preds[b][method] and held_gold[a]!=held_gold[b] for a,b in large_gap_pairs)
                repeat_rows.append(dict(repeat=rep,budget_per_group=budget,total_calibration_labels=budget*len(groups),
                   model=model,method=method,mean_absolute_error_pp=float(err.mean()),
                   median_absolute_error_pp=float(np.median(err)),
                   reversal_count_all=len(reverse_pairs),reversal_rate_all=len(reverse_pairs)/len(all_pairs),
                   reversal_count_fixed_gap10=len(reverse_gap10),
                   fixed_gap10_pairs=len(large_gap_pairs),
                   reversal_rate_fixed_gap10=len(reverse_gap10)/len(large_gap_pairs),
                   reference_order_disagreements_vs_full=reference_sign_changes,
                   ties_all=ties,ties_fixed_gap10=ties_strong,
                   reversal_plus_half_ties_all=(len(reverse_pairs)+0.5*ties)/len(all_pairs),
                   reversal_plus_half_ties_fixed_gap10=(len(reverse_gap10)+0.5*ties_strong)/len(large_gap_pairs),
                   acc_fallback_groups=fallbacks[method]))

rep=pd.DataFrame(repeat_rows)
rep.to_csv(OUT/'gop_calibration_200_repeated_splits.csv',index=False)
pd.DataFrame(detail_rows).to_csv(OUT/'gop_calibration_first_split_group_detail.csv',index=False)

sumrows=[]
for (budget,model,method), d in rep.groupby(['budget_per_group','model','method'],sort=True):
    row=dict(budget_per_group=int(budget),model=model,method=method,n_repetitions=len(d),
             total_calibration_labels=int(budget)*len(groups))
    for metric in ['mean_absolute_error_pp','reversal_rate_all','reversal_rate_fixed_gap10','reversal_plus_half_ties_all','reversal_plus_half_ties_fixed_gap10','ties_all','acc_fallback_groups']:
        vals=d[metric].to_numpy();row[metric+'_mean']=float(vals.mean())
        row[metric+'_q025']=float(np.quantile(vals,.025));row[metric+'_q975']=float(np.quantile(vals,.975))
    sumrows.append(row)
summ=pd.DataFrame(sumrows)
summ.to_csv(OUT/'gop_calibration_budget_summary.csv',index=False)

pairs_d=[]
for (budget,model), d in rep.groupby(['budget_per_group','model']):
    pivot=d.pivot(index='repeat',columns='method',values=['mean_absolute_error_pp','reversal_rate_all','reversal_rate_fixed_gap10','reversal_plus_half_ties_all','reversal_plus_half_ties_fixed_gap10'])
    for target in ['ACC_pooled','ACC_group_shrunk','Human_only']:
        for metric in ['mean_absolute_error_pp','reversal_rate_all','reversal_rate_fixed_gap10','reversal_plus_half_ties_all','reversal_plus_half_ties_fixed_gap10']:
            v=(pivot[metric][target]-pivot[metric]['CC']).to_numpy()
            pairs_d.append(dict(budget_per_group=int(budget),model=model,comparison=f'{target} minus CC',metric=metric,
                                mean_difference=float(v.mean()),q025=float(np.quantile(v,.025)),q975=float(np.quantile(v,.975)),
                                fraction_better=float((v<-1e-10).mean()),fraction_equal=float((abs(v)<=1e-10).mean()),
                                fraction_worse=float((v>1e-10).mean())))
        # Direct human estimate is an essential benchmark, compare subgroup ACC against human-only.
    for metric in ['mean_absolute_error_pp','reversal_rate_all','reversal_rate_fixed_gap10','reversal_plus_half_ties_all','reversal_plus_half_ties_fixed_gap10']:
        v=(pivot[metric]['ACC_group_shrunk']-pivot[metric]['Human_only']).to_numpy()
        pairs_d.append(dict(budget_per_group=int(budget),model=model,
                            comparison='ACC_group_shrunk minus Human_only',metric=metric,
                            mean_difference=float(v.mean()),q025=float(np.quantile(v,.025)),q975=float(np.quantile(v,.975)),
                            fraction_better=float((v<-1e-10).mean()),fraction_equal=float((abs(v)<=1e-10).mean()),
                            fraction_worse=float((v>1e-10).mean())))
pair_cmp=pd.DataFrame(pairs_d);pair_cmp.to_csv(OUT/'gop_calibration_paired_differences.csv',index=False)

# Same set of record IDs never enters calibration and heldout in one split.
record = dict(
  audited_corpora={'airline':len(airline),'gop_primary_unique':len(gop)},
  raw_sha256=EXPECTED_SHA,
  alignment={'airline_text_hash_matches':len(airline),'airline_label_matches':len(airline),
             'gop_source_text_candidate_label_matches':len(gop)},
  calibration={'design':'post-hoc repeated heldout annotation-budget simulation on a single already-labeled archive',
       'seed':SEED,'repetitions':REPS,'holdout_fraction':HOLDOUT_FRACTION,
       'budgets_per_group':BUDGETS,'groups':len(groups),'comparisons_all':len(all_pairs),
       'original_reference_gap10_pairs':len(large_gap_pairs),'Jeffreys_pseudocount_per_cell':JEFFREYS_CELL,
       'shrinkage_prior_conditional_denominator':SHRINK_PSEUDOCOUNT,
       'ACC_fallback_threshold':MIN_ACC_CONTRAST,'overlap_within_repeat':'none',
       'reference_pair_thresholds':'fixed by original complete GOP gold reference rates',
       'model_predictions_rerun':False},
  cautions=['Repeated splits share observations and are not independent studies.',
           'Holdout group labels are only used to evaluate estimators, not fit or tune them.',
           'Original full GOP labels determine fixed strong-gap comparison set; analysis is retrospective, not preregistered.',
           'Models predict tweet-level polarity, not sentiment directed at candidate.',
           'Bootstrap or split quantiles are conditional on one archive, not population confidence intervals.',
           'Comparison to airline is across different sample distributions and fixed budgets 25,50,100 only.',
           'GOP unique-text deduplication weights unique expressions; repeated-record analysis is a different estimand.'],
)
(OUT/'integrity_and_protocol.json').write_text(json.dumps(record,indent=2,ensure_ascii=False),encoding='utf-8')
print('VALIDATED',len(airline),len(gop),'groups',len(groups),'strong pairs',len(large_gap_pairs))
print('MECHANISM SUMMARY')
print(summary_pairs.to_string(index=False))
print('GOP CALIBRATION SUMMARY')
print(summ[['budget_per_group','model','method','mean_absolute_error_pp_mean','reversal_rate_all_mean','reversal_rate_fixed_gap10_mean']].to_string(index=False))
print('FILES WRITTEN',len(list(OUT.glob('*'))))

