# Source records and annotation-task evidence

| Private input | Corpus and actual acquisition source | Source SHA-256 |
|---|---|---|
| Tweets.csv | CrowdFlower/Figure Eight Twitter US Airline Sentiment; https://huggingface.co/datasets/osanseviero/twitter-airline-sentiment | ea94b23f41892b290dec3330bb8cf9cb6b8bc669eaae5f3a84c40f7b0de8f15e |
| GOP_REL_ONLY.csv | CrowdFlower First GOP Debate Twitter Sentiment; https://ptrckprry.com/course/ssd/data/GOP_REL_ONLY.csv | 413bae11a4b04a414baffb63407788a3231a06b8ab806caaf9f930b5e2acec86 |

Publisher listings: https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment and https://www.kaggle.com/datasets/crowdflower/first-gop-debate-twitter-sentiment. Publisher metadata was retrieved on 17 October 2026 from the official public `/api/v1/datasets/view/crowdflower/<slug>` routes. Reduced task/license evidence is stored in `audit/reviewer_revision/*_source_evidence.json`.

The airline description concerns tweet polarity in an airline-service context, followed by reasons for negative labels. The grouping uses the released `airline` field; a complete original assignment manual was not recovered. The debate description separately asks relevance, candidate mention, subject and sentiment of the tweet. Its `candidate` field is not a target-directed sentiment label. Both provide source-specific message-level polarity judgments, but are not proven interchangeable measures.

The public distribution scripts at https://github.com/benhamner/crowdflower-airline-twitter-sentiment/blob/c5841fb0cd3b6a3f346cd7abc4884c44975fe40e/src/process.py and https://github.com/benhamner/crowdflower-first-gop-debate-twitter-sentiment/blob/c31e96fadf3f886364fd010bbe78ac3cef4ba8ec/src/process.py describe reformatting. They do not recover original annotator instructions or votes. The course copy preserves colon-separated confidence names rather than the publisher reformatting's underscore convention.

`airline_sentiment_confidence`, `sentiment:confidence` and `candidate:confidence` are supplied response-confidence fields. Without the aggregation manual and individual votes, they are not treated as calibrated correctness probabilities, raw agreement coefficients or independent reliability estimates. A confidence score of one is a supplied-score filter, not verified annotator unanimity. Gold-designated fields are not substituted for the primary released labels.

The four input digests and exact row checks are enforced in the replication and reviewer scripts. All 14,640 airline and 4,483 GOP primary prediction rows match their reference and source text hashes. This verifies computational correspondence, not every annotator judgment or collection event.

The released airline data contain repeated tweet identifiers and repeated text; the GOP repeated-row sensitivity likewise includes repeated identifiers. These diagnostics do not reconstruct the full history of reposting, collection or release-stage duplication. Do not call repeated rows verified exposure events.


Final input-protocol and statistical extensions are documented in ROUND2_INPUT_AND_STATISTICS.md and Tables S19–S24. S11 model-card placeholders concern VADER; S19 is the separately executed RoBERTa comparison. All budget results continue to use original-input predictions.
