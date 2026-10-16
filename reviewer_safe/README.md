# Reviewer-safe aggregate audit (private review branch)

**Status:** pre-submission private review materials, 16 October 2026. No public release, Zenodo DOI, model-weight redistribution, or ethics authorization is claimed.

## What was added on this branch

- `reviewer_safe/aggregate_results/S3_group_confusion_aggregates.csv`: 32 corpus/group/model confusion rows, with human-reference and predicted negative shares, FP/FN and bias components.
- `reviewer_safe/aggregate_results/S4_strong_gap_reversals.csv`: the 8 model-specific strict ranking reversals for which the original human-reference difference is at least 10 percentage points.
- `reviewer_safe/verify_reviewer_safe_repo.py`: verifies these tables against independently archived confusion and pairwise results, then invokes the repository's original six-main-table and 1,104-budget-cell checker.
- This README and a submission-readiness note.

The **six larger aggregate CSVs** already exist under `audit/aggregates/` on the inherited `main` history, so they have **not been duplicated** on this branch. In particular:

| Previously archived file | Aggregate-only role |
|---|---|
| `group_confusion_error_decomposition.csv` | 32 confusion/decomposition rows used to verify S3 |
| `pairwise_bias_reversal_mechanism.csv` | pairwise contrasts used to verify S4 |
| `airline_calibration_200_repeated_splits.csv` | 8,000 repeated-split method-level outcomes |
| `airline_calibration_budget_summary.csv` | 40 averaged budget/method rows |
| `gop_calibration_200_repeated_splits.csv` | 4,800 repeated-split method-level outcomes |
| `gop_calibration_budget_summary.csv` | 24 averaged budget/method rows |

## Reproduce

From repository root, with dependencies installed from `requirements-analysis.txt`:

```bash
python reviewer_safe/verify_reviewer_safe_repo.py
```

The script checks all six main manuscript table claims through `analysis/verify_archive_tables.py`, plus verifies S3/S4 row-level aggregate identities. It does **not** require original tweets, accounts, row-level prediction archives, or an internet connection.

## What passing the checks means — and does not mean

These are checks of **internal consistency of saved aggregate outputs**. They do not re-run the historical RoBERTa neural model, establish a frozen historical model checkpoint, validate the accuracy of crowdsourced human annotations, or establish representativeness of social-media discourse. The 200 overlapping splits are repeated within-archive assessments, not 200 independent studies. GOP grouping is by candidate **mention** and estimates negative **whole-tweet** sentiment, not disapproval of the candidate.

**Data restrictions:** Raw tweet text, account/user metadata, row-level text hashes and predictions, and original historical source CSV files remain excluded. Lawful external access to the two third-party data sources and any permissible reviewer access must be addressed separately. Neither a private GitHub URL nor this branch is public availability.

**Author declarations:** Ethics applicability, informed-consent wording, third-party data redistribution rights, public-code license and final author review are still pending. No approval/exemption is implied by this file.

Do not merge or release publicly until the author completes repository and manuscript checks.
