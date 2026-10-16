#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""Audit supplementary aggregate tables without sharing message-level records.
Run: python analysis/verify_archive_tables.py
Dependencies: pandas, numpy; no network or original tweet text needed.
"""
import math
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
A=ROOT/'audit/aggregates'

def check_close(actual, expected, label, tol=1e-9):
    if not math.isclose(float(actual),float(expected),rel_tol=0,abs_tol=tol):
        raise AssertionError(f'{label}: actual={actual} != expected={expected}')

def check_summary(detail, summary, grouping, mappings):
    assert not detail.empty and not summary.empty
    for key, grp in detail.groupby(grouping, sort=True):
        selector=np.ones(len(summary),dtype=bool)
        if not isinstance(key,tuple):key=(key,)
        for col,value in zip(grouping,key):selector &= summary[col].eq(value).to_numpy()
        assert int(selector.sum())==1, (key,selector.sum())
        row=summary.loc[selector].iloc[0]
        assert int(row.n_repetitions)==len(grp)
        for metric, stem in mappings.items():
            data=grp[metric].to_numpy(dtype=float)
            for agg,fn in [('mean',np.mean),('q025',lambda s:np.quantile(s,.025)),('q975',lambda s:np.quantile(s,.975))]:
                check_close(fn(data),row[f'{stem}_{agg}'],f'{key} {metric} {agg}',tol=1e-9)

al=pd.read_csv(A/'airline_calibration_200_repeated_splits.csv')
asum=pd.read_csv(A/'airline_calibration_budget_summary.csv')
assert len(al)==8000 and len(asum)==40
check_summary(al,asum,['budget_per_airline','model','method'],{
 'mean_absolute_prevalence_error_pp':'mean_absolute_prevalence_error_pp',
 'reversal_rate_gap0pp':'reversal_rate_gap0pp',
 'reversal_rate_gap5pp':'reversal_rate_gap5pp',
 'reversal_rate_gap10pp':'reversal_rate_gap10pp',
 'acc_denominator_fallback_groups':'acc_denominator_fallback_groups',
})

go=pd.read_csv(A/'gop_calibration_200_repeated_splits.csv')
gsum=pd.read_csv(A/'gop_calibration_budget_summary.csv')
assert len(go)==4800 and len(gsum)==24
check_summary(go,gsum,['budget_per_group','model','method'],{
 'mean_absolute_error_pp':'mean_absolute_error_pp',
 'reversal_rate_all':'reversal_rate_all',
 'reversal_rate_fixed_gap10':'reversal_rate_fixed_gap10',
 'reversal_plus_half_ties_all':'reversal_plus_half_ties_all',
 'reversal_plus_half_ties_fixed_gap10':'reversal_plus_half_ties_fixed_gap10',
 'ties_all':'ties_all',
 'acc_fallback_groups':'acc_fallback_groups',
})

# Exact main-claim checks: proportions are percentages, displayed table rounding to 2 decimals.
m=pd.read_csv(A/'main_metrics.csv')
expected={('Airline','VADER'):(14640,61.9126,62.6913,30.4918),
 ('Airline','RoBERTa'):(14640,86.2295,62.6913,58.8934),
 ('GOP','VADER'):(4483,58.7553,58.5545,30.3368),
 ('GOP','RoBERTa'):(4483,68.9940,58.5545,42.36)}
for r in m.itertuples():
    n,ac,p,q=expected[(r.corpus,r.model)]
    assert r.n==n
    for a,b in [(r.accuracy_pct,ac),(r.gold_negative_pct,p),(r.pred_negative_pct,q)]:
        assert abs(a-b) < .00011

revs=pd.read_csv(A/'reversal_counts.csv')
expect_rev={('Airline','VADER'):(15,3),('Airline','RoBERTa'):(15,0),
 ('GOP','VADER'):(45,7),('GOP','RoBERTa'):(45,7)}
for row in revs.itertuples():assert (row.pairs,row.reversals)==expect_rev[(row.corpus,row.model)]

# Direct checks of Table 2 and Table 4 source totals and group prevalence.
air=pd.read_csv(A/'airline_group_prevalence.csv')
gop=pd.read_csv(A/'gop_group_prevalence.csv')
assert len(air)==6 and air.n.sum()==14640
assert len(gop)==10 and gop.n.sum()==4483
for d in (air,gop):
    for col in ['reference_pct','vader_pct','roberta_pct']:
        assert d[col].between(0,100).all()

# Table 5 group pair sensitivity, using original reference pairs.
pair=pd.read_csv(A/'pairwise_bias_reversal_mechanism.csv')
for corpus,model in expect_rev:
    ds=pair[(pair.corpus==corpus)&(pair.model==model)]
    assert len(ds)==expect_rev[(corpus,model)][0]
    assert int(ds.reversed.sum())==expect_rev[(corpus,model)][1]
    if corpus=='GOP':
        for gap,expected_n,expected_v,expected_r in [(3,43,7,6),(5,39,7,5),(10,30,3,2)]:
            sub=ds[ds.reference_abs_gap_pp>=gap]
            assert len(sub)==expected_n
            assert int(sub.reversed.sum())==(expected_v if model=='VADER' else expected_r)

# Table 3/6 400- or 100-label budget comparisons visible in manuscript.
for (model, method,mae,reversal) in [
 ('vader','CC',27.09,28.83),('vader','ACC_pooled',14.40,28.83),
 ('vader','ACC_airline_shrunk',7.74,13.70),('vader','Human_calibration_only',2.66,3.20),
 ('roberta','CC',3.77,4.93),('roberta','ACC_pooled',3.75,4.93),
 ('roberta','ACC_airline_shrunk',2.61,4.10),('roberta','Human_calibration_only',2.66,3.20)]:
    row=asum[(asum.budget_per_airline==400)&(asum.model==model)&(asum.method==method)].iloc[0]
    check_close(round(row.mean_absolute_prevalence_error_pp_mean,2),mae,'Table 3 MAE')
    check_close(round(100*row.reversal_rate_gap0pp_mean,2),reversal,'Table 3 reversal')
for model,method,mae,rev,gaprev in [
 ('VADER','CC',25.22,26.34,18.42),('VADER','ACC_pooled',17.08,26.17,18.35),
 ('VADER','ACC_group_shrunk',17.11,27.17,19.75),('VADER','Human_only',6.42,13.04,2.23),
 ('RoBERTa','CC',16.30,21.02,14.02),('RoBERTa','ACC_pooled',13.57,20.98,13.95),
 ('RoBERTa','ACC_group_shrunk',12.16,20.36,13.43),('RoBERTa','Human_only',6.42,13.04,2.23)]:
    row=gsum[(gsum.budget_per_group==100)&(gsum.model==model)&(gsum.method==method)].iloc[0]
    for x,y,name in [(round(row.mean_absolute_error_pp_mean,2),mae,'MAE'),(round(100*row.reversal_rate_all_mean,2),rev,'strict reversal'),(round(100*row.reversal_rate_fixed_gap10_mean,2),gaprev,'gap10 reversal')]:
        check_close(x,y,f'Table 6 {model} {method} {name}')

print('PASS: Airline 8,000 and GOP 4,800 split-level summary rows reaggregated exactly.')
print('PASS: Core metrics, all pair reversals and 3/5/10pp sensitivity, manuscript Tables 1-6 matched.')
print('CAUTION: Original model inference and airline split-generation were NOT rerun by this aggregate-only audit.')

