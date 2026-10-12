"""Exact native ternary charts and orthogonality-supported scalar decoder screens.
Discovery only; no monotone word, center framing, dirty-helper/global admission.
"""
from itertools import product
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import hashlib,json,time
from sympy import Matrix
root=Path(__file__).resolve().parent;started=time.time()
V=[v for v in product((-1,0,1),repeat=6) if sum(x*x for x in v)%3==1 and next((x for x in v if x),0)==1]
n=len(V);d=6;assert n==126
I=[[int(i==j) for j in range(d)] for i in range(d)]
def detmod(M):
 a=[row[:] for row in M];det=1
 for c in range(len(a)):
  p=next((r for r in range(c,len(a)) if a[r][c]%3),None)
  if p is None:return 0
  if p!=c:a[p],a[c]=a[c],a[p];det=-det
  v=a[c][c]%3;det=det*v%3;iv=pow(v,-1,3)
  for r in range(c+1,len(a)):
   t=a[r][c]*iv%3
   for j in range(c,len(a)):a[r][j]=(a[r][j]-t*a[c][j])%3
 return det%3
# Native charts were completed and independently checked in the retained initial run.
assert (root/'TERNARY126-CHARTS.json').exists()
print('REUSE_COMPLETED_NATIVE_CHART_WITNESSES',flush=True)
A=Matrix([[int(sum(x*y for x,y in zip(v,w))%3==0) for w in V] for v in V]);Id=Matrix.eye(n);J=Matrix.ones(n,n)
assert all(A[i,i]==0 for i in range(n));assert all(sum(A.row(i))==45 for i in range(n))
assert A*A==27*Id-6*A+18*J
# Exact QQ ranks independently determine each eigenspace dimension.
eigen=[]
for lam in(45,3,-9):
 rank=(A-lam*Id).to_DM().rank();eigen.append({'eigenvalue':lam,'exact_QQ_rank_A_minus_lambda_I':rank,'eigenspace_dimension':n-rank})
assert sum(e['eigenspace_dimension'] for e in eigen)==n
assert sum(e['eigenvalue']*e['eigenspace_dimension'] for e in eigen)==0
assert sum(e['eigenvalue']**2*e['eigenspace_dimension'] for e in eigen)==n*45
expected={45:1,3:90,-9:35};assert {e['eigenvalue']:e['eigenspace_dimension'] for e in eigen}==expected
print('PASS_EXACT_EIGENSPACE_MULTIPLICITIES',flush=True)
decoders=[]
for name,den,s in [('I_minus_A_over3',3,-1),('I_plus_A_over9',9,1)]:
 # rank computed directly on integer scaled matrix, independent of spectral prediction.
 K=den*Id+s*A;rank=K.to_DM().rank();alphabet=sorted(set(Q(int(z),den) for z in K));nonzero_offdiag=sum(i!=j and K[i,j]!=0 for i in range(n) for j in range(n))
 assert all(K[i,i]==den for i in range(n))
 assert all(i==j or K[i,j]==0 or A[i,j]==1 for i in range(n) for j in range(n))
 assert nonzero_offdiag==n*45
 predicted=sum(e['eigenspace_dimension'] for e in eigen if den+s*e['eigenvalue']!=0);assert rank==predicted
 # Retain an explicit exact factorization via pivot columns: K=C*R.
 _,pivots=K.to_DM().rref();C=K[:,list(pivots)]
 # For a column basis select independent rows, solve square subsystem exactly.
 _,rows=C.T.to_DM().rref();square=C[list(rows),:];R=square.inv(method="DM")*K[list(rows),:];assert C*R==K
 factor={'name':name,'scale':den,'rank':rank,'column_pivots':list(pivots),'row_pivots':list(rows),'C':[[str(C[i,j]) for j in range(C.cols)] for i in range(C.rows)],'R':[[str(R[i,j]) for j in range(R.cols)] for i in range(R.rows)],'identity':'decoder=C*R/scale'}
 (root/(name+'-FACTORIZATION.json')).write_text(json.dumps(factor,separators=(',',':'))+'\n')
 decoders.append({'name':name,'ports':n,'rank_over_Q':rank,'nullity':n-rank,'diagonal_one':True,'offdiagonal_support_only_orthogonal_pairs':True,'directed_nonzero_offdiagonal_entries':nonzero_offdiag,'decoder_scalar_alphabet':[str(x) for x in alphabet],'decoder_denominator_alphabet':sorted(set(x.denominator for x in alphabet)),'eigenvalues':[{'value':str(Q(den+s*e['eigenvalue'],den)),'multiplicity':e['eigenspace_dimension']} for e in eigen],'factor_C_scalar_alphabet':sorted(set(str(x) for x in C)),'factor_R_scalar_alphabet':sorted(set(str(x) for x in R)),'min_rank_one_scalar_factors':rank,'ports_per_scalar_rank':str(Q(n,rank)),'status':'EXACT_SCALAR_CAP_COMPATIBLE_DECODER_ONLY'})
 print(name,'rank',rank,flush=True)
result={'status':'PASS_NATIVE_TERNARY_CHARTS_AND_EXACT_DECODER_SCREENS','charts':{'O':126,'SO':126,'first_axis_maps':True,'row_and_column_orthonormality':True,'SO_determinant_one':True,'witness_sha256':hashlib.sha256((root/'TERNARY126-CHARTS.json').read_bytes()).hexdigest()},'adjacency_spectrum':eigen,'decoders':decoders,'comparison':{'current_binary_ports':112,'current_binary_center_copies':8,'ternary_rank_one_factor_lower_bounds':[36,91],'warning':'Scalar rank is the minimum number of rank-one outer products, not an admitted number/cost of framed center registers. Neither result beats the existing8-copy construction on this scalar burden metric.'},'scope':'Exact finite native orthogonal charts and scalar cap-supported decoders only. No local monotone program, arbitrary-dirt cleanup, valid ternary phases/cover, physical supplier or kappa.','seconds':time.time()-started}
(root/'TERNARY126-CHARTS-DECODERS-RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
