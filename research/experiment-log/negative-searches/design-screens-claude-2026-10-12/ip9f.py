import json,sys,importlib.util,gzip
import numpy as np
from collections import Counter
from fractions import Fraction as Q
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import lil_matrix
sys.path.insert(0,'/tmp/r451/research/idle-axis-hosting'); import hosting_core as HC
s=importlib.util.spec_from_file_location('m','/tmp/p433/split-centres-global/vendor/engines/moment.py');MM=importlib.util.module_from_spec(s);s.loader.exec_module(MM)
src='/tmp/vmix/parent445/parent444/upstream442/parent/changed/split-centres/'
t=json.loads(gzip.decompress(open(src+'GLOBAL-TEMPLATE.json.gz','rb').read()))
V,K,T,L,M=120,4,8,9,73
rank={}
for it in t['idle_children']: rank.setdefault(it['child'],it['rank'])
pos={e['stage']:e['pair'] for e in t['recipe'] if e['kind']=='local'}
sched=[]
for e in t['execution_schedule']:
    if e['kind']=='local_cover_sweep': sched.append(dict(kind='local',stage=e['stage'],pair=pos[e['stage']]))
    elif e['kind']=='bridge': sched.append(dict(kind='bridge',dst=e['dst'],src=e['src']))
    elif e['kind']=='idle_cover_sweep':
        for sd,ch in enumerate(e['child_indices']):
            if ch in rank: sched.append(dict(kind='idle',pair=e['pair'],rank=rank[ch],idx=ch))
win={k:x for k,x in HC.windows(sched).items() if x[2]}
allch={ch:r for ch,r in rank.items()}
print('windows',{k:(x[1],sorted(x[2])) for k,x in win.items()})
W=2*K*V*T
g=json.load(open(sys.argv[1])); loc={int(k):v for k,v in g['local'].items()}; wd={int(k):v for k,v in g['widths'].items()}
wd[9]=560-sum(wd.values()); supply={w:n for w,n in wd.items()}; widths=sorted(supply)
G=json.load(open('/tmp/cx/cgrad.json'))
cost=lambda r: -G[str(r)]/1e-9 if 0<r<89 else 0.0
def patterns(r):
    out=[]
    def rec(i,cur,s,spec):
        if i==len(widths): out.append(tuple(cur));return
        w=widths[i];k=0
        while s+k*w<=r and 9*(len(cur)+k)<=M and spec+k*(9-w)<=M-r:
            rec(i+1,cur+[w]*k,s+k*w,spec+k*(9-w));k+=1
    rec(0,[],0,0);return out
idx={}
for i,(p,r,st) in win.items():
    for pat in patterns(r): idx[('y',i,pat)]=len(idx)
    for w in widths:
        for s_ in st: idx[('z',i,w,s_)]=len(idx)
n=len(idx);c=np.zeros(n)
for k,j in idx.items():
    if k[0]=='y': r=win[k[1]][1]; c[j]=cost(r-sum(k[2]))-cost(r)
rows=[];lo=[];hi=[]
for i in win:
    rows.append({j:1 for k,j in idx.items() if k[0]=='y' and k[1]==i});lo.append(V);hi.append(V)
    for w in widths:
        e={j:k[2].count(w) for k,j in idx.items() if k[0]=='y' and k[1]==i and w in k[2]}
        e.update({j:-1 for k,j in idx.items() if k[0]=='z' and k[1]==i and k[2]==w});rows.append(e);lo.append(0);hi.append(0)
PEN=float(sys.argv[2]) if len(sys.argv)>2 else 1e5
for s_ in range(L):
    for w in widths: idx[('u',s_,w)]=len(idx)
c=np.concatenate([c,np.zeros(len(idx)-len(c))])
for k,j in idx.items():
    if k[0]=='u': c[j]=PEN
n=len(idx)
for s_ in range(L):
    for w in widths:
        e={j:1 for k,j in idx.items() if k[0]=='z' and k[2]==w and k[3]==s_}; e[idx['u',s_,w]]=1
        rows.append(e);lo.append(supply[w]);hi.append(supply[w])
A=lil_matrix((len(rows),n))
for ri,e in enumerate(rows):
    for j,x in e.items(): A[ri,j]=x
res=milp(c,constraints=LinearConstraint(A.tocsr(),lo,hi),integrality=np.ones(n),bounds=Bounds(0,np.inf),options=dict(time_limit=900))
print(res.status,res.message)
if res.x is None: sys.exit()
x=[int(round(q)) for q in res.x]
paid=Counter()
for r,k in loc.items(): paid[r]+=k*L*T
for ch,rk in allch.items():
    if ch not in win: paid[rk]+=V*T
for k,j in idx.items():
    if k[0]=='y' and x[j]:
        rr=win[k[1]][1]-sum(k[2])
        if rr: paid[rr]+=x[j]*T
banks=sum(x[j] for k,j in idx.items() if k[0]=='u'); W=W+banks
for k,j in idx.items():
    if k[0]=='u' and x[j]: paid[M-8*k[2]]+=x[j]
print('banks',banks,{k:x[j] for k,j in idx.items() if k[0]=='u' and x[j]})
print('profile',dict(sorted(paid.items())),'deficit',M*W-sum(r*v for r,v in paid.items()))
print('b',float(Q(MM.certify(dict(paid),M,W,True)['lower'])))
