#!/usr/bin/env python3
"""Print an auditable CURRENT Hugging Face model commit, not a historic inference claim.

Requires internet and huggingface_hub; no text or personal information is uploaded.
"""
import argparse,json,datetime
p=argparse.ArgumentParser();p.add_argument('--model',default='cardiffnlp/twitter-roberta-base-sentiment-latest')
a=p.parse_args()
from huggingface_hub import HfApi
info=HfApi().model_info(a.model)
print(json.dumps({'model_id':a.model,'resolved_CURRENT_head_sha':info.sha,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'warning':'This is the current model repository head, NOT proof of the checkpoint used in the original historical inference.'},indent=2))
