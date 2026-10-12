"""Joint tie perturbations for equal-cost two-coordinate Leech decoders.
This is a bounded search, not a proof of minimal binary label dimension.
"""
import json,gzip,itertools,time,math,random
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
A=np.array(json.load(gzip.open(ROOT/'DYADIC-DECODER-WITNESS.json.gz'))['A'],dtype=np.int64)
choices=[[]for _ in range(276)]
for j,k in itertools.combinations(range(23),2):
 dirs=set()
 for x,y in A[:,[j,k]]:
  u,v=int(y),-int(x);g=math.gcd(u,v);u//=g;v//=g
  if u<0:u,v=-u,-v
  dirs.add((u,v))
 for u,v in sorted(dirs):
  z=A[:,j]*u+A[:,k]*v;az=abs(z)
  if np.count_nonzero(z)!=100:continue
  for i in np.flatnonzero((az>0)&((az&(az-1))==0)):
   choices[i].append((j,k,u,v,int(z[i])))
assert all(choices)
def clique(E):
 adj=[sum((1<<int(j)) for j in np.flatnonzero(row)) for row in E];best=[]
 for start in range(276):
  curr=[start];remaining=adj[start]
  while remaining:
   cand=[];bits=remaining
   while bits:
    b=bits&-bits;x=b.bit_length()-1;bits-=b;cand.append(x)
   x=max(cand,key=lambda x:(adj[x]&remaining).bit_count());curr.append(x);remaining&=adj[x]
  if len(curr)>len(best):best=curr
 return best
runs=[];bestscore=None;bestw=None;t0=time.monotonic()
for seed in range(54800,54832):
 rng=random.Random(seed);cs=[rng.choice(c)for c in choices];scale=max(abs(c[-1])for c in cs)
 B=np.zeros((23,276),dtype=np.int64)
 for i,(j,k,u,v,d)in enumerate(cs):B[j,i]=u*(scale//d);B[k,i]=v*(scale//d)
 T=A@B;assert np.all(np.diag(T)==scale)
 E=(T!=0)|(T.T!=0);np.fill_diagonal(E,False);cl=clique(E)
 assert all(E[i,j]for i,j in itertools.combinations(cl,2))
 score=(len(cl),int(E.sum())//2);runs.append({'seed':seed,'clique_lower_bound':len(cl),'undirected_cap_edges':score[1]})
 if bestscore is None or score<bestscore:
  bestscore=score;bestw={'seed':seed,'scale':scale,'B_scaled':B.tolist(),'clique':cl}
res={'status':'COMPLETE_BOUNDED_EQUAL_COST_TIE_SEARCH_NOT_ADMISSION','seeds':32,
 'best_observed_clique_lower_bound':bestscore[0],'best_by_clique_then_edges':bestw['seed'],
 'per_port_equal_cost_choice_count_min':min(map(len,choices)),'per_port_equal_cost_choice_count_max':max(map(len,choices)),
 'seconds':time.monotonic()-t0,'runs':runs,
 'scope':'Each constructed transfer has diagonal1, dyadic coefficients and exactly99 nonzero offdiagonal entries per column. Clique size is only a certified LOWER bound. Smaller lower bound does not establish existence of labels at that dimension. No native center gathering or global cost checked.'}
(ROOT/'SPARSE-TIE-SEARCH.json').write_text(json.dumps(res,indent=2)+'\n')
(ROOT/'SPARSE-TIE-WITNESS.json.gz').write_bytes(gzip.compress(json.dumps(bestw,separators=(',',':')).encode(),mtime=0))
print(json.dumps(res,indent=2))
