# GitHub private repository: upload and check

1. Keep the repository **Private**. Download the `GitHub_仅可上传的仓库内容_20261016.zip` package and extract it.
2. Open your GitHub repository > `Add file` > `Upload files` and select or drag **the CONTENTS** of `comparative-sentiment-validity/` into the repository root. (Do **not** upload the entire ZIP as one file; it will not expose code directories.)
3. If you previously uploaded the earlier v0.1.0 repository, replace each existing file and add the new ones from this review candidate. GitHub may reject duplicate names within one upload; inspect and commit changes as needed.
4. Commit message: `Audit manuscript tables and include safe calibration summaries`.
5. Confirm the repository shows `README.md`, `analysis/verify_archive_tables.py`, `audit/aggregates/airline_calibration_200_repeated_splits.csv`, `audit/aggregates/gop_calibration_200_repeated_splits.csv`, `docs/MANUSCRIPT_TABLE_MAP.md`, `tests/`.
6. NEVER upload: `Tweets.csv`, `GOP_REL_ONLY.csv`, the original prediction CSVs/ZIPs, Colab session outputs, text hash mappings, author phone number, account credentials, or the entire private study archive. This archive excludes them.
7. If GitHub shows repository Public, switch it to Private until licenses and journal/ethics statements have been resolved. Do not publish a GitHub Release or request a Zenodo DOI yet.
8. Optional: connect GitHub to ChatGPT to allow repo-specific future checks after authorization; otherwise share your repository URL. A private repo URL by itself does not grant access.

**Smoke test on a machine with Python and pandas/numpy:**
```bash
python -m pip install -r requirements-analysis.txt
python -m unittest discover -s tests -v
python analysis/verify_archive_tables.py
python analysis/verify_release_integrity.py
```

This public-safe aggregate test does not require original tweets, historical prediction files, GPU or model weights.
