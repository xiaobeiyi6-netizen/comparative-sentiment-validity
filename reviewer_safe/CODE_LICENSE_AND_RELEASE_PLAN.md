# Code-only license and release plan — author review

**Proposed choice:** MIT for code solely owned by the author. This is a plan, **not a current grant of a license**. The repository remains private, and the main branch retains `LICENSE_PENDING.md`.

## What may eventually be licensed under MIT
- Original author-controlled analysis scripts and small numerical unit tests, subject to independent authorship and third-party license checks.
- Documentation owned by the author if specifically included in the eventual public code release.

## What is expressly excluded from this proposal
- `Tweets.csv`, `GOP_REL_ONLY.csv`, their text, metadata, user handles and tweet IDs.
- Row-level text hashes or prediction archives including `airline_predictions.csv` and `gop_external_validation_results.zip`.
- Third-party annotation labels when redistribution is not authorized.
- Pretrained model weights, external datasets, third-party packages, and third-party copyrighted material.
- The academic manuscript and figures unless separately licensed or permitted.

## Why no license is committed yet
1. The author must review all relevant code and contributions and confirm rights to license it.
2. Some scripts may embed or depend on third-party code: verify attribution and provenance first.
3. Data reuse rights do not follow from code authorship or a public download location.
4. A root `LICENSE` file could be misread as extending to all bundled material unless the release is carefully scoped.

## Publication steps once the above is cleared
- Assemble a **code-and-aggregate-only** public repository/release, without private inputs.
- Apply standard MIT text to the author's own release code only and add a `LICENSE_SCOPE.md` clarifying excluded datasets, pretrained weights and third-party content.
- Preserve explicit source provenance and integrity checks for independently acquired datasets.
- Tag a reviewed commit; connect Zenodo and insert the **actual** DOI only if a release is created.
- Update the article's Code Availability Statement to reflect what is actually accessible.

No legal or ethics compliance is established by this planning note.
