# Reviewer access and data availability — draft protocol

**Research:** historical whole-tweet negative-sentiment measurement audit across airline and GOP candidate-mention message groups.

## Access levels

| Level | Materials | Status |
|---|---|---|
| A — aggregate-only | Group confusion matrices, pairwise bias decomposition, 200-split summaries, S3 and S4, consistency tests | Available **within this private repository to authorized collaborators**. Not presently public. |
| B — locally reproducible, rights-dependent | Raw historical CSVs, row-level text hashes, archived predictions, full script inputs | Private analyst copies only; not authorized for public redistribution. Reviewers may need to independently acquire lawful source copies. |
| C — original full neural inference | Historical RoBERTa revision and full dependency lockfile | Not retained; exact historical inference is **not** reproducible as currently archived. |

## Manuscript wording (only when accurate at submission)

**Data Availability Statement — current private stage**

> The analyses used two previously distributed historical Twitter corpora. Source locations and checksums are documented in the reproducibility notes. Row-level source messages and archived model predictions are not publicly deposited because the author has not established redistribution permissions and must avoid disclosing potentially identifying social-media data. Aggregate statistics and verification scripts have been prepared in a private audit repository. Any reviewer-access arrangement and eventual release URL will be specified only after they are established.

**Code Availability Statement — current private stage**

> Scripts for checking archived group-level and repeated-split aggregate results are preserved in an author-controlled private GitHub repository. The repository is not publicly accessible. The independent checks do not re-execute the historical RoBERTa inference; its exact historical model revision is unavailable. Any publicly accessible release will be cited once it actually exists.

If the editor requires underlying row-level data, do not promise unrestricted access. Ask about confidential review procedures and third-party usage rights, and supply only the materials permitted by the sources' terms.

## Before manuscript submission

- Verify exact third-party dataset redistribution and social-media platform conditions.
- Decide whether authorized reviewers can access aggregate-only material privately, or whether a separately scrubbed review ZIP should be uploaded as supplementary material.
- Ensure the article's Data Availability and Code Availability statements match the real access state.
- Verify required ethics and informed-consent wording independently: these documents do not establish exemption.
- Preserve the original source SHA-256 values and computational environment limitations.
