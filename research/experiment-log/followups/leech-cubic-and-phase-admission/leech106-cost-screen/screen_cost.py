"""Exact copied-center and sparse-functional obstruction for both106-port Leech words.
No phase work. Uses frozen finite vectors/labels, not a lattice census.
"""
from pathlib import Path
import json,gzip,math,itertools,hashlib,time
from collections import Counter
import sympy as S
ROOT=Path(__file__).resolve().parent
src=ROOT/'INPUT.json.gz'
if not src.exists():
 original=ROOT.parent/'leech-full-minimal-screen/PUNCTURED-WITNESSES.json.gz'
 src.write_bytes(gzip.compress(json.dumps([w for w in json.load(gzip.open(original))if len(w['vectors'])==106],separators=(',',':')).encode(),mtime=0))
ws=json.load(gzip.open(src))
def binary_basis(xs):
 p={}
 for x in xs:
  while x:
   k=x.bit_length()-1
   if k in p:x^=p[k]
   else:p[k]=x;break
 return list(p.values())
results=[];certs=[];start=time.monotonic()
for w in ws:
 W=S.Matrix(w['vectors']);P=w['labels'];N=W.rows;d=W.cols
 assert(N,d)==(106,24)and W.rank()==24
 assert len(set(P))==106 and all(p.bit_count()%2 for p in P)
 G=W*W.T;assert all(G[i,i]==32 for i in range(N))
 assert all((P[i]&P[j]).bit_count()%2==0 for i in range(N)for j in range(N)if i!=j and G[i,j])
 cr=[len(binary_basis([P[i]for i in range(N)if W[i,k]]))for k in range(d)];assert cr==[24]*24
 available=list(range(N));bases=[];basis_certs=[];minimums=[]
 for bnum in range(4):
  _,piv=W[available,:].T.rref();assert len(piv)==24,('disjoint_basis_failed',w['seed'],bnum,len(piv))
  idx=[available[p]for p in piv];basis=W[idx,:];assert basis.det()!=0
  bases.append(idx);available=[i for i in available if i not in idx]
  inv=basis.inv();M=W*inv;C=inv.copy()
  for j in range(d):
   denom=S.ilcm(*[x.q for x in M[:,j]]);nums=[int(x*denom)for x in M[:,j]];common=math.gcd(*nums);factor=S.Rational(denom,common)
   M[:,j]=M[:,j]*factor;C[:,j]=C[:,j]*factor
  assert all(x.q==1 for x in M)and W*C==M
  rows=[[int(x)for x in row]for row in M.tolist()];pair_records=[]
  for j,k in itertools.combinations(range(d),2):
   patterns=Counter();zero=0
   for row in rows:
    a,b=row[j],row[k]
    if not a and not b:zero+=1;continue
    g=math.gcd(a,b);a//=g;b//=g
    if a<0 or(a==0 and b<0):a,b=-a,-b
    patterns[(a,b)]+=1
   maximum=zero+max(patterns.values());pair_records.append({'pair':[j,k],'minimum_nonzero_ports':N-maximum})
  minimum=min(x['minimum_nonzero_ports']for x in pair_records);minimums.append(minimum)
  basis_certs.append({'basis_indices':idx,'response_matrix':rows,'coefficient_map':[[str(x)for x in row]for row in C.tolist()],'pair_records':pair_records,'minimum_over_two_coordinate_families':minimum})
  print(w['seed'],'basis',bnum,'two_sparse_min',minimum,flush=True)
 assert len(set(sum(bases,[])))==96
 # If total support<=11, four disjoint bases include one with support<=2.
 # The exhaustive pair-family minimum excludes that possibility.
 assert min(minimums)>11
 result={'seed':w['seed'],'ports':N,'scalar_rank':d,'coordinate_gather_ranks':cr,'coordinate_copy_charge':sum(cr),'coordinate_deficit_upper_polynomial':{'L':N-sum(cr),'constant':-N},'disjoint_real_bases':4,'disjoint_basis_rows':96,'two_coordinate_families_checked':4*math.comb(d,2),'per_basis_family_minimum_support':minimums,'proved_every_nonzero_functional_support_at_least':12,'proved_every_nonzero_gather_binary_rank_at_least':5,'all_rowspace_spanning_gather_collections_copy_charge_at_least':d*5,'all_rowspace_deficit_upper_polynomial':{'L':N-d*5,'constant':-N},'status':'PASS_EXACT_ALL_ROWSPACE_COST_OBSTRUCTION','proof':'Suppose a nonzero real functional has at most11nonzero ports. Among4disjoint24-row bases it is nonzero in at most2basis positions for one basis. Its entire response therefore lies in one of276two-coordinate column spans for that basis. Exact projective-ratio counts show every nonzero response in every such family has more than11nonzero ports, contradiction. Every gather consequently supports at least12distinct odd labels. A binary subspace of dimensionr contains at most2^(r-1)odd vectors, so r>=5. Rank24 transfer requires at least24independent gather rows in any spanning collection within this transfer rowspace, costing at least120copied ranks.','scope':'Fixed106-port natural Gram transfer and gathers drawn from its24-dimensional rowspace, separately copied under conventional cover. Arbitrary coefficient recombinations included; outside-rowspace auxiliary gathers and new interfaces excluded.'}
 results.append(result);certs.append({'seed':w['seed'],'bases':basis_certs})
(ROOT/'RESULT.json').write_text(json.dumps({'status':'PASS_BOTH106PORT_ALL_ROWSPACE_OBSTRUCTIONS','seconds':time.monotonic()-start,'results':results},indent=2)+'\n')
(ROOT/'SPARSE-FUNCTIONAL-CERTIFICATES.json.gz').write_bytes(gzip.compress(json.dumps(certs,separators=(',',':')).encode(),mtime=0))
print(json.dumps(results,indent=2))
