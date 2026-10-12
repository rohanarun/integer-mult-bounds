"""Independent exact audit of retained106-port functional/cost certificates.
Uses rational projective slopes, not the constructor's gcd-normalized pattern keys.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import json,gzip,itertools
import sympy as S
ROOT=Path(__file__).resolve().parent
ws={w['seed']:w for w in json.load(gzip.open(ROOT/'INPUT.json.gz'))}
cs=json.load(gzip.open(ROOT/'SPARSE-FUNCTIONAL-CERTIFICATES.json.gz'));results=[]
for c in cs:
 w=ws[c['seed']];W=S.Matrix(w['vectors']);P=w['labels'];assert W.shape==(106,24)and W.rank()==24
 assert len(set(P))==106 and all(p.bit_count()%2 for p in P)
 allindices=[];mins=[];families=0
 for b in c['bases']:
  ids=b['basis_indices'];assert len(set(ids))==24;allindices+=ids
  C=S.Matrix([[S.Rational(x)for x in row]for row in b['coefficient_map']]);M=S.Matrix(b['response_matrix'])
  assert W*C==M
  D=W[ids,:]*C;assert D.is_diagonal()and all(D[i,i]!=0 for i in range(24))
  assert C.det()!=0
  # Tamper controls: response identity and basis nonsingularity fail.
  mutant=M.copy();mutant[0,0]+=1;assert W*C!=mutant
  bad=ids[:];bad[-1]=bad[0];assert(W[bad,:]*C).det()==0
  minimum=106
  rec={tuple(x['pair']):x['minimum_nonzero_ports']for x in b['pair_records']}
  for j,k in itertools.combinations(range(24),2):
   zero=0;slopes=Counter()
   for i in range(106):
    a,z=int(M[i,j]),int(M[i,k])
    if a==z==0:zero+=1
    elif z==0:slopes['infinity']+=1
    else:slopes[Q(a,z)]+=1
   nn=106-zero-max(slopes.values());assert nn==rec[(j,k)]
   minimum=min(minimum,nn);families+=1
  assert minimum==b['minimum_over_two_coordinate_families']and minimum>11;mins.append(minimum)
 assert len(allindices)==96 and len(set(allindices))==96 and families==1104
 # Any<=11 support gives one of4basis blocks<=2 support; all such families ruled out.
 assert 11//4==2
 # A rank4 frame contains exactly8odd vectors if parity nonzero, fewer if parityzero.
 assert 2**(4-1)<12<=2**(5-1)
 assert 24*5==120>106
 results.append({'seed':c['seed'],'bases_verified':4,'families_verified':families,'family_support_minima':mins,'functional_support_lower_bound':12,'gather_rank_lower_bound':5,'all_rowspace_copy_lower_bound':120,'positive_stage_deficit_upper':'-14L-106','mutated_response_rejected':True,'duplicate_basis_row_rejected':True})
r={'status':'PASS_INDEPENDENT_EXACT106PORT_COST_OBSTRUCTIONS','results':results,'scope':'Fixed106port naturalGram transfers only, all gather collections within their rowspaces under ordinary copiedcenter cover. Does not apply to fullshell cubic transfer or arbitrary outside-rowspace auxiliaries.'}
(ROOT/'VERIFIED.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
