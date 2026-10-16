# Mapping of the six main manuscript tables to archived outputs

**Manuscript snapshot:** 16 October 2026, pre-submission. A table number refers to the latest 18-page English review manuscript. These are historical-archive analyses, not prospectively preregistered studies.

| Manuscript exhibit | Input or aggregate file | Exact check performed | Note |
|---|---|---|---|
| Table 1. Study and overall classifier summary | `audit/aggregates/main_metrics.csv`, `reversal_counts.csv`; source CSV audit | Dataset n, full-corpus negative shares, **binary** accuracy | Three-class accuracies 48.99%/81.00% are **not** Table 1 binary accuracies. |
| Table 2. Six-airline group rates | `audit/aggregates/airline_group_prevalence.csv` | Compare n and displayed two-decimal human/VADER/RoBERTa shares | Airlines are not a random sample of travelers. |
| Table 3. Airline annotation-budget analysis | `audit/aggregates/airline_calibration_200_repeated_splits.csv`, `airline_calibration_budget_summary.csv` | 400 labels/airline, average MAE and all-15-pair strict reversal | Estimator outcomes are conditional on overlapping repeated splits; not 200 studies. |
| Table 4. Ten GOP groups | `audit/aggregates/gop_group_prevalence.csv` | Compare n and rounded rates | Candidate-mention messages, **not** target-directed approval. |
| Table 5. Reversal/gap sensitivity | `audit/aggregates/reversal_counts.csv`, `audit/aggregates/pairwise_bias_reversal_mechanism.csv` | Strict reversals and number of original reference pairs meeting 3/5/10-pp threshold | At least 10 pp means >= 10 pp in **original complete human archive**, not heldout. |
| Table 6. GOP annotation-budget analysis | `audit/aggregates/gop_calibration_200_repeated_splits.csv`, `gop_calibration_budget_summary.csv` | 100 labels/candidate, pooled/group-adjusted/direct-human MAE and rates | The 200 splits reuse the same archive and are a sensitivity study, not separate samples. |

**Important boundaries:**
- These summary files contain no tweet text, social accounts, or row-level text hashes. Both raw datasets and the model-prediction archives are intentionally excluded from the public repository.
- `analysis/reproduce_analysis.py` recomputes all two-corpus main statistics and GOP calibration from raw archives and saved row predictions *when those lawful local inputs are supplied*. It does not rerun neural inference.
- The **airline budget analysis** is preserved as observed repeated-split results; the original Colab experiment code and further provenance remain in the researcher's private archive. Re-aggregation of its saved splits can be independently checked with `analysis/verify_archive_tables.py`. This does **not** constitute a fresh rerun from raw tweets of every airline calibration split.
- Raw file hashes in `audit/original_source_hashes.json` validate exact byte identity only, not licenses or future availability.
- The English manuscript, author declarations, and IRB status require author review before journal submission.

