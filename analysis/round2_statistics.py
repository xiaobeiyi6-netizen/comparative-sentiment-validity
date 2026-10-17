# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""Paired Monte Carlo precision, duplicate conflicts, overlap and ACC diagnostics.

Requires lawful private inputs; only aggregate outputs are written. Existing
per-repeat scores are read, not replaced. Diagnostic reruns assert exact score
agreement with all common-protocol stored results.
"""
import argparse, hashlib, json
from collections import defaultdict
from pathlib import Path
from itertools import combinations
import numpy as np
import pandas as pd
import reviewer_revision as rr
from revision_sensitivity import get_data,norm

ROOT=Path(__file__).resolve().parents[1]

def paired_records():
    a=ROOT/'audit/reviewer_revision';runs=[]
    for mode in ['message_holdout','finite_archive','account_holdout']:
        runs.append(pd.read_csv(a/(mode+'_replicates.csv')))
    for corpus in ['Airline','GOP']:
        d=pd.read_csv(a/(corpus.lower()+'_sensitivity_splits.csv'))
        d=d[(d.k==-1)|((d.method=='Group ACC')&(d.k==100))].copy()
        d['mode']='native';d['rule']='native';d['strict_pct']=100*d.reversal_all
        den=15-d.reference_ties if corpus=='Airline' else 45
        d['half_penalty_pct']=d.strict_pct+50*d.predicted_ties/den;runs.append(d)
    d=pd.concat(runs,ignore_index=True);out=[]
    for key,z in d.groupby(['corpus','mode','budget','model','rule']):
        for metric in ['MAE_pp','strict_pct','half_penalty_pct']:
            p=z.pivot(index='repeat',columns='method',values=metric)
            difference=p['Group ACC']-p['Human-only'];difference[np.abs(difference)<1e-12]=0
            out.append(dict(zip(['corpus','mode','budget','model','rule'],key),metric=metric,repetitions=len(p),
                difference='Group ACC minus Human-only',mean_difference=difference.mean(),
                Monte_Carlo_SE=difference.std(ddof=1)/np.sqrt(len(p)),
                difference_q025=difference.quantile(.025),difference_q975=difference.quantile(.975),
                group_better=int((difference<0).sum()),same=int((difference==0).sum()),group_worse=int((difference>0).sum())))
    return pd.DataFrame(out)

def conflicts(inputs):
    a=pd.read_csv(inputs/'Tweets.csv');raw=pd.read_csv(inputs/'GOP_REL_ONLY.csv')
    candidate=raw.candidate.fillna('').astype(str).str.strip();label=raw.sentiment.fillna('').astype(str).str.strip().str.title()
    text=raw.text.fillna('').astype(str).str.strip()
    valid=candidate.ne('')&~candidate.str.casefold().isin({'no candidate mentioned','none','no candidate','not mentioned','not applicable'})&label.isin(['Negative','Neutral','Positive'])&text.ne('')
    g=raw[valid].copy();g['text']=text[valid];g['sentiment']=label[valid]
    out=[]
    for corpus,d,labelcol in [('Airline',a,'airline_sentiment'),('GOP',g,'sentiment')]:
        z=d.copy();z['normalized']=z.text.map(norm);z['negative']=z[labelcol].str.casefold().eq('negative')
        t=z.groupby('normalized').agg(records=('text','size'),threeclass=(labelcol,'nunique'),binary=('negative','nunique'))
        repeat=t.records>1
        out.append(dict(corpus=corpus,eligible_records=len(z),unique_normalized_texts=len(t),repeated_text_groups=int(repeat.sum()),
            records_in_repeated_groups=int(t.loc[repeat,'records'].sum()),
            threeclass_conflict_groups=int((t.threeclass>1).sum()),records_in_threeclass_conflict_groups=int(t.loc[t.threeclass>1,'records'].sum()),
            binary_conflict_groups=int((t.binary>1).sum()),records_in_binary_conflict_groups=int(t.loc[t.binary>1,'records'].sum())))
    return pd.DataFrame(out),a,g.drop_duplicates('text')

def overlap(inputs,tweet_eval):
    from locked_model_replication import load_inputs
    a,g,_=load_inputs(inputs/'four_validated_inputs.zip');out=[];sources={}
    for split in ['train','val']:
        p=tweet_eval/(split+'_text.txt');b=p.read_bytes();lines=b.decode().splitlines();known=set(map(norm,lines))
        sources[split]=dict(sha256=hashlib.sha256(b).hexdigest(),lines=len(lines),unique_normalized_texts=len(known),
            url='https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/sentiment/'+p.name)
        for corpus,d in [('Airline',a),('GOP',g)]:
            hits=d.text.map(norm).isin(known)
            for group,sub in [('ALL',d.index)]+[(group,z.index) for group,z in d.groupby('group')]:
                out.append(dict(corpus=corpus,supervised_split=split,group=group,n=len(sub),matching_records=int(hits.loc[sub].sum()),
                    matching_unique_normalized_texts=int(d.loc[sub][hits.loc[sub]].text.map(norm).nunique())))
    return pd.DataFrame(out),sources

def acc_diagnostics(air,gop):
    rows=[];original=rr.estimate_methods
    for corpus,data in [('Airline',air),('GOP',gop)]:
        for mode in ['message_holdout','finite_archive','account_holdout']:
            counter=defaultdict(int)
            def instrument(cal,evaluated,column,rule):
                result=original(cal,evaluated,column,rule);c=rr.counts(cal,column);po=c.sum(0)
                pt=(po[0]+.5)/(po[0]+po[1]+1);pf=(po[2]+.5)/(po[2]+po[3]+1)
                pos=c[:,0]+c[:,1];neg=c[:,2]+c[:,3];jt=(c[:,0]+.5)/(pos+1);jf=(c[:,2]+.5)/(neg+1)
                st=(pos*jt+100*pt)/(pos+100) if rule=='blend_Jeffreys' else (c[:,0]+.5+100*pt)/(pos+1+100)
                sf=(neg*jf+100*pf)/(neg+100) if rule=='blend_Jeffreys' else (c[:,2]+.5+100*pf)/(neg+1+100)
                q=np.array([x[:,column].mean() for x in evaluated]);target=np.array([x[:,0].mean() for x in evaluated])
                b=len(cal[0]);key=(b,column,rule);repeat=counter[key];counter[key]+=1
                n=np.array([len(x)+len(y) for x,y in zip(cal,evaluated)]);h=np.array([x[:,0].mean() for x in cal])
                if mode=='finite_archive':target=(b*h+(n-b)*target)/n
                for method,t,f in [('Pooled ACC',np.repeat(pt,len(q)),np.repeat(pf,len(q))),('Group ACC',st,sf)]:
                    den=t-f;fallback=abs(den)<.10
                    with np.errstate(divide='ignore',invalid='ignore'):before=(q-f)/den
                    working=np.where(fallback,q,before);after=np.clip(working,0,1)
                    assert np.max(abs(after-result[method][0]))<1e-12
                    lower=(~fallback)&(before<0);upper=(~fallback)&(before>1)
                    if mode=='finite_archive':working=(b*h+(n-b)*working)/n;after=(b*h+(n-b)*after)/n
                    pairs=np.array(list(combinations(range(len(q)),2)));aa,bb=pairs.T
                    eligible=abs(target[aa]-target[bb])>=1e-12
                    created=eligible&(abs(working[aa]-working[bb])>=1e-12)&(abs(after[aa]-after[bb])<1e-12)
                    rows.append(dict(corpus=corpus,mode=mode,budget=b,model='VADER' if column==1 else 'RoBERTa',rule=rule,
                        method=method,repeat=repeat,groups=len(q),fallback_groups=int(fallback.sum()),preclip_below0_groups=int(lower.sum()),
                        preclip_above1_groups=int(upper.sum()),negative_denominator_groups=int((den<0).sum()),
                        clipped_new_tied_pairs=int(created.sum())))
                return result
            rr.estimate_methods=instrument
            try:computed,_,skipped=rr.run_budget(data,corpus,mode)
            finally:rr.estimate_methods=original
            assert not skipped
            old=pd.read_csv(ROOT/'audit/reviewer_revision'/(mode+'_replicates.csv'))
            old=old[old.corpus==corpus].reset_index(drop=True)
            pd.testing.assert_frame_equal(computed[old.columns],old,check_dtype=False,atol=1e-10,rtol=1e-10)
    d=pd.DataFrame(rows);out=[]
    keys=['corpus','mode','budget','model','rule','method']
    for key,z in d.groupby(keys):
        r=dict(zip(keys,key));r.update(repetitions=z.repeat.nunique(),group_repetitions=int(z.groups.sum()))
        for c in ['fallback_groups','preclip_below0_groups','preclip_above1_groups','negative_denominator_groups']:
            r[c+'_mean_per_repeat']=z[c].mean();r[c+'_pct_group_repetitions']=100*z[c].sum()/z.groups.sum()
        r['clipped_new_tied_pairs_mean_per_repeat']=z.clipped_new_tied_pairs.mean();out.append(r)
    return d,pd.DataFrame(out)

def main(a):
    a.out.mkdir(parents=True,exist_ok=True)
    paired_records().to_csv(a.out/'paired_group_vs_human.csv',index=False)
    conflict,_,_=conflicts(a.inputs);conflict.to_csv(a.out/'duplicate_label_conflicts.csv',index=False)
    matched,sources=overlap(a.inputs,a.tweet_eval);matched.to_csv(a.out/'supervised_overlap.csv',index=False)
    (a.out/'overlap_sources.json').write_text(json.dumps(sources,indent=2)+'\n')
    air,gop,_,_=get_data(a.inputs);rep,summary=acc_diagnostics(air,gop)
    rep.to_csv(a.out/'acc_diagnostics_replicates.csv',index=False);summary.to_csv(a.out/'acc_diagnostics_summary.csv',index=False)
    metadata=dict(seed=20261017,repetitions=200,diagnostic_reruns_match_stored_results=True,
        Monte_Carlo_SE='Sample SD of paired split differences / sqrt(200); simulation mean precision conditional on the fixed archive and protocol, not a population interval.',
        clipping_counts='Only nonfallback corrections are counted below 0 or above 1; fallback is counted separately. Negative denominators include fallback groups.',
        clipping_ties='New predicted ties among non-tied reference pairs created by clipping, evaluated after finite-archive recombination where applicable.',
        difference_direction='Group ACC minus Human-only; negative favors Group ACC; ties use absolute tolerance 1e-12.')
    (a.out/'protocol.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(conflict.to_string(index=False));print(matched[matched.group=='ALL'].to_string(index=False));print('All diagnostic reruns agree with existing per-repeat scores.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--inputs',type=Path,required=True);p.add_argument('--tweet-eval',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    main(p.parse_args())
