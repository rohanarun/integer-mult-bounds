"""Remove24 dyadic centers using unit-coefficient norm32 identities."""
from pathlib import Path
from itertools import combinations
import json,gzip,hashlib
import numpy as np
import leech_vectors as lv
r=Path(__file__).resolve().parent
V=lv.V;W=V[V[np.arange(len(V)),np.argmax(V!=0,axis=1)]>0]
pairs=[(i,j) for i in range(24) for j in range(24) if i!=j]
triples=list(combinations(range(24),3));removed={((i+1)%24,i) for i in range(24)}
kept=[x for x in pairs if x not in removed]
def source(w):return [(int(x)**3-int(x))//3 for x in w]+list(map(int,w))+[int(w[i]**2*w[j]) for i,j in kept]+[int(w[i]*w[j]*w[k]) for i,j,k in triples]
def target(v):
 c=[int(v[(i+1)%24]**2*v[i]) for i in range(24)]
 return [int(v[i]**3)-3*c[i] for i in range(24)]+[(int(v[i])**3-256*int(v[i]))//3+31*c[i] for i in range(24)]+[int(v[i]**2*v[j])-c[j] for i,j in kept]+[int(2*v[i]*v[j]*v[k]) for i,j,k in triples]
idx=sorted(set([0,132,32890]+np.random.default_rng(564).choice(len(W),125,replace=False).tolist()))
A=np.array([target(W[i]) for i in idx],dtype=np.int64);G=np.array([source(W[i]) for i in idx],dtype=np.int64)
assert A.shape[1]==G.shape[1]==2600
S=W[idx]@W[idx].T;expected=(S**3-256*S)//3
assert np.array_equal(A@G.T,expected)
# Exhaustively verify every integer sphere-elimination identity on all98280sourcevectors.
for i in range(24):
 j=(i+1)%24
 lhs=W[:,j]**2*W[:,i]
 rhs=31*W[:,i]-(W[:,i]**3-W[:,i])-sum(W[:,k]**2*W[:,i] for k in range(24) if k not in (i,j))
 assert np.array_equal(lhs,rhs)
mut=A.copy();mut[0,24]+=1;assert not np.array_equal(mut@G.T,expected)
allbases=json.loads(gzip.decompress((r/'GATHER-BASES.json.gz').read_bytes()))
bases=[x for x in allbases if x['kind']!='square_linear' or tuple(x['indices']) not in removed]
assert len(bases)==2600 and all(x['rank']==25 for x in bases)
(r/'COMPRESSED-GATHER-BASES.json.gz').write_bytes(gzip.compress(json.dumps(bases).encode(),mtime=0))
res={'status':'PASS_2600_DYADIC_CENTER_SPHERE_COMPRESSION','identity':'w_i*w_j^2 = 31*w_i -3*((w_i^3-w_i)/3) -sum_{k != i,j} w_i*w_k^2; j=(i+1)mod24; sum(w_k^2)=32','removed_centers':24,'remaining_centers':2600,'sphere_identity_checks':98280*24,'exact_factor_pair_checks':len(idx)**2,'denominator':8192,'all_gather_ranks':25,'copied_rank_C':65000,'ports':98280,'optimistic_deficit_formula':'33280*L-98280','optimistic_first_positive_L':3,'deficit_at_L3':1560,'scope':'Exact dyadic scalar factorization and proper gather spans only. Positive optimistic copied-center deficit is a necessary screen, not a paid circuit, new kappa or performance claim.','negative_controls':['changed_target_linear_coefficient_rejected']}
(r/'COMPRESSED-RESULT.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2),flush=True)
# Reusable finite sampled matrices for an independent verifier, never a98k squaredmatrix.
(r/'FACTOR-SAMPLE.json.gz').write_bytes(gzip.compress(json.dumps({'vectors':W[idx].tolist(),'scatter_numerators':A.tolist(),'gather_integers':G.tolist(),'denominator':8192}).encode(),mtime=0))
