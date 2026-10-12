"""Exact shape/majorization screen for cyclic subset transfers among three bins.
One chosen whole-helper subset leaves each bin for the next; empty subsets allowed.
Prepared for Rohan Arun with OpenAI Codex assistance.
"""
from pathlib import Path
from collections import defaultdict
from itertools import product
import json,gzip,hashlib
R=Path(__file__).resolve().parent;O=R/'complex548-three-bin-cycles';O.mkdir(exist_ok=False)
rf=R/'source548-review/complex-global/SAT-OWNERS.json.gz';pf=R/'pr548-complex314/complex-global/base/split-centres/GLOBAL-TEMPLATE.json.gz'
roles=json.loads(gzip.decompress(rf.read_bytes()));parent=json.loads(gzip.decompress(pf.read_bytes()));bins={(z['child'],rep,z['port']):[z['rank'],[]]for z in parent['idle_children']for rep in range(8)}
for z in roles:
 bs=bins[z['child'],z['owner_replica'],z['port']];bs[0]-=z['width'];bs[1].append(z['width'])
groups=defaultdict(int)
for index,(left,ws)in enumerate(bins.values()):
 for mask in range(1<<len(ws)):
  width=sum(w for i,w in enumerate(ws)if mask>>i&1);groups[width,left]|=1<<index
infeasible=unrealizable=proved=0;unresolved=[];patterns=set()
for gg in product(groups,repeat=3):
 a=[g[1]for g in gg];ww=[g[0]for g in gg];aa=[a[i]+ww[i]-ww[(i-1)%3]for i in range(3)]
 if min(aa)<0:infeasible+=1;continue
 sets=[groups[g]for g in gg]
 if any((sets[i]|sets[j]).bit_count()<2 for i,j in[(0,1),(1,2),(0,2)])or(sets[0]|sets[1]|sets[2]).bit_count()<3:
  unrealizable+=1;continue
 old=sorted(a,reverse=True);new=sorted(aa,reverse=True);assert sum(old)==sum(new)
 if all(sum(old[:k])>=sum(new[:k])for k in[1,2]):
  assert sum(x>0 for x in aa)>=sum(x>0 for x in a);proved+=1;patterns.add((tuple(old),tuple(new)))
 else:unresolved.append(dict(groups=gg,before=a,after=aa))
r=dict(status='PASS_EXACT_FIXED_MAP_THREE_BIN_CYCLE_OBSTRUCTION'if not unresolved else'INCOMPLETE_MAJORISATION_SCREEN_WITH_UNRESOLVED_SHAPES',source_head='66dbc2bffc1bfa8d50b3f9a2ac7ccba8fd9f6f36',roles_sha256=hashlib.sha256(rf.read_bytes()).hexdigest(),parent_sha256=hashlib.sha256(pf.read_bytes()).hexdigest(),total_group_triples=len(groups)**3,capacity_infeasible=infeasible,unrealizable_distinct_bins=unrealizable,majorization_proved=proved,unresolved=unresolved,distinct_remainder_patterns=[dict(before=a,after=b)for a,b in sorted(patterns)],argument='Exhaustive subset-sum groups from actual bins, including empty subsets. Hall conditions on the three bin-choice sets prove distinct representatives exist or exclude the shape. For each remaining capacity-feasible shape, old remainders majorize new remainders. Concavity of r^(1-b) for all 0<b<1 implies the paid moment cannot decrease. Positive child count also cannot decrease, so the retained per-child fallback cost cannot improve.',scope='Fixed-map cyclic transfers of one whole-helper subset from each of three distinct bins to the next. Does not cover splitting one subset among two destinations, neutral preparatory moves, longer cycles, changed order/local word/stock/geometry. Not a global packing optimum.')
(O/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],{k:r[k]for k in['total_group_triples','capacity_infeasible','unrealizable_distinct_bins','majorization_proved']},'unresolved',len(unresolved))
