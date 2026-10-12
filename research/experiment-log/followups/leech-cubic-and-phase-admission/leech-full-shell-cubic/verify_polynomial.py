"""Exact coefficient proof of the compressed kernel identity modulo sphere norm."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
from collections import defaultdict
import json
r=Path(__file__).resolve().parent
actual=defaultdict(Q)
def prod(vterms,wterms):
 for v,a in vterms:
  for w,b in wterms:actual[(tuple(sorted(v)),tuple(sorted(w)))]+=a*b
for i in range(24):
 j=(i+1)%24;c=(j,j,i)
 prod([((i,i,i),Q(1)),(c,Q(-3))],[((i,i,i),Q(1,3)),((i,),Q(-1,3))])
 prod([((i,i,i),Q(1,3)),((i,),Q(-256,3)),(c,Q(31))],[((i,),Q(1))])
 for k in range(24):
  if k not in (i,j):prod([((k,k,i),Q(1)),(c,Q(-1))],[((k,k,i),Q(1))])
for i,j,k in combinations(range(24),3):prod([((i,j,k),Q(2))],[((i,j,k),Q(1))])
expected=defaultdict(Q)
# Expand (sum vi*wi)^3/3 -256/3*sumviwi by ordered triple enumeration.
for i in range(24):
 expected[((i,),(i,))]-=Q(256,3)
 for j in range(24):
  for k in range(24):m=tuple(sorted((i,j,k)));expected[(m,m)]+=Q(1,3)
# Residual is (32 -sumwk^2)*sum_i v_{i+1}^2*v_i*w_i; vanishesonnorm32.
for i in range(24):
 j=(i+1)%24;c=tuple(sorted((j,j,i)));expected[(c,(i,))]+=32
 for k in range(24):expected[(c,tuple(sorted((i,k,k))))]-=1
actual={k:v for k,v in actual.items() if v};expected={k:v for k,v in expected.items() if v}
assert actual==expected
mut=dict(actual);key=next(iter(mut));mut[key]+=1;assert mut!=expected
result={'status':'PASS_EXACT_POLYNOMIAL_COEFFICIENT_IDENTITY','nonzero_bivariate_monomials':len(actual),'identity':'compressed_numerator = ((v dot w)^3-256(v dot w))/3 +(32-||w||^2)*sum_i(v_{i+1}^2 v_i w_i)','denominator':8192,'on_sphere':'Every source vector has ||w||^2=32, so the second term vanishes identically.','center_count':2600,'control':'single_monomial_coefficient_mutation_rejected'}
(r/'POLYNOMIAL-CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
