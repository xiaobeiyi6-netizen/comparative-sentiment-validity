# Historical inference — what is and is not documented

Source notebooks from the analyst archive specify:

- **VADER:** `vaderSentiment.vaderSentiment.SentimentIntensityAnalyzer`, negative if `compound <= -0.05`; for airline, neutral if in between and positive if `>= 0.05`. A binary negative/not-negative indicator is used for comparative analysis.
- **RoBERTa:** `cardiffnlp/twitter-roberta-base-sentiment-latest`; via Hugging Face `transformers.pipeline('text-classification', ... , truncation=True)`, mapping `negative/neutral/positive` labels. GOP notebook additionally specifies `max_length=128`, `batch_size=24`; the airline notebook calls with `batch_size=32` and no explicit `max_length`.
- **Supervision:** the pre-trained sentiment model was not fine-tuned on the study’s human labels in these validation experiments. Model providers report TweetEval sentiment fine-tuning. Thus potential supervision overlap must be investigated in each corpus.
- **Original exact checkpoint revision:** **UNVERIFIED**. Original full `transformers`/`tokenizers`/`vaderSentiment` versions were not all recorded. Calling the model's current repository head is **not evidence** of the historical snapshot.
- The GOP audit records Python 3.13.16, pandas 2.2.3, numpy 2.1.3. Airline metadata recorded PyTorch 2.11.0+cpu, no GPU. These are partial historical records, not a complete lockfile.

Re-running inference with today's downloads is a *new replication run*. It must be labeled as such and compared row by row with archived outputs rather than silently replacing historical predictions. The analysis script in this release deliberately starts from previously archived predictions, preserving the historical outcome.
