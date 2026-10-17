# Comparative sentiment validity audit code

This package accompanies **Ranking Reversals in Automated Estimates of Negative Message Shares: An Audit of Two Twitter Archives**. It supplies executable statistical code, aggregate audit records, Tables S1–S24 and Figures 1–3. Original eligible code is MIT licensed; third-party data, models and dependencies are not relicensed.

This complete revision is Supplementary Code S1, version 0.4.0-input-audit. The authorized complete code/aggregate revision is published on branch `revision/reviewer-20261017` in https://github.com/xiaobeiyi6-netizen/comparative-sentiment-validity. The manuscript and outer package provenance identify its immutable commit. Use the complete package and its SHA-256 manifests for S1–S24; public baseline 77ecdd19d93eb0bce92063cdf9dd89ceefe63975 remains earlier provenance, rather than the source of all final tables. No DOI is claimed.

## Aggregate checks without source posts

```bash
python -m pip install -r requirements-statistics.txt
python analysis/verify_archive_tables.py
python analysis/verify_package.py
python analysis/verify_reviewer_revision.py
python analysis/verify_round2.py
python analysis/verify_release_integrity.py
```

These checks reaggregate stored outputs and verify identities; they do not establish each original human annotation as correct. The last check verifies the added budget designs, diagnostics, tie treatment and regenerated figure assets.

## Rerun from lawful local inputs

Keep the following four files in a private directory. No source tweets, account strings, row-level text hashes or individual prediction exports are distributed here.

- `Tweets.csv`: 14,640 source records.
- `airline_predictions.csv`: aligned original three-class predictions and reference labels.
- `GOP_REL_ONLY.csv`: 13,871 source records.
- `gop_external_validation_results.zip`: preserved primary-row prediction archive.

Exact file hashes are recorded in `analysis/locked_model_replication.py`, and acquisition routes in `docs/DATA_PROVENANCE.md`. Use direct distributor copies and digest matching first; editorial requests for unavailable matched inputs go to the corresponding author through the process in `docs/REVIEWER_ACCESS.md`.

```bash
python -m pip install -r requirements-reviewer.txt
python analysis/airline_budget.py --raw /absolute/private/inputs/Tweets.csv --pred /absolute/private/inputs/airline_predictions.csv --out rerun_airline
SCIE_DATA_ROOT=/absolute/private/inputs SCIE_OUTPUT_DIR=rerun_gop python analysis/reproduce_analysis.py
python analysis/revision_sensitivity.py --inputs /absolute/private/inputs --out rerun_revision
python analysis/reviewer_revision.py --inputs /absolute/private/inputs --out rerun_reviewer
```

The last script conducts VADER input/lexicon diagnostics, native tie reaggregation, a fresh paired bootstrap, common-formula holdouts, complete finite-archive evaluation and account-disjoint budget evaluation. It does not run a neural model, recruit annotators, tune an optimal k, or replace the primary archived predictions. See `docs/REVIEWER_REVISION_20261017.md` and protocol JSON for precise targets and seeds.

## Figures and inference provenance

```bash
python -m pip install -r requirements-figures.txt
python analysis/make_figures.py
```

Figures are numerical plots supplied in 600 dpi PNG and vector PDF/SVG. Figure 2 has prevalence and ordering panels and a genuine log2 budget axis. Its PNG is nonempty. Recreating PDFs can alter metadata bytes without altering plotted values.

The separately completed 17 October 2026 fixed-revision inference matched all primary binary predictions. The script/notebook and Table S9 reside in `analysis/`, `audit/locked_inference/` and `supplementary_tables/`. This is a new run, not recovery of the historical model or software environment. Legacy filenames containing “independent verification” refer to computational rechecking within the author's AI-assisted workflow, not validation by an independent research team.

## Evidence and scope

The original input protocol leaves handles and URLs in the text. VADER recognizes @United as the positive word united: masking the handle eliminates its three airline inversions but leaves substantial prevalence bias. This sensitivity qualifies, rather than erases, the original raw-input audit.

Label budgets retrospectively reuse released labels. Held-out transfer and complete-archive estimation are different tasks; the airline comparison of human-only and model-assisted ordering changes between them. Neither these records nor their resamples represent current public opinion or platform-wide probability samples. Source-specific human labels are fallible; complete original annotation manuals and individual votes were not recovered. Product and SemEval exploratory numerical results are not part of this revision's empirical evidence.

Ethics and consent declarations in the revised manuscript state non-applicability for this secondary archive analysis. No institutional approval, exemption or waiver number is invented. The author's reported editorial clarification that no additional determination is required is not represented as an institutional approval. No confidential editor correspondence is distributed.

## File map

- `Supplementary_Tables_S1_S24.md`: readable selections, notes and full-table CSV links by filename.
- `supplementary_tables/`: full-precision S1–S24 CSVs, including S17b.
- `audit/aggregates/`, `audit/revision/`: preserved native outputs and earlier revision sensitivities.
- `audit/reviewer_revision/`: new aggregate outputs, per-repeat statistics and metadata.
- `docs/`: current methods, source/license evidence and editorial access instructions.
- `docs/historical/`: superseded editorial records, retained only as history.

Historical records are not the current release checklist. Do not distribute the four private individual inputs or install artifacts with this public package.

## Paired RoBERTa input audit and final statistical diagnostics

`analysis/roberta_input_sensitivity.py` actually executes original and model-card inputs at the same fixed revision. The exact source bytes are validated and the original binary predictions must match the archives. Current CPU runtime versions and fixed model asset hashes are in `audit/roberta_input/runtime.json`; this is separate from the earlier T4 run. The model-card condition changes only the specified token-placeholder preprocessing. Budget tables continue to use original-input predictions. S19a/b/c retain overall/group results, confusion counts and all reversal identities; S20 retains token diagnostics.

Keep all row outputs in a private directory outside this repository. The four lawful private inputs must be zipped with their unchanged basenames. Download only the model assets at commit 3216a57f2a0d9c45a2e6c20157c20c49fb4bf9c7 (the pinned config, model bin, vocabulary, merges, special-token map and README); do not update the revision or substitute model weights. See `docs/ROUND2_INPUT_AND_STATISTICS.md` for commands and operational definitions.

`analysis/round2_statistics.py` generates paired differences, conflict/overlap counts and ACC diagnostics. It asserts per-repeat equality with all stored common-design scores. `analysis/verify_round2.py` reconstructs the aggregate metrics without source text. S21 records simulation-mean precision; S22 distinguishes mean groups per draw from group-repetition percentages. S23 and S24 report actual reference conflicts and matching scope. Source records and tweet identifiers are not independent dissemination events by definition.

Airline common 400 ordering is similar for Group ACC and human-only and depends on tie penalties. In finite-airline estimation, Group ACC has fewer reversals than human-only but more than raw CC. Account comparisons use matched 100 budgets. No universal estimator or budget optimum is asserted.
