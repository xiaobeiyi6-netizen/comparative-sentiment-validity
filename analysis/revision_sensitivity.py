# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""Additional retrospective sensitivity analyses of archived sentiment predictions.

No model inference and no new human observations. Outputs are group/split aggregates.
Run with --inputs pointing to lawful local copies of the four input files.
"""
import argparse, hashlib, html, io, json, unicodedata, zipfile
from pathlib import Path
from itertools import combinations
import numpy as np
import pandas as pd

def norm(x):
    return ' '.join(unicodedata.normalize('NFKC',html.unescape(str(x))).casefold().split())

def rates(d):
    gs=sorted(d.group.unique()); pair=np.array(list(combinations(range(len(gs)),2)))
    p=d.groupby('group').human_negative.mean().reindex(gs).to_numpy()
    out=[]
    for m in ['VADER','RoBERTa']:
        q=d.groupby('group')[m].mean().reindex(gs).to_numpy()
        a,b=pair.T; delta=p[a]-p[b]; pred=q[a]-q[b]
        out.append(dict(model=m,n=len(d),groups=len(gs),pairs=len(pair),reference_ties=int((delta==0).sum()),
                        predicted_ties=int((pred==0).sum()),reversals=int((delta*pred<0).sum()),
                        group_MAE_pp=float(np.mean(abs(q-p))*100)))
    return out

def get_data(root):
    a=pd.read_csv(root/'Tweets.csv'); pa=pd.read_csv(root/'airline_predictions.csv')
    checks={}
    expected={'Tweets.csv':'ea94b23f41892b290dec3330bb8cf9cb6b8bc669eaae5f3a84c40f7b0de8f15e',
              'GOP_REL_ONLY.csv':'413bae11a4b04a414baffb63407788a3231a06b8ab806caaf9f930b5e2acec86'}
    for f,h in expected.items():
        actual=hashlib.sha256((root/f).read_bytes()).hexdigest();assert actual==h
        checks[f]=actual
    assert len(a)==len(pa)==14640
    assert (a.text.map(lambda s:hashlib.sha256(str(s).encode()).hexdigest()).to_numpy()==pa.text_sha256.to_numpy()).all()
    assert (a.airline_sentiment.map({'negative':0,'neutral':1,'positive':2}).to_numpy()==pa.reference.to_numpy()).all()
    air=pd.DataFrame({'group':a.airline,'human_negative':(pa.reference==0).astype(int),
                      'VADER':(pa.vader==0).astype(int),'RoBERTa':(pa.roberta==0).astype(int),
                      'account':a.name,'confidence':a.airline_sentiment_confidence})
    raw=pd.read_csv(root/'GOP_REL_ONLY.csv')
    candidate=raw.candidate.fillna('').astype(str).str.strip()
    label=raw.sentiment.fillna('').astype(str).str.strip().str.title()
    text=raw.text.fillna('').astype(str).str.strip()
    no=candidate.str.casefold().isin({'no candidate mentioned','none','no candidate','not mentioned','not applicable'})
    missing=candidate.eq('');badlabel=~label.isin(['Negative','Neutral','Positive']);empty=text.eq('')
    keep=~(no|missing|badlabel|empty)
    d=raw.loc[keep].copy();d['candidate']=candidate[keep];d['sentiment']=label[keep];d['text']=text[keep]
    d['normalized']=d.text.map(norm);d['hash']=d.text.map(lambda s:hashlib.sha256(s.encode()).hexdigest())
    du=d.groupby('normalized').agg(n=('sentiment','size'),labels=('sentiment','nunique'),candidates=('candidate','nunique'))
    with zipfile.ZipFile(root/'gop_external_validation_results.zip') as z:
        pg=pd.read_csv(io.BytesIO(z.read('gop_external_validation_results/row_predictions_and_overlap_flags.csv')))
    first=d.drop_duplicates('normalized',keep='first').copy()
    assert len(first)==len(pg)==4483
    assert (first.hash.to_numpy()==pg.text_sha256.to_numpy()).all()
    assert (first.candidate.to_numpy()==pg.candidate.to_numpy()).all()
    assert (first.sentiment.to_numpy()==pg.sentiment.to_numpy()).all()
    for m in ['VADER','RoBERTa']:first[m]=pg[m].to_numpy()
    first['human_negative']=(first.sentiment=='Negative').astype(int)
    # Tie rule: retain original first label if several labels share the maximum count.
    modal={}
    for key,sub in d.groupby('normalized',sort=False):
        counts=sub.sentiment.value_counts();winners=set(counts[counts==counts.max()].index)
        modal[key]=next(v for v in sub.sentiment if v in winners)
    majority=first.copy();majority['human_negative']=(majority.normalized.map(modal)=='Negative').astype(int)
    shared=set(du[du.candidates>1].index)
    alternative=first[~first.normalized.isin(shared)].copy()
    mapped=d.copy()
    for m in ['VADER','RoBERTa']:mapped[m]=mapped.normalized.map(first.set_index('normalized')[m])
    mapped['human_negative']=(mapped.sentiment=='Negative').astype(int)
    audit={'source_hashes':checks,'airline_row_alignment':14640,'gop_row_alignment':4483,
           'gop_exclusions':{'no_candidate_mentioned':int(no.sum()),'candidate_missing':int(missing.sum()),
           'additional_invalid_label_or_empty_text':int(((badlabel|empty)&~(no|missing)).sum())},
           'gop_duplicate_groups':int((du.n>1).sum()),'gop_conflicting_label_groups':int(((du.n>1)&(du.labels>1)).sum()),
           'gop_cross_candidate_texts':len(shared),'gop_duplicate_surplus':len(d)-len(first),
           'majority_label_changes':int((majority.human_negative!=first.human_negative).sum()),
           'majority_tie_rule':'original first occurrence among tied modal sentiment categories',
           'raw_data_and_model_inference_redistributed':False}
    variants=[]
    for name,fr in [('Airline primary',air),('Airline confidence 1',air[air.confidence==1]),
                    ('GOP primary',first.rename(columns={'candidate':'group'})),
                    ('GOP majority labels',majority.rename(columns={'candidate':'group'})),
                    ('GOP exclude cross-candidate texts',alternative.rename(columns={'candidate':'group'})),
                    ('GOP repeated records',mapped.rename(columns={'candidate':'group'}))]:
        variants.extend(dict(variant=name,**r) for r in rates(fr))
    gop=first.rename(columns={'candidate':'group','name':'account'})
    return air,gop,audit,pd.DataFrame(variants)

def budget_sensitivity(data,corpus,out):
    groups=sorted(data.group.unique());arr=[data[data.group==g][['human_negative','VADER','RoBERTa']].to_numpy(int) for g in groups]
    pairs=np.array(list(combinations(range(len(groups)),2)));aa,bb=pairs.T
    full=np.array([x[:,0].mean() for x in arr]); fixed=abs(full[aa]-full[bb])>=.1
    budgets=[25,50,100,200,400] if corpus=='Airline' else [25,50,100]
    seed=20261015 if corpus=='Airline' else 20261016
    rng=np.random.default_rng(seed);rows=[];ks=[0,25,50,100,200,400]
    for rep in range(200):
        hold=[];pool=[]
        for x in arr:
            ix=rng.permutation(len(x));n=int(np.ceil(.2*len(x))) if corpus=='Airline' else round(.2*len(x))
            hold.append(x[ix[:n]]);pool.append(x[ix[n:]])
        p=np.array([x[:,0].mean() for x in hold]);gap=p[aa]-p[bb];dynamic=abs(gap)>=.1
        for budget in budgets:
            cal=[x[rng.choice(len(x),size=budget,replace=False)] for x in pool] if corpus=='Airline' else [x[:budget] for x in pool]
            for j,model in [(1,'VADER'),(2,'RoBERTa')]:
                q=np.array([x[:,j].mean() for x in hold]);counts=[]
                for x in cal:
                    y=x[:,0];pred=x[:,j]
                    counts.append([((y==1)&(pred==1)).sum(),((y==1)&(pred==0)).sum(),((y==0)&(pred==1)).sum(),((y==0)&(pred==0)).sum()])
                c=np.array(counts,float);po=c.sum(axis=0);pt=(po[0]+.5)/(po[0]+po[1]+1);pf=(po[2]+.5)/(po[2]+po[3]+1)
                pos=c[:,0]+c[:,1];neg=c[:,2]+c[:,3];t=(c[:,0]+.5)/(pos+1);f=(c[:,2]+.5)/(neg+1)
                def adjust(t,f):
                    den=t-f;bad=abs(den)<.1
                    est=np.clip((q-f)/np.where(bad,1,den),0,1);return np.where(bad,q,est),int(np.sum(bad))
                estimators=[('CC',-1,q,0),('Human-only',-1,np.array([x[:,0].mean() for x in cal]),0)]
                est,fb=adjust(np.repeat(pt,len(q)),np.repeat(pf,len(q)));estimators.append(('Pooled ACC',-1,est,fb))
                for k in ks:
                    if corpus=='Airline':
                        st=(pos*t+k*pt)/(pos+k);sf=(neg*f+k*pf)/(neg+k)
                        if k==0:
                            st=np.where(pos==0,t,st);sf=np.where(neg==0,f,sf)
                    else:st=(c[:,0]+.5+k*pt)/(pos+1+k);sf=(c[:,2]+.5+k*pf)/(neg+1+k)
                    est,fb=adjust(st,sf);estimators.append(('Group ACC',k,est,fb))
                for method,k,e,fb in estimators:
                    egap=e[aa]-e[bb];rev=gap*egap<0
                    eligible=(gap!=0) if corpus=='Airline' else np.ones(len(pairs),bool)
                    def rr(mask):return float(rev[mask].mean()) if mask.any() else np.nan
                    rows.append(dict(corpus=corpus,repeat=rep,budget=budget,model=model,method=method,k=k,
                        MAE_pp=float(np.mean(abs(e-p))*100),reversal_all=rr(eligible),
                        reversal_fixed10=rr(fixed),reversal_holdout10=rr(dynamic),
                        fixed_pairs=int(fixed.sum()),holdout10_pairs=int(dynamic.sum()),
                        reference_ties=int((gap==0).sum()),predicted_ties=int(((egap==0)&(gap!=0)).sum()),fallback_groups=fb))
    d=pd.DataFrame(rows);d.to_csv(out/f'{corpus.lower()}_sensitivity_splits.csv',index=False)
    by=['corpus','budget','model','method','k']
    summary=d.groupby(by).agg(repetitions=('repeat','size'),MAE_pp=('MAE_pp','mean'),reversal_all=('reversal_all','mean'),
              reversal_fixed10=('reversal_fixed10','mean'),reversal_holdout10=('reversal_holdout10','mean'),
              holdout10_pairs=('holdout10_pairs','mean'),reference_ties=('reference_ties','mean'),predicted_ties=('predicted_ties','mean'),fallback_groups=('fallback_groups','mean')).reset_index()
    return summary

def account_bootstrap(d,corpus):
    # Global account-name weights preserve shared accounts across groups.
    accounts=d.account.astype(object).copy();missing=accounts.isna()|accounts.fillna('').astype(str).str.strip().eq('')
    accounts.loc[missing]=['missing_record_'+str(i) for i in d.index[missing]]
    codes,labels=pd.factorize(accounts,sort=False);groups=sorted(d.group.unique());nacc=len(labels)
    mats=[]
    for g in groups:
        mask=d.group.eq(g).to_numpy();mat=np.zeros((nacc,4))
        for j,col in enumerate([None,'human_negative','VADER','RoBERTa']):
            vals=np.ones(len(d)) if col is None else d[col].to_numpy()
            mat[:,j]=np.bincount(codes[mask],weights=vals[mask],minlength=nacc)
        mats.append(mat)
    M=np.stack(mats,axis=1);pairs=np.array(list(combinations(range(len(groups)),2)));a,b=pairs.T
    rng=np.random.default_rng(20261016);rows=[]
    for rep in range(2000):
        w=np.bincount(rng.integers(0,nacc,size=nacc),minlength=nacc)
        ct=np.tensordot(w,M,axes=(0,0));assert (ct[:,0]>0).all()
        p=ct[:,1]/ct[:,0];gap=p[a]-p[b]
        for j,m in [(2,'VADER'),(3,'RoBERTa')]:
            q=ct[:,j]/ct[:,0];r=int((gap*(q[a]-q[b])<0).sum())
            rows.append(dict(corpus=corpus,repeat=rep,model=m,reversal_rate=r/len(a),MAE_pp=np.mean(abs(q-p))*100))
    r=pd.DataFrame(rows);summary=[]
    for model,s in r.groupby('model'):
        summary.append(dict(corpus=corpus,model=model,clusters=nacc,missing_accounts=int(missing.sum()),repetitions=2000,
                   reversal_mean_pct=100*s.reversal_rate.mean(),reversal_q025_pct=100*s.reversal_rate.quantile(.025),reversal_q975_pct=100*s.reversal_rate.quantile(.975),
                   MAE_mean_pp=s.MAE_pp.mean(),MAE_q025_pp=s.MAE_pp.quantile(.025),MAE_q975_pp=s.MAE_pp.quantile(.975)))
    return r,pd.DataFrame(summary)

def main():
    p=argparse.ArgumentParser();p.add_argument('--inputs',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    air,gop,audit,variants=get_data(a.inputs);variants.to_csv(a.out/'reference_and_duplicate_sensitivity.csv',index=False)
    (a.out/'source_and_label_audit.json').write_text(json.dumps(audit,indent=2))
    s=pd.concat([budget_sensitivity(air,'Airline',a.out),budget_sensitivity(gop,'GOP',a.out)],ignore_index=True)
    s.to_csv(a.out/'shrinkage_and_pairset_sensitivity.csv',index=False)
    runs=[];summary=[]
    for corpus,d in [('Airline',air),('GOP',gop)]:
        r,t=account_bootstrap(d,corpus);runs.append(r);summary.append(t)
    pd.concat(runs).to_csv(a.out/'account_cluster_bootstrap_splits.csv',index=False)
    pd.concat(summary).to_csv(a.out/'account_cluster_bootstrap_summary.csv',index=False)
    print(json.dumps(audit,indent=2));print(variants.to_string(index=False));print(s[(s.budget.isin([100,400]))&(s.method=='Group ACC')].to_string(index=False));print(pd.concat(summary).to_string(index=False))

if __name__=='__main__':main()
