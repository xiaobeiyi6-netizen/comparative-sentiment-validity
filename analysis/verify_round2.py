# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""Reconstruct all round-two aggregate metrics; no source text required."""
from pathlib import Path
from itertools import combinations
import hashlib,json
import numpy as np
import pandas as pd
from round2_statistics import paired_records

R=Path(__file__).resolve().parents[1];A=R/'audit/roberta_input';B=R/'audit/round2'
s=pd.read_csv(A/'summary.csv');g=pd.read_csv(A/'groups.csv');p=pd.read_csv(A/'pairs.csv');l=pd.read_csv(A/'token_lengths.csv')
runtime=json.loads((A/'runtime.json').read_text())
assert runtime['status']=='COMPLETED_PAIRED_INPUT_INFERENCE' and runtime['raw_binary_agreement_verified']
assert runtime['model_commit']=='3216a57f2a0d9c45a2e6c20157c20c49fb4bf9c7'
assert hashlib.sha256((R/'analysis/roberta_input_sensitivity.py').read_bytes()).hexdigest()==runtime['code_sha256']
assert len(s)==4 and (s.raw_binary_changes_vs_archived==0).all()
assert (g[['TP','FN','FP','TN']].sum(1)==g.n).all()
assert np.max(abs(100*(g.TP+g.FN)/g.n-g.reference_negative_pct))<1e-9
assert np.max(abs(100*(g.TP+g.FP)/g.n-g.negative_pct))<1e-9
for row in s.itertuples():
    z=g[(g.corpus==row.corpus)&(g.condition==row.condition)].set_index('group')
    assert row.n==z.n.sum()
    assert abs(row.negative_pct-100*(z.TP+z.FP).sum()/row.n)<1e-9
    assert abs(row.binary_accuracy_pct-100*(z.TP+z.TN).sum()/row.n)<1e-9
    assert abs(row.group_MAE_pp-abs(z.negative_pct-z.reference_negative_pct).mean())<1e-9
    pairs=p[p.corpus==row.corpus];condition=row.condition
    assert len(pairs)==len(list(combinations(z.index,2)))
    for pair in pairs.itertuples():
        gap=z.loc[pair.a,'reference_negative_pct']-z.loc[pair.b,'reference_negative_pct']
        pred=z.loc[pair.a,'negative_pct']-z.loc[pair.b,'negative_pct']
        assert abs(gap-pair.reference_gap_pp)<1e-9
        assert abs(pred-getattr(pair,condition+'_gap_pp'))<1e-9
        assert int(gap*pred<0)==getattr(pair,condition+'_reversal')
    for threshold in [0,3,5,10]:
        eligible=pairs[(pairs.reference_gap_pp.abs()>=threshold)&pairs.reference_gap_pp.ne(0)]
        assert len(eligible)==getattr(row,f'gap{threshold}_pairs')
        assert eligible[condition+'_reversal'].sum()==getattr(row,f'gap{threshold}_reversals')
for row in p.itertuples():
    status='preserved_reversal' if row.original_reversal and row.model_card_reversal else 'disappeared_reversal' if row.original_reversal else 'new_reversal' if row.model_card_reversal else 'neither'
    assert row.transition==status
for (corpus,condition),z in l.groupby(['corpus','condition']):
    total=z[z.group=='ALL'].iloc[0];parts=z[z.group!='ALL']
    assert total.n==parts.n.sum() and total.max_tokens_with_specials==parts.max_tokens_with_specials.max()
    for c in ['over128','actual_truncated']:assert total[c]==parts[c].sum()
    if corpus=='GOP':assert (z.actual_truncated==z.over128).all()
    else:assert (z.actual_truncated==0).all() and total.max_tokens_with_specials<=total.architecture_capacity

paired=pd.read_csv(B/'paired_group_vs_human.csv');computed=paired_records()
pd.testing.assert_frame_equal(paired,computed,check_dtype=False,atol=1e-10,rtol=1e-10)
assert (paired.group_better+paired.same+paired.group_worse==paired.repetitions).all()
diag=pd.read_csv(B/'acc_diagnostics_replicates.csv');ds=pd.read_csv(B/'acc_diagnostics_summary.csv')
keys=['corpus','mode','budget','model','rule','method']
for key,z in diag.groupby(keys):
    row=ds.set_index(keys).loc[key]
    assert row.repetitions==len(z)==200 and row.group_repetitions==z.groups.sum()
    for c in ['fallback_groups','preclip_below0_groups','preclip_above1_groups','negative_denominator_groups']:
        assert abs(z[c].mean()-row[c+'_mean_per_repeat'])<1e-10
        assert abs(100*z[c].sum()/z.groups.sum()-row[c+'_pct_group_repetitions'])<1e-10
for mode in ['message_holdout','finite_archive','account_holdout']:
    old=pd.read_csv(R/'audit/reviewer_revision'/(mode+'_replicates.csv'))
    merged=diag[diag['mode']==mode].merge(old,on=keys+['repeat'],suffixes=('_diag','_old'))
    assert len(merged)==len(diag[diag['mode']==mode])
    assert (merged.fallback_groups_diag==merged.fallback_groups_old).all()
conflict=pd.read_csv(B/'duplicate_label_conflicts.csv').set_index('corpus')
assert (conflict.loc['Airline',['threeclass_conflict_groups','binary_conflict_groups']].to_numpy()==[27,8]).all()
assert (conflict.loc['GOP',['threeclass_conflict_groups','binary_conflict_groups']].to_numpy()==[60,56]).all()
assert conflict.loc['GOP','records_in_binary_conflict_groups']==1435
matched=pd.read_csv(B/'supervised_overlap.csv')
assert matched[(matched.corpus=='Airline')&(matched.group=='ALL')].matching_records.sum()==0
assert matched[(matched.corpus=='GOP')&(matched.group=='ALL')].matching_records.sum()==1
assert json.loads((B/'protocol.json').read_text())['diagnostic_reruns_match_stored_results']
print('PASS: executed paired input provenance, shares, accuracy, confusions, pair identities, all gap thresholds, actual truncation, paired Monte Carlo SE/counts, ACC diagnostics, label conflicts and supervision audit.')
