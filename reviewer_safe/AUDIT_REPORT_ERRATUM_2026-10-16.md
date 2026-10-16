# Reviewer aggregate-report correction — 2026-10-16

The earlier **standalone reviewer-safe ZIP's** `VERIFICATION_RESULT.json` reported erroneous corpus-wide `pred_negative_pct` fields: a variable used for predicted-negative count was overwritten by the final pairwise predicted difference. This was a **generated JSON report bug**, not a change to source data or the manuscript's archived main summary.

**Corrected predicted-negative whole-corpus percentages:** Airline VADER 30.4918%, Airline RoBERTa 58.8934%; GOP VADER 30.3368%, GOP RoBERTa 42.3600%. Original human-reference rates: Airline 62.6913%, GOP 58.5545%.

The standalone script now separates `pred_count` from `pred_diff` and checks four corpus/model percentages against Table 1. An updated safe package was generated with corrected report, checksum manifest, and an erratum. It was unpacked to a fresh directory and passed all original aggregate-only verification tests.

The **GitHub review-branch** script `reviewer_safe/verify_reviewer_safe_repo.py` has also been updated to independently reconstruct and verify **Table 1 whole-corpus predicted proportions and binary accuracy** from group confusion matrices, in addition to its S3/S4, pairwise reversal and budget reaggregation checks. A pending/recent GitHub Actions run must be reviewed separately from local test success.

The exact historical RoBERTa revision, raw-source redistribution rights, ethics applicability, and public release remain unresolved. No raw tweets or row-level predictions were uploaded.