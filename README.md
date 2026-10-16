# Supplementary Code S1 and revision supporting materials

This package accompanies the revised comparative sentiment measurement-validity manuscript. It contains reviewable code, aggregate tables, regenerated figure assets, and revision sensitivity outputs. It contains no tweet text, account-name records, row-level text hashes, or individual predictions. Original statistical code is licensed under MIT; see `LICENSE` and `LICENSE_SCOPE.md`. Third-party source data and individual prediction exports are not included or relicensed. The development repository is still private at this preparation step; a public release DOI is not claimed.

## What can be checked without restricted inputs

From this package directory, install the statistical dependencies, then run:

```bash
python -m pip install -r requirements-statistics.txt
python analysis/verify_archive_tables.py
python analysis/verify_package.py
```

The first command checks main tables and reaggregates all 8,000 airline and 4,800 GOP classifier-row summaries. The second checks package hashes, error identities, new sensitivity summaries, and k=100 agreement. These checks validate stored aggregates and do not reconstruct the source human annotations or original neural inference. The complete budget protocols were separately executed during this revision using lawful local source records and archived predictions. Their 40 and 24 summaries matched the preserved summaries to all stored numerical precision.

## Full statistical reruns with lawful local inputs

Place these exact files in a private directory you control; the package does not supply them:

- `Tweets.csv`: 14,640-row source CSV, expected digest in audit/original_source_hashes.json.
- `airline_predictions.csv`: aligned source export with reference, vader, roberta, text_sha256. Three-class labels are 0/1/2, negative=0.
- `GOP_REL_ONLY.csv`: 13,871-row source CSV, expected digest in audit/original_source_hashes.json.
- `gop_external_validation_results.zip`: preserved archive with `gop_external_validation_results/row_predictions_and_overlap_flags.csv` containing the 4,483 primary rows.

Run from the package root, replacing `/absolute/private/inputs` with that lawful local directory:

```bash
python analysis/airline_budget.py --raw /absolute/private/inputs/Tweets.csv --pred /absolute/private/inputs/airline_predictions.csv --out rerun_airline
SCIE_DATA_ROOT=/absolute/private/inputs SCIE_OUTPUT_DIR=rerun_gop python analysis/reproduce_analysis.py
python analysis/revision_sensitivity.py --inputs /absolute/private/inputs --out rerun_revision
```

The recovered airline routine uses seed 20261015, upward-rounded 20% holdouts and independently sampled budgets. GOP uses seed 20261016, nearest-integer 20% holdouts and nested budgets. Calibration and evaluation records never overlap within a split. k=100 and the exact native smoothing/shrinkage formulas are preserved separately for each corpus; see manuscript Appendix A2. No code trains a classifier or regenerates historical neural predictions. To regenerate all figure formats from exact aggregates, install requirements-figures.txt and run `python analysis/make_figures.py`. The PNG/PDF/SVG assets are also supplied directly. Regeneration creates new PDF metadata and therefore may change figure-file hashes without changing their plotted data.

## Files

- `supplementary_tables/`: S1–S8 full-precision CSVs.
- `Supplementary_Tables_S1_S8.md`: readable tables with units and interpretation.
- `audit/aggregates/`: original main summaries and regenerated original split records.
- `audit/revision/`: reference checks, shrinkage and pairset summaries, and conditional bootstrap aggregate records.
- `analysis/`: executable statistical scripts and verification checks.
- `audit/REVISION_RUNTIME.json`: current statistical runtime, not a reconstruction of historical inference versions.
- `docs/INFERENCE_PROTOCOL.md`: historical partial inference notes; missing revision/version information remains missing.
- `figures/`: rebuilt Figures 1–3 as 600 dpi PNG and vector PDF/SVG.
- `revision_changes.json`: paragraph-level before/after revision record.
- `02_Revision_Verification_and_Action_Log.md`: Chinese item-by-item verification and author actions.

## Boundaries

The exact historical RoBERTa commit, tokenizer snapshot, VADER package version, complete inference environment, and prediction-generation timestamps remain unavailable. Current software cannot be retrospectively asserted as those versions. New source inference would be a separately documented replication. Only archived prediction-based statistics are reproduced here. Brand-target and SemEval historical supplement results were not fully rerun in this revision and remain limited construct/leakage diagnostics.

The source data are historical curated/convenience archives, not samples of current public attitudes. Splits, bootstrap replicates, and group pairs are dependent. Their quantiles are conditional archive variability. The new k grid does not establish an optimal deployment parameter. Institutional ethics/consent applicability remains undetermined. The author has authorized MIT release of eligible original code and is willing to support editorial source-level verification through the procedure in `docs/REVIEWER_ACCESS.md`. A specific confidential channel has not yet been agreed with the journal. No DOI, ethics approval, existing public repository access, or unrestricted raw-data distribution permission is claimed.

## Licensing and editorial access

The author's code authorization has been implemented in `LICENSE`. Dataset provenance and current source-license evidence are in `THIRD_PARTY_NOTICES.md`, `docs/DATA_PROVENANCE.md` and `docs/LICENSE_EVIDENCE.md`. The four required individual inputs already exist in the author's archive. `docs/REVIEWER_ACCESS.md` explains direct source retrieval, digest matching and, if necessary, a restricted journal-arranged verification route. This is not an offer to relicense source records under MIT. Public availability and institutional ethics status are independent facts and will be updated only when actually established.
