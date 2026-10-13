import json,gzip
from fractions import Fraction as F
from collections import Counter
w=json.load(gzip.open('/tmp/g44/x4/jx/FULL-WORD.json.gz'))
def basis(vs):
    b={}
    for x in vs:
        for p in sorted(b,reverse=True):
            if x>>p&1:x^=b[p]
        if x:
            p=x.bit_length()-1
            for q in b:
                if b[q]>>p&1:b[q]^=x
            b[p]=x
    return tuple(b[p] for p in sorted(b,reverse=True))
V=len(w['ports']);R=w['report']['R'];n=2*V+R
def apply(e,rows):
    if e[0]=='scale': rows[e[1]]={k:F(e[2],e[3])*x for k,x in rows[e[1]].items()}
    else:
        q=F(e[3],e[4])
        for k,x in list(rows[e[2]].items()):
            z=rows[e[1]].get(k,F(0))+q*x
            if z: rows[e[1]][k]=z
            else: rows[e[1]].pop(k,None)
rows=[{k:F(1)} for k in range(n)]
for e in w['A']: apply(e,rows)
print('centres',w['centers'])
for k,(c,Fr) in enumerate(zip(w['centers'],w['center_frames'])):
    src=[s for s in rows[c] if s<V]
    span=basis([w['ports'][s] for s in src])
    print(k,'reg',c,'frame rank',len(basis(Fr)),'data sources',len(src),'label-span rank',len(span),'helper-dirt terms',sum(1 for s in rows[c] if s>=2*V))
print('scatter row sample',w['scatter'][:3])
print('cut sample',w['cut'][:4])
import itertools
roots=[tuple(F(x) for x in r) for r in w['root_lines']]
ports=w['ports']
print('ports rank',len(basis(ports)),'roots',len(roots))
# candidate directions: E8 vectors with small coords
cands=set()
vals=[F(0),F(1),F(-1)]
for i in range(8): 
    v=[F(0)]*8;v[i]=F(1);cands.add(tuple(v))
for r in roots: cands.add(r)
for i,j in itertools.combinations(range(8),2):
    for a,b in itertools.product((1,-1),repeat=2):
        v=[F(0)]*8;v[i]=F(a);v[j]=F(b);cands.add(tuple(v))
for sg in itertools.product((1,-1),repeat=8):
    cands.add(tuple(F(s,2) for s in sg))
res=Counter();best=[]
for u in cands:
    S=[s for s,r in enumerate(roots) if sum(a*b for a,b in zip(r,u))!=0]
    rk=len(basis([ports[s] for s in S]))
    res[(len(S),rk)]+=1
    if rk<=7: best.append((rk,len(S),u))
print(sorted(res.items()))
print('directions with label-span rank<=7:',len(best),best[:5])
