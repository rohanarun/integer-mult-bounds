import json,gzip,itertools,math
from pathlib import Path
import sympy as s
O=Path(__file__).resolve().parent

def f2rank(xs):
 p={}
 for x in xs:
  while x:
   k=x.bit_length()-1
   if k in p:x^=p[k]
   else:p[k]=x;break
 return len(p)
results=[]
for name in ['E6','E7','D4','D5','D6','D8','A4','A6','A8','CURRENT112']:
 data=json.loads((O/(name+'-CENTER-SCREEN.json')).read_text())
 if name=='CURRENT112':w=json.load(gzip.open(O.parent/'pr548-complex314/complex-local/syndrome/FULL-WORD.json.gz'));R=s.Matrix(w['root_lines']);ports=w['ports'];den=4
 else:w=json.loads((O/(name+'-WITNESS.json')).read_text());R=s.Matrix(w['roots_scaled_by_2']);ports=w['ports'];den=8
 X=R[:,R.rref()[1]];d=X.cols;vectors=set();items=[]
 for f in data['directions']:
  for vs in f['directions']:
   u=[s.Rational(x) for x in vs];n=s.ilcm(*[x.q for x in u]);u=[int(x*n) for x in u];g=math.gcd(*u);u=tuple(x//g for x in u)
   if u in vectors:continue
   vectors.add(u);col=X*s.Matrix(u);supp=[p for p,c in zip(ports,col) if c];rank=f2rank(supp)
   items.append((rank,len(supp),u))
 selected=[]
 for rank,nn,u in sorted(items):
  if s.Matrix(selected+[u]).rank()>len(selected):selected.append(u)
  if len(selected)==d:break
 U=s.Matrix(selected).T;collect=X*U;gram=R*R.T/den;idx=collect.T.rref()[1];scatter=gram[:,list(idx)]*collect[list(idx),:].T.inv();assert scatter*collect.T==gram
 dyadic=all(x.q&(x.q-1)==0 for x in scatter)
 ranks=[f2rank([p for p,x in zip(ports,collect[:,i]) if x]) for i in range(d)];cost=sum(ranks);v=R.rows
 row={'name':name,'ports':v,'centers':d,'label_h':data['h'],'center_ranks':ranks,'copy_cost':cost,'nine_stage_deficit_relaxation':8*v-9*cost,'five_stage_deficit_relaxation':4*v-5*cost,'eleven_stage_deficit_relaxation':10*v-11*cost,'dyadic_exact_gram_factorization':dyadic,'center_rank_histogram':{str(r):sum(x[0]==r for x in items) for r in sorted(set(x[0] for x in items))},'scope':'Minimum-weight independent basis among enumerated nullspace basis directions only; no full circuit or global admission.'}
 results.append(row);print(json.dumps(row),flush=True)
 (O/(name+'-MINCENTER-DECODER.json')).write_text(json.dumps({'summary':row,'collect':[[str(x) for x in r] for r in collect.tolist()],'scatter':[[str(x) for x in r] for r in scatter.tolist()]},indent=2)+'\n')
(O/'MINCENTER-RESULT.json').write_text(json.dumps(results,indent=2)+'\n')
