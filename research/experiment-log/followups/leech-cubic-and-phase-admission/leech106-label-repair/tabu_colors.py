"""Bounded tabu repair of low-color correction-graph completions."""
from pathlib import Path
import os,json,gzip,time,random
import numpy as np
P=Path(__file__).resolve().parent;assert os.path.ismount('/Volumes/SP AI 01_16') and os.access(P,os.W_OK)
ws=json.load(gzip.open(P/'COLOR-WITNESSES.json.gz'));runs=[];solutions=[];allstart=time.monotonic()
for w in ws:
 G=np.array(w['transfer_scaled']);E=G!=0;np.fill_diagonal(E,False);N=len(G);adj=[np.flatnonzero(E[i]) for i in range(N)]
 for q in [19,18]:
  begin=time.monotonic();rng=np.random.default_rng(552000+w['source_seed']+q);best=10**9;bestC=None;iters=0;restart=0;done=False
  while time.monotonic()-begin<22:
   C=np.array(w['coloring'])%q if restart==0 else rng.integers(0,q,N);counts=np.zeros((N,q),dtype=np.int16)
   for i in range(N):np.add.at(counts[i],C[adj[i]],1)
   taboo=np.zeros((N,q),dtype=np.int64);conf=int(counts[np.arange(N),C].sum())//2;stale=0
   for it in range(16000):
    iters+=1
    if conf<best:best=conf;bestC=C.copy();stale=0
    else:stale+=1
    if conf==0:done=True;break
    if it%128==0 and time.monotonic()-begin>=22:break
    bad=np.flatnonzero(counts[np.arange(N),C]);delta=counts[bad]-counts[bad,C[bad]][:,None];allowed=(taboo[bad]<=it)|(conf+delta<best);allowed[np.arange(len(bad)),C[bad]]=False
    score=np.where(allowed,delta,10000);m=score.min();idx=np.argwhere(score==m)
    if not len(idx):break
    ri,new=idx[rng.integers(len(idx))];v=int(bad[ri]);old=int(C[v]);conf+=int(delta[ri,new]);C[v]=new;counts[adj[v],old]-=1;counts[adj[v],new]+=1;taboo[v,old]=it+7+int(.6*len(bad))+int(rng.integers(10))
    if stale>5000:break
   restart+=1
   if done:break
  row=dict(source_seed=w['source_seed'],target_colors=q,best_conflicts=best,iterations=iters,restarts=restart,seconds=time.monotonic()-begin);runs.append(row);print(json.dumps(row),flush=True)
  if best==0:
   colors=bestC.tolist();assert all(colors[i]!=colors[j] for i in range(N) for j in adj[i]);sol=dict(w);sol['coloring']=colors;sol['colors']=q;solutions.append(sol)
   (P/'TABU-SOLUTIONS.json.gz').write_bytes(gzip.compress(json.dumps(solutions,separators=(',',':')).encode(),mtime=0));print('COLOR_SOLUTION',w['source_seed'],q,flush=True)
(P/'TABU-RESULT.json').write_text(json.dumps(dict(status='COMPLETE_BOUNDED_COLOR_REPAIR',runs=runs,seconds=time.monotonic()-allstart,scope='Heuristic graph coloring with exact final edge checks; failed runs are not chromatic lower bounds.'),indent=2)+'\n')
