# New inference with a fixed model revision

On 17 October 2026 the author executed the supplied Colab notebook on the two primary corpora. This is a new inference replication, not recovery of historical model identity. All 14,640 airline and 4,483 GOP binary predictions matched the archived outputs for VADER and RoBERTa. Airline three-class labels also matched; historical GOP three-class agreement cannot be tested with its binary archive.

`audit/locked_inference/` supplies aggregate comparisons, the complete model/runtime lock, and independent downstream verification results. Table S9 contains the four model-by-corpus summaries. Raw tweet text, accounts, individual predictions, and row-level text hashes are excluded.

## Execute with lawful private inputs

Use `analysis/locked_model_replication_colab.ipynb` or install the observed inference requirements in a suitable Python/PyTorch environment and run:

```bash
python analysis/locked_model_replication.py --inputs /private/four_inputs.zip --out /private/new_run
```

The ZIP must contain exactly one copy of each of the four canonical inputs listed in the main README; input bytes are checked against fixed digests. The Colab setup pins the tested package versions and handles PyTorch. The standalone requirements list records the actual CUDA build and therefore assumes a compatible installation source. Model assets download only from the fixed commit; never substitute `main`.

The tokenizer reports a sentinel model_max_length for airline (no explicit historical max_length); no numeric airline cap is retrospectively asserted. GOP uses max_length=128. Output probabilities are new, not reconstructed historical probabilities.

The resulting ZIP contains private individual outputs and must not be published wholesale. Only the summary directory is intended for aggregate release. Budget experiments and auxiliary/duplicate-retained corpora were not re-inferred in this run. Identical primary binary inputs leave existing deterministic budget results unchanged; they do not extend the inference test to additional records or deployment settings.
