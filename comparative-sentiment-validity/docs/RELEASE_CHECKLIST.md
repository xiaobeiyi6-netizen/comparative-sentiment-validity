# Review before releasing a public repository or Zenodo DOI

- [ ] Author confirms all code was reviewed and repository contents are accurate.
- [ ] No raw text, user handles, private contact data, row-level unique hashes/predictions, access tokens, or private paths included.
- [ ] Source dataset terms and license compatibility have been checked and documented.
- [ ] Author selects and adds a code license; none is granted by `LICENSE_PENDING.md`.
- [ ] Verify complete computational environment or state clearly that exact historical RoBERTa commit is unavailable.
- [ ] Clarify model pretraining and supervised fine-tuning overlap limitations.
- [ ] Verify institution's ethics applicability and required journal wording separately; never claim nonexistent approval.
- [ ] Review human-reference annotation source and copyright/consent conditions.
- [ ] Add final versioned GitHub URL and, once released, the actual Zenodo DOI to manuscript; never invent them.
- [ ] Confirm contribution, AI assistance, conflict, funding, and research integrity declarations.
- [ ] Make repository public only after completing the privacy and licensing gates.

Suggested route: private GitHub first; audit and add license; make *code and aggregate tables only* public; connect Zenodo after public release eligibility; create a tagged release; cite its actual DOI. GitHub-to-Zenodo integration does not archive private repositories.
