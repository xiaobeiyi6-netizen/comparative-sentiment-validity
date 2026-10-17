# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""Verify the distributable aggregate package, without individual source records."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd

R=Path(__file__).resolve().parents[1];A=R/'audit/aggregates';N=R/'audit/revision'
manifest=json.loads((R/'audit/PACKAGE_SHA256.json').read_text())
for name,digest in manifest.items():
    assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest,name
g=pd.read_csv(A/'group_confusion_error_decomposition.csv')
assert len(g)==32
assert np.all(g[['TP','FN','FP','TN']].sum(axis=1)==g.n)
p=(g.TP+g.FN)/g.n;q=(g.TP+g.FP)/g.n
assert np.max(abs((q-p)*100-g.bias_pp))<1e-10
assert np.max(abs(g.false_positive_component_pp+g.false_negative_component_pp-g.bias_pp))<1e-10

s=pd.read_csv(N/'shrinkage_and_pairset_sensitivity.csv')
for corpus,file,bcol,methods,metrics in [
 ('Airline','airline_calibration_budget_summary.csv','budget_per_airline',{'CC':'CC','Pooled ACC':'ACC_pooled','Group ACC':'ACC_airline_shrunk','Human-only':'Human_calibration_only'},('mean_absolute_prevalence_error_pp_mean','reversal_rate_gap0pp_mean')),
 ('GOP','gop_calibration_budget_summary.csv','budget_per_group',{'CC':'CC','Pooled ACC':'ACC_pooled','Group ACC':'ACC_group_shrunk','Human-only':'Human_only'},('mean_absolute_error_pp_mean','reversal_rate_all_mean'))]:
    old=pd.read_csv(A/file)
    for r in s[(s.corpus==corpus)&((s.k==100)|(s.method!='Group ACC'))].itertuples():
        model=r.model.lower() if corpus=='Airline' else r.model
        z=old[(old[bcol]==r.budget)&(old.model==model)&(old.method==methods[r.method])].iloc[0]
        assert abs(r.MAE_pp-z[metrics[0]])<1e-10
        assert abs(r.reversal_all-z[metrics[1]])<1e-10
    detail=pd.read_csv(N/(corpus.lower()+'_sensitivity_splits.csv'))
    by=['corpus','budget','model','method','k']
    metrics=['MAE_pp','reversal_all','reversal_fixed10','reversal_holdout10','holdout10_pairs','reference_ties','predicted_ties','fallback_groups']
    avg=detail.groupby(by)[metrics].mean().sort_index()
    archived=s[s.corpus==corpus].set_index(by)[metrics].sort_index()
    assert avg.index.equals(archived.index)
    assert np.nanmax(abs(avg.to_numpy()-archived.to_numpy()))<1e-10
audit=json.loads((N/'source_and_label_audit.json').read_text())
assert audit['gop_duplicate_groups']==150 and audit['gop_conflicting_label_groups']==60
assert audit['gop_cross_candidate_texts']==5 and audit['majority_label_changes']==15
v=pd.read_csv(N/'reference_and_duplicate_sensitivity.csv')
expected={'Airline primary':(14640,3,0),'Airline confidence 1':(10445,3,0),'GOP primary':(4483,7,7),
          'GOP majority labels':(4483,7,7),'GOP exclude cross-candidate texts':(4478,7,7),'GOP repeated records':(6284,16,5)}
for name,(n,vader,roberta) in expected.items():
    ds=v[v.variant==name].set_index('model');assert set(ds.n)=={n}
    assert ds.loc['VADER','reversals']==vader and ds.loc['RoBERTa','reversals']==roberta
bc=pd.read_csv(N/'account_cluster_bootstrap_splits.csv');bs=pd.read_csv(N/'account_cluster_bootstrap_summary.csv')
for row in bs.itertuples():
    z=bc[(bc.corpus==row.corpus)&(bc.model==row.model)]
    assert len(z)==2000
    assert abs(100*z.reversal_rate.mean()-row.reversal_mean_pct)<1e-10
    assert abs(100*z.reversal_rate.quantile(.025)-row.reversal_q025_pct)<1e-10
    assert abs(100*z.reversal_rate.quantile(.975)-row.reversal_q975_pct)<1e-10
print('PASS: package hashes, group error identities, all k=100 budget matches, sensitivity reaggregation, label checks, and account-cluster summaries.')
print('Boundary: aggregate checks do not replace source-record verification, institutional ethics review, or historical neural inference.')

# New fixed-revision inference summary invariants (no private records required).
s9=pd.read_csv(R/"supplementary_tables/Table_S9_Locked_Inference_Comparison.csv")
assert len(s9)==4 and (s9.binary_label_changes==0).all()
assert (s9.old_reversals_gap0==s9.new_reversals_gap0).all()
assert (s9.changed_reversal_pairs==0).all()
assert (s9.maximum_absolute_group_share_change_pp==0).all()
lock=json.loads((R/"audit/locked_inference/runtime_and_model_lock.json").read_text())
assert lock["historical_revision_recovered"] is False
assert hashlib.sha256((R/"analysis/locked_model_replication.py").read_bytes()).hexdigest()==lock["code_sha256"]
print("Fixed-revision inference aggregates and script provenance PASS")
