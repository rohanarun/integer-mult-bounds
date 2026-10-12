"""Deterministic maximal two-coordinate hyperplane slices of retained276Leech ETF.
No full lattice enumeration; exact integer normals and rational rank witnesses.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,gzip,itertools,math,time
import numpy as np
import sympy as S
ROOT=Path(__file__).resolve().parent;OLD=ROOT.parent/'radical-geometry-leech'
raw=json.load(gzip.open(OLD/'WITNESSES.json.gz'));Y=np.array(raw['equiangular_lines_scaled'],dtype=np.int64)
(rootraw:=ROOT/'SOURCE-LINES.json.gz').write_bytes(gzip.compress(json.dumps({'Y':Y.tolist()},separators=(',',':')).encode(),mtime=0))
idx=np.arange(276);results=[];witness=[];t0=time.monotonic()
for level in range(10):
 A=Y[idx];G=A@A.T;dim=int(S.Matrix(A.tolist()).rank());N=len(idx)
 assert np.all(np.diag(G)==80) and np.all(abs(G[~np.eye(N,dtype=bool)])==16)
 bound=(dim-1)*24//(26-dim)
 choices={}
 for j,k in itertools.combinations(range(24),2):
  normals=set()
  for a,b in A[:,[j,k]]:
   u,v=int(b),-int(a);g=math.gcd(u,v)
   if not g:continue
   u//=g;v//=g
   if u<0 or(u==0 and v<0):u,v=-u,-v
   normals.add((u,v))
  for u,v in normals:
   z=A[:,j]*u+A[:,k]*v
   if not np.any(z):continue
   zeros=tuple(np.flatnonzero(z==0).tolist());choices.setdefault(zeros,(j,k,u,v))
 best=max(choices,key=lambda a:(len(a),tuple(-i for i in a)))
 assert len(best)<=bound
 tight=np.array_equal(G@G,(N*80//dim)*G) if N*80%dim==0 else False
 r={'level':level,'ports':N,'rank':dim,'tight':tight,'coherence':'1/5','hyperplane_zero_upper_bound':bound,'largest_two_coordinate_zero_set':len(best),'distinct_two_coordinate_zero_sets':len(choices),'zero_set_size_histogram':dict(sorted(Counter(map(len,choices)).items()))}
 results.append(r);witness.append({'port_indices_original':idx.tolist(),'next_zero_indices_local':list(best),'next_normal':choices[best]})
 if len(best)<24 or len(best)==N:break
 idx=idx[list(best)]
res={'status':'COMPLETE_EXACT_NESTED_SLICE_SCREEN_NOT_ADMISSION','seconds':time.monotonic()-t0,'levels':results}
(ROOT/'NESTED-SLICES.json').write_text(json.dumps(res,indent=2)+'\n')
(ROOT/'NESTED-WITNESS.json').write_text(json.dumps(witness,indent=2)+'\n')
print(json.dumps(res,indent=2))
