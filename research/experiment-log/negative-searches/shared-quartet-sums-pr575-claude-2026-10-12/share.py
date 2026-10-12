"""Shared-sum rewrite: when register B rebuilds a data sum S that register A already holds, replace B's build gates
with one gate B += c*A (dyadic c). Exactness and entrances are checked later by the PR531 auditor."""
import json,gzip,sys,copy
from fractions import Fraction as Q
from collections import defaultdict,Counter
sys.path.insert(0,'/tmp/w531/research/direct-delivery504-global/vendor/gk')
import gk_common as common
basis=common.basis
def load(p): return json.load(gzip.open(p))
def simulate(w):
    V=len(w['ports']);R=w['report']['R'];n=2*V+R
    rows=[{r:Q(1)} for r in range(n)]
    seq=[('A',i,e) for i,e in enumerate(w['A'])]+[('cut',i,e) for i,e in enumerate(w['cut'])]+[('B',i,e) for i,e in enumerate(w['B'])]
    hist=[]   # after each op: data-key of target
    for sec,i,e in seq:
        if e[0]=='scale':
            _,t,a,b,*_=e;q=Q(a,b);rows[t]={j:q*x for j,x in rows[t].items()}
        else:
            _,t,s,a,b,*_=e;q=Q(a,b)
            for j,x in list(rows[s].items()):
                z=rows[t].get(j,Q(0))+q*x
                if z: rows[t][j]=z
                else: rows[t].pop(j,None)
        hist.append((sec,i,e[1],{k:x for k,x in rows[e[1]].items() if k<V}))
    return seq,hist
def key(d):
    if len(d)<2: return None
    k0=min(d);c=d[k0];return tuple(sorted((k,x/c) for k,x in d.items()))
def candidates(w):
    V=len(w['ports']);seq,hist=simulate(w)
    first=defaultdict(list)
    for pos,(sec,i,t,d) in enumerate(hist):
        k=key(d)
        if k: first[k].append((pos,t,d))
    out=[]
    for k,L in first.items():
        regs=[]
        for pos,t,d in L:
            if t not in [r for _,r,_ in regs]: regs.append((pos,t,d))
        if len(regs)<2: continue
        out.append((k,regs))
    return seq,hist,out
