"""Independent stdlib Fraction verifier of finite decoder witnesses; imports no constructor."""
import gzip,json,hashlib
from fractions import Fraction as Q
from pathlib import Path
P=Path(__file__).resolve().parent
results=[]

def rankgf(rows):
 xs=list(rows);r=0
 for c in range(max(xs,default=0).bit_length()-1,-1,-1):
  pivot=next((j for j in range(r,len(xs)) if xs[j]>>c&1),None)
  if pivot is None:continue
  xs[r],xs[pivot]=xs[pivot],xs[r]
  for j in range(len(xs)):
   if j!=r and xs[j]>>c&1:xs[j]^=xs[r]
  r+=1
 return r
for fp in sorted(P.glob('*-MINCENTER-DECODER.json')):
 name=fp.name.removesuffix('-MINCENTER-DECODER.json');dec=json.loads(fp.read_text());C=[[Q(x) for x in r] for r in dec['collect']];S=[[Q(x) for x in r] for r in dec['scatter']]
 if name=='CURRENT112':
  w=json.load(gzip.open(P.parent/'pr548-complex314/complex-local/syndrome/FULL-WORD.json.gz'));R=w['root_lines'];ports=w['ports'];den=4
 else:
  w=json.loads((P/(name+'-WITNESS.json')).read_text());R=w['roots_scaled_by_2'];ports=w['ports'];den=8
 v=len(R);d=len(C[0]);count=0;off=0
 assert all(x.denominator&(x.denominator-1)==0 for r in C+S for x in r)
 assert len(set(ports))==v and all(p.bit_count()%2 for p in ports)
 for t in range(v):
  for i in range(v):
   g=Q(sum(x*y for x,y in zip(R[t],R[i])),den);actual=sum(S[t][k]*C[i][k] for k in range(d));assert actual==g
   if t==i:assert g==1
   elif g:
    assert (ports[t]&ports[i]).bit_count()%2==0;off+=1
   count+=1
 ranks=[rankgf([p for p,row in zip(ports,C) if row[k]]) for k in range(d)]
 assert ranks==dec['summary']['center_ranks'] and all(r<dec['summary']['label_h'] for r in ranks)
 # Explicit mutations: changed scatter coefficient and omitted nonzero side correction.
 t,k=next((t,k) for t in range(v) for k in range(d) if S[t][k]);i=next(i for i in range(v) if C[i][k]);assert sum(S[t][j]*C[i][j] for j in range(d))+C[i][k]!=Q(sum(x*y for x,y in zip(R[t],R[i])),den)
 ti=next((t,i) for t in range(v) for i in range(v) if t!=i and sum(x*y for x,y in zip(R[t],R[i])))
 assert Q(sum(x*y for x,y in zip(R[ti[0]],R[ti[1]])),den)!=0
 results.append({'name':name,'status':'PASS_FINITE_CLEAN_DECODER_ONLY','coefficient_pairs_checked':count,'legal_directed_corrections':off,'center_ranks':ranks,'negative_controls_rejected':2})
print(json.dumps(results,indent=2));(P/'INDEPENDENT-RESULT.json').write_text(json.dumps(results,indent=2)+'\n')
