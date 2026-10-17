# Final input and statistical audit protocol

All primary and budget estimates preserve their original predictions. Model-card input sensitivity is a separately executed two-condition experiment at the pinned revision. Airline input is source text; GOP input is stripped first-retained text after canonical deduplication. The exact model-card code splits on space, changes a token starting with @ (length>1) to @user, and a token starting with http to http. Other settings are identical within conditions: float32/eager, deterministic algorithms, seed 20261017, airline batch 32/no explicit maximum, GOP batch 24/maximum128. Private probability/label rows are excluded from this repository.

Untruncated lengths include special tokens. Airline's tokenizer sentinel disables automatic truncation; model position embeddings and padding index imply512 total supported sequence tokens. Observed lengths are verified within this capacity; no input is silently capped at the sentinel. Encoded attention-mask lengths are asserted against the applicable actual truncation rule. GOP truncates only above 128.

Example inference rerun (private inputs and outputs remain outside the repository):

```bash
python -m pip install -r requirements-input-audit.txt --extra-index-url https://download.pytorch.org/whl/cpu
python analysis/roberta_input_sensitivity.py --inputs /private/four_validated_inputs.zip --snapshot /private/pinned_model_directory --out /private/rerun_summary --private-out /private/individual_outputs --threads 8
python analysis/round2_statistics.py --inputs /private/inputs --tweet-eval /private/TweetEval --out /private/rerun_statistics
```

Input files are the unchanged four basenames listed in the README. Obtain the exact six model assets from the official model's resolve/3216a57f2a0d9c45a2e6c20157c20c49fb4bf9c7 URLs. Download TweetEval sentiment train_text.txt and val_text.txt from the official repository and verify hashes against audit/round2/overlap_sources.json. No additional labels are collected.

Paired Group-ACC-minus-human losses use the same repeat within every cell. Monte Carlo SE=sample SD/√200, conditional on archive/protocol. Better/tied/worse counts have tolerance 1e-12. Native GOP keeps fixed denominators; all common designs exclude reference ties (comparison tolerance 1e-12). Strict and half-penalty metrics, as well as MAE, are separate losses.

ACC diagnostics count applied preclip excursions separately from fallback. Every event reports average groups per draw and percentage of all group-repetitions. Negative estimated TPR–FPR is not conflated with the absolute<0.10 fallback condition. Clipping-created ties count non-tied reference pairs changed from distinct preclip estimates to equal final estimates; finite-archive estimates are recombined with exact known labels before this comparison. Diagnostic reruns assert equality with the preserved per-repeat scores.

Source rows, identifiers, normalized text, accounts and negative shares are distinct concepts. Repeated-record GOP weighting maps the prediction of the first canonical occurrence back to each eligible source row while keeping its source human label and candidate. This is not new inference on 6,284 input variants. Exact-normalized train/validation screening is applied to both corpora; conflicts count groups and associated records, not proven errors. The native, common, finite-archive and account-disjoint targets must not be pooled.
