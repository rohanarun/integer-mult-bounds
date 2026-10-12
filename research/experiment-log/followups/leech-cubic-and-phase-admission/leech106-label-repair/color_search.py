"""Bounded alternative Gram completions for exact Leech106 transfers."""
from pathlib import Path
import os,json,gzip,hashlib,random,time
from collections import Counter
import numpy as np
P=Path(__file__).resolve().parent;R=P.parent;assert os.path.ismount('/Volumes/SP AI 01_16') and os.access(P,os.W_OK)
src=R/'leech-full-minimal-screen/PUNCTURED-WITNESSES.json.gz';ws=json.load(gzip.open(src));started=time.monotonic()
def basis(xs):
 b={}
 for v in xs:
  while v:
   k=v.bit_length()-1
   if k in b:v^=b[k]
   else:
    for j in b:
     if b[j]>>k&1:b[j]^=v
    b[k]=v;break
 return tuple(b[k] for k in sorted(b,reverse=True))
def rank(xs):return len(basis(xs))
results=[];bestw=[]
for w in ws:
 if len(w['labels'])!=106:continue
 U=np.asarray(w['vectors'],dtype=np.int64);G=U@U.T;N=len(U);E=G!=0;np.fill_diagonal(E,False);adj=[set(np.flatnonzero(E[i]).tolist()) for i in range(N)];supports=[np.flatnonzero(U[:,j]).tolist() for j in range(24)];trials=[];best=None
 # A clique is only a verified lower bound here, not an optimality claim.
 clique=[]
 for seed in range(128):
  rng=random.Random(seed+w['seed']*1000);can=set(range(N));cl=[]
  while can:
   p=max(can,key=lambda x:(len(adj[x]&can),rng.random()));cl.append(p);can&=adj[p]
  if len(cl)>len(clique):clique=cl
 for seed in range(256):
  rng=random.Random(seed+w['seed']*1000);C={};sat=[set() for _ in range(N)]
  while len(C)<N:
   free=[i for i in range(N) if i not in C];i=max(free,key=lambda x:(len(sat[x]),len(adj[x]),rng.random() if seed else -x));used=sat[i];c=next(x for x in range(N) if x not in used);C[i]=c
   for j in adj[i]:sat[j].add(c)
  cs=[C[i] for i in range(N)];q=max(cs)+1;groups=[[i for i in range(N) if cs[i]==c] for c in range(q)];t=(max(map(len,groups))-1).bit_length();labels=[0]*N
  for c,gr in enumerate(groups):
   for z,i in enumerate(gr):labels[i]=(1<<c)|(z<<q)|(z<<(q+t))
  h=q+2*t;rs=[rank(labels[i] for i in ids) for ids in supports];assert len(set(labels))==N and all(x.bit_count()%2 for x in labels);assert all((labels[i]&labels[j]).bit_count()%2==0 for i in range(N) for j in adj[i])
  row=dict(seed=seed,colors=q,tag_bits=t,dimension=h,label_span_rank=rank(labels),gather_ranks=rs,copied_rank=sum(rs),all_gathers_proper=max(rs)<h,class_sizes=sorted(map(len,groups),reverse=True));trials.append(row)
  key=(h,sum(rs),max(rs))
  if best is None or key<best[0]:best=(key,row,labels,cs)
 r=dict(source_seed=w['seed'],ports=N,edges=int(E.sum())//2,original_dimension=25,original_span_rank=rank(w['labels']),original_gather_ranks=[rank(w['labels'][i] for i in ids) for ids in supports],clique_lower_bound=len(clique),clique_indices=clique,best=best[1],trials=trials);results.append(r)
 bestw.append(dict(source_seed=w['seed'],vectors=w['vectors'],original_labels=w['labels'],labels=best[2],dimension=best[1]['dimension'],coloring=best[3],gather_frames=[list(basis(best[2][i] for i in ids)) for ids in supports],transfer_denominator=32,transfer_scaled=G.tolist()))
 print('BEST',json.dumps({k:v for k,v in r.items() if k!='trials'}),flush=True)
(P/'COLOR-RESULT.json').write_text(json.dumps(dict(status='COMPLETE_BOUNDED_COLOR_COMPLETION_SEARCH',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),seconds=time.monotonic()-started,records=results,scope='Explicit alternative ordinary-dot-product labels preserve all forced correction orthogonality, oddness and distinctness. No physical word or kappa.'),indent=2)+'\n');(P/'COLOR-WITNESSES.json.gz').write_bytes(gzip.compress(json.dumps(bestw,separators=(',',':')).encode(),mtime=0))
