# Third party materials and attribution

## Source corpora

The study uses previously distributed human-labeled social-media corpora credited to CrowdFlower, subsequently Figure Eight:

| Corpus | Publisher page | Listed dataset license | Access copy used in the audit |
|---|---|---|---|
| Twitter US Airline Sentiment | https://www.kaggle.com/datasets/crowdflower/twitter-airline-sentiment | CC BY-NC-SA 4.0 | https://huggingface.co/datasets/osanseviero/twitter-airline-sentiment |
| First GOP Debate Twitter Sentiment | https://www.kaggle.com/datasets/crowdflower/first-gop-debate-twitter-sentiment | CC BY-NC-SA 4.0 | https://ptrckprry.com/course/ssd/data/GOP_REL_ONLY.csv |

License terms: https://creativecommons.org/licenses/by-nc-sa/4.0/

The airline publisher describes its Kaggle files as a reformatted version of the original CrowdFlower release. The airline mirror also identifies CC BY-NC-SA 4.0. The GOP course-hosted copy does not independently establish license provenance. The audit matched local source bytes to the manuscript fingerprints; it did not newly download every publisher version and prove byte identity to the currently listed Kaggle release. Do not use a license label on another Kaggle user's notebook as evidence about these datasets.

The source license requires appropriate attribution, compliance with its noncommercial condition, and ShareAlike licensing where applicable to shared adaptations. It does not necessarily settle other people's privacy, publicity, or moral rights. No finding is made here that a particular commercial publication or redistribution satisfies every applicable condition. The public code package omits source tweets, account fields, row-level identifiers/hashes, and individual prediction files. See `docs/REVIEWER_ACCESS.md` for the review route.

## Software and model assets

The original statistical scripts import Python standard-library modules, NumPy and pandas; figure generation additionally imports Matplotlib. Their implementations are installed separately, not copied into the package. The optional checkpoint-inspection script in the repository uses `huggingface_hub`. Users must preserve the notices and conditions of dependencies in their own redistribution.

VADER and `cardiffnlp/twitter-roberta-base-sentiment-latest` are credited as the sources of historical archived predictions. Neither pretrained weights nor the VADER lexicon is bundled. Their distribution terms are not replaced by this code license. Exact historical neural revision, tokenizer snapshot and full inference environment remain unavailable. The documented new fixed-revision inference comparison matches primary archived predictions; it does not identify their historical environment. The reviewer extension reruns VADER for explicit input diagnostics, using a separately installed dependency, and otherwise reuses archived neural predictions.

## Original code and AI assistance

The original analysis and verification code was assembled from the author's study materials and revised with disclosed AI assistance. The MIT notice records the author's permission to release eligible code, not an external ownership audit or certification of scientific results. No third-party copyright header was removed during this release preparation.
