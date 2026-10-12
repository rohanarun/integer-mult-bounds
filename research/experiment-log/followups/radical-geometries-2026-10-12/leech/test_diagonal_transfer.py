"""Test actual diagonal-one dyadic transfer constructions on Leech ETF, exact finite matrices."""
import json,gzip,itertools
from pathlib import Path
from collections import Counter
import numpy as np
from fractions import Fraction
ROOT=Path(__file__).resolve().parent
w=json.load(gzip.open(ROOT/'DYADIC-DECODER-WITNESS.json.gz'));A=np.array(w['A'],dtype=np.int64)
# Greedy one-coordinate functional per target. Every row has a +-1 coordinate.
B=np.zeros((23,276),dtype=np.int64);piv=[]
for i,row in enumerate(A):
 j=int(np.flatnonzero(np.abs(row)==1)[0]);B[j,i]=row[j];piv.append(j)
T=A@B
assert np.array_equal(np.diag(T),np.ones(276,dtype=np.int64))
assert np.all(T!=0) # A has all odd entries; a single coordinate never vanishes.
# Any orthogonal-cap implementation of this transfer needs 276 independent odd labels.
# Exact elementary fact: P P^T=I_276 implies rank(P)>=276 overF2.
# Natural full-symmetry diagonal-one low-rank filters are aI+bG.
# G has eigenvalues0,960 and diag80. Rank23 branch: a=0,b=1/80.
# Rank253 branch: a+960b=0 and a+80b=1.
res={'status':'PASS_DIAGONAL_ONE_DYADIC_TRANSFER_REJECTED_AT_NATIVE_LABEL_BUDGET',
 'coordinate_pivot_transfer':{'shape':[276,276],'diagonal_one':True,'integer_coefficients':True,
 'latent_coordinates_used':len(set(piv)),'B_nonzeros':276,'A_nonzeros':int(np.count_nonzero(A)),
 'directed_offdiagonal_corrections':276*275,'undirected_cap_constraints':276*275//2,
 'forced_binary_label_dimension_minimum':276,
 'reason':'Every offdiagonal transfer entry is nonzero, forcing p_i dot p_j=0 for all i!=j. Each source port must have odd self product, so labels are independent.'},
 'symmetry_algebra_filters':{'form':'a I+b G, where G^2=960G and diagonal(G)=80',
 'rank23_diagonal_one':{'a':'0','b':'1/80','dyadic':False},
 'rank253_diagonal_one':{'a':'12/11','b':'-1/880','dyadic':False},
 'scope':'Exact obstruction only to nontrivial rank-deficient diagonal-one filters in the two-dimensional Gram algebra.'},
 'remaining_escape':'A nonuniform multi-coordinate dyadic decoder could create enough exact offdiagonal zeros; no general impossibility is proved.',
 'not_done':['native frame chains and gathering caps','phase compiler','paid profile','hosting','moment and outer pricing']}
(ROOT/'DIAGONAL-TRANSFER.json').write_text(json.dumps(res,indent=2)+'\n')
(ROOT/'DIAGONAL-TRANSFER-WITNESS.json.gz').write_bytes(gzip.compress(json.dumps({'B':B.tolist(),'pivot_coordinates':piv},separators=(',',':')).encode(),mtime=0))
print(json.dumps(res,indent=2))
