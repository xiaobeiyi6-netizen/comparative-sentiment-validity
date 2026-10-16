# Editorial verification access procedure

This protocol is prepared on the author's express agreement to support restricted verification. It is ready to offer to the journal; no editor/reviewer identity, accepted channel, access grant, or completed transfer is asserted.

## 1 Verify distributable results first

Supply Supplementary Code S1 and Tables S1-S8 with the manuscript. The two verification commands in the README check original main tables, all 8,000 airline and 4,800 GOP classifier-row split summaries, and the newly supplied sensitivity aggregates without individual source records. These checks do not establish the historical annotation process or recreate neural inference.

## 2 Resolve the necessary local inputs

| Canonical input | Available author-held filename | Purpose |
|---|---|---|
| `Tweets.csv` | `Tweets(1).csv` | Airline source labels, groups, text and account-name clusters |
| `airline_predictions.csv` | `airline_predictions(2).csv` | Archived aligned VADER/RoBERTa predictions and text digests |
| `GOP_REL_ONLY.csv` | `GOP_REL_ONLY(1).csv` | Debate source labels, candidate groups, texts and account-name clusters |
| `gop_external_validation_results.zip` | `gop_external_validation_results(1).zip` | Primary 4,483-row prediction archive; required internal path is `gop_external_validation_results/row_predictions_and_overlap_flags.csv` |

The author already holds all four inputs. Duplicate copies do not need to be requested from the author to prepare this protocol. Reviewers should obtain the two corpus files directly from their lawful distributors when feasible, retain source attribution and terms, and compare the complete 64-character digests in `audit/original_source_hashes.json`. Renaming a file does not change its digest. Do not replace a mismatch with a new digest merely to make the check pass.

## 3 Arrange additional access only if needed

The editor can specify which claim requires source-level checking and designate a confidential channel or secure analysis arrangement. The author will seek to provide the necessary matching historical inputs or a supervised execution route under applicable source conditions. No email address, reviewer account, password, unrestricted download link, or fixed response time is invented here. Additional source rights are obtained only where the actual terms or intended transfer require them; author willingness alone is not additional permission from other rights holders.

Use the minimum records and fields needed for the agreed check. Account-name fields are needed for the supplied account-cluster sensitivity but not for ordinary group summaries. If a reduced export or controlled environment is used, document its transformation and scope rather than pretending it has the original CSV digest or can execute unmodified scripts. Source-license rights are not overridden by this review protocol. Do not post confidential access links or source records in public issues, repository commits, or ordinary published supplements.

## 4 Execute and record the review

Use the README commands for source checks, airline budget analysis, GOP budget analysis and revision sensitivities. Record the code commit or package digest, runtime, input digests, seeds, commands and numeric differences from supplied aggregates. Keep individual text, account identifiers and text-hash mappings out of the resulting public review report. Source correspondence and statistical reruns remain separate from ethical approval, original annotation certification and locked neural-inference replication.

## Proposed wording for the editor

The author can provide the code and aggregate audit package directly with the submission. For source-level verification, the original corpus CSVs should first be obtained from their cited distributors and checked against the supplied file digests. The author retains the archived prediction exports and matching historical inputs and is willing to arrange confidential verification through a channel agreed with the editor, subject to applicable source terms. Please specify the checks and access arrangement needed. The package reproduces downstream statistics from archived predictions; it does not recreate the original neural inference environment.
