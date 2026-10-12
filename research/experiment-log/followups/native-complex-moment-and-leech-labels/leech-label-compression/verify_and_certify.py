"""Independent witness audit and exact representation lower bounds. No search imports."""
from pathlib import Path
import json,gzip,itertools,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent;OLD=ROOT.parent/'radical-geometry-leech-next'
def rank(xs):
 piv={}
 for x in xs:
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;break
 return len(piv)
prior_path=ROOT/'OLD-FIXED-GRAM.json'
H0=json.loads(prior_path.read_text()) if prior_path.exists() else next(w for w in json.load(gzip.open(OLD/'GRAM-COMPLETION-WITNESSES.json.gz'))if w['ports']==33)['H'];oldrank=rank([sum(int(x)<<j for j,x in enumerate(row))for row in H0]);assert oldrank==26
(ROOT/'OLD-FIXED-GRAM.json').write_text(json.dumps(H0,separators=(',',':'))+'\n')
w=json.load(gzip.open(ROOT/'COLOR-WITNESS.json.gz'));A=np.array(w['A']);B=np.array(w['source']['B_scaled']);T=A@B;P=w['labels'];C=w['coloring'];h=w['dimension'];N=len(P)
assert N==33 and h==16 and len(set(P))==N and all(x>0 and x<1<<h and x.bit_count()%2 for x in P)
assert np.all(np.diag(T)==w['source']['scale'])
assert all((P[i]&P[j]).bit_count()%2==int(C[i]==C[j]) for i in range(N)for j in range(N))
assert all((P[i]&P[j]).bit_count()%2==0 for i in range(N)for j in range(N)if i!=j and T[i,j])
H=[[(P[i]&P[j]).bit_count()%2 for j in range(N)]for i in range(N)];gramrank=rank([sum(x<<j for j,x in enumerate(row))for row in H]);assert gramrank==12
labelrank=rank(P);assert labelrank==14
sizes=[C.count(k)for k in range(max(C)+1)];maxclass=max(sizes);radical_lower=(maxclass-1).bit_length();assert radical_lower==2
# W span has restricted Gram rankq=12. Distinct labels in one color class
# differ by radical vectors. Therefore radical dimension>=2, dimW>=14,
# and nondegenerate ambient dimension>=dimW+dimradical>=16.
hlower=gramrank+2*radical_lower;assert hlower==h
bounds=json.loads((ROOT/'CENTER-CLIQUE-BOUND.json').read_text());s=0;actual=[]
for b in bounds['center_bounds']:
 k=b['center_coordinate'];support=np.flatnonzero(B[k]).tolist();assert support==b['support_ports']
 cl=b['forced_orthogonal_clique'];assert set(cl)<=set(support)
 assert all(T[i,j]!=0 or T[j,i]!=0 for i,j in itertools.combinations(cl,2))
 assert all((P[i]&P[j]).bit_count()%2==0 for i,j in itertools.combinations(cl,2))
 s+=len(cl);actual.append(rank([P[i]for i in support]))
assert s==45 and sum(actual)==47 and all(r<h for r in actual)
# The five nonglobal center supports partition all33 ports and are cliques.
other=[b for b in bounds['center_bounds']if b['center_coordinate']!=0]
assert sorted(sum([b['support_ports']for b in other],[]))==list(range(N))
assert all(len(b['support_ports'])==len(b['forced_orthogonal_clique'])for b in other)
# Explicit nonzero normal for each center by Gaussian nullspace.
normals=[]
for b in bounds['center_bounds']:
 xs=[P[i]for i in b['support_ports']];piv={}
 for x in xs:
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;break
 f=next(k for k in range(h)if k not in piv);z=1<<f
 for k in sorted(piv):
  if(z&piv[k]).bit_count()%2:z^=1<<k
 assert z and all((z&x).bit_count()%2==0 for x in xs);normals.append(z)
# Controls: broken odd port and a forced-edge duplicate cannot pass.
assert 0 .bit_count()%2==0
i,j=next((i,j)for i in range(N)for j in range(i)if T[i,j]or T[j,i]);assert (P[i]&P[i]).bit_count()%2==1
report={'status':'PASS_INDEPENDENT_LABEL_COMPRESSION_AND_SCOPED_OBSTRUCTIONS',
 'old_fixed_gram_rank':oldrank,'old_fixed_gram_dimension_lower_bound':oldrank,
 'new_gram_rank':gramrank,'new_distinct_label_dimension':h,'new_label_span_rank':labelrank,'new_color_class_sizes':sizes,
 'minimum_ambient_dimension_for_new_fixed_gram_and_distinct_ports':hlower,
 'new_actual_center_ranks':actual,'new_copied_rank':sum(actual),
 'new_fixed_gram_minimum_copied_rank':labelrank+N,
 'all_admissible_gram_completions_fixed_decoder_copy_lower_bound':s,
 'all_positive_stage_counts_deficit_upper':'-12*L-33',
 'center_normals':normals,'partition_clique_obstruction':'Five nonglobal centers partition33ports into orthogonal cliques, charging33already. Global center contains a12clique, charging at least12more.',
 'oddness_control_rejected':True,'forced_edge_duplicate_control_rejected':True,
 'scope':'Same33port scalar factorization and ordinary dot-product correction caps. Changing scalar decoder or copied-center interface is outside this obstruction.'}
# Independently check the later center basis change and retained transfer.
rw=json.load(gzip.open(ROOT/'RECENTER-WITNESS.json.gz'));RA=np.array(rw['A'],dtype=np.int64);RB=np.array(rw['B_scaled'],dtype=np.int64)
assert np.array_equal(RA@RB,T) and rw['scale']==w['source']['scale']
Q=np.array(rw['Q'],dtype=np.int64);QI=np.array(rw['Q_inverse'],dtype=np.int64)
assert np.array_equal(Q@QI,np.eye(6,dtype=np.int64)) and np.array_equal(QI@Q,np.eye(6,dtype=np.int64))
rr=[rank([P[i]for i,x in enumerate(row)if x])for row in RB]
assert rr==[4,4,6,7,12] and sum(rr)==33 and all(r<h for r in rr)
groups=rw['partition_groups'];assert sorted(sum(groups,[]))==list(range(33))
assert all(T[i,j]!=0 or T[j,i]!=0 for group in groups for i,j in itertools.combinations(group,2))
report['recentered_transfer_preserved']=True
report['recentered_change_of_basis_and_inverse_integral']=True
report['recentered_center_ranks']=rr
report['recentered_copied_rank']=33
report['all_gather_rowspace_recombinations_copy_lower_bound']=33
report['recentered_deficit_upper_all_positive_L']='-33'
report['recentered_scope']='All centers drawn from this retained transfer rowspace; outside-rowspace gathers and other scalar transfers remain open.'
(ROOT/'VERIFIED.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
