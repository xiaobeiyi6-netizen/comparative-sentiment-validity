# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""Paired, fixed-revision raw/model-card input audit; aggregate/public output only.

All row-level predictions, probabilities and lengths are written to --private-out,
which must remain outside the public repository. Run both conditions in the same
process, device, dtype, batch sizes and tokenizer. No budget/model tuning occurs.
"""
import argparse, datetime, hashlib, importlib.metadata, itertools, json, os, platform, random, time
from pathlib import Path
import numpy as np
import pandas as pd
from locked_model_replication import load_inputs, MODEL_ID, MODEL_REVISION, EXPECTED_INPUT_HASHES, file_hash

def preprocess(text):
    # Exact space-token algorithm in the model card at the pinned revision.
    result=[]
    for token in text.split(' '):
        token='@user' if token.startswith('@') and len(token)>1 else token
        token='http' if token.startswith('http') else token
        result.append(token)
    return ' '.join(result)

def report(corpus,d,predictions):
    groups=[];pairs=[];summary=[]
    for condition,y in predictions.items():
        frame=d[['group','human_negative']].copy();frame['pred']=y
        for g,z in frame.groupby('group',sort=True):
            h=z.human_negative.to_numpy().astype(bool);p=z.pred.to_numpy().astype(bool)
            groups.append(dict(corpus=corpus,condition=condition,group=g,n=len(z),
                reference_negative_pct=100*h.mean(),negative_pct=100*p.mean(),
                TP=int((h&p).sum()),FN=int((h&~p).sum()),FP=int((~h&p).sum()),TN=int((~h&~p).sum())))
    g=pd.DataFrame(groups)
    raw=g[g.condition=='original'].set_index('group');card=g[g.condition=='model_card'].set_index('group')
    for a,b in itertools.combinations(raw.index,2):
        gap=float(raw.loc[a,'reference_negative_pct']-raw.loc[b,'reference_negative_pct'])
        x=float(raw.loc[a,'negative_pct']-raw.loc[b,'negative_pct']);z=float(card.loc[a,'negative_pct']-card.loc[b,'negative_pct'])
        r=gap*x<0;s=gap*z<0
        status='preserved_reversal' if r and s else 'disappeared_reversal' if r else 'new_reversal' if s else 'neither'
        pairs.append(dict(corpus=corpus,a=a,b=b,reference_gap_pp=gap,original_gap_pp=x,model_card_gap_pp=z,
            original_reversal=int(r),model_card_reversal=int(s),transition=status))
    pair=pd.DataFrame(pairs)
    for condition,y in predictions.items():
        sub=g[g.condition==condition];changed=np.asarray(predictions['original'])!=np.asarray(predictions['model_card'])
        r=dict(corpus=corpus,condition=condition,n=len(d),binary_changes=int(changed.sum()),
            binary_change_pct=100*changed.mean(),reference_negative_pct=100*d.human_negative.mean(),
            negative_pct=100*np.mean(y),binary_accuracy_pct=100*np.mean(y==d.human_negative.to_numpy()),
            group_MAE_pp=np.abs(sub.negative_pct-sub.reference_negative_pct).mean(),
            raw_binary_changes_vs_archived=int(np.sum(predictions['original']!=d.old_RoBERTa.to_numpy())))
        for threshold in [0,3,5,10]:
            eligible=pair[(pair.reference_gap_pp.abs()>=threshold)&pair.reference_gap_pp.ne(0)]
            prefix='original' if condition=='original' else 'model_card'
            r[f'gap{threshold}_pairs']=len(eligible);r[f'gap{threshold}_reversals']=int(eligible[prefix+'_reversal'].sum())
        summary.append(r)
    return pd.DataFrame(summary),g,pair

def main(args):
    os.environ['CUBLAS_WORKSPACE_CONFIG']=':4096:8'
    import torch
    from transformers import AutoTokenizer,AutoModelForSequenceClassification
    random.seed(20261017);np.random.seed(20261017);torch.manual_seed(20261017)
    torch.set_num_threads(args.threads);torch.use_deterministic_algorithms(True)
    if torch.cuda.is_available():torch.cuda.manual_seed_all(20261017)
    torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    assets={p.name:dict(bytes=p.stat().st_size,sha256=file_hash(p)) for p in sorted(args.snapshot.iterdir()) if p.is_file()}
    assert assets['pytorch_model.bin']['sha256']=='4d24a3e32a88ed1c4e5b789fc6644e2e767500554e954b27dccf52a8e762cbae'
    tokenizer=AutoTokenizer.from_pretrained(str(args.snapshot),use_fast=True,local_files_only=True,trust_remote_code=False)
    model=AutoModelForSequenceClassification.from_pretrained(str(args.snapshot),local_files_only=True,
        use_safetensors=False,trust_remote_code=False,attn_implementation='eager').float().to(device).eval()
    labels={int(k):str(v).lower() for k,v in model.config.id2label.items()};negative=[i for i,v in labels.items() if v=='negative'][0]
    capacity=int(model.config.max_position_embeddings-model.config.pad_token_id-1)
    air,gop,_=load_inputs(args.inputs)
    args.out.mkdir(parents=True,exist_ok=True);args.private_out.mkdir(parents=True,exist_ok=True)
    sums=[];groups=[];pairs=[];lengths=[];protocol={};start=time.monotonic()
    for corpus,d,batch,limit in [('Airline',air,32,None),('GOP',gop,24,128)]:
        result={};private=d[['source_position','text_sha256','group','human_negative','old_RoBERTa']].copy()
        for condition in ['original','model_card']:
            texts=d.text.tolist() if condition=='original' else d.text.map(preprocess).tolist()
            ids=tokenizer(texts,add_special_tokens=True,truncation=False,padding=False)['input_ids']
            lens=np.asarray([len(x) for x in ids]);private[condition+'_untruncated_tokens_with_specials']=lens
            # The sentinel means no automatic tokenizer truncation in airline;
            # the separate architecture capacity is verified, not used to alter inputs.
            automatic_limit=int(tokenizer.model_max_length) if tokenizer.model_max_length<10**9 else None
            effective_limit=limit if limit is not None else automatic_limit
            if corpus=='Airline':assert lens.max()<=capacity,'Airline input exceeds architecture; inspect original protocol'
            for group,ix in [('ALL',np.arange(len(d)))]+[(g,np.flatnonzero(d.group.eq(g))) for g in sorted(d.group.unique())]:
                ll=lens[ix];truncated=0 if effective_limit is None else int((ll>effective_limit).sum())
                lengths.append(dict(corpus=corpus,condition=condition,group=group,n=len(ix),
                    max_tokens_with_specials=int(ll.max()),over128=int((ll>128).sum()),over128_pct=100*float((ll>128).mean()),
                    actual_truncated=truncated,actual_truncated_pct=100*truncated/len(ix),
                    explicit_max_length=limit,tokenizer_active_limit=automatic_limit,architecture_capacity=capacity))
            probs=[]
            for i in range(0,len(d),batch):
                kw=dict(padding=True,truncation=True,return_tensors='pt')
                if limit is not None:kw['max_length']=limit
                encoded=tokenizer(texts[i:i+batch],**kw)
                expected=np.minimum(lens[i:i+batch],effective_limit) if effective_limit is not None else lens[i:i+batch]
                assert np.array_equal(encoded['attention_mask'].sum(-1).numpy(),expected)
                with torch.inference_mode():p=model(**{k:v.to(device) for k,v in encoded.items()}).logits.float().softmax(-1).cpu().numpy()
                probs.append(p)
                if i==0 or (i//batch+1)%25==0 or i+batch>=len(d):
                    print(corpus,condition,min(i+batch,len(d)),'/',len(d),'elapsed_s',round(time.monotonic()-start,1),flush=True)
            p=np.concatenate(probs);result[condition]=(p.argmax(1)==negative).astype(int)
            private[condition+'_negative']=result[condition]
            for j,label in labels.items():private[condition+'_probability_'+label]=p[:,j]
        assert np.array_equal(result['original'],d.old_RoBERTa),'Original binary outputs did not match archive; investigate'
        private.to_csv(args.private_out/(corpus.lower()+'_input_protocol_rows.csv'),index=False)
        s,g,p=report(corpus,d,result);sums.append(s);groups.append(g);pairs.append(p)
        protocol[corpus]=dict(batch_size=batch,explicit_max_length=limit,records=len(d))
    for frames,name in [(sums,'summary.csv'),(groups,'groups.csv'),(pairs,'pairs.csv')]:pd.concat(frames,ignore_index=True).to_csv(args.out/name,index=False)
    pd.DataFrame(lengths).to_csv(args.out/'token_lengths.csv',index=False)
    runtime=dict(status='COMPLETED_PAIRED_INPUT_INFERENCE',recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        model_id=MODEL_ID,model_commit=MODEL_REVISION,model_files=assets,source_input_sha256=EXPECTED_INPUT_HASHES,
        python=platform.python_version(),software_versions={x:importlib.metadata.version(x) for x in ['torch','transformers','tokenizers','huggingface_hub','numpy','pandas']},
        device=str(device),cpu_threads=args.threads,seed=20261017,dtype='float32',attention='eager',deterministic_algorithms=True,
        tokenizer_class=type(tokenizer).__name__,tokenizer_model_max_length=int(tokenizer.model_max_length),
        architecture_max_sequence_tokens_including_specials=capacity,protocol=protocol,
        preprocessing='Exact pinned model-card space-token algorithm; raw protocol otherwise unchanged',
        code_sha256=file_hash(__file__),raw_binary_agreement_verified=True,historical_environment_recovered=False)
    (args.out/'runtime.json').write_text(json.dumps(runtime,indent=2)+'\n')
    print(pd.concat(sums).to_string(index=False),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--inputs',type=Path,required=True);p.add_argument('--snapshot',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--private-out',type=Path,required=True);p.add_argument('--threads',type=int,default=8)
    main(p.parse_args())
