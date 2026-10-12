"""Exhaustive {-1,0,1} six-center direction catalog plus exact dyadic basis change.
Also certifies a global lower bound for every gather-row recombination of these centers.
"""
from pathlib import Path
import json,gzip,itertools
from collections import Counter
import numpy as np
import sympy as S
ROOT=Path(__file__).resolve().parent
w=json.load(gzip.open(ROOT/'COLOR-WITNESS.json.gz'));A=np.array(w['A']);B=np.array(w['source']['B_scaled']);P=w['labels'];h=w['dimension'];scale=w['source']['scale']
ks=np.flatnonzero(np.any(B!=0,axis=1));A6=A[:,ks];B6=B[ks];assert len(ks)==6
assert np.array_equal(B6[0],-B6[1:].sum(axis=0))
def rank(xs):
 piv={}
 for x in xs:
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;break
 return len(piv)
cat=[]
for c in itertools.product([-1,0,1],repeat=6):
 if not any(c)or next(x for x in c if x)!=1:continue
 row=np.array(c)@B6;support=np.flatnonzero(row).tolist();r=rank([P[i]for i in support])
 cat.append({'coefficients':list(c),'gather_rank':r,'nonzero_ports':len(support)})
assert len(cat)==364
chosen=[];dim=0
for x in sorted(cat,key=lambda x:(x['gather_rank'],sum(abs(c)for c in x['coefficients']),x['coefficients'])):
 candidate=chosen+[x['coefficients']];newdim=S.Matrix(candidate).rank()
 if newdim>dim:chosen=candidate;dim=newdim
 if dim==6:break
Q=S.Matrix(chosen);det=Q.det();inv=Q.inv();assert det!=0
assert all(v.q&(v.q-1)==0 for v in inv)
newA=S.Matrix(A6.tolist())*inv;newB=Q*S.Matrix(B6.tolist());D=S.Matrix(A.tolist())*S.Matrix(B.tolist())
assert newA*newB==D and all(v.q==1 for v in newA)and all(v.q==1 for v in newB)
keep=[k for k in range(6)if any(newB[k,:])];AA=newA[:,keep];BB=newB[keep,:]
assert AA*BB==D;assert D.rank()==5 and len(keep)==5
ranks=[rank([P[i]for i,q in enumerate(BB.row(k))if q])for k in range(len(keep))]
assert sum(ranks)==33 and all(r<h for r in ranks)
# Exact global lower bound: B6 rows1..5 form disjoint group rows; each
# source group is an orthogonal clique forced by the unchanged transfer D.
groups=[np.flatnonzero(row).tolist()for row in B6[1:]];weights=list(map(len,groups))
assert sorted(sum(groups,[]))==list(range(33))
for group in groups:
 assert all(D[i,j]!=0 or D[j,i]!=0 for i,j in itertools.combinations(group,2))
 assert all((P[i]&P[j]).bit_count()%2==0 for i,j in itertools.combinations(group,2))
assert sum(weights)==33
res={'status':'PASS_EXACT_DYADIC_RECENTERING_AND_ALL_RECOMBINATIONS_LOWER_BOUND',
 'original_center_coordinates':ks.tolist(),'exact_gather_relation':'B0+B1+B2+B3+B4+B5=0','catalog_projective_directions':len(cat),
 'catalog_gather_rank_histogram':dict(Counter(x['gather_rank']for x in cat)),
 'selected_change_of_basis':chosen,'determinant':str(det),'inverse_is_dyadic':True,
 'original_nonzero_centers':6,'new_nonzero_centers':len(keep),'scalar_transfer_rank':int(D.rank()),
 'new_center_ranks':ranks,'new_copied_rank':sum(ranks),'label_dimension_unchanged':h,
 'partition_clique_sizes':weights,'global_recombination_copy_lower_bound':33,
 'proof':'Each nonzero linear combination of five disjoint gather rows contains the entire support clique of every group with nonzero coefficient. For any five independent combinations, an invertible5x5 coefficient matrix has a determinant permutation with nonzero entries; the corresponding five gathered frames therefore charge at least the five group sizes in some order. Sum>=33. Any spanning overcomplete collection contains an independent five-row subset and cannot cost less. This bound applies to all coefficients, not only the364catalog directions.',
 'nine_stage_deficit':-33,'all_positive_stage_count_deficit_upper':'-33',
 'scope':'Every gather collection lying in this fixed decoder rowspace, under ordinary separately copied-center accounting. All minimal-rank5center factorizations of the same scalar transfer lie in that rowspace. New scalar transfers, auxiliary gather directions outside the rowspace, or center-copy elimination are not ruled out.'}
(ROOT/'RECENTER-RESULT.json').write_text(json.dumps(res,indent=2)+'\n')
(ROOT/'RECENTER-CATALOG.json.gz').write_bytes(gzip.compress(json.dumps(cat,separators=(',',':')).encode(),mtime=0))
wit={'A':[[str(v)for v in row]for row in AA.tolist()],'B_scaled':[[str(v)for v in row]for row in BB.tolist()],'scale':scale,'labels':P,'dimension':h,'Q':chosen,'Q_inverse':[[str(v)for v in row]for row in inv.tolist()],'partition_groups':groups}
(ROOT/'RECENTER-WITNESS.json.gz').write_bytes(gzip.compress(json.dumps(wit,separators=(',',':')).encode(),mtime=0))
print(json.dumps(res,indent=2))
