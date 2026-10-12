"""Exact binary Gram completions for deterministic nested Leech slices."""
from pathlib import Path
import gzip,json,itertools,math,time
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parent
Y=np.array(json.load(gzip.open(ROOT/'SOURCE-LINES.json.gz'))['Y'],dtype=np.int64)
slices=json.loads((ROOT/'NESTED-WITNESS.json').read_text())
def gf2rank(H):
 piv={}
 for row in H:
  x=sum(int(v)<<i for i,v in enumerate(row))
  while x:
   p=x.bit_length()-1
   if p in piv:x^=piv[p]
   else:piv[p]=x;break
 return len(piv)
results=[];wits=[]
for lev,sl in enumerate(slices[1:],1):
 A=Y[sl['port_indices_original']];N=len(A);best=np.full(N,N+1);choices=[None]*N
 for j,k in itertools.combinations(range(24),2):
  dirs=set()
  for x,y in A[:,[j,k]]:
   u,v=int(y),-int(x);g=math.gcd(u,v)
   if not g:continue
   u//=g;v//=g
   if u<0 or(u==0 and v<0):u,v=-u,-v
   dirs.add((u,v))
  for u,v in sorted(dirs):
   z=A[:,j]*u+A[:,k]*v;az=abs(z);legal=(az>0)&((az&(az-1))==0);nz=np.count_nonzero(z)
   for i in np.flatnonzero(legal&(best>nz)):best[i]=nz;choices[i]=(j,k,u,v,int(z[i]))
 assert all(c is not None for c in choices)
 scale=max(abs(c[-1])for c in choices);B=np.zeros((24,N),dtype=np.int64)
 for i,(j,k,u,v,d)in enumerate(choices):B[j,i]=u*(scale//d);B[k,i]=v*(scale//d)
 T=A@B;assert np.all(np.diag(T)==scale)
 edges=(T!=0)|(T.T!=0);np.fill_diagonal(edges,False)
 H=(~edges).astype(np.uint8);assert np.all(np.diag(H)==1)
 results.append({'level':lev,'ports':N,'column_support_histogram':dict(Counter(map(int,best))),'directed_offdiagonal':int(np.count_nonzero(T))-N,'binary_gram_rank_all_free_entries_one':gf2rank(H),'scope':'H is an exact symmetric completion with diagonal1 and zeros at every forced correction edge. Rank is for this completion, not a minimum.'})
 wits.append({'ports_original':sl['port_indices_original'],'B_scaled':B.tolist(),'scale':scale,'H':H.tolist()})
(ROOT/'SLICE-GRAM-RANK.json').write_text(json.dumps(results,indent=2)+'\n')
(ROOT/'SLICE-GRAM-WITNESSES.json.gz').write_bytes(gzip.compress(json.dumps(wits,separators=(',',':')).encode(),mtime=0))
print(json.dumps(results,indent=2))
