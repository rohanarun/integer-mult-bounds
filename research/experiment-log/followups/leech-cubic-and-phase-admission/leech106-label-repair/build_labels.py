"""Create and exactly check labels for the saved proper correction-graph colorings."""
from pathlib import Path
import os,json,gzip,random,hashlib,time
from collections import Counter
import numpy as np
P=Path(__file__).resolve().parent;assert os.path.ismount('/Volumes/SP AI 01_16') and os.access(P,os.W_OK)
files=[P/'TABU-SOLUTIONS.json.gz',P/'TABU-LOWER-SOLUTIONS.json.gz'];ws=[]
for f in files:
 if f.exists():ws+=json.load(gzip.open(f))
def independent_basis(vs):
 a=list(vs);i=0
 for bit in range(max(a,default=0).bit_length()-1,-1,-1):
  k=next((j for j in range(i,len(a)) if a[j]>>bit&1),None)
  if k is None:continue
  a[i],a[k]=a[k],a[i]
  for j in range(len(a)):
   if j!=i and a[j]>>bit&1:a[j]^=a[i]
  i+=1
 return a[:i]
allrows=[];witnesses=[]
for w in ws:
 U=np.array(w['vectors'],dtype=np.int64);G=U@U.T;cs=w['coloring'];q=max(cs)+1;groups=[[i for i,c in enumerate(cs) if c==j] for j in range(q)];t=(max(map(len,groups))-1).bit_length();h=q+2*t;supports=[np.flatnonzero(U[:,j]).tolist() for j in range(24)];best=None;trials=[]
 for seed in range(64):
  rng=random.Random(seed);labels=[0]*106
  for col,group in enumerate(groups):
   order=group[:] 
   if seed:rng.shuffle(order)
   for tag,i in enumerate(order):labels[i]=(1<<col)|(tag<<q)|(tag<<(q+t))
  frames=[independent_basis([labels[i] for i in ids]) for ids in supports];ranks=list(map(len,frames));key=(sum(ranks),max(ranks));trials.append(dict(seed=seed,copied_rank=key[0],ranks=ranks))
  if best is None or key<best[0]:best=(key,seed,labels,frames)
 _,tagseed,labels,frames=best
 assert len(set(labels))==106 and all(v.bit_count()%2==1 for v in labels)
 assert all(G[i,i]==32 for i in range(106));assert all(G[i,j]==0 or i==j or (labels[i]&labels[j]).bit_count()%2==0 for i in range(106) for j in range(106))
 assert all(len(F)<h for F in frames)
 row=dict(source_seed=w['source_seed'],colors=q,tag_bits=t,ambient_dimension=h,label_span_rank=len(independent_basis(labels)),gather_ranks=list(map(len,frames)),copied_rank=sum(map(len,frames)),tag_seed=tagseed,all_correction_caps=True,all_gathers_proper=True,tag_trials=trials);allrows.append(row)
 witnesses.append(dict(source_seed=w['source_seed'],vectors=w['vectors'],labels=labels,dimension=h,coloring=cs,gather_frames=frames,transfer_scaled=G.tolist(),transfer_denominator=32,tag_seed=tagseed))
best=min(range(len(allrows)),key=lambda i:(allrows[i]['ambient_dimension'],allrows[i]['copied_rank']))
(P/'REPAIRED-WITNESSES.json.gz').write_bytes(gzip.compress(json.dumps(witnesses,separators=(',',':')).encode(),mtime=0));(P/'REPAIRED-RESULT.json').write_text(json.dumps(dict(status='PASS_FINITE_LABEL_COMPLETIONS',best=allrows[best],records=allrows,scope='Same scalar Gram transfer, changed unconstrained binary pairings, exact oddness/distinctness/correction caps/proper gathers. No chronological word, paid profile, phase admission or kappa.'),indent=2)+'\n');print(json.dumps({k:v for k,v in allrows[best].items() if k!='tag_trials'},indent=2))
