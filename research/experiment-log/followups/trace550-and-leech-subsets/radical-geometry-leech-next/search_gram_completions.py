"""Bounded coordinate search of exact binary Gram rank, retaining each best matrix.
Free offdiagonal pairs are those unconstrained by the actual decoder correction.
"""
from pathlib import Path
import json,gzip,time,random
import numpy as np
ROOT=Path(__file__).resolve().parent
wits=json.load(gzip.open(ROOT/'SLICE-GRAM-WITNESSES.json.gz'))
def rank(rows):
 piv={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in piv:x^=piv[p]
   else:piv[p]=x;break
 return len(piv)
allres=[];bestw=[]
for wi in [4,3,2]:
 w=wits[wi];H=w['H'];N=len(H);free=[(i,j)for i in range(N)for j in range(i)if H[i][j]]
 rows=[sum(v<<j for j,v in enumerate(row))for row in H];initial=rank(rows);best=initial;keep=rows[:];rng=random.Random(55000+N);start=time.monotonic();it=0;progress=[];cur=initial
 while time.monotonic()-start<12:
  i,j=rng.choice(free);rows[i]^=1<<j;rows[j]^=1<<i;r=rank(rows);it+=1
  if r<=cur:cur=r
  else:rows[i]^=1<<j;rows[j]^=1<<i
  if r<best:
   best=r;keep=rows[:];progress.append({'iteration':it,'rank':r,'seconds':time.monotonic()-start})
  # Restart from retained best after long plateau to explore free-entry combinations.
  if it%10000==0:rows=keep[:];cur=best
 matrix=[[(x>>j)&1 for j in range(N)]for x in keep]
 assert all(matrix[i][i]==1 for i in range(N))
 assert all(matrix[i][j]==matrix[j][i]and(H[i][j]or matrix[i][j]==0)for i in range(N)for j in range(N))
 allres.append({'ports':N,'initial_rank':initial,'best_exact_rank':best,'iterations':it,'seconds':time.monotonic()-start,'free_pairs':len(free),'improvements':progress})
 bestw.append({'source_witness_index':wi,'ports':N,'best_rank':best,'H':matrix})
 print(N,initial,best,it,flush=True)
(ROOT/'GRAM-COMPLETION-SEARCH.json').write_text(json.dumps({'status':'COMPLETE_BOUNDED_EXACT_BINARY_RANK_SEARCH','results':allres,'scope':'Each best rank is exact for retained completion; no minimum-rank proof. Explicit dot-product labels and center gathering not yet checked.'},indent=2)+'\n')
(ROOT/'GRAM-COMPLETION-WITNESSES.json.gz').write_bytes(gzip.compress(json.dumps(bestw,separators=(',',':')).encode(),mtime=0))
