"""All non-root line intersections of R480's first-touch planes.
Modular full rank only discards provably disjoint rational planes; survivors checked over Q.
"""
from pathlib import Path
from collections import Counter
from math import gcd,lcm
from functools import reduce
import json,gzip,sys,time,itertools
import sympy as S
R=Path(__file__).resolve().parent;O=R/'bit510-nonroot-screen';O.mkdir(exist_ok=False);t=time.monotonic();w=json.load(gzip.open(R/'bit510-review/research/e8-r480-dead-totals/data/bitE8mut-r480.json.gz'));lines=w['lines'];v=w['v'];n=2*v+w['R'];ret=set(w['ret']);first={}
for phase in ['D','A','B','C']:
 for f,d,ss in w[phase]:
  if w['frames'][f]:
   for h in [d]+ss:
    if h>=2*v:first.setdefault(h,f)
resp={h:0 for h in range(2*v,n)}
for f,d,ss in w['D']:
 for h in ss:resp[h]^=1<<(d-v)
def norm(x):
 den=lcm(*(int(a.q)for a in x));z=[int(a*den)for a in x];g=reduce(gcd,z);z=[a//g for a in z];return tuple(z if next(a for a in z if a)>0 else[-a for a in z])
roots={norm(list(map(S.Rational,x)))for x in lines};planes=sorted({f for h,f in first.items()if h not in ret and len(w['frames'][f])==2});p=1000003
# Rank mod p is a certified lower bound on rank over Q.
def mrank(rows):
 b={}
 for rr in rows:
  x=[int(a)%p for a in rr]
  for k,y in sorted(b.items()):
   if x[k]:a=x[k];x=[(s-a*z)%p for s,z in zip(x,y)]
  if any(x):k=next(i for i,a in enumerate(x)if a);inv=pow(x[k],-1,p);b[k]=[a*inv%p for a in x]
 return len(b)
def frank(cols):
 b={}
 for x in cols:
  while x:
   k=x.bit_length()-1
   if k in b:x^=b[k]
   else:b[k]=x;break
 return len(b)
new={};pairs=0;disjoint=0;survivors=0
for a,b in itertools.combinations(planes,2):
 pairs+=1;A=[lines[i]for i in w['frames'][a]];B=[lines[i]for i in w['frames'][b]]
 if mrank(A+B)==4:disjoint+=1;continue
 survivors+=1;mat=S.Matrix.hstack(S.Matrix(A).T,-S.Matrix(B).T);ns=mat.nullspace()
 assert len(ns)<=1
 if not ns:continue
 line=norm(S.Matrix(A).T*ns[0][:2,0])
 if line not in roots:new.setdefault(line,set()).update((a,b))
# Any non-root line is in no rank-one first frame. All planes containing it occur in a pair above.
rows=[]
for line,fs in sorted(new.items()):
 hs=sorted(h for h,f in first.items()if h not in ret and f in fs);rank=frank([resp[h]for h in hs]);rows.append(dict(line=line,frames=sorted(fs),helpers=hs,rank=rank,nullity=len(hs)-rank))
res=dict(status='COMPLETE_EXACT_NONROOT_FIRST_PLANE_INTERSECTION_SCREEN',plane_count=len(planes),pairs=pairs,modular_disjoint=disjoint,rational_survivors=survivors,nonroot_lines=len(rows),positive_nullity=[r for r in rows if r['nullity']],classes=rows,seconds=time.monotonic()-t,scope='All non-root rational lines shared by at least two first-touch planes of non-total R480 helpers. Total carriers excluded as in PR510. Existing first-touch planes, fixed response map, exact F2 column dependence. No shifted first uses or new scalar word; not a universal kernel impossibility.')
(O/'RESULT.json').write_text(json.dumps(res,indent=2)+'\n');print({k:v for k,v in res.items()if k!='classes'},flush=True)
