"""Exact all-functional support bound for the retained Leech equiangular slice.
A functional must be nonzero on the 23-dimensional line span (not merely in R24).
"""
from pathlib import Path
from fractions import Fraction as Q
import gzip,json
import numpy as np
ROOT=Path(__file__).resolve().parent
raw=json.load(gzip.open(ROOT/'WITNESSES.json.gz'))
Y=np.array(raw['equiangular_lines_scaled'],dtype=np.int64)
G=Y@Y.T
assert Y.shape==(276,24) and np.all(np.diag(G)==80)
assert np.all(abs(G[~np.eye(276,dtype=bool)])==16)
assert np.array_equal(G@G,960*G)
# This identity and trace establish exact rank=276*80/960=23.
dimension=Q(int(np.trace(G)),960);assert dimension==23
hyperplane_dimension=int(dimension)-1
coherence_squared=Q(16,80)**2;assert coherence_squared==Q(1,25)
# For m zero lines, trace(H)=m and trace(H^2)=m+m(m-1)/25.
# PSD Gram eigenvalue Cauchy-Schwarz: m^2 <= rank(H) trace(H^2)
# <=22*m*(m+24)/25. For m>0, (25-22)m <=22*24.
max_zeros=Q(hyperplane_dimension*24,25-hyperplane_dimension)
assert max_zeros==176
assert 176**2==Q(22*176*(176+24),25)
assert 177**2>Q(22*177*(177+24),25)
minimum_support=276-int(max_zeros);assert minimum_support==100
w=json.load(gzip.open(ROOT/'SPARSE-FUNCTIONALS-WITNESS.json.gz'))
A=Y[:,:23];B=np.array(w['B_scaled'],dtype=np.int64);T=A@B
assert np.all(np.diag(T)==w['scale']) and np.all(np.count_nonzero(T,axis=0)==minimum_support)
# One explicit equality case: 176 zero ports form a tight rank22 frame.
zero=np.flatnonzero(T[:,0]==0);assert len(zero)==176
H=G[np.ix_(zero,zero)]
assert np.array_equal(H@H,640*H)
assert Q(int(np.trace(H)),640)==22
result={
 'status':'PASS_EXACT_UNIVERSAL_FUNCTIONAL_SUPPORT_BOUND_AND_ATTAINMENT',
 'configuration':'276 equiangular lines spanning dimension23, squared coherence1/25',
 'functional_scope':'Every real linear functional nonzero on the23-dimensional line span; in particular every decoder column normalized to1 at its target.',
 'zero_set_rank_at_most':22,
 'normalized_zero_set_gram_trace':'m',
 'normalized_zero_set_gram_squared_trace':'m(m+24)/25',
 'inequality':'m^2 <=22*m*(m+24)/25; for m>0 this implies3*m<=528',
 'maximum_zero_ports':176,'minimum_nonzero_ports':100,
 'minimum_offdiagonal_nonzeros_per_diagonal_one_column':99,
 'minimum_total_directed_offdiagonal_corrections':276*99,
 'all276_saved_two_coordinate_columns_attain_bound':True,
 'equality_subset_gram_identity':'H^2=640H for retained raw Gram of176zero ports; exact rank22',
 'equality_subset_ports':zero.tolist(),
 'consequence':'Additional coordinates cannot reduce scalar support below100 for this fixed276-line encoding. They might change support locations and improve binary-label topology.',
 'limits':'Does not prove minimal binary label dimension, full supplier admission, global cost or kappa. Does not apply unchanged to different subsets, projections or encodings.'}
(ROOT/'SUPPORT-BOUND.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='equality_subset_ports'},indent=2))
