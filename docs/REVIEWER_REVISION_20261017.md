# Reviewer revision of 17 October 2026

The revision retains the primary raw-input audit and native split estimates, with explicit source-label and inference limits. It adds the following executable checks from the same four hash-matched inputs.

| Addition | Definition | Evidence |
|---|---|---|
| Annotation allocation | Native group archive, holdout, calibration pool, label count and fractions | S10 |
| Input and lexicon sensitivity | Original VADER exactly matches archived binary labels; separate handle, URL, bare-name and lexicon interventions | S11–S12 |
| Common implementation | Nested samples, upward-rounded 20% holdouts, shared fallback/tie rules; both formulas on identical partitions | S13 |
| Finite archive | Sample labels from full groups; known labels enter exactly, corrections estimate only the unlabeled remainder | S14 |
| Account-disjoint budgets | Globally withhold 20% of names and all their messages; budgets 25/50/100 from other names | S15 |
| Native ties | Reaggregate the same native partitions, preserving their original denominator rules | S16 |
| Duplicate identifiers | Repeated normalized text and tweet IDs; airline normalized-text counterpart | S17/S17b |
| Fresh paired bootstrap | 5,000 within-candidate resamples carrying human and both predictions together, with recalculated reference order | S18 |

Common budget designs use 200 repetitions and seed 20261017; the fresh bootstrap uses the same seed and 5,000 repetitions. No split-budget cells are infeasible. k=100 is held fixed. Reference ties are excluded in all common and fresh-bootstrap metrics; predicted ties receive a half penalty in a companion outcome.

VADER's original @United handling is not a generic model ranking result: masking only that handle moves the United negative estimate from 18.7075% to 37.9383% and all-airline inversions from 3/15 to 0/15. Removing the united lexicon entry instead yields 1/15. Source labels are not recollected after perturbation; no universal deployment remedy is validated.

At the finite-airline target and 400 labels per group, RoBERTa group ACC and human-only MAEs are 1.5582 and 1.5547 pp, but strict reversal rates are 0.4333% and 1.9000%. Raw RoBERTa CC already has zero full-archive inversions. At 100 GOP labels, human-only retains its advantage against tested corrections under common, finite and account-disjoint comparisons. These results support target-specific choices, not universal estimator superiority.

The old 500-repeat internal airline stability claim is not used as inferential evidence. The fresh fully specified bootstrap replaces the old 5,000-resample numerical narrative. Precise product/brand and SemEval numerical claims are removed from the manuscript's empirical support because their traceability did not match that of the primary studies. Previously archived text remains history rather than a current result.

Publication-file fixes include numbered native Word equations, an empirical finite-archive definition of p, a majority-class baseline, shorter abstract, unified estimator terminology, native airline half-penalty reporting, expanded Figure 2, regenerated nonempty PNG/PDF/SVG assets, revised declarations and removal of reviewer comments. The manuscript identifies the complete versioned Code S1 package and distinguishes it from public baseline commit 77ecdd19d93eb0bce92063cdf9dd89ceefe63975. No unpublished GitHub revision is represented as public.


Final input-protocol and statistical extensions are documented in ROUND2_INPUT_AND_STATISTICS.md and Tables S19–S24. S11 model-card placeholders concern VADER; S19 is the separately executed RoBERTa comparison. All budget results continue to use original-input predictions.
