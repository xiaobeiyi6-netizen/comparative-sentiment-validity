# Comparative Sentiment Validity — reproducibility package

**Status:** Private upload candidate, version 0.1.1-review, 16 October 2026. Not a public data release or journal submission.

This repository supports the manuscript *When Automated Sentiment Analysis Reverses Public Discourse Rankings: A Comparative Measurement-Validity Audit Across Two Twitter Contexts*. The analytic estimand is **negative whole-tweet sentiment prevalence among messages grouped by airline or by mentioned debate candidate**. It is **not** representative public opinion, sentiment directed at each person, or a causal algorithm-amplification estimate.

## What this repository includes and omits

Includes: independently checked group-aggregate findings, reproducibility analysis code, raw-file checksums, sources, review notes and basic algebraic tests.

**Deliberately excludes:** copyrighted or privacy-sensitive tweet text; social handles and user metadata; row-level text hashes and predictions (potentially linkable); the original model weights; API keys; the author's phone/email; and individual account identifiers. Publication rights for the two historical raw CSVs have **not yet been verified**. The materials here do **not** grant access to either original dataset.

## Reproduce using your own lawful copies

1. Install Python with `numpy>=2.1,<3` and `pandas>=2.2,<3` from `requirements-analysis.txt`. Run `python -m unittest discover -s tests -v` and `python analysis/verify_archive_tables.py`. The latter runs with only the public-safe *aggregate tables*, without the original tweet text or the saved prediction archives.
2. Obtain the correct raw data under source terms; compare hashes in `audit/original_source_hashes.json` against `Tweets.csv` and `GOP_REL_ONLY.csv`. See `docs/DATA_PROVENANCE.md`.
3. Place in `private_inputs/`: `Tweets.csv`, `GOP_REL_ONLY.csv`, `airline_predictions.csv`, `gop_external_validation_results.zip`. Prediction files are **archived outputs**, not public source files; see `docs/INFERENCE_PROTOCOL.md` for regenerating them with an explicitly fixed *current* model version.
4. Run `python analysis/check_sources.py --input-dir private_inputs`.
5. Run `SCIE_DATA_ROOT=private_inputs SCIE_OUTPUT_DIR=reproduced_outputs python analysis/reproduce_analysis.py` (Unix/macOS) or set the equivalent two environment variables in Windows PowerShell.
6. Compare generated tables with `audit/aggregates/`. The repeated-split experiment draws 200 overlapping splits from **one** historical GOP archive; percentile ranges are *conditional* on the chosen archive.

## Key observational study figures (reference archive)

| Context | Unique/model-evaluation records | Groups | Pairs | VADER reversals | RoBERTa reversals |
|---|---:|---:|---:|---:|---:|
| US airline tweets | 14,640 | 6 | 15 | 3 | 0 |
| GOP debate: unique texts with a named candidate | 4,483 | 10 | 45 | 7 | 7 |

A strict reversal means that the signed *human-reference* difference and the model-predicted difference in group negative proportions have opposite signs. Exact predicted ties are not counted as strict reversals. Gap-threshold analyses select pairs by the original reference gap.

## Reproduction boundaries

- Full original neural inference **was not rerun** in the archived auditing stage; group/pair statistics were reproduced from saved predictions, verified against original source row labels and SHA-256.
- The exact historical RoBERTa model revision and complete inference libraries **are not known**. `analysis/check_local_checkpoint.py` reports only the model's **current** revision, which must not be misrepresented as the historical revision.
- GOP duplicate retention shifts the descriptive estimand from unique expressions to message-occurrence-weighted records; it materially affects results.
- Public and target-directed supplementary datasets are not interchangeable with these whole-tweet main benchmarks.
- The source archives are convenience samples and lack platform-exposure or person-level representativeness.

## Original research responsibility

The author must validate the draft, the data-use conditions, any licensing choice, ethical applicability, and AI-assistance declaration before depositing this publicly or submitting the manuscript. `LICENSE_PENDING.md` and `docs/RELEASE_CHECKLIST.md` are intentional unresolved gates.

## Manuscript tables and reproducibility gates

See `docs/MANUSCRIPT_TABLE_MAP.md` for the source of **each of the six main tables**. The archive now includes the 8,000 aggregate repeated-split outcomes from airline calibration and 4,800 such outcomes from GOP calibration. These records contain repeated-split summary statistics, not individual post text or account data. The saved aggregate outcomes can be independently re-aggregated, but **only** GOP's split-generation is rerun by `analysis/reproduce_analysis.py` when the locally archived row predictions are supplied.

Run `python analysis/verify_archive_tables.py` before uploading or tagging a release. It checks exact summary reaggregation, main numerical claims, and the original reference-gap subsets.

**Repository status:** Private GitHub staging only until copyright, license, model-revision disclosures, ethics applicability, manuscript declarations, and author review have been resolved. Do not claim an actual Zenodo DOI until Zenodo assigns one.
