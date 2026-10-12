"""Repeat previously stale connectivity/substitution questions on exact PR548.
Full-row substitution is impossible for independent arbitrary registers under
invertible elementary gates; test the meaningful protected-column quotient instead.
Prepared for Rohan Arun with OpenAI Codex assistance.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict,Counter
import json,gzip,hashlib,time
O=Path(__file__).resolve().parent;R=O.parent;src=R/'pr548-complex314/complex-local/local/CANONICAL-WORD.json.gz';raw=gzip.decompress(src.read_bytes());w=json.loads(raw);V=w['v'];N=2*V+w['R'];start=time.monotonic();par=list(range(N))
def root(x):
 while par[x]!=x:par[x]=par[par[x]];x=par[x]
 return x
def union(a,b):par[root(a)]=root(b)
scalar_steps=0
for ph in ['precondition','compensation','A','cut','B','cleanup']:
 for e in w[ph]:
  scalar_steps+=1
  if e[0]=='add':assert e[1]!=e[2] and e[4]!=0;union(e[1],e[2])
  else:assert e[0]=='scale'and e[2]!=0 and e[3]!=0
for i in range(V):union(i,V+i)
components=Counter(root(i)for i in range(N))
protected=set(range(2*V))|{i for i in range(2*V,N)if w['frames'][w['start'][i]]}
rows=[({i:Q(1)}if i in protected else{})for i in range(N)]
def apply(e):
 t=e[1]
 if e[0]=='scale':q=Q(e[2],e[3]);rows[t]={j:q*x for j,x in rows[t].items()}
 else:
  q=Q(e[3],e[4])
  for j,x in list(rows[e[2]].items()):
   z=rows[t].get(j,Q(0))+q*x
   if z:rows[t][j]=z
   else:rows[t].pop(j,None)
for ph in ['precondition','compensation']:
 for e in w[ph]:apply(e)
cur=list(w['start']);at=defaultdict(set)
for i,f in enumerate(cur):at[f].add(i)
checked=nonempty=pooltotal=0;candidates=[];cold_zero=[]
def signature(row):
 if not row:return (),Q(0)
 j=min(row);scale=row[j];return tuple((k,x/scale)for k,x in sorted(row.items())),scale
for ph in ['A','cut','B']:
 for index,e in enumerate(w[ph]):
  if ph=='cut':apply(e);continue
  f=e[-1]
  if e[0]=='add'and e[2]>=2*V and cur[e[2]]!=f:
   s=e[2];checked+=1;pool=[r for r in at[f]if r not in(e[1],s)and not V<=r<2*V];pooltotal+=len(pool);nonempty+=bool(pool);sig,scale=signature(rows[s])
   if not sig:cold_zero.append(dict(section=ph,index=index,source=s,from_frame=cur[s],to_frame=f))
   else:
    for r in pool:
     other,ss=signature(rows[r])
     if other==sig:candidates.append(dict(section=ph,index=index,old_source=s,new_source=r,multiplier=str(scale/ss),from_frame=cur[s],to_frame=f,protected_columns=len(protected)));break
  for r in[e[1]]+([e[2]]if e[0]=='add'else[]):at[cur[r]].discard(r);cur[r]=f;at[f].add(r)
  apply(e)
result=dict(status='COMPLETE_CURRENT_WORD_CONNECTIVITY_AND_QUOTIENT_SUBSTITUTION_SCREEN',source_head='66dbc2bffc1bfa8d50b3f9a2ac7ccba8fd9f6f36',canonical_content_sha256=hashlib.sha256(raw).hexdigest(),registers=N,components=len(components),component_sizes=sorted(components.values()),invertible_elementary_steps=scalar_steps,full_row_obstruction='Every add with distinct operands and every nonzero scale is invertible, so independent arbitrary register rows remain independent. A full-row source substitution by other registers cannot exist. Only a restricted observable/dirty quotient can offer a meaningful replacement.',protected_columns=len(protected),helper_source_climbs=checked,nonempty_pools=nonempty,total_pool_size=pooltotal,proportional_candidates=candidates,cold_zero_source_candidates=cold_zero,seconds=time.monotonic()-start,scope='Connectivity excludes only direct-summand deletion of this word. Quotient screen preserves source and target input columns plus nonzero-frame initial helper columns; ignores only initially cold helper dirt. Candidate equality alone does not prove frame legality after deletion, dirt compensation, mutable-source contract, phase maps, global invoice or improved kappa. No candidate is applied or admitted here.')
(O/'current-word-screens.json').write_text(json.dumps(result,indent=2)+'\n');print({k:result[k]for k in['status','registers','components','helper_source_climbs','nonempty_pools','seconds']},'proportional',len(candidates),'cold_zero',len(cold_zero))
