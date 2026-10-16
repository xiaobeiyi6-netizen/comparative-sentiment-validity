# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
AGG=ROOT/"audit/aggregates"
FIG=ROOT/"figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,
 'axes.labelsize':10,'axes.titlesize':11,'legend.fontsize':9,'savefig.facecolor':'white','pdf.fonttype':42,'svg.fonttype':'none'})
colors=['#333333','#D55E00','#0072B2','#009E73']
def savefig(fig,name):
    for ext in ['png','pdf','svg']:fig.savefig(FIG/(name+'.'+ext),dpi=600,bbox_inches='tight')
    plt.close(fig)

# Figures are generated from exact aggregate values, never estimated from pixels.
a=pd.read_csv(AGG/'airline_group_prevalence.csv')
fig,ax=plt.subplots(figsize=(7.2,3.55));y=np.arange(len(a));h=.22
for off,col,label,color in [(-h,'reference_pct','Human reference',colors[0]),(0,'vader_pct','VADER',colors[1]),(h,'roberta_pct','Archived RoBERTa',colors[2])]:
    bars=ax.barh(y+off,a[col],height=h*.90,label=label,color=color,zorder=3)
    for bar,v in zip(bars,a[col]):ax.text(v+.8,bar.get_y()+bar.get_height()/2,f'{v:.1f}',ha='left',va='center',fontsize=8)
ax.set_yticks(y,a.airline);ax.invert_yaxis();ax.set_xlim(0,100);ax.set_xlabel('Negative tweets (%)')
ax.xaxis.grid(True,color='#E5E5E5',lw=.6);ax.set_axisbelow(True)
ax.legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=3,frameon=False)
ax.text(.99,-.19,'United: VADER bias = −50.18 pp; reference rank 3 → model rank 6',transform=ax.transAxes,ha='right',fontsize=8.5)
savefig(fig,'Figure_1_Airline_Negative_Shares')

s=pd.read_csv(AGG/'airline_calibration_budget_summary.csv')
fig,axes=plt.subplots(1,2,figsize=(7.2,3.6),sharey=True)
methods=[('CC','Classify and count'),('ACC_pooled','Pooled ACC'),('ACC_airline_shrunk','Group ACC, k = 100'),('Human_calibration_only','Human-only')]
for ax,model in zip(axes,['vader','roberta']):
    for (method,label),color in zip(methods,colors):
        sub=s[(s.model==model)&(s.method==method)].sort_values('budget_per_airline');x=np.arange(len(sub))
        mean=sub.mean_absolute_prevalence_error_pp_mean.to_numpy();lo=sub.mean_absolute_prevalence_error_pp_q025.to_numpy();hi=sub.mean_absolute_prevalence_error_pp_q975.to_numpy()
        ax.plot(x,mean,label=label,color=color,lw=1.5,marker='o',ms=3)
        ax.fill_between(x,lo,hi,color=color,alpha=.09,lw=0)
    ax.set_xticks(range(5),['25','50','100','200','400']);ax.set_xlabel('Human labels per airline');ax.set_title('VADER' if model=='vader' else 'Archived RoBERTa')
    ax.grid(axis='y',color='#E5E5E5',lw=.6);ax.set_ylim(0,36)
axes[0].set_ylabel('Mean group prevalence MAE (pp)')
handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=2,frameon=False,bbox_to_anchor=(.5,-.12))
fig.tight_layout(w_pad=1.4);savefig(fig,'Figure_2_Airline_Budget_Comparison')

fig,ax=plt.subplots(figsize=(7.2,3.5));x=np.arange(4);width=.3;den=[45,43,39,30]
for off,num,model,color in [(-width/2,[7,7,7,3],'VADER',colors[1]),(width/2,[7,6,5,2],'Archived RoBERTa',colors[2])]:
    v=np.array(num)/np.array(den)*100;bars=ax.bar(x+off,v,width,label=model,color=color,zorder=3)
    for b,n,d,val in zip(bars,num,den,v):ax.text(b.get_x()+b.get_width()/2,val+.65,f'{n}/{d}',ha='center',va='bottom',fontsize=9)
ax.set_xticks(x,['All pairs','Gap ≥3 pp','Gap ≥5 pp','Gap ≥10 pp']);ax.set_ylim(0,24);ax.set_ylabel('Strict reversal rate (%)');ax.grid(axis='y',color='#E5E5E5',lw=.6);ax.set_axisbelow(True)
ax.legend(frameon=False,ncol=2,loc='lower center',bbox_to_anchor=(.5,1.0));savefig(fig,'Figure_3_GOP_Reference_Gaps')

