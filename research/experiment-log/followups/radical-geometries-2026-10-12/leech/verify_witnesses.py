"""Independent saved-witness checker. Does not import geometry or decoder constructors."""
import json,gzip,hashlib,itertools
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
def read(n):return json.load(gzip.open(ROOT/n))
raw=read('WITNESSES.json.gz');Y=np.array(raw['equiangular_lines_scaled'],dtype=np.int64);c=np.array(raw['norm6_slice_c'])
assert Y.shape==(276,24) and np.all(Y@c==0)
G=Y@Y.T;assert np.all(np.diag(G)==80) and np.all(abs(G[~np.eye(276,dtype=bool)])==16)
assert np.array_equal(G@G,960*G)
assert np.array_equal(Y.T@Y,960*np.eye(24,dtype=np.int64)-20*np.outer(c,c))
Gbad=G.copy();Gbad[0,1]+=1;assert not np.array_equal(Gbad@Gbad,960*Gbad)
for name,o in raw['octad_subsets'].items():
 A=np.array(o['A']);D=np.array(o['128_times_decoder_transpose']);active=np.any(A!=0,axis=0)
 assert np.array_equal(D.T@A,np.diag(128*active))
w=read('DYADIC-DECODER-WITNESS.json.gz');A=np.array(w['A']);B8=np.array(w['eight_B'])
assert np.array_equal(A,Y[:,:23]);assert np.array_equal(B8@A,8*np.eye(23,dtype=np.int64))
Bbad=B8.copy();Bbad[0,0]+=1;assert not np.array_equal(Bbad@A,8*np.eye(23,dtype=np.int64))
Q8=A@B8;assert np.array_equal(Q8@Q8,8*Q8)
x=read('DECODER-CAPS-WITNESS.json.gz');assert np.array_equal(x['Q8'],Q8)
P=x['labels_h36'];assert len(set(P))==276 and all(v.bit_count()%2 for v in P)
assert all((P[i]&P[j]).bit_count()%2==0 for i in range(276) for j in range(i) if Q8[i,j] or Q8[j,i])
p=read('DIAGONAL-TRANSFER-WITNESS.json.gz');T=A@np.array(p['B']);assert np.all(np.diag(T)==1) and np.all(T!=0)
verified=[]
for file,report in [('SPARSE-FUNCTIONALS-WITNESS.json.gz','SPARSE-FUNCTIONALS.json'),('SPARSE-TIE-WITNESS.json.gz','SPARSE-TIE-SEARCH.json')]:
 w=read(file);T=A@np.array(w['B_scaled']);scale=w['scale'];assert scale>0 and scale&(scale-1)==0
 assert np.all(np.diag(T)==scale);assert np.all(np.count_nonzero(T,axis=0)==100)
 r=json.loads((ROOT/report).read_text());cl=w.get('clique',r.get('clique_ports'))
 assert all(T[i,j]!=0 or T[j,i]!=0 for i,j in itertools.combinations(cl,2))
 verified.append({'witness':file,'clique_size':len(cl)})
result={'status':'PASS_INDEPENDENT_INTEGER_WITNESS_CHECKS','geometry_mutant_rejected':True,'decoder_mutant_rejected':True,'sparse_variants':verified,'scope':'Saved finite Gram, decoder and cap-support identities only. No global admission or kappa.'}
(ROOT/'VERIFIED.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
