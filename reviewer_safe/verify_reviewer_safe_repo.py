#!/usr/bin/env python3
"""Reviewer-safe audit of archived aggregate statistics (no original tweet data).

Run from the repository root:
    python reviewer_safe/verify_reviewer_safe_repo.py

Validates the archived aggregate tables and Supplementary S3/S4 against
repository group confusion and pairwise decomposition sources.
Does not regenerate historical neural inference or validate data rights.
"""
from pathlib import Path
import math
import runpy
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'audit' / 'aggregates'
HERE = Path(__file__).resolve().parent / 'aggregate_results'

def close(a, b, label, tol=1e-7):
    assert math.isclose(float(a), float(b), rel_tol=0, abs_tol=tol), f'{label}: {a} != {b}'

# Existing independent checker re-aggregates 8,000 airline and 4,800 GOP
# split summaries (1,104 summary cells) and checks manuscript Tables 1-6.
runpy.run_path(str(ROOT / 'analysis' / 'verify_archive_tables.py'), run_name='__main__')

s3 = pd.read_csv(HERE / 'S3_group_confusion_aggregates.csv')
s4 = pd.read_csv(HERE / 'S4_strong_gap_reversals.csv')
base_group = pd.read_csv(AUDIT / 'group_confusion_error_decomposition.csv')
base_pairs = pd.read_csv(AUDIT / 'pairwise_bias_reversal_mechanism.csv')
assert len(s3) == len(base_group) == 32
assert len(s4) == 8
assert not s3.duplicated(['corpus','group','model']).any()
assert not s4.duplicated(['corpus','model','group_a','group_b']).any()

for r in s3.itertuples(index=False):
    matching = base_group[(base_group.corpus == r.corpus) &
                          (base_group.group == r.group) & (base_group.model == r.model)]
    assert len(matching) == 1
    z = matching.iloc[0]
    for k in ('n','TP','FN','FP','TN'):
        assert int(getattr(r,k)) == int(z[k]), f'S3 {r.group} {r.model} {k}'
    assert r.n == r.TP+r.FN+r.FP+r.TN
    close(r.reference_negative_pct,100*z.gold_negative_prop,'S3 gold')
    close(r.predicted_negative_pct,100*z.pred_negative_prop,'S3 predicted')
    close(r.FNR_pct,100*z.FNR,'S3 FNR')
    close(r.FPR_pct,100*z.FPR,'S3 FPR')
    close(r.bias_pp,z.bias_pp,'S3 bias')
    close(r.FP_component_pp,z.false_positive_component_pp,'S3 FP')
    close(r.FN_component_pp,z.false_negative_component_pp,'S3 FN')
    close(r.bias_pp,100*(r.FP-r.FN)/r.n,'FP-FN identity')
    close(r.bias_pp,r.FP_component_pp+r.FN_component_pp,'S3 error decomposition')

# Guard against confusing whole-corpus prevalence with the final pairwise
# difference (a known reporting bug in an earlier standalone review ZIP).
table1 = pd.read_csv(AUDIT / 'main_metrics.csv')
assert len(table1) == 4
for (corpus, model), d in s3.groupby(['corpus', 'model']):
    n = int(d.n.sum())
    gold_share = 100 * int((d.TP + d.FN).sum()) / n
    predicted_share = 100 * int((d.TP + d.FP).sum()) / n
    binary_accuracy = 100 * int((d.TP + d.TN).sum()) / n
    row = table1[(table1.corpus == corpus) & (table1.model == model)]
    assert len(row) == 1
    row = row.iloc[0]
    assert n == int(row.n)
    assert 0 <= predicted_share <= 100
    close(gold_share, row.gold_negative_pct, f'Table 1 {corpus} gold', tol=0.00011)
    close(predicted_share, row.pred_negative_pct, f'Table 1 {corpus} prediction', tol=0.00011)
    close(binary_accuracy, row.accuracy_pct, f'Table 1 {corpus} binary accuracy', tol=0.00011)
    print(f'TABLE 1 VERIFIED: {corpus} / {model}; negative prediction {predicted_share:.4f}%')

observed = base_pairs.groupby(['corpus','model']).reversed.sum().to_dict()
assert observed == {('Airline','RoBERTa'):0,('Airline','VADER'):3,
                    ('GOP','RoBERTa'):7,('GOP','VADER'):7}
strong = base_pairs[(base_pairs.reversed == 1) &
                    (base_pairs.reference_abs_gap_pp >= 10)]
assert len(strong) == 8
assert set(map(tuple,strong[['corpus','model','group_a','group_b']].to_numpy())) == set(
    map(tuple,s4[['corpus','model','group_a','group_b']].to_numpy()))
for r in s4.itertuples(index=False):
    matching = strong[(strong.corpus == r.corpus) & (strong.model == r.model) &
                      (strong.group_a == r.group_a) & (strong.group_b == r.group_b)]
    assert len(matching) == 1
    z = matching.iloc[0]
    for source,target in [('gold_diff_pp','ref_diff_pp'),
                          ('pred_diff_pp','pred_diff_pp'),
                          ('reference_abs_gap_pp','gap_pp'),
                          ('fp_component_difference_pp','FP_difference_pp'),
                          ('fn_component_difference_pp','FN_difference_pp'),
                          ('bias_difference_pp','bias_diff_pp')]:
        close(getattr(r,target),z[source],f'S4 {target}')
    assert r.ref_diff_pp * r.pred_diff_pp < 0
    close(r.pred_diff_pp,r.ref_diff_pp+r.bias_diff_pp,'pairwise identity')
    close(r.bias_diff_pp,r.FP_difference_pp+r.FN_difference_pp,'FP/FN pairwise')

print('PASS: 32 S3 rows match archived confusion matrices and FP/FN identities.')
print('PASS: 8 S4 rows match all strong-gap reversal cases and pairwise identities.')
print('PASS: archived split-summary verification completed (see above).')
print('LIMITATION: checks archived aggregates, not original neural inference or ethics.')
