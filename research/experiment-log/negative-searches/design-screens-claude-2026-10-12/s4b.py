"""Idea 4 screen: find ops where a source operand climbs to the op frame only for this op, but an exact substitute
(a rational combination of registers already sitting at that frame with the identical full row, dirt included) exists."""
import json,gzip,time
from fractions import Fraction as Q
from collections import defaultdict,Counter
c=json.load(gzip.open('c112.json.gz')); v=c['v'];R=c['R'];n=2*v+R;F=c['frames']
ops=[('A',e) for e in c['A']]+[('B',e) for e in c['B']]
cur=list(c['start']); rows=[{r:Q(1)} for r in range(n)]
def apply(e):
    if e[0]=='scale':
        _,t,a,b,*_=e;q=Q(a,b);rows[t]={j:q*x for j,x in rows[t].items()}
    else:
        _,t,s,a,b,*_=e;q=Q(a,b)
        for j,x in list(rows[s].items()):
            z=rows[t].get(j,Q(0))+q*x
            if z: rows[t][j]=z
            else: rows[t].pop(j,None)
atF=defaultdict(set)
for r in range(n): atF[cur[r]].add(r)
def inspan(target,vecs):
    piv={}
    for vr in vecs:
        row=dict(vr)
        while row:
            k=min(row)
            if k in piv:
                pr=piv[k];q=row[k]/pr[k]
                for j,x in pr.items():
                    z=row.get(j,Q(0))-q*x
                    if z: row[j]=z
                    else: row.pop(j,None)
            else: piv[k]=row;break
    row=dict(target)
    while row:
        k=min(row)
        if k not in piv: return False
        pr=piv[k];q=row[k]/pr[k]
        for j,x in pr.items():
            z=row.get(j,Q(0))-q*x
            if z: row[j]=z
            else: row.pop(j,None)
    return True
cand=Counter();checked=0;t0=time.time()
for idx,(ph,e) in enumerate(ops):
    f=e[-1]
    if e[0]=='add':
        s=e[2]
        if cur[s]!=f and 2*v<=s:   # helper source climbs to f here
            pool=[{j:x for j,x in rows[r].items() if j<2*v} for r in atF[f] if r not in (s,e[1])]
            checked+=1
            cand['pool_nonempty']+=bool(pool); cand['pool_size_sum']+=len(pool)
            if pool and len(pool)<=60 and inspan({j:x for j,x in rows[s].items() if j<2*v},pool): cand[ph]+=1
    regs=[e[1]]+([e[2]] if e[0]=='add' else [])
    for r in regs:
        atF[cur[r]].discard(r); cur[r]=f; atF[f].add(r)
    apply(e)
print('helper-source climbs checked',checked,'substitutable',dict(cand),'%.0fs'%(time.time()-t0))
