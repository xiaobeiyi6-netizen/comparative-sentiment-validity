# Data provenance and integrity

| Local input | Original corpus | SHA256 of audited bytes | Rows | Access source |
|---|---|---|---:|---|
| `Tweets.csv` | Twitter US Airline Sentiment, CrowdFlower/Figure Eight | `ea94b23f41892b290dec3330bb8cf9cb6b8bc669eaae5f3a84c40f7b0de8f15e` | 14,640 | https://huggingface.co/datasets/osanseviero/twitter-airline-sentiment |
| `GOP_REL_ONLY.csv` | First GOP Debate Twitter Sentiment, CrowdFlower/Figure Eight | `413bae11a4b04a414baffb63407788a3231a06b8ab806caaf9f930b5e2acec86` | 13,871 | https://ptrckprry.com/course/ssd/data/GOP_REL_ONLY.csv |

Both source digests were recalculated from the actual local files during the 16 October 2026 revision. The 14,640 airline prediction records and the 4,483 primary GOP records were aligned with their source texts and reference labels. This verifies correspondence, not the authenticity of every historical annotation or the complete original collection process. Reference labels concern overall message sentiment rather than approval of a named airline or candidate.

## License evidence and distribution decision

The publisher pages identify both corpora as CC BY-NC-SA 4.0, and the airline access mirror lists the same license. See `LICENSE_EVIDENCE.md` for URLs and evidence limits. The corpus name and local hash identify the analyzed inputs; a hash alone is not a license, and the present publisher pages are not proof of identical historical download terms or of all underlying post rights.

The author agrees to provide feasible editorial verification. The public package nevertheless supplies code and statistical aggregates rather than re-hosting source posts or account records. Full statistical reruns need lawful access to the four local inputs in the README, including archived prediction exports. Reviewers should first use the source distributors for the corpus CSVs and compare digests. If a matching copy or archived prediction is unavailable, the author can arrange a journal-approved restricted review route, subject to applicable source conditions. That route is described concretely in `REVIEWER_ACCESS.md`; no request has yet been received or access granted to a third party through this revision.

Changing the data license or imposing new legal restrictions on CC-licensed materials is not part of this procedure. Author-specific handling requests concern confidential review copies, access credentials, account-associated fields, and unpublished prediction provenance, and cannot remove rights already granted by the applicable source license.
