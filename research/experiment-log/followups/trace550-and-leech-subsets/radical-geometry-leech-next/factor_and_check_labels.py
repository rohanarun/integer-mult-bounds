"""Exact GF2 Gram factorization and center-gathering checks, independent of rank search.
Nonalternating rankr Gram matrices factor into r ordinary-dot-product coordinates.
"""
from pathlib import Path
import json,gzip
import numpy as np
ROOT=Path(__file__).resolve().parent
base=json.load(gzip.open(ROOT/'SLICE-GRAM-WITNESSES.json.gz'))
Y=np.array(json.load(gzip.open(ROOT/'SOURCE-LINES.json.gz'))['Y'],dtype=np.int64)
wits=json.load(gzip.open(ROOT/'GRAM-COMPLETION-WITNESSES.json.gz'))
def rank(xs):
 piv={}
 for x in xs:
  while x:
   p=x.bit_length()-1
   if p in piv:x^=piv[p]
   else:piv[p]=x;break
 return len(piv)
res=[];out=[]
for w in wits:
 H=np.array(w['H'],dtype=np.int64);rem=H.copy();columns=[];N=len(H)
 while np.any(rem):
  diag=np.flatnonzero(np.diag(rem))
  if len(diag):
   i=int(diag[0]);u=rem[:,i].copy();columns.append(u);rem^=np.outer(u,u)
  else:
   i,j=map(int,np.argwhere(rem)[0]);u=rem[:,i].copy();v=rem[:,j].copy()
   rem^=np.outer(u,v)^np.outer(v,u)
   assert columns
   z=columns.pop();columns.extend([z^u,z^v,z^u^v])
 F=np.array(columns,dtype=np.int64).T;assert np.array_equal((F@F.T)%2,H)
 h=len(columns);assert h==w['best_rank']
 labels=[sum(int(v)<<j for j,v in enumerate(row)) for row in F]
 assert all(x.bit_count()%2 for x in labels)
 b=base[w['source_witness_index']];A=Y[b['ports_original']];B=np.array(b['B_scaled'],dtype=np.int64);T=A@B
 assert np.all(np.diag(T)==b['scale'])
 assert all((labels[i]&labels[j]).bit_count()%2==0 for i in range(N) for j in range(N) if i!=j and T[i,j])
 center_ranks={str(k):rank([labels[i]for i in np.flatnonzero(B[k])])for k in range(24)if np.any(B[k])}
 # Build a nonzero normal to every proper center span by brutefree variable Gaussian backsolve.
 def normal(xs):
  piv={}
  for x in xs:
   while x:
    p=x.bit_length()-1
    if p in piv:x^=piv[p]
    else:piv[p]=x;break
  free=next((i for i in range(h)if i not in piv),None)
  if free is None:return None
  z=1<<free
  for p in sorted(piv):
   if (z&piv[p]).bit_count()%2:z^=1<<p
  assert z and all((z&x).bit_count()%2==0 for x in xs)
  return z
 normals={str(k):normal([labels[i]for i in np.flatnonzero(B[k])])for k in range(24)if np.any(B[k])}
 res.append({'ports':N,'binary_label_dimension':h,'distinct_labels':len(set(labels)),'required_orthogonal_cap_checks_pass':True,'center_gathering_span_ranks':center_ranks,'all_nonzero_centers_admit_proper_hyperplane':all(x is not None for x in normals.values()),'status':('PASS_FINITE_LABEL_AND_CENTER_CAP_SCREEN_NOT_WORD_ADMISSION' if all(x is not None for x in normals.values()) else 'CORRECTION_CAPS_PASS_CENTER_GATHERING_FAIL'),'scope':'Exact binary labels, scalar transfer diagonal and required correction caps. No frame-chain scheduling, dirty helper word, scalar phase or global invoice checked.'})
 out.append({'source_witness_index':w['source_witness_index'],'labels':labels,'dimension':h,'center_normals':normals})
(ROOT/'LABEL-CHECKS.json').write_text(json.dumps(res,indent=2)+'\n')
(ROOT/'LABEL-WITNESSES.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(res,indent=2))
