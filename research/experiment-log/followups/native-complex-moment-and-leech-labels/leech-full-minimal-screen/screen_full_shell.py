"""Actual lattice quotient labels and bounded puncturing of the full Leech shell.
No quadratic all-pairs shell matrix. New claim is finite discovery only.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations
import json,gzip,hashlib,time
import numpy as np
from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form
import leech_vectors as lv
r=Path(__file__).resolve().parent;started=time.time()
V=lv.V.astype(np.int16);assert V.shape==(196560,24);assert np.all(np.sum(V.astype(np.int32)**2,axis=1)==32)
W=V[V[np.arange(len(V)),np.argmax(V!=0,axis=1)]>0];assert W.shape==(98280,24)
# Exact scaled Leech lattice basis:4D24, twice the Golay code generators, odd coset.
Z=[[8]+[0]*23]
for j in range(1,24):z=[0]*24;z[0]=-4;z[j]=4;Z.append(z)
Z += [[2*x for x in row] for row in lv.G];Z += [[-3]+[1]*23]
B=hermite_normal_form(Matrix(Z).T).T;assert B.det()==2**36
H=B*B.T/8;assert all(x.q==1 for x in H);assert H.det()==1;assert all(int(H[i,i])%2==0 for i in range(24))
inv=B.inv();J=np.array((8*inv).tolist(),dtype=np.int64);assert all(x.q==1 for x in 8*inv)
coordinates=W.astype(np.int64)@J;assert np.all(coordinates%8==0);coordinates//=8
assert np.array_equal(coordinates@np.array(B.tolist(),dtype=np.int64),W)
Q=[sum((int(z)&1)<<i for i,z in enumerate(row)) for row in coordinates]
assert len(set(Q))==98280
naive=[sum((int(z)&1)<<i for i,z in enumerate(row)) for row in W]
# D=1 direct sum alternating lattice Gram, congruent to ordinary odd25-dimensional dot.
Drows=[1]+[sum((int(H[i,j])&1)<<(j+1) for j in range(24)) for i in range(24)]
def bil(a,b):
 s=0
 while a:
  bit=a&-a;s^=Drows[bit.bit_length()-1];a^=bit
 return (s&b).bit_count()%2
def inverse_rows(rows):
 n=len(rows);a=[z|(1<<(n+i)) for i,z in enumerate(rows)]
 for j in range(n):
  k=next(i for i in range(j,n) if a[i]>>j&1);a[j],a[k]=a[k],a[j]
  for i in range(n):
   if i!=j and a[i]>>j&1:a[i]^=a[j]
 assert [z&((1<<n)-1) for z in a]==[1<<i for i in range(n)]
 return [z>>n for z in a]
cur=[1<<i for i in range(25)];C=[]
while cur:
 chosen=None
 for i,v in enumerate(cur):
  if bil(v,v) and (len(cur)==1 or any(bil(v,w)!=bil(w,w) for w in cur)):chosen=i;break
 if chosen is None:
  i=next(i for i,v in enumerate(cur) if bil(v,v));j=next(j for j,w in enumerate(cur) if j!=i and not bil(w,w));cur[i]^=cur[j];chosen=i
 v=cur.pop(chosen);assert bil(v,v)==1;C.append(v);cur=[w^(v if bil(v,w) else 0) for w in cur]
assert all(bil(v,w)==int(i==j) for i,v in enumerate(C) for j,w in enumerate(C))
T=inverse_rows(C)
assert all((a&b).bit_count()%2==((Drows[i]>>j)&1) for i,a in enumerate(T) for j,b in enumerate(T))
def embed(a):
 z=0
 while a:b=a&-a;z^=T[b.bit_length()-1];a^=b
 return z
P=[embed(1|(q<<1)) for q in Q];assert len(set(P))==98280 and all(z.bit_count()%2 for z in P)
def rank(vs,stop=25):
 piv={}
 for x in vs:
  x=int(x)
  while x:
   j=x.bit_length()-1
   if j in piv:x^=piv[j]
   else:piv[j]=x;break
  if len(piv)==stop:return stop
 return len(piv)
# Construction-wide label identities follow matrix congruence and integer coordinates.
# Independently check full-shell pairings against three representative shape vectors.
census=[]
for shape in [(4,4),(2,)*8,(3,)+(1,)*23]:
 idx=next(i for i,w in enumerate(W) if tuple(sorted((abs(int(z)) for z in w if z),reverse=True))==shape)
 dots=W@W[idx];assert np.all(dots%8==0)
 for j,dot in enumerate(dots):assert (P[j]&P[idx]).bit_count()%2==(1+int(dot)//8)%2
 census.append({'line_index':idx,'shape':shape,'absolute_lattice_inner_product_counts':dict(Counter(abs(int(z))//8 for z in dots)),'bad_natural_decoder_cap_edges':int(np.count_nonzero(np.abs(dots)==16))})
# Tightness is a24x24 matrix multiplication, not a98280x98280 Gram.
S=W.astype(np.int64).T@W.astype(np.int64);assert np.array_equal(S,np.eye(24,dtype=np.int64)*131040)
# natural dyadic diagonal-one transfer W W^t/32 has rank24 but absdot16 corrections incompatible.
full_center_ranks=[rank(P[i] for i in range(len(W)) if W[i,j]) for j in range(24)]
even=np.flatnonzero(np.all(W%2==0,axis=1));assert len(even)==49128
x8=np.array([8]+[0]*23,dtype=np.int64)@J;assert np.all(x8%8==0);x8//=8
normal=embed(sum((int(z)&1)<<(i+1) for i,z in enumerate(x8)));assert normal
assert all((P[i]&normal).bit_count()%2==0 for i in even)
even_center_ranks=[rank(P[i] for i in even if W[i,j]) for j in range(24)]
print('PASS_EXACT_LATTICE_QUOTIENT_AND_NATIVE_LABELS',flush=True)
# Three deterministic bounded greedy maximal independent sets in the bad-edge graph.
# Each selected port removes incompatible survivors via one vector-dot batch; noallpairs fullshell storage.
trials=[];witnesses=[]
for seed,pool in [(55024,np.arange(len(W))),(55025,even),(55026,even)]:
 rng=np.random.default_rng(seed);alive=rng.permutation(pool);selected=[];dot_tests=0
 while len(alive):
  i=int(alive[0]);selected.append(i);alive=alive[1:]
  if len(alive):
   dots=W[alive]@W[i];dot_tests+=len(alive);alive=alive[np.abs(dots)!=16]
 U=W[selected];G=U@U.T;assert np.all(np.diag(G)==32);assert not np.any(np.abs(G-np.diag(np.diag(G)))==16)
 labels=[P[i] for i in selected]
 assert all(not G[i,j] or i==j or not ((labels[i]&labels[j]).bit_count()%2) for i in range(len(selected)) for j in range(len(selected)))
 rr=Matrix(U.tolist()).to_DM().rank();gather=[rank(labels[i] for i in range(len(U)) if U[i,j]) for j in range(24)]
 profile=dict(Counter(abs(int(z)) for z in G.flat));trial={'seed':seed,'pool':'full_shell' if len(pool)==98280 else 'even_coordinate_half','pool_lines':len(pool),'ports':len(selected),'exact_real_rank':rr,'binary_label_span':rank(labels),'coordinate_gather_frame_ranks':gather,'all_coordinate_gathers_proper':all(x<25 for x in gather),'maximal_in_pool':True,'batched_dot_products':dot_tests,'absolute_scaled_Gram_entry_histogram':profile,'offdiagonal_nonzero_corrections':int(np.count_nonzero(G)-len(U)),'dyadic_decoder':'T=U U^t/32','diagonal_one':True,'native_correction_caps_pass':True}
 trials.append(trial);witnesses.append({'seed':seed,'line_indices':selected,'vectors':U.tolist(),'labels':labels,'common_normal_even_pool':normal if len(pool)==49128 else None});print(json.dumps(trial),flush=True)
# exact input/output witness containers
basis={'scaled_basis':B.tolist(),'integral_unimodular_Gram':H.tolist(),'inverse_times8':J.tolist(),'original_form_rows':Drows,'orthonormalizing_rows':C,'embedding_rows':T,'even_half_normal':normal}
basis={k:([[int(z) for z in row] for row in v] if k in ['scaled_basis','integral_unimodular_Gram'] else v) for k,v in basis.items()}
(r/'LATTICE-BASIS-AND-LABELS.json').write_text(json.dumps(basis,indent=2)+'\n')
(r/'PUNCTURED-WITNESSES.json.gz').write_bytes(gzip.compress(json.dumps(witnesses,separators=(',',':')).encode(),mtime=0))
# Retain all lattice-coordinate quotient classes and ordinary odd labels, compact and hashed.
(r/'ALL-QUOTIENT-LABELS.json.gz').write_bytes(gzip.compress(json.dumps({'canonical_vectors_sha256':hashlib.sha256(W.astype('<i2').tobytes()).hexdigest(),'lattice_quotients':Q,'odd_labels':P},separators=(',',':')).encode(),mtime=0))
result={'status':'PASS_FULL_SHELL_LATTICE_QUOTIENT_AND_PUNCTURED_DECODER_SCREEN','minimal_vectors':len(V),'antipodal_lines':len(W),'prior_census_reused_as_regression':True,'new_exact_lattice_basis_determinant':str(B.det()),'normalized_lattice_Gram_determinant':str(H.det()),'actual_Lambda_mod2Lambda_classes':len(set(Q)),'naive_coordinate_parity_classes':len(set(naive)),'odd_native_labels_distinct':len(set(P)),'label_dimension':25,'exact_label_formula':'p(v) dot p(w) =1+<v,w>_Lambda mod2','full_shell_tight_frame':131040,'natural_rank24_decoder_diagonal_one':True,'natural_rank24_decoder_dyadic_denominator':32,'sampled_shape_neighbor_censuses':census,'full_shell_coordinate_gather_ranks':full_center_ranks,'even_half_lines':len(even),'even_half_coordinate_gather_ranks':even_center_ranks,'punctured_trials':trials,'scope':'Finite dyadic rank24 scalar decoders, lattice labels, correction caps, and coordinate gather span ranks only. No chronological dirty-helper word, phases, global supplier, paid profile or kappa. Noallpairs fullshell census.','seconds':time.time()-started}
(r/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print('DONE',flush=True)
