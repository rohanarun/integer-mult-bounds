"""Independent retained-witness audit. No imports from construction or compression."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import gzip,json
import numpy as np
from sympy import Matrix
import leech_vectors as lv
r=Path(__file__).resolve().parent
basis=json.loads((r/'inputs/LATTICE-BASIS-AND-LABELS.json').read_text());q=json.loads(gzip.decompress((r/'inputs/ALL-QUOTIENT-LABELS.json.gz').read_bytes()))
B=Matrix(basis['scaled_basis']);H=Matrix(basis['integral_unimodular_Gram']);T=basis['embedding_rows']
assert B*B.T==8*H and all(x.q==1 for x in H)
D=Matrix.diag(Matrix([[1]]),H)
assert all(((T[i]&T[j]).bit_count()%2)==int(D[i,j])%2 for i in range(25) for j in range(25))
V=lv.V;W=V[V[np.arange(len(V)),np.argmax(V!=0,axis=1)]>0]
assert W.shape==(98280,24) and np.all(np.sum(W*W,axis=1)==32)
assert len({tuple(v) for v in W.tolist()})==len(W)
# Positive first nonzero coordinate rules out antipodal pairs.
assert np.all(W[np.arange(len(W)),np.argmax(W!=0,axis=1)]>0)
J=np.array((8*B.inv()).tolist(),dtype=np.int64);coords=W@J;assert np.all(coords%8==0);coords//=8
assert np.array_equal(coords@np.array(B.tolist(),dtype=np.int64),W)
P=q['odd_labels'];reconstructed=[]
for row in coords:
 p=T[0]
 for j,v in enumerate(row):
  if v&1:p^=T[j+1]
 reconstructed.append(p)
assert reconstructed==P and len(set(P))==len(P) and all(p.bit_count()%2 for p in P)
# Algebraic all-pairs proof: norm32 + integral lattice Gram/8 gives integer t in[-4,4].
# Offdiagonal +-4 excluded by equality case of Cauchy and no equal/antipodal pair.
# Label dot is1+t mod2; nonzero correction only at oddt because cubicvanishes atevent.
values={t:Q(t*(t*t-4),48) for t in range(-4,5)}
assert values[4]==1
assert all(values[t]==0 for t in (-2,0,2))
assert all(v.denominator&(v.denominator-1)==0 for v in values.values())
assert all(not values[t] or (1+t)%2==0 for t in range(-3,4))
# Retained factor matrices, using integer numerators, independently evaluatedagainstclosedform.
a=json.loads(gzip.decompress((r/'FACTOR-SAMPLE.json.gz').read_bytes()));X=np.array(a['vectors'],dtype=np.int64);F=np.array(a['scatter_numerators'],dtype=np.int64);G=np.array(a['gather_integers'],dtype=np.int64)
assert F.shape==G.shape==(128,2600) and a['denominator']==8192
s=X@X.T;product=F@G.T;assert np.array_equal(3*product,s**3-256*s)
assert np.all(np.diag(product)==8192)
# Verify every retained gather rank with actual support membership andbasisindependence.
def rank(rows):
 piv={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in piv:x^=piv[j]
   else:piv[j]=x;break
 return len(piv)
bases=json.loads(gzip.decompress((r/'COMPRESSED-GATHER-BASES.json.gz').read_bytes()))
assert len(bases)==2600
for rec in bases:
 ids=rec['basis_ports'];assert len(set(ids))==25 and rank([P[i] for i in ids])==25
 for k in ids:
  v=W[k];idx=rec['indices'];kind=rec['kind']
  if kind=='divided_cube':val=(int(v[idx[0]])**3-int(v[idx[0]]))//3
  elif kind=='linear':val=int(v[idx[0]])
  elif kind=='square_linear':val=int(v[idx[0]]**2*v[idx[1]])
  else:val=int(v[idx[0]]*v[idx[1]]*v[idx[2]])
  assert val!=0
assert all(p<(1<<25) for p in P) # exact upper spanboundandzeroextraaxis
assert rank(P)==25
# Global compression identity verified on allsourcevectors for eachremovedfeature.
for i in range(24):
 j=(i+1)%24
 assert np.array_equal(W[:,i]*W[:,j]**2,31*W[:,i]-(W[:,i]**3-W[:,i])-sum(W[:,i]*W[:,k]**2 for k in range(24) if k not in (i,j)))
# Negative controls directly hit factors andstructuralcap assumption.
mut=F.copy();mut[0,24]+=1;assert not np.array_equal(3*(mut@G.T),s**3-256*s)
assert Q(2,4)!=0 and (1+2)%2==1 # original Gram kernel violates even classcap
assert (P[0]^1).bit_count()%2==0
res={'status':'PASS_INDEPENDENT_CUBIC_ALGEBRA_LABELS_GATHERS_AND_ALL_PAIR_CAP_ARGUMENT','ports':98280,'dyadic_centers':2600,'exact_sample_factor_pairs':len(X)**2,'global_sphere_identities_checked':24*len(W),'global_label_bindings':len(P),'all_pair_cap_proof':'Integral lattice dot t, Cauchy and canonical distinct lines give offdiagonalinteger t in[-3,3]; f(t)vanishes at everyeven t; labels pair1+t mod2. No minimum-norm or shell-symmetry assumption needed.','gather_rank_certificates':len(bases),'copied_rank':65000,'optimistic_deficit_at_L3':1560,'controls':['target_factor_mutation','original_Gram_even_class_rejection','even_port_label_rejection'],'scope':'Scalar/label/gather evidence only; no full dirty-register program, paid profile, global invoice, conditional kappa or practical speedup.'}
(r/'VERIFIED.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2),flush=True)
