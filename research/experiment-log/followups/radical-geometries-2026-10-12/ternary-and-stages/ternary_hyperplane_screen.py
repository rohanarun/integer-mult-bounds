"""Exhaustive proper-frame necessary test for minimum-rank ternary decoder factors."""
from pathlib import Path
from itertools import product
from collections import Counter
import json,hashlib,time
import numpy as np
from sympy import Matrix
root=Path(__file__).resolve().parent;started=time.time();p=1000003
V=[v for v in product((-1,0,1),repeat=6) if sum(x*x for x in v)%3==1 and next((x for x in v if x),0)==1]
normals=[v for v in product((-1,0,1),repeat=6) if next((x for x in v if x),0)==1];assert len(normals)==364
factor=json.loads((root/'I_minus_A_over3-FACTORIZATION.json').read_text());C=np.array([[int(x) for x in row] for row in factor['C']],dtype=np.int64);assert C.shape==(126,36)
def modrank(a,ids):
 a=a.copy()%p;ids=list(ids);r=0;chosen=[];det=1
 for col in range(a.shape[1]):
  poss=np.flatnonzero(a[r:,col])
  if len(poss)==0:continue
  i=r+int(poss[0]);a[[r,i]]=a[[i,r]];ids[r],ids[i]=ids[i],ids[r]
  z=int(a[r,col]);det=det*z%p;chosen.append(ids[r]);a[r,col:]=a[r,col:]*pow(z,-1,p)%p
  if r+1<len(a):a[r+1:,col:]=(a[r+1:,col:]-a[r+1:,col,None]*a[r,col:])%p
  r+=1
  if r==a.shape[1] or r==len(a):break
 return r,chosen
records=[];survivors=[]
for i,q in enumerate(normals):
 inside=[j for j,v in enumerate(V) if sum(a*b for a,b in zip(q,v))%3==0];outside=[j for j in range(126) if j not in inside]
 rank,pivots=modrank(C[outside],outside);rec={'normal':q,'normal_norm_mod3':sum(x*x for x in q)%3,'inside_ports':len(inside),'outside_rows':len(outside),'rank_mod_prime':rank,'pivot_original_rows':pivots}
 if rank<36:
  null=Matrix(C[outside].tolist()).nullspace();rec['exact_QQ_rank']=36-len(null);rec['exact_directions']=len(null)
  if null:
   M=Matrix(C.tolist());directions=[]
   for b in null:
    w=M*b;assert all(w[j]==0 for j in outside);assert any(w)
    directions.append({'coefficients':[str(x) for x in b],'port_values':[str(x) for x in w]})
   survivors.append({'normal':q,'directions':directions})
 else:rec['exact_QQ_rank']=36;rec['exact_directions']=0
 records.append(rec)
(root/'TERNARY126-HYPERPLANE-WITNESSES.json').write_text(json.dumps({'prime':p,'factor_sha256':hashlib.sha256((root/'I_minus_A_over3-FACTORIZATION.json').read_bytes()).hexdigest(),'records':records,'survivors':survivors},separators=(',',':'))+'\n')
# Independently verify each claimed modular obstruction from its36x36 actual original-row minor.
# Fraction-free integer determinant via DomainMatrix is exact; it is a different arithmetic path.
minorchecks=0
for rec in records:
 if rec['rank_mod_prime']==36:
  det=int(Matrix(C[rec['pivot_original_rows']].tolist()).det(method='domain-ge'))
  assert det%p!=0;minorchecks+=1
r={'status':'COMPLETE_EXHAUSTIVE_TERNARY_HYPERPLANE_CENTER_SCREEN','projective_hyperplanes':364,'decoder_rank':36,'modular_prime':p,'independent_exact_integer_minor_checks':minorchecks,'inside_port_histogram':dict(Counter(x['inside_ports'] for x in records)),'rank_mod_prime_histogram':dict(Counter(x['rank_mod_prime'] for x in records)),'exact_direction_count_histogram':dict(Counter(x['exact_directions'] for x in records)),'surviving_hyperplanes':len(survivors),'interpretation':'A full-column-rank restriction outside a hyperplane proves no nonzero rational decoder column-space vector is supported inside it. All proper ternary frames lie inside some enumerated hyperplane. If all fail, a minimum-rank36 outer-product factorization cannot gather every center in a proper ternary frame. This does not exclude overcomplete factorizations with cancellations outside the decoder column space, a changed decoder, or other phase/label representations.','scope':'Necessary obstruction for minimal scalar decoder factors, not universal theorem against ternary geometry.','seconds':time.time()-started}
(root/'TERNARY126-HYPERPLANE-RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
