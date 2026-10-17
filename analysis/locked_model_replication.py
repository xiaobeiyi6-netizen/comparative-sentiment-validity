# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""New version-pinned inference comparison, not historical-version recovery."""
import argparse, datetime, hashlib, html, io, itertools, json, os, platform, re, subprocess, sys, unicodedata, zipfile
from pathlib import Path
import importlib.metadata
import numpy as np
import pandas as pd

MODEL_ID = 'cardiffnlp/twitter-roberta-base-sentiment-latest'
MODEL_REVISION = '3216a57f2a0d9c45a2e6c20157c20c49fb4bf9c7'
EXPECTED_INPUT_HASHES = {'Tweets.csv': 'ea94b23f41892b290dec3330bb8cf9cb6b8bc669eaae5f3a84c40f7b0de8f15e', 'airline_predictions.csv': '5674f3e56dc3667344ab43c867ee8dd4f61126823950524c3f5cd54d92f9eda2', 'GOP_REL_ONLY.csv': '413bae11a4b04a414baffb63407788a3231a06b8ab806caaf9f930b5e2acec86', 'gop_external_validation_results.zip': '8a93da7db63b6d2f5c0c2daec0faabdbab0b8cf7be415b1af30e3d49636968e7'}
LABELS = {'negative':0,'neutral':1,'positive':2}

