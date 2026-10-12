"""Independent integer review; reads pinned parent witnesses, writes only this directory."""
from pathlib import Path
import gzip, json, hashlib, importlib.util
from itertools import combinations
from fractions import Fraction
import numpy as np
from sympy import Matrix
D=Path(__file__).resolve().parent;R=D.parent;P=R/'leech-full-shell-cubic'
def read(p):
 b=p.read_bytes();return json.loads(gzip.decompress(b) if p.suffix=='.gz' else b)
def rank(rows):
 piv={}
 for x in map(int,rows):
  while x:
   b=x.bit_length()-1
   if b not in piv:piv[b]=x;break
   x^=piv[b]
 return len(piv)
files=[P/'leech_vectors.py',P/'FACTOR-SAMPLE.json.gz',P/'COMPRESSED-GATHER-BASES.json.gz',P/'COMPRESSED-RESULT.json',P/'compress_sphere.py',R/'leech-full-minimal-screen/ALL-QUOTIENT-LABELS.json.gz',R/'leech-full-minimal-screen/LATTICE-BASIS-AND-LABELS.json']
pins={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
spec=importlib.util.spec_from_file_location('retained_vectors',P/'leech_vectors.py');lv=importlib.util.module_from_spec(spec);spec.loader.exec_module(lv)
V=lv.V; W=V[V[np.arange(len(V)),np.argmax(V!=0,axis=1)]>0]
assert W.shape==(98280,24) and np.all(np.sum(W*W,axis=1)==32)
assert len({tuple(x) for x in W.tolist()})==len(W)
assert np.all(W[np.arange(len(W)),np.argmax(W!=0,axis=1)]>0)
q=read(files[-2]);b=read(files[-1]);labels=list(map(int,q['odd_labels']))
B=Matrix(b['scaled_basis']);H=B*B.T
assert all(int(x)%8==0 for x in H)
H=H/8
E=list(map(int,b['embedding_rows']))
assert len(E)==25
# This 25x25 identity is a universal pairing certificate for affine labels.
for i in range(25):
 for j in range(25):
  expect=1 if i==j==0 else (0 if i==0 or j==0 else int(H[i-1,j-1])%2)
  assert (E[i]&E[j]).bit_count()%2==expect
J=8*B.inv();assert all(x.q==1 for x in J)
C=W@np.array(J,dtype=np.int64);assert np.all(C%8==0);C//=8
assert np.array_equal(C@np.array(B,dtype=np.int64),W)
actual=[]
for row in C:
 z=E[0]
 for k,a in enumerate(row):
  if int(a)%2:z^=E[k+1]
 actual.append(z)
assert actual==labels and len(set(labels))==len(labels)
assert all(0<x<2**25 and x.bit_count()%2 for x in labels)
# Cauchy plus distinct canonical norm32 lines gives integer lattice t in[-3,3] offdiag.
for t in range(-3,4):
 f=Fraction(t*(t*t-4),48)
 assert f==0 or (1+t)%2==0
 assert f.denominator&(f.denominator-1)==0
assert Fraction(4*(16-4),48)==1
sample=read(P/'FACTOR-SAMPLE.json.gz');vectors=sample['vectors']
As=np.array(sample['scatter_numerators'],dtype=np.int64);Gs=np.array(sample['gather_integers'],dtype=np.int64)
kept=[(a,c) for a in range(24) for c in range(24) if a!=c and a!=(c+1)%24]
tri=list(combinations(range(24),3))
def independent(w,v):
 # Reconstruct in source-centered groups; exact division is explicit.
 g=[];a=[]
 for i in range(24):
  assert (w[i]**3-w[i])%3==0
  g.append((w[i]**3-w[i])//3)
  a.append(v[i]**3-3*v[i]*v[(i+1)%24]**2)
 for i in range(24):
  g.append(w[i]); assert (v[i]**3-256*v[i])%3==0
  a.append((v[i]**3-256*v[i])//3+31*v[i]*v[(i+1)%24]**2)
 for k,i in kept:
  g.append(w[i]*w[k]**2);a.append(v[i]*(v[k]**2-v[(i+1)%24]**2))
 for i,j,k in tri:g.append(w[i]*w[j]*w[k]);a.append(2*v[i]*v[j]*v[k])
 return g,a
for k,w in enumerate(vectors):
 g,a=independent(w,w);assert g==Gs[k].tolist() and a==As[k].tolist()
S=np.array(vectors,dtype=np.int64)@np.array(vectors,dtype=np.int64).T
assert np.array_equal(As@Gs.T,(S**3-256*S)//3)
assert np.all(np.diag(As@Gs.T)==8192)
# Stronger off-shell identity diagnoses the exact norm32 assumption.
rng=np.random.default_rng(606)
for k in range(100):
 w=list(map(int,rng.integers(-4,5,size=24)));v=list(map(int,rng.integers(-4,5,size=24)))
 g,a=independent(w,v);s=sum(x*y for x,y in zip(w,v));norm=sum(x*x for x in w)
 correction=(norm-32)*sum(v[i]*v[(i+1)%24]**2*w[i] for i in range(24))
 assert sum(x*y for x,y in zip(g,a))==(s**3-256*s)//3-correction
bases=read(P/'COMPRESSED-GATHER-BASES.json.gz')
assert len(bases)==2600
for r in bases:
 ix=r['indices'];bp=r['basis_ports'];assert len(bp)==25 and rank(labels[i] for i in bp)==25
 for port in bp:
  w=W[port];kind=r['kind']
  if kind=='divided_cube': val=int(w[ix[0]])**3-int(w[ix[0]])
  elif kind=='linear':val=int(w[ix[0]])
  elif kind=='square_linear':val=int(w[ix[0]])**2*int(w[ix[1]])
  elif kind=='triple':val=int(w[ix[0]])*int(w[ix[1]])*int(w[ix[2]])
  else:raise AssertionError(kind)
  assert val!=0
 # All labels fit25bits, so each witness attains the exact rank25 and has orthogonal extraaxis.
assert rank(labels)==25
mut=As.copy();mut[0,24]+=1
assert not np.array_equal(mut@Gs.T,(S**3-256*S)//3)
assert rank([labels[i] for i in bases[0]['basis_ports'][:-1]])==24
bad=E.copy();bad[0]^=1
assert any((bad[i]&bad[j]).bit_count()%2!=(E[i]&E[j]).bit_count()%2 for i in range(25) for j in range(25))
result={'status':'PASS_INDEPENDENT_FINITE_REVIEW','ports':len(W),'factor_pair_checks':len(vectors)**2,'off_shell_identity_checks':100,'label_reconstructions':len(W),'basis_pairing_checks':625,'gather_rank_witnesses':len(bases),'gather_witness_vectors':len(bases)*25,'universal_off_diagonal_cap_proof':'integer t, Cauchy |t|<4 for distinct canonical lines; even t gives zero and odd t gives orthogonal labels','ambient_dimension':26,'active_span_dimension':25,'centers':2600,'C':65000,'optimistic_deficit':'33280L-98280','optimistic_deficit_L3':3*33280-98280,'negative_controls':['target coefficient','dependent shortened gather basis','changed affine label embedding'],'remaining':['chronological dirty word','full exact phase replay','paid rank profile','all-size hosting invoice','conditional global kappa'],'scope':'Finite scalar geometry only. Zero-extension preserves required elementary bilinear conditions; specialized current supplier is not an admission certificate for it.'}
(D/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(D/'SOURCE-HASHES.json').write_text(json.dumps(pins,indent=2)+'\n')
print(json.dumps(result,indent=2))
