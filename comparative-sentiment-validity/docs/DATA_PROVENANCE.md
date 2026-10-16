# Raw data provenance and integrity

| File | Original corpus | SHA256 | Original rows | Source location |
|---|---|---|---:|---|
| `Tweets.csv` | Twitter US Airline Sentiment / Figure Eight | `ea94b23f41892b290dec3330bb8cf9cb6b8bc669eaae5f3a84c40f7b0de8f15e` | 14,640 | https://huggingface.co/datasets/osanseviero/twitter-airline-sentiment |
| `GOP_REL_ONLY.csv` | First GOP Debate Twitter Sentiment / CrowdFlower | `413bae11a4b04a414baffb63407788a3231a06b8ab806caaf9f930b5e2acec86` | 13,871 | https://ptrckprry.com/course/ssd/data/GOP_REL_ONLY.csv |

Both original CSV hashes were checked in the 16 October 2026 analysis session. GOP filtered primary analysis retained 4,483 named-candidate unique-text records. Airline analysis retains 14,640 rows. Reference labels are *overall tweet sentiment* (negative vs neutral/positive), not directly measured approval of the airline or candidate. GOP sources may be unavailable at a later date; access or local copies are subject to original distributors' conditions.

**Reuse rights unresolved:** public download does not imply unrestricted distribution or public re-hosting of tweet text, user IDs, metadata, or derived row-hash mappings. Preserve full sources in a private analyst folder until licensing and platform conditions are reviewed.
