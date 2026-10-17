# Source-level editorial verification procedure

Contact the corresponding author at the address in the manuscript. The cited public baseline and complete supplied Code S1 aggregates require no private source-data access.

1. Obtain the source CSVs from the distributor or the identified acquisition source, subject to the source terms. Compare exact digests with Appendix A and `docs/DATA_PROVENANCE.md`.
2. Statistical reruns additionally need `airline_predictions.csv` and `gop_external_validation_results.zip`, whose exact digests are enforced by `analysis/locked_model_replication.py`. The author retains these original inputs.
3. If matching records or exports cannot be obtained directly, the author and handling editor can arrange restricted inspection by an authorized reviewer under the applicable source conditions. Use an editor-approved confidential transfer or supervised inspection. Do not post these inputs to the public code repository or an unrestricted supplement.
4. Execute the specified source/row checks and statistical scripts. The optional fixed-revision inference script tests the documented new revision; it cannot authenticate the missing historical environment.

This is a standing verification route, not a claim that confidential access has already been granted. No source rights are transferred or relicensed by this procedure. Requests for original annotator manuals or votes must be distinguished from the archived record/prediction verification the author can support.
