"""Exact discovery screens, not supplier admission. No third-party dependencies."""
import itertools,json,time,hashlib
from pathlib import Path
from collections import Counter
from fractions import Fraction
ROOT=Path(__file__).resolve().parent
x=json.loads((ROOT/'INPUT.json').read_text())
def binary_rank(vs):
 b={}
 for z in vs:
  while z:
   k=z.bit_length()-1
   if k in b:z^=b[k]
   else:b[k]=z;break
 return len(b)
def canonical(v):
 z=next(a for a in v if a)
 return tuple(a if z==1 else -a for a in v)
def signed(a):return ((a+1)%3)-1
R={'scope':'Finite discovery identities and literal-lift rejection only; no complete local word, helper count, global admission, or new kappa.','input_sha256':hashlib.sha256((ROOT/'INPUT.json').read_bytes()).hexdigest(),'source_head':x['source_head']}
# Native orthogonal chart formula used by original supplier auditor.
charts=[]
for q in x['ports']:
 u=q^1
 order=list(range(9))
 # q has odd norm and q[0] may vanish. Pick a coordinate i with q_i=1.
 pivot=next(i for i in range(9) if q>>i&1)
 u=q^(1<<pivot)
 order=[pivot]+[i for i in range(9) if i!=pivot]
 # The native transvection sends e_pivot to q when q_pivot=1,
 # but its u_pivot is zero: use paired transvections through a norm-one axis.
 # Instead use literal chart from recipe orthogonal_axes; INPUT supplies it below.
 charts.append(x['native_axes'][len(charts)])
counts={str(p):Counter() for p in (2,3,4)};first={}
for k,B in enumerate(charts):
 for p in (2,3,4):
  mismatches=sum(((a&b).bit_count()%p)!=(i==j) for i,a in enumerate(B) for j,b in enumerate(B))
  counts[str(p)]['charts']+=1;counts[str(p)]['orthogonal']+=mismatches==0
  counts[str(p)]['bad_gram_entries']+=mismatches
  counts[str(p)]['zero_norm_rows']+=sum(a.bit_count()%p==0 for a in B)
  if mismatches and str(p) not in first:first[str(p)]={'port_index':k,'axis_weights':[z.bit_count() for z in B]}
assert counts['2']['orthogonal']==112
R['literal_label_lifts']={'counts':{p:dict(c) for p,c in counts.items()},'first_obstruction':first,'interpretation':'Literal 0/1 chart lift only. A new odd-characteristic reflection construction is tested separately.'}
rank=binary_rank(x['ports']);assert rank==9
# Exhaust all nonnegative excesses above minimum admitted local dimension.
# Nine full-rank 9D calls sharing one direction consume 9*8+1=73 dimensions.
remaining=x['m']-1-x['stages']*(rank-1)
R['nonuniform_fixed_word_stages']={'port_span_rank':rank,'stages':x['stages'],'ambient':x['m'],'remaining_dimensions':remaining,'admissible_dimension_allocations':[[rank]*x['stages']] if remaining==0 else [],'scope':'In the current shared-axis, disjoint-complement stage construction every invocation contains the whole rank-nine port set; variable h_j>=9 with sum(h_j-1)=72 forces all h_j=9. Does not rule out new overlapping stage geometry or new local words.'}
# New ternary reflection geometry: projectivized norm-one vectors, q(v)=sum v_i^2 mod3.
trials=[]
for d in range(3,9):
 started=time.time();V=[v for v in itertools.product((-1,0,1),repeat=d) if sum(a*a for a in v)%3==1 and next((a for a in v if a),0)==1];S=set(V)
 shell=Counter(sum(a*a for a in v) for v in V)
 # Exact rational normalized Euclidean tight-frame identity, an auxiliary identity only.
 G=[[sum(Fraction(v[i]*v[j],sum(a*a for a in v)) for v in V) for j in range(d)] for i in range(d)]
 tight=all(G[i][j]==(Fraction(len(V),d) if i==j else 0) for i in range(d) for j in range(d));assert tight
 # Reflection r_v(w)=w+<v,w>v over F3 preserves q, involutive, and the full projective port set.
 tested=0;orthogonal_degrees=[]
 for v in V:
  degree=0
  for w in V:
   dot=sum(a*b for a,b in zip(v,w))%3
   degree+=dot==0
   z=tuple(signed(b+dot*a) for a,b in zip(v,w))
   assert canonical(z) in S
   dot2=sum(a*b for a,b in zip(v,z))%3
   assert tuple(signed(b+dot2*a) for a,b in zip(v,z))==w
   tested+=1
  orthogonal_degrees.append(degree)
 trials.append({'dimension':d,'ports':len(V),'norm_shells':dict(shell),'orthogonal_degree_histogram':dict(Counter(orthogonal_degrees)),'exact_reflection_pairs_tested':tested,'projective_closure':True,'involution':True,'normalized_real_tight_frame':True,'tight_frame_coefficient':str(Fraction(len(V),d)),'seconds':time.time()-started})
 print(json.dumps(trials[-1]),flush=True)
R['ternary_geometry_trials']=trials
R['missing_for_kappa']=['Design the scalar local transform and decoder on these ports with arbitrary dirty helpers.','Specify monotone ternary frames, phase conventions, residual maps, and exact scalar cleanup.','Derive a valid odd-characteristic global cover/compiler and child cost recurrence; binary price cannot be reused.','Count physical registers, paid child ranks, deficit, coefficient/tape invoices and bootstrap/outer inequalities.']
(ROOT/'RESULT.json').write_text(json.dumps(R,indent=2)+'\n')
print('PASS_ALL_FINITE_DISCOVERY_CHECKS',flush=True)
