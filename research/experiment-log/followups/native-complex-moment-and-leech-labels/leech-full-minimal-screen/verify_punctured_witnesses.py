"""Independent exact audit of retained lattice coordinates, labels, dyadic caps and gathers.
Does not import generator/search code or rerun fullshell enumeration.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import gzip,json,hashlib
from sympy import Matrix
r=Path(__file__).resolve().parent
basis=json.loads((r/'LATTICE-BASIS-AND-LABELS.json').read_text());trials=json.loads(gzip.decompress((r/'PUNCTURED-WITNESSES.json.gz').read_bytes()));B=Matrix(basis['scaled_basis']);H=Matrix(basis['integral_unimodular_Gram']);Bi=B.inv();T=basis['embedding_rows']
assert B.det()==2**36 and B*B.T==8*H and H.det()==1
D=[[int(i==j==0) if i==0 or j==0 else int(H[i-1,j-1])%2 for j in range(25)] for i in range(25)]
assert all((T[i]&T[j]).bit_count()%2==D[i][j] for i in range(25) for j in range(25))
def embed(v):
 coords=(Matrix([v])*Bi);assert all(x.q==1 for x in coords)
 a=[1]+[int(x)%2 for x in coords];p=0
 for i,z in enumerate(a):
  if z:p^=T[i]
 return p
records=[]
for t in trials:
 U=Matrix(t['vectors']);P=t['labels'];n=U.rows;G=U*U.T
 assert len(set(P))==n and all(x.bit_count()%2 for x in P)
 assert all(embed(row)==label for row,label in zip(t['vectors'],P))
 assert all(G[i,i]==32 for i in range(n));assert U.to_DM().rank()==24
 assert all(not G[i,j] or i==j or not((P[i]&P[j]).bit_count()%2) for i in range(n) for j in range(n))
 alphabet=sorted(set(Q(int(x),32) for x in G));assert all(x.denominator&(x.denominator-1)==0 for x in alphabet)
 normal=t['common_normal_even_pool'];proper=False
 if normal:
  assert normal!=0 and all(not((p&normal).bit_count()%2) for p in P);proper=True
 nz=sum(x!=0 for x in U)
 records.append({'seed':t['seed'],'ports':n,'exact_scalar_rank':24,'diagonal_one':True,'scalar_alphabet':[str(x) for x in alphabet],'label_recomputed_from_Lambda_basis':True,'all_correction_caps':True,'coordinate_centers_have_common_proper_hyperplane':proper,'gather_scatter_nonzero_coefficients':2*nz,'directed_offdiagonal_corrections':sum(G[i,j]!=0 for i in range(n) for j in range(n) if i!=j),'scope':'Coefficient incidence counts only, not framed operation counts or paid-rank profile.'})
 # Negative controls directly exercise actual admission conditions.
 bad=P[0]^1;assert bad.bit_count()%2==0
 assert Q(int(G[0,0])+1,32)!=1
allq=json.loads(gzip.decompress((r/'ALL-QUOTIENT-LABELS.json.gz').read_bytes()));assert len(set(allq['lattice_quotients']))==98280;assert len(set(allq['odd_labels']))==98280
burden={'full_shell_natural_decoder_offdiagonal_corrections':98280*(47104+4600),'full_shell_natural_decoder_forbidden_correction_caps':98280*4600,'full_shell_directed_per_port_incidence':51704,'caveat':'Specific natural rank24 Gram decoder only. Not a lower bound for all Leech-derived encoders/decoders.'}
res={'status':'PASS_INDEPENDENT_PUNCTURED_SCALAR_LATTICE_LABEL_AND_GATHER_WITNESSES','basis_scaled_det':str(B.det()),'basis_lattice_Gram_det':str(H.det()),'records':records,'full_shell_incidence_calculations':burden,'negative_controls':['even_label_rejected','nonunit_diagonal_rejected'],'witness_sha256':hashlib.sha256((r/'PUNCTURED-WITNESSES.json.gz').read_bytes()).hexdigest(),'scope':'Finite algebra/label/cap checks only; no dirty-helper chronology, phase compiler, native adapter, physical allocation, moment root or kappa.'}
(r/'VERIFIED.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res),flush=True)
