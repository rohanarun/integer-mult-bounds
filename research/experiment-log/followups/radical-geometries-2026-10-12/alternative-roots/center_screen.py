"""Find every legal rank-(h-1) center collection direction for each finite port set.
For cap a^perp a center may collect only sources with p_i.a=0.
Its coefficient linear form u must vanish on all other roots. Enumerate all a.
"""
import json,gzip,itertools,hashlib
from pathlib import Path
from collections import Counter
import sympy as s
O=Path(__file__).resolve().parent;B=O.parent

def spanbasis(rows):
 piv={}
 for row in rows:
  v=list(map(s.Rational,row))
  for c,b in sorted(piv.items()):
   if v[c]:q=v[c];v=[x-q*y for x,y in zip(v,b)]
  c=next((i for i,x in enumerate(v) if x),None)
  if c is not None:q=v[c];piv[c]=[x/q for x in v]
 return list(piv.values())

def solve(name,roots,ports,h):
 # compress ambient coordinates to independent columns, preserving rank.
 R=s.Matrix(roots);_,cols=R.rref();cols=R.T.rref()[1] if False else cols
 rank=R.rank();indcols=R.rref()[1];R=R[:,indcols];assert R.cols==rank
 rows=R.tolist();found=[];dist=Counter()
 for a in range(1,1<<h):
  forbidden=[r for r,p in zip(rows,ports) if (p&a).bit_count()%2]
  basis=spanbasis(forbidden);null=s.Matrix(basis).nullspace() if basis else list(s.eye(rank).columnspace());dist[len(null)]+=1
  if null:found.append({'normal':a,'nullity':len(null),'directions':[[str(x) for x in v] for v in null]})
 allrows=[[s.Rational(x) for x in v] for f in found for v in f['directions']]
 sr=s.Matrix(allrows).rank() if allrows else 0
 r={'geometry':name,'dimension':rank,'h':h,'normals_tested':(1<<h)-1,'legal_center_nullity_histogram':dict(dist),'legal_center_normals':len(found),'legal_direction_span_rank':sr,'full_rank_decoder_possible_under_hyperplane_condition':sr==rank,'directions':found,'scope':'Necessary center-collection condition; full span alone is not a legal circuit or factorization proof.'}
 (O/(name+'-CENTER-SCREEN.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='directions'}),flush=True);return r
results=[]
for p in sorted(O.glob('*-WITNESS.json')):
 w=json.loads(p.read_text());results.append(solve(p.name.removesuffix('-WITNESS.json'),w['roots_scaled_by_2'],w['ports'],w['h']))
w=json.load(gzip.open(B/'pr548-complex314/complex-local/syndrome/FULL-WORD.json.gz'))
results.append(solve('CURRENT112',w['root_lines'],w['ports'],9))
(O/'CENTER-RESULT.json').write_text(json.dumps({'status':'EXACT_NECESSARY_CENTER_SCREEN','results':[{k:v for k,v in r.items() if k!='directions'} for r in results]},indent=2)+'\n')
