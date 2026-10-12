"""Exhaustive two-coordinate cancellation-direction screen for Leech diagonal transfer.
For each coordinate pair, a zero on any port determines a direction. Normalize at
any target with a dyadic reciprocal; select sparsest column per target. Exact ints.
"""
import json,gzip,itertools,time,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
A=np.array(json.load(gzip.open(ROOT/'DYADIC-DECODER-WITNESS.json.gz'))['A'],dtype=np.int64)
t0=time.monotonic();best=np.full(276,276);choice=[None]*276;directions=0;admissions=0
for j,k in itertools.combinations(range(23),2):
 dirs=set()
 for x,y in A[:,[j,k]]:
  u,v=int(y),-int(x);g=math.gcd(u,v);u//=g;v//=g
  if u<0:u,v=-u,-v
  dirs.add((u,v))
 for u,v in sorted(dirs):
  directions+=1;z=A[:,j]*u+A[:,k]*v;nz=int(np.count_nonzero(z));az=abs(z)
  legal=(az>0)&((az&(az-1))==0);admissions+=int(legal.sum())
  for i in np.flatnonzero(legal&(best>nz)):
   best[i]=nz;choice[i]=(j,k,u,v,int(z[i]))
assert all(c is not None for c in choice)
scale=max(abs(c[-1]) for c in choice);assert scale&(scale-1)==0
B=np.zeros((23,276),dtype=np.int64)
for i,(j,k,u,v,d) in enumerate(choice):B[j,i]=u*(scale//d);B[k,i]=v*(scale//d)
T=A@B;assert np.all(np.diag(T)==scale)
E=(T!=0)|(T.T!=0);np.fill_diagonal(E,False)
# Valid lower bound, not an exact maximum clique claim.
bestclique=[]
for start in range(276):
 cl=[start];remaining=set(np.flatnonzero(E[start]).tolist())
 while remaining:
  x=max(remaining,key=lambda x:(sum(E[x,y] for y in remaining),-x));cl.append(x);remaining={y for y in remaining if E[x,y]}
 if len(cl)>len(bestclique):bestclique=cl
assert all(E[i,j] for i,j in itertools.combinations(bestclique,2))
res={'status':'PASS_EXACT_SPARSE_DYADIC_DIAGONAL_TRANSFER_SCREEN_NOT_ADMISSION',
 'coordinate_pairs':253,'distinct_cancellation_directions':directions,'legal_target_direction_normalizations':admissions,
 'scope_of_search':'For each target independently, all two-coordinate directions annihilating at least one port and admitting dyadic normalization; min column support among these directions. Ties fixed lexicographically, not joint binary-label optimization.',
 'common_denominator':scale,'decoder_nonzeros':int(np.count_nonzero(B)),'diagonal_one':True,
 'directed_offdiagonal_corrections':int(np.count_nonzero(T))-276,'undirected_orthogonality_constraints':int(E.sum())//2,
 'column_support_histogram':{str(int(v)):int(np.sum(best==v)) for v in np.unique(best)},
 'certified_orthogonal_clique_size':len(bestclique),'clique_ports':bestclique,
 'binary_label_dimension_lower_bound':len(bestclique),'seconds':time.monotonic()-t0,
 'remaining':'No binary labels constructed, center hyperplanes tested, dirty local word/frame chain built, global admission or kappa calculated.'}
(ROOT/'SPARSE-FUNCTIONALS.json').write_text(json.dumps(res,indent=2)+'\n')
(ROOT/'SPARSE-FUNCTIONALS-WITNESS.json.gz').write_bytes(gzip.compress(json.dumps({'scale':scale,'B_scaled':B.tolist(),'choices':choice},separators=(',',':')).encode(),mtime=0))
print(json.dumps(res,indent=2))
