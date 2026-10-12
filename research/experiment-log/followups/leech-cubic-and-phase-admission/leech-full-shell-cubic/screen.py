"""Exact scalar/cap screen of a new Leech cubic decoder, no supplier admission."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,gzip,hashlib,time
import numpy as np
import leech_vectors as lv
r=Path(__file__).resolve().parent;start=time.time()
src=r/'inputs'
q=json.loads(gzip.decompress((src/'ALL-QUOTIENT-LABELS.json.gz').read_bytes()))
V=lv.V.astype(np.int64);W=V[V[np.arange(len(V)),np.argmax(V!=0,axis=1)]>0]
assert W.shape==(98280,24)
# Match retained ordering by the same exact canonical vector hash convention.
P=[int(x) for x in q['odd_labels']]
assert len(P)==len(W) and len(set(P))==len(P) and all(x.bit_count()%2 for x in P)
# Independently reconstruct every label to bind vector order.
basis=json.loads((src/'LATTICE-BASIS-AND-LABELS.json').read_text())
from sympy import Matrix
B=Matrix(basis['scaled_basis']);J=np.array((8*B.inv()).tolist(),dtype=np.int64)
coords=W@J;assert np.all(coords%8==0);coords//=8
emb=basis['embedding_rows'];actual=[]
for row in coords:
 z=emb[0]
 for i,a in enumerate(row):
  if a&1:z^=emb[i+1]
 actual.append(z)
assert actual==P
pairs=[(i,j) for i in range(24) for j in range(24) if i!=j]
triples=list(combinations(range(24),3))
def source(w):
 return [int((z**3-z)//3) for z in w]+[int(z) for z in w]+[int(w[i]**2*w[j]) for i,j in pairs]+[int(w[i]*w[j]*w[k]) for i,j,k in triples]
def target(v):
 assert all((int(z)**3-256*int(z))%3==0 for z in v)
 return [int(z**3) for z in v]+[int((z**3-256*z)//3) for z in v]+[int(v[i]**2*v[j]) for i,j in pairs]+[int(2*v[i]*v[j]*v[k]) for i,j,k in triples]
assert len(source(W[0]))==2624
# Exact factor check on every pair of a sampled square block including all shapes.
idx=sorted(set([0,132,32890]+np.random.default_rng(561).choice(len(W),125,replace=False).tolist()))
A=np.array([target(W[i]) for i in idx],dtype=np.int64);G=np.array([source(W[i]) for i in idx],dtype=np.int64)
S=W[idx]@W[idx].T;num=S**3-256*S
assert np.all(num%3==0);assert np.array_equal(A@G.T,num//3)
assert np.all(np.diag(A@G.T)==8192)
# All full rows at sampled anchors, including all three coordinate shapes.
anchors=sorted(set([0,132,32890]+np.random.default_rng(562).choice(len(W),61,replace=False).tolist()))
rec=[];bad_original=0;tested=0
for i in anchors:
 s=W@W[i];assert set(s.tolist())<={-16,-8,0,8,16,32};assert np.count_nonzero(s==32)==1
 numer=s*(s*s-256)
 # Entries are {-1/16,0,1/16,1}; diagonal self only.
 assert set(numer.tolist()) <= {-1536,0,1536,24576}
 bad=0
 for j,t in enumerate(s):
  assert ((P[i]&P[j]).bit_count()%2)==(1+int(t)//8)%2
  if j!=i and numer[j] and ((P[i]&P[j]).bit_count()%2):bad+=1
 assert bad==0
 bad_original+=int(np.count_nonzero(np.abs(s)==16));tested+=len(W)
 rec.append({'anchor':i,'nonzero_off_diagonal':int(np.count_nonzero(numer))-1,'natural_gram_incompatible_edges':int(np.count_nonzero(np.abs(s)==16)),'cubic_incompatible_edges':bad})
# Degree<=3 multivariate identity, tested also away from shell; captures coefficient controls.
random=np.random.default_rng(563)
for _ in range(100):
 v=random.integers(-5,6,24,dtype=np.int64);w=random.integers(-5,6,24,dtype=np.int64);s=int(v@w)
 assert sum(a*b for a,b in zip(target(v),source(w)))==(s**3-256*s)//3
# Proper gathers: append a zero coordinate to 25-bit labels. Actual normal is e25.
normal=1<<25;assert all((p&normal)==0 for p in P)
# Source feature supports: every exact binary span is computed, bases retained.
def span_on(mask):
 piv={}
 for ix in np.flatnonzero(mask):
  x=P[int(ix)];original=x
  while x:
   j=x.bit_length()-1
   if j in piv:x^=piv[j][0]
   else:piv[j]=(x,int(ix),original);break
  if len(piv)==25:break
 return len(piv),[v[1] for v in piv.values()]
records=[];nz=W!=0
for i in range(24):
 rank,inds=span_on((W[:,i]**3-W[:,i])!=0);records.append({'kind':'divided_cube','indices':[i],'rank':rank,'basis_ports':inds})
for i in range(24):
 rank,inds=span_on(nz[:,i]);records.append({'kind':'linear','indices':[i],'rank':rank,'basis_ports':inds})
for i,j in pairs:
 rank,inds=span_on(nz[:,i]&nz[:,j]);records.append({'kind':'square_linear','indices':[i,j],'rank':rank,'basis_ports':inds})
for i,j,k in triples:
 rank,inds=span_on(nz[:,i]&nz[:,j]&nz[:,k]);records.append({'kind':'triple','indices':[i,j,k],'rank':rank,'basis_ports':inds})
# An explicit single coefficient mutation must break factorization.
mut=A.copy();mut[0,0]+=1
assert not np.array_equal(mut@G.T,num//3)
C=sum(x['rank'] for x in records);N=len(W)
result={'status':'PASS_NEW_CUBIC_DYADIC_DECODER_FINITE_SCREEN','ports':N,'binary_label_dimension':26,'active_label_span_dimension':25,'scalar_rank_upper_bound_over_Q':2600,'explicit_dyadic_centers':2624,'decoder':'T(v,w)=s*(s^2-256)/24576, s=v dot w in scaled integer coordinates','equivalent_lattice_formula':'t*(t^2-4)/48','factorization_denominator':8192,'factor_pair_checks':len(idx)**2,'off_shell_integer_pair_checks':100,'full_rows_checked':len(anchors),'row_pair_checks':tested,'removed_bad_natural_gram_edges_in_checked_rows':bad_original,'all_cubic_bad_edges_in_checked_rows':0,'gather_rank_histogram':dict(Counter(x['rank'] for x in records)),'copied_rank_C':C,'ports_minus_copy_rank':N-C,'optimistic_deficit_formula':f'{N-C}*L-{N}','optimistic_first_positive_stage':N//(N-C)+1 if N>C else None,'controls':['single_target_coefficient_mutation_rejected','natural_rank24_kernel_has_incompatible_edges'],'scope':'Exact polynomial identity and full-line label reconstruction; bounded full-row checks, not all 9.66 billion pairs. General cap implication uses the known Leech minimal-shell inner-product classes. All gathers are proper after zero-coordinate extension. No native phase replay, dirty-helper word, paid profile, hosting invoice or kappa.'}
(r/'GATHER-BASES.json.gz').write_bytes(gzip.compress(json.dumps(records).encode(),mtime=0));(r/'ROW-CHECKS.json').write_text(json.dumps(rec,indent=2)+'\n');(r/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2),flush=True);print('Seconds',time.time()-start,flush=True)