def digest_bytes(b): return hashlib.sha256(b).hexdigest()
def file_hash(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def norm(t):return ' '.join(unicodedata.normalize('NFKC',html.unescape(str(t))).casefold().split())
def text_hashes(s):return s.map(lambda t:digest_bytes(str(t).encode('utf-8'))).to_numpy()

def load_inputs(bundle):
    with zipfile.ZipFile(bundle) as z:
        inputs={}
        for name,expected in EXPECTED_INPUT_HASHES.items():
            found=[n for n in z.namelist() if Path(n).name==name]
            assert len(found)==1, f'输入文件缺失或重名: {name}'
            b=z.read(found[0]);assert digest_bytes(b)==expected,f'输入字节校验失败: {name}'
            inputs[name]=b
    raw=pd.read_csv(io.BytesIO(inputs['Tweets.csv']))
    old=pd.read_csv(io.BytesIO(inputs['airline_predictions.csv']))
    assert len(raw)==len(old)==14640
    assert np.array_equal(text_hashes(raw.text),old.text_sha256.to_numpy()),'航空文本未逐行对齐'
    reference=raw.airline_sentiment.map(LABELS).to_numpy()
    assert np.array_equal(reference,old.reference.to_numpy()),'航空人工标签不一致'
    air=pd.DataFrame({'group':raw.airline,'text':raw.text.astype(str),'source_position':np.arange(len(raw)),
        'reference_class':reference,'human_negative':(reference==0).astype(int),
        'old_vader_class':old.vader,'old_roberta_class':old.roberta,'text_sha256':old.text_sha256})
    for model,col in [('VADER','vader'),('RoBERTa','roberta')]:air['old_'+model]=(old[col].to_numpy()==0).astype(int)

    raw=pd.read_csv(io.BytesIO(inputs['GOP_REL_ONLY.csv']))
    assert len(raw)==13871
    text=raw.text.fillna('').astype(str).str.strip()
    candidate=raw.candidate.fillna('').astype(str).str.strip()
    label=raw.sentiment.fillna('').astype(str).str.strip().str.title()
    excluded={'no candidate mentioned','none','no candidate','not mentioned','not applicable'}
    keep=text.ne('') & candidate.ne('') & ~candidate.str.casefold().isin(excluded) & label.isin(['Negative','Neutral','Positive'])
    valid=pd.DataFrame({'text':text[keep],'group':candidate[keep],'sentiment':label[keep],'source_position':np.flatnonzero(keep)})
    valid['normalized']=valid.text.map(norm)
    first=valid.drop_duplicates('normalized',keep='first').reset_index(drop=True)
    with zipfile.ZipFile(io.BytesIO(inputs['gop_external_validation_results.zip'])) as z:
        old=pd.read_csv(io.BytesIO(z.read('gop_external_validation_results/row_predictions_and_overlap_flags.csv')))
    assert len(valid)==6284 and len(first)==len(old)==4483
    assert np.array_equal(text_hashes(first.text),old.text_sha256.to_numpy()),'GOP文本未逐行对齐'
    assert np.array_equal(first.group.to_numpy(),old.candidate.to_numpy()),'GOP分组不一致'
    assert np.array_equal(first.sentiment.to_numpy(),old.sentiment.to_numpy()),'GOP人工标签不一致'
    first['reference_class']=first.sentiment.str.lower().map(LABELS)
    first['human_negative']=(first.reference_class==0).astype(int)
    first['text_sha256']=old.text_sha256.to_numpy()
    assert np.array_equal(first.human_negative.to_numpy(),old.human_negative.to_numpy())
    for model in ['VADER','RoBERTa']:first['old_'+model]=old[model].to_numpy()
    return air,first,old

def group_and_pair_reports(corpus,d):
    group=[];pair=[];summary=[]
    for model in ['VADER','RoBERTa']:
        for g,z in d.groupby('group',sort=True):
            p=z.human_negative.mean();rec={'corpus':corpus,'model':model,'group':g,'n':len(z),'reference_negative_pct':100*p}
            for version in ['old','new']:
                y=z[version+'_'+model].to_numpy();gold=z.human_negative.to_numpy();q=y.mean()
                tp=int(((gold==1)&(y==1)).sum());fn=int(((gold==1)&(y==0)).sum());fp=int(((gold==0)&(y==1)).sum());tn=int(((gold==0)&(y==0)).sum())
                rec.update({version+'_negative_pct':100*q,version+'_bias_pp':100*(q-p),version+'_TP':tp,version+'_FN':fn,version+'_FP':fp,version+'_TN':tn})
            rec['negative_share_change_pp']=rec['new_negative_pct']-rec['old_negative_pct'];group.append(rec)
        gm=pd.DataFrame([x for x in group if x['model']==model]).set_index('group')
        model_pairs=[]
        for a,b in itertools.combinations(gm.index,2):
            gap=float(gm.loc[a,'reference_negative_pct']-gm.loc[b,'reference_negative_pct'])
            rec={'corpus':corpus,'model':model,'a':a,'b':b,'reference_gap_pp':gap,'reference_tie':gap==0}
            for version in ['old','new']:
                q=float(gm.loc[a,version+'_negative_pct']-gm.loc[b,version+'_negative_pct'])
                rec.update({version+'_gap_pp':q,version+'_strict_reversal':int(gap*q<0),version+'_predicted_tie':q==0})
            rec['reversal_status_changed']=rec['old_strict_reversal']!=rec['new_strict_reversal'];model_pairs.append(rec);pair.append(rec)
        model_pairs=pd.DataFrame(model_pairs)
        old=d['old_'+model].to_numpy();new=d['new_'+model].to_numpy()
        rec={'corpus':corpus,'model':model,'n':len(d),'groups':len(gm),'pair_count':len(model_pairs),
             'binary_label_changes':int((old!=new).sum()),'binary_label_agreement_pct':100*float((old==new).mean()),
             'old_group_prevalence_MAE_pp':float(gm.old_bias_pp.abs().mean()),'new_group_prevalence_MAE_pp':float(gm.new_bias_pp.abs().mean()),
             'maximum_absolute_group_share_change_pp':float(gm.negative_share_change_pp.abs().max()),
             'changed_reversal_pairs':int(model_pairs.reversal_status_changed.sum())}
        for threshold in [0,3,5,10]:
            subset=model_pairs[model_pairs.reference_gap_pp.abs()>=threshold]
            rec[f'gap{threshold}_pairs']=len(subset)
            for version in ['old','new']:rec[f'{version}_reversals_gap{threshold}']=int(subset[version+'_strict_reversal'].sum())
        if corpus=='Airline':
            col=model.lower();rec['three_class_label_changes']=int((d['old_'+col+'_class']!=d['new_'+col+'_class']).sum())
        summary.append(rec)
    return group,pair,summary

def save_comparison(air,gop,old_gop,out):
    public=out/'summary';private=out/'private_row_outputs';public.mkdir(parents=True,exist_ok=True);private.mkdir(exist_ok=True)
    groups=[];pairs=[];summaries=[]
    for corpus,d in [('Airline',air),('GOP',gop)]:
        g,p,s=group_and_pair_reports(corpus,d);groups+=g;pairs+=p;summaries+=s
        keep=[c for c in d.columns if c not in {'text','normalized','sentiment'}]
        d[keep].to_csv(private/(corpus.lower()+'_row_comparison.csv'),index=False)
    pd.DataFrame(groups).to_csv(public/'group_comparison.csv',index=False)
    pd.DataFrame(pairs).to_csv(public/'pairwise_comparison.csv',index=False)
    table=pd.DataFrame(summaries);table.to_csv(public/'comparison_summary.csv',index=False)
    # Canonical exports permit downstream budget reruns without changing old predictions.
    pa=pd.DataFrame({'reference':air.reference_class,'vader':air.new_vader_class,'roberta':air.new_roberta_class,
                     'text_length':air.text.str.len(),'text_sha256':air.text_sha256})
    pa.to_csv(private/'new_airline_predictions.csv',index=False)
    pg=old_gop.copy()
    for m in ['VADER','RoBERTa']:pg[m]=gop['new_'+m].to_numpy()
    pg.to_csv(private/'new_gop_row_predictions_and_overlap_flags.csv',index=False)
    with zipfile.ZipFile(private/'new_gop_external_validation_results.zip','w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('gop_external_validation_results/row_predictions_and_overlap_flags.csv',pg.to_csv(index=False))
        z.writestr('gop_external_validation_results/run_audit.json',json.dumps({'is_new_locked_inference':True,'model_id':MODEL_ID,'model_revision':MODEL_REVISION,'historical_revision_recovered':False}))
    return table

def main(bundle,out):
    out.mkdir(parents=True,exist_ok=False)
    air,gop,old_gop=load_inputs(bundle)
    print('四个输入文件已校验；航空14,640行与GOP4,483行均逐行对齐。',flush=True)
    os.environ['CUBLAS_WORKSPACE_CONFIG']=':4096:8'
    import random,torch
    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer,AutoModelForSequenceClassification
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    seed=20261017;random.seed(seed);np.random.seed(seed);torch.manual_seed(seed)
    if torch.cuda.is_available():torch.cuda.manual_seed_all(seed)
    torch.use_deterministic_algorithms(True)
    if hasattr(torch.backends,'cuda'):torch.backends.cuda.matmul.allow_tf32=False
    if hasattr(torch.backends,'cudnn'):torch.backends.cudnn.allow_tf32=False
    device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print('本次复核固定模型commit:',MODEL_REVISION,'；设备:',device,flush=True)
    if device.type=='cpu':print('未检测到GPU，CPU可以运行但速度可能明显更慢。',flush=True)
    # Download only files belonging to the exact commit; no automatic safetensors conversion PR.
    snapshot=Path(snapshot_download(repo_id=MODEL_ID,revision=MODEL_REVISION,token=False,
        allow_patterns=['config.json','pytorch_model.bin','vocab.json','merges.txt','special_tokens_map.json','README.md','.gitattributes']))
    assert snapshot.name==MODEL_REVISION,'模型快照目录与固定commit不符'
    assets={p.name:{'bytes':p.stat().st_size,'sha256':file_hash(p)} for p in sorted(snapshot.iterdir()) if p.is_file()}
    assert 'pytorch_model.bin' in assets
    tokenizer=AutoTokenizer.from_pretrained(str(snapshot),use_fast=True,local_files_only=True,trust_remote_code=False)
    model=AutoModelForSequenceClassification.from_pretrained(str(snapshot),local_files_only=True,use_safetensors=False,
        trust_remote_code=False,attn_implementation='eager').float().to(device).eval()
    id2label={int(k):str(v).lower() for k,v in model.config.id2label.items()}
    assert set(id2label.values())==set(LABELS),'非预期模型标签映射'
    analyzer=SentimentIntensityAnalyzer()
    lex_path=Path(importlib.metadata.distribution('vaderSentiment').locate_file('vaderSentiment/vader_lexicon.txt'))
    for corpus,d,batch,max_length in [('Airline',air,32,None),('GOP',gop,24,128)]:
        compound=np.array([analyzer.polarity_scores(t)['compound'] for t in d.text])
        vc=np.where(compound<=-.05,0,np.where(compound>=.05,2,1));d['new_vader_class']=vc;d['new_VADER']=(vc==0).astype(int)
        all_prob=[]
        for i in range(0,len(d),batch):
            kwargs={'padding':True,'truncation':True,'return_tensors':'pt'}
            if max_length is not None:kwargs['max_length']=max_length
            encoded=tokenizer(d.text.iloc[i:i+batch].tolist(),**kwargs)
            encoded={k:v.to(device) for k,v in encoded.items()}
            with torch.inference_mode():prob=model(**encoded).logits.float().softmax(-1).cpu().numpy()
            all_prob.append(prob)
            if i==0 or (i//batch+1)%50==0 or i+batch>=len(d):print(corpus,min(i+batch,len(d)),'/',len(d),flush=True)
        probs=np.concatenate(all_prob);rc=np.array([LABELS[id2label[int(j)]] for j in probs.argmax(axis=1)])
        d['new_roberta_class']=rc;d['new_RoBERTa']=(rc==0).astype(int)
        for j,label in id2label.items():d['new_roberta_probability_'+label]=probs[:,j]
    table=save_comparison(air,gop,old_gop,out)
    versions={}
    for name in ['torch','transformers','tokenizers','huggingface_hub','vaderSentiment','numpy','pandas','safetensors','scikit-learn']:
        versions[name]=importlib.metadata.version(name)
    runtime={'status':'COMPLETE_NEW_LOCKED_INFERENCE','recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'historical_revision_recovered':False,'new_model_inference_executed':True,'model_id':MODEL_ID,'model_commit':MODEL_REVISION,
        'model_files':assets,'source_input_sha256':EXPECTED_INPUT_HASHES,'python':platform.python_version(),'software_versions':versions,
        'device':str(device),'gpu_name':torch.cuda.get_device_name(0) if device.type=='cuda' else None,'cuda_version':torch.version.cuda,
        'cudnn_version':torch.backends.cudnn.version(),'seed':seed,'dtype':'float32','attention':'eager','deterministic_algorithms':True,
        'tokenizer_class':type(tokenizer).__name__,'tokenizer_model_max_length':int(tokenizer.model_max_length),
        'vader_lexicon_sha256':file_hash(lex_path),
        'protocol':{'Airline':{'n':14640,'batch_size':32,'truncation':True,'max_length':'tokenizer default'},'GOP':{'n':4483,'batch_size':24,'truncation':True,'max_length':128}},
        'text_preprocessing':'Airline original text; GOP strip then original normalization for deduplication only; no added @user/http replacement',
        'code_sha256':file_hash(__file__),'budgets_and_auxiliary_corpora_rerun':False,
        'boundary':'This new run tests stability of archived-output findings. It does not restore the historical inference environment.'}
    (out/'summary/runtime_and_model_lock.json').write_text(json.dumps(runtime,indent=2)+'\n')
    (out/'private_row_outputs/environment_freeze.txt').write_text(subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True))
    (out/'private_row_outputs/requirements_observed.txt').write_text('\n'.join(f'{k}=={v}' for k,v in versions.items())+'\n')
    report=['# New version-pinned inference comparison','',f'Model commit: `{MODEL_REVISION}`. Historical model revision remains unavailable.','',
        'Both source corpora and archived prediction inputs passed exact-byte and row-alignment checks. This run re-executed VADER and RoBERTa on both primary analysis corpora. No new human labels or posts were collected.','']
    for r in table.itertuples():
        report.append(f'- {r.corpus} / {r.model}: binary label changes {r.binary_label_changes}/{r.n}; strict reversals {r.old_reversals_gap0}/{r.pair_count} archived and {r.new_reversals_gap0}/{r.pair_count} new; changed reversal-pair identities {r.changed_reversal_pairs}; maximum group share change {r.maximum_absolute_group_share_change_pp:.6f} pp.')
    report+=['','Budget and supplementary-corpus analyses have not been rerun by this notebook. If predictions differ, downstream analyses must be reassessed before updating the paper.','',
        'The summary folder contains aggregates and runtime/model provenance. The private_row_outputs folder contains individual prediction records and must not be placed in the public repository. No model weights, original tweet text or account fields are bundled in this result archive.']
    (out/'summary/RESULT_README.md').write_text('\n'.join(report)+'\n')
    manifest={str(p.relative_to(out)):file_hash(p) for p in sorted(out.rglob('*')) if p.is_file()}
    (out/'RESULT_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
    archive=out.parent/'Locked_Model_Replication_Results.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(out).as_posix())
    print('\n新复核完成。请下载并交回:',archive,flush=True)
    print(table[['corpus','model','binary_label_changes','old_reversals_gap0','new_reversals_gap0','changed_reversal_pairs']].to_string(index=False),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--inputs',required=True,type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args();main(a.inputs,a.out)
