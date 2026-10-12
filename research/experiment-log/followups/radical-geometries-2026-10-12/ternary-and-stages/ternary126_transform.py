"""Exact clean scalar transform for the 126-port F3^6 norm-one orthogonality graph.
Dense radix-3 construction is a reference, not an efficient/admitted supplier.
"""
from pathlib import Path
from itertools import product
from collections import Counter
import json,time
root=Path(__file__).resolve().parent;started=time.time();d=6;N=3**d
V=[v for v in product((-1,0,1),repeat=d) if sum(x*x for x in v)%3==1 and next((x for x in v if x),0)==1]
A=[[int(sum(x*y for x,y in zip(v,w))%3==0) for w in V] for v in V]
assert all(sum(row)==45 for row in A)
assert all(A[i][i]==0 for i in range(126))
counts=Counter()
for i in range(126):
 for j in range(i+1,126):counts[(A[i][j],sum(a*b for a,b in zip(A[i],A[j])))]+=1
assert counts=={(0,18):5040,(1,12):2835}
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def omega(a):return(-a[1],a[0]-a[1])
def fft(a):
 stride=1
 for _ in range(d):
  for base in range(0,N,3*stride):
   for k in range(stride):
    u,v,w=a[base+k],a[base+k+stride],a[base+k+2*stride]
    a[base+k]=add(add(u,v),w)
    a[base+k+stride]=add(add(u,omega(v)),omega(omega(w)))
    a[base+k+2*stride]=add(add(u,omega(omega(v))),omega(w))
  stride*=3
 return a
idx=lambda v:sum((x%3)*3**k for k,x in enumerate(v))
indices=[(idx(v),idx(tuple(-x for x in v))) for v in V]
for c in range(126):
 inputs=[int(c==i) for i in range(126)];a=[(0,0)]*N
 for z,(i,j) in zip(inputs,indices):a[i]=a[j]=(z,0)
 f=fft(a);S=sum(inputs)
 for r,(i,_) in enumerate(indices):
  assert f[i][1]==0
  assert (f[i][0]+S)==3*A[r][c]
print('PASS_EXHAUSTIVE_126_BASIS_COLUMNS',flush=True)
r={'status':'PASS_EXACT_CLEAN_SCALAR_126_PORT_TRANSFORM','dimension':6,'ports':126,'address_count':729,'basis_columns_checked':126,'scalar_output_entries_checked':126*126,'adjacency_degree':45,'common_neighbors_adjacent':12,'common_neighbors_nonadjacent':18,'matrix_identity':'A^2=27 I-6 A+18 J','radix3_butterflies_per_application':d*(N//3),'radix3_additions_per_application':6*d*(N//3),'eisenstein_omega_scales_per_application':6*d*(N//3),'output_formula':'(DFT(even extension)(q)+sum(inputs))/3','comparison':'126 ports in F3^6 instead of112 ports in F2^9;729 ternary addresses exceed512 binary addresses. Lower coordinate dimension is not automatically lower cost.','scope':'Reference clean scalar circuit only. Does not implement dirty-helper cleanup, monotone frame climbs, supplier rank invoice, or all-size theorem. Full729-cell reference is too broad to claim helper reduction.','seconds':time.time()-started}
(root/'TERNARY126-TRANSFORM.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
