import json,gzip,sys
from fractions import Fraction as Q
from collections import Counter,defaultdict
sys.path.insert(0,'/tmp/w531/research/direct-delivery504-global/vendor/gk')
import gk_common as common
w=json.load(gzip.open(sys.argv[1]));basis=common.basis
V=len(w['ports']);R=w['report']['R'];n=2*V+R
rows=[{r:Q(1)} for r in range(n)]
cur={}
for r in range(n):
    cur[r]=(w['ports'][r],) if r<V else ((basis(w['start_extra'][str(r)]) if str(r) in w.get('start_extra',{}) else ()) if r>=2*V else ())
lev={int(t):basis(E) for t,E in w.get('target_levels',{}).items()}
def norm(row):
    # value restricted to source coordinates (data part); normalize by first coefficient
    d={k:x for k,x in row.items() if k<V}
    if not d: return None
    k0=min(d);c=d[k0]
    return tuple(sorted((k,x/c) for k,x in d.items()))
built=defaultdict(list)   # value -> list of (register, section, index, step)
def apply(e):
    if e[0]=='scale':
        _,t,a,b,*_=e;q=Q(a,b);rows[t]={j:q*x for j,x in rows[t].items()}
    else:
        _,t,s,a,b,*_=e;q=Q(a,b)
        for j,x in list(rows[s].items()):
            z=rows[t].get(j,Q(0))+q*x
            if z: rows[t][j]=z
            else: rows[t].pop(j,None)
for part in ('A','B'):
    if part=='B':
        for r,f in zip(w['centers'],w['center_frames']): cur[r]=basis(f)
        for t in range(V): cur[V+t]=lev.get(t,())
    seq=w[part] if part=='A' else w['cut']+w['B']
    for i,e in enumerate(seq):
        regs=[e[1]]+([e[2]] if e[0]=='add' else [])
        F=basis(e[-1]) if e[-1] is not None else None
        apply(e)
        t=e[1]
        if F is not None:
            d=len(F)-len(cur[t])
            for r in regs: cur[r]=F
            key=norm(rows[t])
            if key and len(key)>=2: built[key].append((t,part,i,d))
mult=Counter()
dup_steps=0
for key,L in built.items():
    regs={x[0] for x in L}
    mult[len(regs)]+=1
    if len(regs)>1: dup_steps+=len(L)
print('distinct data-sums (>=2 sources) formed:',len(built))
print('# sums by number of distinct registers that hold them:',sorted(mult.items())[:10])
sz=Counter(len(k) for k,L in built.items() if len({x[0] for x in L})>1)
print('shared sums by #sources:',sorted(sz.items()))
