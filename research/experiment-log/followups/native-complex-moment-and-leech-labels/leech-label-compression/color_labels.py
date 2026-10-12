"""New valid Gram completions through graph coloring plus isotropic distinctness tags.
Uses the ordinary binary dot product; no alternate supplier interface.
"""
from pathlib import Path
import gzip,json,itertools,time,math,random,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent;OLD=ROOT.parent/'radical-geometry-leech-next'
inp=json.load(gzip.open(ROOT/'INPUT.json.gz'));old=inp['source'];A=np.array(inp['A']);B=np.array(old['B_scaled']);T=A@B;N=len(T);assert np.all(np.diag(T)==old['scale'])
E=(T!=0)|(T.T!=0);np.fill_diagonal(E,False);adj=[{j for j in range(N)if E[i,j]}for i in range(N)]
def rank(xs):
 p={}
 for x in xs:
  while x:
   k=x.bit_length()-1
   if k in p:x^=p[k]
   else:p[k]=x;break
 return len(p)
def greedy(seed):
 rng=random.Random(seed);colors={}
 while len(colors)<N:
  left=[i for i in range(N)if i not in colors]
  if seed:priority={i:rng.random()for i in left}
  else:priority={i:-i for i in left}
  i=max(left,key=lambda i:(len({colors[j]for j in adj[i]if j in colors}),len(adj[i]),priority[i]))
  used={colors[j]for j in adj[i]if j in colors};colors[i]=next(c for c in range(N)if c not in used)
 return[colors[i]for i in range(N)]
# Exact maximum clique establishes a certified chromatic lower bound.
bestcl=[]
def clique(cl,can):
 global bestcl
 if len(cl)+len(can)<=len(bestcl):return
 if not can:
  if len(cl)>len(bestcl):bestcl=cl[:]
  return
 while can:
  if len(cl)+len(can)<=len(bestcl):return
  i=max(can,key=lambda i:len(adj[i]&can));can.remove(i);clique(cl+[i],can&adj[i])
clique([],set(range(N)))
trials=[];wits=[]
for seed in range(64):
 C=greedy(seed);q=max(C)+1;assert all(C[i]!=C[j]for i in range(N)for j in adj[i])
 groups=[[i for i,c in enumerate(C)if c==k]for k in range(q)];t=(max(map(len,groups))-1).bit_length();P=[0]*N
 for col,group in enumerate(groups):
  for tag,i in enumerate(group):P[i]=(1<<col)|(tag<<q)|(tag<<(q+t))
 h=q+2*t
 assert len(set(P))==N and all(x.bit_count()%2 for x in P)
 assert all((P[i]&P[j]).bit_count()%2==int(C[i]==C[j])for i in range(N)for j in range(N))
 assert all((P[i]&P[j]).bit_count()%2==0 for i in range(N)for j in range(N)if i!=j and T[i,j])
 ranks=[rank([P[i]for i in np.flatnonzero(row)])for row in B if np.any(row)]
 rr={'seed':seed,'colors':q,'tag_bits_each_copy':t,'dimension':h,'label_span_rank':rank(P),'center_ranks':ranks,'copy_charge':sum(ranks),'all_gathers_proper':all(r<h for r in ranks)}
 trials.append(rr);wits.append({'source':old,'A':A.tolist(),'labels':P,'dimension':h,'coloring':C,'ranks':ranks})
best=min(range(len(trials)),key=lambda i:(trials[i]['copy_charge'],trials[i]['dimension'],trials[i]['colors']))
res={'status':'PASS_CONSTRUCTIVE_NEW_GRAM_LABEL_REALIZATIONS','ports':N,'forced_orthogonality_edges':int(E.sum())//2,'exact_maximum_clique':len(bestcl),'clique_ports':bestcl,'best':trials[best],'trials':trials,'scope':'Changing unconstrained Gram entries only. Same ordinary F2 dot product, source labels/target caps, dyadic scalar transfer. No global pricing.'}
(ROOT/'COLOR-RESULT.json').write_text(json.dumps(res,indent=2)+'\n')
(ROOT/'COLOR-WITNESS.json.gz').write_bytes(gzip.compress(json.dumps(wits[best],separators=(',',':')).encode(),mtime=0))
print(json.dumps({k:v for k,v in res.items()if k!='trials'},indent=2))
