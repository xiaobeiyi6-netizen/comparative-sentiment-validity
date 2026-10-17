# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""Check reviewer-revision aggregates without any individual source records."""
from pathlib import Path
import json
import numpy as np
import pandas as pd

R=Path(__file__).resolve().parents[1];A=R/'audit/reviewer_revision'

for mode in ['message_holdout','finite_archive','account_holdout']:
    d=pd.read_csv(A/(mode+'_replicates.csv'))
    s=pd.read_csv(A/(mode+'_summary.csv'))
    keys=['corpus','mode','budget','model','rule','method']
    cols=['MAE_pp','strict_pct','half_penalty_pct','predicted_ties','eligible_pairs','reference_ties','fallback_groups']
    assert (d.MAE_pp>=0).all() and d.eligible_pairs.gt(0).all()
    assert np.max(abs(d.half_penalty_pct-d.strict_pct-50*d.predicted_ties/d.eligible_pairs))<1e-8
    assert d['strict_pct'].between(0,100).all() and d.half_penalty_pct.between(0,100).all()
    indexed=s.set_index(keys)
    for key,x in d.groupby(keys):
        ref=indexed.loc[key]
        assert len(x)==ref.repetitions==200
        for c in cols:
            for agg,fn in [('mean',lambda v:v.mean()),('q025',lambda v:v.quantile(.025)),('q975',lambda v:v.quantile(.975))]:
                assert abs(fn(x[c])-ref[c+'_'+agg])<1e-8,(mode,key,c,agg)
    # Human-only is exactly the same estimator in both model bookkeeping branches.
    h=d[d.method=='Human-only'].pivot(index=['corpus','mode','budget','repeat','rule'],columns='model',values='MAE_pp')
    assert np.max(abs(h.VADER-h.RoBERTa))<1e-12

alloc=pd.read_csv(A/'label_allocations.csv')
v=alloc[(alloc.group=='Virgin America')&(alloc.budget==400)].iloc[0]
assert (v.archive_n,v.evaluation_n,v.calibration_pool_n)==(504,101,403)
assert abs(v.labeled_pool_pct-100*400/403)<1e-10

diag=pd.read_csv(A/'vader_input_diagnostics_groups.csv')
z=diag[(diag.group=='United')&(diag.variant=='United handle only masked')].iloc[0]
assert (z.n,z.TP,z.FN,z.FP,z.TN)==(3822,1331,1302,119,1070)
assert z.recovered_original_false_negatives==643 and z.newly_missed_negatives==0
assert (diag.TP+diag.FN+diag.FP+diag.TN==diag.n).all()
q=pd.read_csv(A/'vader_input_diagnostics_summary.csv').set_index('variant')
assert q.loc['Original input','binary_changes_from_original']==0
assert q.loc['Original input','reversals']==3
assert q.loc['United handle only masked','reversals']==0
assert q.loc['United lexicon entry removed','reversals']==1

native=pd.read_csv(A/'native_budget_ties.csv')
mapping=[('Airline','airline_calibration_budget_summary.csv','budget_per_airline',
    {'CC':'CC','Pooled ACC':'ACC_pooled','Group ACC':'ACC_airline_shrunk','Human-only':'Human_calibration_only'},
    'mean_absolute_prevalence_error_pp_mean','reversal_rate_gap0pp_mean'),
 ('GOP','gop_calibration_budget_summary.csv','budget_per_group',
    {'CC':'CC','Pooled ACC':'ACC_pooled','Group ACC':'ACC_group_shrunk','Human-only':'Human_only'},
    'mean_absolute_error_pp_mean','reversal_rate_all_mean')]
for corpus,f,bc,mm,mc,rc in mapping:
    old=pd.read_csv(R/'audit/aggregates'/f)
    for x in native[native.corpus==corpus].itertuples():
        model=x.model.lower() if corpus=='Airline' else x.model
        row=old[(old[bc]==x.budget)&(old.model==model)&(old.method==mm[x.method])].iloc[0]
        assert abs(row[mc]-x.MAE_pp)<1e-8 and abs(100*row[rc]-x.strict_pct)<1e-8

b=pd.read_csv(A/'gop_paired_bootstrap_replicates.csv')
s=pd.read_csv(A/'gop_paired_bootstrap_summary.csv').set_index('model')
for model,x in b.groupby('model'):
    assert len(x)==5000
    for c in ['MAE_pp','strict_pct','half_penalty_pct']:
        assert abs(x[c].mean()-s.loc[model,c+'_mean'])<1e-8
        assert abs(x[c].quantile(.025)-s.loc[model,c+'_q025'])<1e-8
        assert abs(x[c].quantile(.975)-s.loc[model,c+'_q975'])<1e-8
for c in ['MAE_pp','strict_pct','half_penalty_pct']:
    d=b.pivot(index='repeat',columns='model',values=c)
    assert np.max(abs(d.VADER-d.RoBERTa-d['VADER minus RoBERTa']))<1e-8

meta=json.loads((A/'reviewer_revision_protocol.json').read_text())
assert meta['infeasible_split_budget_cells']==[]
assert meta['new_transformer_inference'] is False and meta['primary_results_replaced'] is False
for slug in ['twitter-airline-sentiment','first-gop-debate-twitter-sentiment']:
    assert json.loads((A/(slug+'_source_evidence.json')).read_text())['licenseName']=='CC BY-NC-SA 4.0'
for stem in ['Figure_1_Airline_Negative_Shares','Figure_2_Airline_Budget_Comparison','Figure_3_GOP_Reference_Gaps']:
    for ext in ['png','pdf','svg']:
        assert (R/'figures'/(stem+'.'+ext)).stat().st_size>1000
print('PASS: common, finite-archive, account-disjoint, native-tie and paired-bootstrap reaggregation; VADER diagnostics; label fractions; source metadata; nonempty figure files.')
print('Boundary: computational consistency with released labels, not independent authentication of original annotations or population inference.')
