"""Concrete E7 clean/dirt-restoring local schedules. No vendor emitter modified."""
import json,random,gzip,time,hashlib
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
O=Path(__file__).resolve().parent;P=O.parent
w=json.loads((P/'E7-WITNESS.json').read_text());dec=json.loads((P/'E7-MINCENTER-DECODER.json').read_text());ports=w['ports'];v=len(ports);h=w['h'];full=tuple(1<<i for i in range(h-1,-1,-1));roots=w['roots_scaled_by_2'];C=[[Q(x) for x in r] for r in dec['collect']];S=[[Q(x) for x in r] for r in dec['scatter']];d=len(C[0]);G=[[Q(sum(a*b for a,b in zip(x,y)),8) for y in roots] for x in roots]

def basis(xs):
 p={}
 for x in xs:
  for i in sorted(p,reverse=True):
   if x>>i&1:x^=p[i]
  if x:
   i=x.bit_length()-1
   for j in p:
    if p[j]>>i&1:p[j]^=x
   p[i]=x
 return tuple(p[i] for i in sorted(p,reverse=True))
def join(a,b):return basis((*a,*b))
def perp(p):return basis(x for x in range(1,1<<h) if not (p&x).bit_count()%2)
def legal(F,p):return all(not (p&x).bit_count()%2 for x in F)
frames=[basis(ports[i] for i in range(v) if C[i][k]) for k in range(d)]
assert all(len(F)==7 for F in frames)

def construct(seed):
 rng=random.Random(seed);n=2*v;A=[];cuts=[];B=[];factory=[];cur={i:((ports[i],) if i<v else ()) for i in range(n)};pools={i:[i] for i in range(v)};origin={i:i for i in range(v)}
 def helper(i=None):
  nonlocal n
  r=n;n+=1;cur[r]=()
  if i is not None:factory.append((r,i,Q(1),(ports[i],)));cur[r]=(ports[i],);origin[r]=i
  return r
 centers=[helper() for _ in range(d)]
 # Dedicated clean-source deliveries into center frames, so original sources remain available for corrections.
 for k in range(d):
  for i in range(v):
   if C[i][k]:
    r=helper(i);A.append((centers[k],r,C[i][k],frames[k]));cur[r]=frames[k];cur[centers[k]]=frames[k];pools[i].append(r)
 for t in range(v):
  for k in range(d):
   if S[t][k]:cuts.append((v+t,centers[k],S[t][k],None))
 targets=list(range(v))
 if seed:rng.shuffle(targets)
 new=0;uses=0
 for t in targets:
  todo=[i for i in range(v) if i!=t and G[t][i]];cur[v+t]=()
  while todo:
   choices=[]
   for i in todo:
    cand=[]
    for r in pools[i]:
     if legal(cur[r],ports[t]):
      F=join(cur[v+t],cur[r]);cand.append((len(F)-len(cur[r]),len(F),r,F))
    if cand:
     delta,dim,r,F=min(cand);choices.append((0,dim,delta,rng.random() if seed else i,i,r,F))
    else:
     F=join(cur[v+t],(ports[i],));choices.append((1,len(F),len(F)-1,rng.random() if seed else i,i,None,F))
   _,_,_,_,i,r,F=min(choices)
   if r is None:r=helper(i);pools[i].append(r);new+=1
   else:uses+=1
   assert legal(F,ports[t]);B.append((v+t,r,-G[t][i],F));cur[r]=F;cur[v+t]=F;todo.remove(i)
 A=factory+A
 # compute full literal monotone frame charge incl copied centers and final cleanup frame climbs.
 current={i:((ports[i],) if i<v else ()) for i in range(n)};paid=Counter()
 def climb(r,F):
  F=basis(F);assert join(current[r],F)==F
  if current[r]!=F:paid[len(F)-len(current[r])]+=1;current[r]=F
 for phase in (A,B):
  if phase is B:
   for k,r in enumerate(centers):assert current[r]==frames[k];paid[len(frames[k])]+=1
  for t,r,q,F in phase:climb(t,F);climb(r,F)
 for r in range(n):climb(r,perp(ports[r-v]) if v<=r<2*v else full)
 mass=sum(k*z for k,z in paid.items());R=n-2*v
 assert mass==2*v*(h-1)+h*R+sum(map(len,frames))
 return {'seed':seed,'v':v,'h':h,'R':R,'centers':centers,'center_frames':frames,'ports':ports,'A':A,'cut':cuts,'B':B,'profile':dict(paid),'new_B_clones':new,'B_reuses':uses,'rank_mass':mass}

def enc(w):
 o=dict(w)
 for phase in ('A','cut','B'):o[phase]=[['add',t,r,q.numerator,q.denominator,F] for t,r,q,F in w[phase]]
 return o
results=[];best=None
for seed in range(32):
 a=construct(seed);fee=sum(z*r*((73/r)**.0015935194192823068-1) for r,z in a['profile'].items());summary={k:a[k] for k in ('seed','R','profile','new_B_clones','B_reuses','rank_mass')};summary['diagnostic_fee_at_current_b']=fee;results.append(summary)
 if best is None or (fee,a['R'])<(best[0],best[1]['R']):best=(fee,a)
 print(json.dumps(summary),flush=True)
(O/'SEARCH.json').write_text(json.dumps(results,indent=2)+'\n');(O/'WORD.json.gz').write_bytes(gzip.compress(json.dumps(enc(best[1]),sort_keys=True,separators=(',',':')).encode(),mtime=0));print('BEST',best[0],best[1]['R'],flush=True)
