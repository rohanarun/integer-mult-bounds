"""Exact new slice/decoder tests. Reuses earlier Claude Golay generator with attribution.
No supplier admission or kappa claim. All matrices below are integer arithmetic.
"""
from pathlib import Path
import json,gzip,itertools,time,hashlib
import numpy as np
from collections import Counter
from fractions import Fraction
from leech_vectors import V,octads
ROOT=Path(__file__).resolve().parent

def rank_mod(A,p):
 A=np.asarray(A,dtype=np.int64).copy()%p;r=0
 for j in range(A.shape[1]):
  nz=np.flatnonzero(A[r:,j])
  if not len(nz):continue
  i=r+int(nz[0]);A[[i,r]]=A[[r,i]];A[r]=A[r]*pow(int(A[r,j]),-1,p)%p
  for i in range(A.shape[0]):
   if i!=r and A[i,j]:A[i]=(A[i]-A[i,j]*A[r])%p
  r+=1
  if r==A.shape[0]:break
 return r

def positive_rows(A):return A[np.array([next(int(x) for x in v if x)>0 for v in A])]
def dump(name,x):(ROOT/name).write_text(json.dumps(x,indent=2)+'\n')
start=time.monotonic()
x=V[0];y=V[np.flatnonzero(V@x==-8)[0]];c=x+y
assert int(c@c)==48
S=V[V@c==24];Y=positive_rows(2*S-c)
assert S.shape==(552,24) and Y.shape==(276,24)
G=Y@Y.T
assert set(np.diag(G))=={80}
assert set(G[~np.eye(len(G),dtype=bool)])=={-16,16}
assert np.array_equal(G@G,960*G)
assert np.array_equal(Y.T@Y,960*np.eye(24,dtype=np.int64)-20*np.outer(c,c))
# Is the obvious orthogonal projector itself dyadic? It is G/960.
frac=Fraction(16,960)
assert frac==Fraction(1,60)
# Matrix must have dyadic coefficients to be a finite composition of current legal scalar gates.
# A changed decoder or additional block can escape this specific obstruction.
res={'status':'PASS_EXACT_GEOMETRY_SCREEN_NOT_SUPPLIER_ADMISSION','seconds':time.monotonic()-start,
 'norm6_slice':{'scaled_norm6_vector':c.tolist(),'vectors':552,'lines':276,'dimension':23,'scaled_line_norm_squared':80,'off_diagonal_gram_values':[-16,16],
 'gram_identity':'G^2=960 G','coordinate_frame_identity':'Y^T Y=960 I - 20 cc^T',
 'coherence':'1/5','normalized_projector_off_diagonal':'1/60','direct_orthogonal_decoder_dyadic':False,
 'modular_coordinate_ranks':{str(p):rank_mod(Y,p) for p in [3,5,7,11,13,17]},
 'rejection_scope':'The direct orthogonal projector G/960 is not realizable by a finite dyadic scalar circuit. This does not rule out a different scalar word, encoding or nonorthogonal decoder.'}}
# Further octad subsets: one, disjoint pairs/triples, overlap2 and overlap4.
O=sorted(tuple(i for i,b in enumerate(o) if b) for o in octads)
def octad_lines(o):
 rows=[]
 for sg in itertools.product([1,-1],repeat=7):
  signs=(1,)+sg
  if sum(s<0 for s in signs)%2:continue
  row=np.zeros(24,dtype=np.int64);row[list(o)]=signs;rows.append(row)
 return np.asarray(rows)
first=O[0];selected={'one_octad':[first]}
for n in [0,2,4]:
 second=next(o for o in O if len(set(o)&set(first))==n)
 selected['two_octads_intersection_'+str(n)]=[first,second]
 if n==0:
  third=next(o for o in O if not(set(o)&(set(first)|set(second))))
  selected['three_disjoint_octads']=[first,second,third]
res['octad_subsets']={}
witness={'norm6_slice_c':c.tolist(),'equiangular_lines_scaled':Y.tolist(),'octad_subsets':{}}
for name,os in selected.items():
 A=np.vstack([octad_lines(o) for o in os]);F=A.T@A;diag=np.diag(F)
 assert np.array_equal(F,np.diag(diag))
 active=np.flatnonzero(diag);recip=[Fraction(1,int(diag[i])) for i in active]
 assert all(q.denominator&(q.denominator-1)==0 for q in recip)
 D=np.zeros_like(A,dtype=np.int64)
 # Scale entire coordinate decoder by128, enough for one or two coverings.
 for i in active:D[:,i]=A[:,i]*(128//int(diag[i]))
 assert np.array_equal(D.T@A,np.diag([128 if i in active else 0 for i in range(24)]))
 gram=A@A.T;off=gram[~np.eye(len(A),dtype=bool)]
 res['octad_subsets'][name]={'lines':len(A),'dimension':len(active),'coordinate_frame_diagonal':dict(Counter(map(int,diag))),
 'dyadic_decoder':True,'integer_decoder_identity':'D^T A=128 I on active coordinates','coherence':str(Fraction(int(abs(off).max()),8)),
 'nonzero_offdiagonal_pairs':int(np.count_nonzero(off)),'line_incidence_nonzeros':int(np.count_nonzero(A)),
 'scope':'Exact sparse encoder/decoder pair only. No frame labels, arbitrary-dirt identity, paid profile or global hosting.'}
 witness['octad_subsets'][name]={'octads':[list(o) for o in os],'A':A.tolist(),'128_times_decoder_transpose':D.tolist()}
dump('RESULT.json',res)
(ROOT/'WITNESSES.json.gz').write_bytes(gzip.compress(json.dumps(witness,sort_keys=True).encode(),mtime=0))
print(json.dumps(res,indent=2))
