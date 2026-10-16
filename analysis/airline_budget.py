# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""Computational communication: real-data calibration-budget evaluation.
Inputs: matched Tweets.csv (Twitter Airline Sentiment) and airline_predictions.csv.
No language model inference; hard-label CC and ACC only.
Protocol: 200 seeded repeated stratified holdouts, calibration size per airline
25/50/100/200/400, untouched per-airline test fold 20%.
"""
import argparse, hashlib, json, os
from itertools import combinations
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 20261015
BUDGETS = (25,50,100,200,400)
REPEATS = 200
MODELS = ('vader','roberta')
METHODS = ('CC','ACC_pooled','ACC_airline_shrunk','Human_calibration_only')
THRESHOLDS = (0,5,10)


def match_inputs(raw_path, pred_path):
    raw = pd.read_csv(raw_path, low_memory=False)
    pred = pd.read_csv(pred_path)
    required_raw={'text','airline','airline_sentiment'}
    required_pred={'reference','vader','roberta','text_sha256'}
    if not required_raw.issubset(raw.columns) or not required_pred.issubset(pred.columns):
        raise ValueError(f'Missing required columns: raw={required_raw-set(raw.columns)}, pred={required_pred-set(pred.columns)}')
    if len(raw)!=len(pred) or len(pred)!=14640:
        raise ValueError(f'Row count mismatch raw={len(raw)}, predictions={len(pred)}; do not assume same order')
    refmap={'negative':0,'neutral':1,'positive':2}
    ref=raw['airline_sentiment'].map(refmap)
    if not np.array_equal(ref.to_numpy(),pred['reference'].to_numpy()):
        raise ValueError('Human labels do not match exact row order')
    text_hash=raw['text'].astype(str).map(lambda x:hashlib.sha256(x.encode('utf-8')).hexdigest()).to_numpy()
    if not np.array_equal(text_hash,pred['text_sha256'].to_numpy()):
        raise ValueError('SHA-256 text mismatch; do NOT assign company labels to predictions')
    d=pred[['reference','vader','roberta']].copy()
    d['airline']=raw['airline'].to_numpy()
    if d.isna().any().any(): raise ValueError('Missing predictions or airline')
    if not set(np.unique(d[['reference','vader','roberta']].values)).issubset({0,1,2}):raise ValueError('Unexpected label values')
    return d


def binary_rates(s, model):
    negative=s['reference'].to_numpy()==0
    predneg=s[model].to_numpy()==0
    tp=int((negative & predneg).sum()); fn=int((negative & ~predneg).sum())
    fp=int((~negative & predneg).sum()); tn=int((~negative & ~predneg).sum())
    # Jeffreys smoothing prevents exact 0/1 on small calibration strata.
    return (tp+.5)/(tp+fn+1), (fp+.5)/(fp+tn+1), tp+fn, fp+tn


def acc(q,tpr,fpr):
    denom=tpr-fpr
    if abs(denom)<.10: return q,True
    return float(np.clip((q-fpr)/denom,0,1)),False


def run_study(df, repeats=REPEATS, seed=SEED, budgets=BUDGETS):
    rng=np.random.default_rng(seed)
    groups=sorted(df.airline.unique().tolist())
    arr={g: df.loc[df.airline==g,['reference','vader','roberta']].to_numpy(np.int8) for g in groups}
    for g,x in arr.items():
        if len(x)-int(np.ceil(.20*len(x)))<max(budgets):
            raise ValueError(f'{g} too small for the largest calibration budget')
    pairs=list(combinations(groups,2))
    runrows=[]; detailrows=[]
    for rep in range(repeats):
        test={}; remaining={}
        for g,x in arr.items():
            ix=rng.permutation(len(x)); ntest=int(np.ceil(len(x)*.20))
            test[g]=x[ix[:ntest]];remaining[g]=x[ix[ntest:]]
        test_ref={g:float((x[:,0]==0).mean()) for g,x in test.items()}
        for budget in budgets:
            calib={g:remaining[g][rng.choice(len(remaining[g]),size=budget,replace=False)] for g in groups}
            calall=np.vstack(list(calib.values()))
            for model in MODELS:
                j=1 if model=='vader' else 2
                # Each calibration group has same sample count; pooled rates aggregate across groups.
                calpooled=pd.DataFrame({'reference':calall[:,0],model:calall[:,j]})
                tp_pool,fp_pool,npos_pool,nneg_pool=binary_rates(calpooled,model)
                est={meth:{} for meth in METHODS}
                fallback={meth:0 for meth in METHODS}
                for g in groups:
                    testq=float((test[g][:,j]==0).mean())
                    cg=calib[g]
                    cgframe=pd.DataFrame({'reference':cg[:,0],model:cg[:,j]})
                    tp_g,fp_g,npos_g,nneg_g=binary_rates(cgframe,model)
                    est['CC'][g]=testq
                    est['ACC_pooled'][g],bad=acc(testq,tp_pool,fp_pool)
                    fallback['ACC_pooled']+=int(bad)
                    # Shrink subgroup conditional error rate towards pooled data
                    # regularization parameter 100 in the supplied routine; prospective timing is unverified.
                    k=100
                    shrink_tpr=(npos_g*tp_g+k*tp_pool)/(npos_g+k)
                    shrink_fpr=(nneg_g*fp_g+k*fp_pool)/(nneg_g+k)
                    est['ACC_airline_shrunk'][g],bad=acc(testq,shrink_tpr,shrink_fpr)
                    fallback['ACC_airline_shrunk']+=int(bad)
                    # Transparent manual-only baseline uses labeled calibration responses, never test labels.
                    est['Human_calibration_only'][g]=float((cg[:,0]==0).mean())
                for meth in METHODS:
                    errors=[abs(est[meth][g]-test_ref[g])*100 for g in groups]
                    inversions={thr:0 for thr in THRESHOLDS}
                    denom={thr:0 for thr in THRESHOLDS}
                    for a,b in pairs:
                        truegap=(test_ref[a]-test_ref[b])*100
                        predgap=(est[meth][a]-est[meth][b])*100
                        for thr in THRESHOLDS:
                            if abs(truegap) < max(1e-12,thr): continue
                            denom[thr]+=1
                            if predgap*truegap < 0:inversions[thr]+=1
                            # predicted ties do not count as correctly ordered; report separately below.
                    row={'repeat':rep,'budget_per_airline':budget,'total_calibration_labels':budget*len(groups),'model':model,'method':meth,'mean_absolute_prevalence_error_pp':np.mean(errors),'median_absolute_prevalence_error_pp':np.median(errors),'max_absolute_prevalence_error_pp':np.max(errors),'acc_denominator_fallback_groups':fallback[meth]}
                    for thr in THRESHOLDS:
                        row[f'reversal_count_gap{thr}pp']=inversions[thr]
                        row[f'eligible_pairs_gap{thr}pp']=denom[thr]
                        row[f'reversal_rate_gap{thr}pp']=(inversions[thr]/denom[thr] if denom[thr]>0 else np.nan)
                    runrows.append(row)
                    if rep==0:
                        for g in groups:
                            detailrows.append({'repeat':rep,'budget_per_airline':budget,'airline':g,'model':model,'method':meth,'heldout_reference_pct':100*test_ref[g],'heldout_estimated_pct':100*est[meth][g],'abs_error_pp':100*abs(est[meth][g]-test_ref[g])})
    runs=pd.DataFrame(runrows)
    keys=['budget_per_airline','model','method']
    agg={'n_repetitions':('repeat','nunique')}
    for metric in ['mean_absolute_prevalence_error_pp','reversal_rate_gap0pp','reversal_rate_gap5pp','reversal_rate_gap10pp','acc_denominator_fallback_groups']:
        agg[metric+'_mean']=(metric,'mean')
        agg[metric+'_q025']=(metric,lambda s:s.quantile(.025))
        agg[metric+'_q975']=(metric,lambda s:s.quantile(.975))
    summary=runs.groupby(keys,as_index=False).agg(**agg)
    return runs,summary,pd.DataFrame(detailrows)


def main():
    p=argparse.ArgumentParser();p.add_argument('--raw',required=True);p.add_argument('--pred',required=True);p.add_argument('--out',default='airline_calibration_outputs');p.add_argument('--repeats',type=int,default=REPEATS);args=p.parse_args()
    d=match_inputs(args.raw,args.pred)
    runs,summary,details=run_study(d,repeats=args.repeats)
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    runs.to_csv(out/'all_repeated_splits.csv',index=False)
    summary.to_csv(out/'calibration_budget_summary.csv',index=False)
    details.to_csv(out/'first_split_group_detail.csv',index=False)
    meta={'source':'Twitter US Airline Sentiment; original Tweets.csv','n':len(d),'groups':sorted(d.airline.unique().tolist()),'seed':SEED,'n_repeated_splits':args.repeats,'budgets_per_airline':list(BUDGETS),'test_fraction_per_group':.20,'calibration_does_not_overlap_test':True,'hard_labels_only':True,'methods':list(METHODS),'no_pacc_because_probabilities_not_collected':True,'regularization_pseudocount_k':100,'acc_fallback_if_abs_TPR_minus_FPR_below':.10,'test_data_target':'held-out labeled airline tweets','uncertainty':'quantiles across repeated splits, NOT population confidence intervals','limitations':'reference corpus not representative of all customers; repeated splits correlated; no causal inference; near-tie company comparisons need caution'}
    (out/'protocol_and_audit.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf-8')
    print(summary[['budget_per_airline','model','method','mean_absolute_prevalence_error_pp_mean','reversal_rate_gap5pp_mean']].round(3).to_string(index=False))
    print('Saved',out)




if __name__ == "__main__":
    main()
