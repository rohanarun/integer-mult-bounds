"""Exact dyadic decoder factorizations from legal center directions."""
import itertools,json,random,math
from pathlib import Path
from collections import Counter
import sympy as s
O=Path(__file__).resolve().parent
res=[]
for name in ['E6','E7','D4','D6','D8','A4','A6','A8','CURRENT112']:
 w=json.loads((O/(name+'-CENTER-SCREEN.json')).read_text());vectors=[];normals=[]
 for z in w['directions']:
  for v in z['directions']:
   a=[s.Rational(x) for x in v];den=s.ilcm(*[x.q for x in a]);a=[int(x*den) for x in a];g=math.gcd(*a);a=tuple(x//g for x in a)
   if a not in vectors:vectors.append(a);normals.append(z['normal'])
 if name=='CURRENT112':
  import gzip
  q=json.load(gzip.open(O.parent/'pr548-complex314/complex-local/syndrome/FULL-WORD.json.gz'));R=s.Matrix(q['root_lines']);denom=4
 else:q=json.loads((O/(name+'-WITNESS.json')).read_text());R=s.Matrix(q['roots_scaled_by_2']);denom=8
 cols=R.rref()[1];X=R[:,cols];d=X.cols;M=s.Matrix(vectors);gram=R*R.T/denom
 def dyadic(x):return x.q&(x.q-1)==0
 trials=[];seed=random.Random(547548)
 if len(vectors)>=d:
  combos=list(itertools.islice(itertools.combinations(range(len(vectors)),d),300))
  combos.extend(tuple(sorted(seed.sample(range(len(vectors)),d))) for _ in range(300))
 else:combos=[]
 win=None;hist=Counter()
 for c in dict.fromkeys(combos):
  U=s.Matrix([vectors[i] for i in c]).T
  if not U.det():hist['dependent']+=1;continue
  collect=X*U
  selected=collect.T.rref()[1];Cs=collect[list(selected),:]
  scatter=gram[:,list(selected)]*Cs.T.inv()
  assert scatter*collect.T==gram
  if all(dyadic(x) for x in scatter):
   hist['dyadic']+=1
   win={'directions_indices':c,'center_normals':[normals[i] for i in c],'collect':[[str(x) for x in row] for row in collect.tolist()],'scatter':[[str(x) for x in row] for row in scatter.tolist()],'all_coefficients_dyadic':True};break
  hist['odd_denominator']+=1
 r={'geometry':name,'distinct_legal_directions':len(vectors),'attempts':sum(hist.values()),'outcomes':dict(hist),'dyadic_basis_found':win is not None,'scope':'Clean Gram factorization and legal collection supports only, not phase/frame/circuit/global admission.'};res.append(r)
 if win:(O/(name+'-DECODER.json')).write_text(json.dumps(win,indent=2)+'\n')
 print(json.dumps(r),flush=True)
(O/'DECODER-RESULT.json').write_text(json.dumps(res,indent=2)+'\n')
