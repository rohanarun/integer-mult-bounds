"""Exact prerequisite audit for applying the existing E7 dirty-word factory to Leech.
No chronological word is claimed: the copied-center deficit already has wrong sign.
"""
from pathlib import Path
import json,gzip,hashlib
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'SOURCE-WITNESSES.json.gz'
if not SRC.exists(): SRC=ROOT.parent/'radical-geometry-leech-next/SPLIT-CENTERS-WITNESSES.json.gz'
raw=SRC.read_bytes();witnesses=json.loads(gzip.decompress(raw))
def basis(xs):
 p={}
 for x in xs:
  for k in sorted(p,reverse=True):
   if x>>k&1:x^=p[k]
  if x:
   k=x.bit_length()-1
   for j in p:
    if p[j]>>k&1:p[j]^=x
   p[k]=x
 return [p[k] for k in sorted(p,reverse=True)]
results=[];certs=[]
for w in witnesses:
 N=w['ports'];h=w['dimension'];labels=w['labels'];centers=[]
 assert len(labels)==N and len(set(labels))==N
 assert all(0<p<1<<h and p.bit_count()%2 for p in labels)
 for k,(row,norm)in enumerate(zip(w['B_scaled'],w['center_normals'])):
  indices=[i for i,q in enumerate(row)if q];bs=basis([labels[i] for i in indices])
  assert bs and len(bs)<h
  assert all((p&norm).bit_count()%2==0 for p in bs)
  # Independent rank calculation via exhaustive coordinate-column elimination.
  matrix=[[(labels[i]>>j)&1 for j in range(h)]for i in indices];r=0
  for col in range(h):
   pivot=next((i for i in range(r,len(matrix))if matrix[i][col]),None)
   if pivot is None:continue
   matrix[r],matrix[pivot]=matrix[pivot],matrix[r]
   for i in range(len(matrix)):
    if i!=r and matrix[i][col]:matrix[i]=[a^b for a,b in zip(matrix[i],matrix[r])]
   r+=1
  assert r==len(bs)
  centers.append({'center':k,'support_ports':indices,'source_label_basis':bs,'forced_minimum_gather_rank':r,'proper_hyperplane_normal':norm})
 ranks=[c['forced_minimum_gather_rank']for c in centers];cop=sum(ranks);slope=N-cop
 assert slope<0
 # delta(L)=(L-1)N-L*cop=L*(N-cop)-N, negative for all real L>0.
 assert slope-N<0
 d9=8*N-9*cop
 minhelpers=len(centers);factory_deliveries=sum(len(c['support_ports'])for c in centers)
 # Same telescoping local rank-mass identity as the inspected E7 factory.
 mass_lower=2*N*(h-1)+h*minhelpers+cop
 dedicated_mass=2*N*(h-1)+h*(minhelpers+factory_deliveries)+cop
 result={'ports':N,'binary_dimension':h,'center_count':minhelpers,'minimum_center_rank_list':ranks,'minimum_total_copied_rank':cop,'deficit_polynomial':{'coefficient_of_L':slope,'constant':-N},'all_positive_L_deficit_strictly_negative':True,'nine_stage_deficit':d9,'local_rank_mass_lower_bound_ignoring_delivery_helpers':mass_lower,'dedicated_factory_delivery_clones_before_corrections':factory_deliveries,'dedicated_factory_rank_mass_before_correction_clones':dedicated_mass,'largest_integer_copy_charge_for_positive_deficit_at_some_stage':N-1,'largest_integer_copy_charge_for_positive_deficit_at_L9':(8*N-1)//9,'status':'REJECT_THIS_CENTER_FACTORIZATION_IN_EXISTING_COPIED_CENTER_COVER'}
 results.append(result);certs.append({'ports':N,'labels':labels,'centers':centers})
report={'status':'PASS_EXACT_PREBUILD_STRUCTURAL_OBSTRUCTION','source_sha256':hashlib.sha256(raw).hexdigest(),'results':results,'proof':'Gathering scalar center k requires a frame containing all source labels with nonzero decoder coefficient. Its rank is at least their exact GF2 span rank. Ordinary copied-center delivery charges at least this rank. In the existing uniform odd-stage cover, deficit=(L-1)V-L*sum(center_ranks). Each retained factorization has sum(center_ranks)>V, making deficit negative for every positive L. All other costs were optimistically set to zero.','scope':'Rejects saved33/52/80port factorizations under the existing E7 factory and copied-center cover. Does not reject other Leech decoders, shared packet words, center-copy elimination or a new supplier interface.','not_executed_due_to_obstruction':['chronological dirty-register word','full scalar endpoint and helper restoration','full monotone frame profile','phase compiler','global hosting or kappa calculation']}
(ROOT/'SOURCE-WITNESSES.json.gz').write_bytes(raw)
(ROOT/'OBSTRUCTION.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'RANK-CERTIFICATES.json').write_text(json.dumps(certs,indent=2)+'\n')
print(json.dumps(report,indent=2))
