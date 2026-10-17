# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Beiyi Xiao
"""Regenerate all primary figures from numerical aggregates at 600 dpi."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
AGG=ROOT/'audit/aggregates'
FIG=ROOT/'figures'; FIG.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,
 'axes.spines.top':False,'axes.spines.right':False,'axes.labelsize':10,
 'axes.titlesize':11,'legend.fontsize':9,'savefig.facecolor':'white',
 'pdf.fonttype':42,'svg.fonttype':'none'})
COLORS=['#444444','#D55E00','#0072B2','#009E73']

def save(fig,name):
    for ext in ['png','pdf','svg']:
        path=FIG/(name+'.'+ext)
        fig.savefig(path,dpi=600,bbox_inches='tight')
        if ext=='svg':path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
    plt.close(fig)

a=pd.read_csv(AGG/'airline_group_prevalence.csv')
v=pd.read_csv(ROOT/'audit/reviewer_revision/vader_input_diagnostics_groups.csv')
mask=v[v.variant=='United handle only masked'].set_index('group')
a['vader_masked_pct']=a.airline.map(mask.predicted_pct)
fig,ax=plt.subplots(figsize=(7.1,4.1)); y=np.arange(len(a)); h=.19
for off,col,label,color in [(-1.5*h,'reference_pct','Human reference',COLORS[0]),
 (-.5*h,'vader_pct','VADER, original',COLORS[1]),(.5*h,'vader_masked_pct','VADER, @United masked',COLORS[3]),
 (1.5*h,'roberta_pct','RoBERTa, original',COLORS[2])]:
    bars=ax.barh(y+off,a[col],height=h*.88,label=label,color=color,zorder=3)
    for bar,v in zip(bars,a[col]):
        ax.text(v+.8,bar.get_y()+bar.get_height()/2,f'{v:.1f}',ha='left',va='center',fontsize=8.5)
ax.set_yticks(y,a.airline); ax.invert_yaxis(); ax.set_xlim(0,95)
ax.set_xlabel('Negative message share (%)'); ax.xaxis.grid(True,color='#E5E5E5',lw=.65)
ax.set_axisbelow(True); ax.legend(loc='lower center',bbox_to_anchor=(.5,1.01),ncol=2,frameon=False)
save(fig,'Figure_1_Airline_Negative_Shares')

s=pd.read_csv(AGG/'airline_calibration_budget_summary.csv')
fig,axes=plt.subplots(2,2,figsize=(7.1,5.7),sharex=True)
methods=[('CC','Classify and count'),('ACC_pooled','Pooled ACC'),
 ('ACC_airline_shrunk','Group ACC, k = 100'),('Human_calibration_only','Human-only')]
for j,model in enumerate(['vader','roberta']):
    for row,metric in [(0,'mean_absolute_prevalence_error_pp'),(1,'reversal_rate_gap0pp')]:
        ax=axes[row,j]
        for (method,label),color in zip(methods,COLORS):
            sub=s[(s.model==model)&(s.method==method)].sort_values('budget_per_airline')
            x=sub.budget_per_airline.to_numpy(); mul=100 if row else 1
            mean=sub[metric+'_mean'].to_numpy()*mul
            lo=sub[metric+'_q025'].to_numpy()*mul; hi=sub[metric+'_q975'].to_numpy()*mul
            ax.plot(x,mean,label=label,color=color,lw=1.6,marker='o',ms=3)
            ax.fill_between(x,lo,hi,color=color,alpha=.055,lw=0)
        ax.set_xscale('log',base=2); ax.set_xticks([25,50,100,200,400],['25','50','100','200','400'])
        ax.grid(axis='y',color='#E5E5E5',lw=.65)
        ax.text(.02,.95,'('+chr(97+row*2+j)+')',transform=ax.transAxes,ha='left',va='top',fontsize=11,fontweight='bold')
        if row==0: ax.set_title('Native VADER' if j==0 else 'Native RoBERTa')
        if row==1: ax.set_xlabel('Labels per airline (log2 scale)')
        ax.set_ylim(0,(36 if j==0 else 20) if row==0 else 65)
axes[0,0].set_ylabel('Group prevalence MAE (pp)')
axes[1,0].set_ylabel('Strict reversal rate (%)')
handles,labels=axes[0,0].get_legend_handles_labels()
fig.legend(handles,labels,loc='upper center',ncol=2,frameon=False,bbox_to_anchor=(.52,1.05))
fig.tight_layout(w_pad=1.8,h_pad=1.4)
save(fig,'Figure_2_Airline_Budget_Comparison')

fig,ax=plt.subplots(figsize=(7.1,3.2)); x=np.arange(4); width=.30; den=[45,43,39,30]
for off,num,model,color in [(-width/2,[7,7,7,3],'VADER',COLORS[1]),
 (width/2,[7,6,5,2],'RoBERTa',COLORS[2])]:
    values=np.array(num)/np.array(den)*100
    bars=ax.bar(x+off,values,width,label=model,color=color,zorder=3)
    for bar,n,d,val in zip(bars,num,den,values):
        ax.text(bar.get_x()+bar.get_width()/2,val+.6,f'{n}/{d}',ha='center',va='bottom',fontsize=10)
ax.set_xticks(x,['All pairs','Gap ≥3 pp','Gap ≥5 pp','Gap ≥10 pp'])
ax.set_ylim(0,22); ax.set_ylabel('Strict reversal rate (%)')
ax.grid(axis='y',color='#E5E5E5',lw=.65); ax.set_axisbelow(True)
ax.legend(frameon=False,ncol=2,loc='lower center',bbox_to_anchor=(.5,1.0))
save(fig,'Figure_3_GOP_Reference_Gaps')
