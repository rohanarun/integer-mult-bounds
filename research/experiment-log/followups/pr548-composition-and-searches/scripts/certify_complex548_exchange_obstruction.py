"""Exact remainder-majorization obstruction for fixed PR548 whole-role exchanges.
For 0<b<1, f(r)=73**b*r**(1-b) is concave on r>=0.
At fixed sum, increasing the smaller of two remainders cannot lower f(a)+f(b).
This finite shape certificate is independent of numerical moment approximation.
Prepared for Rohan Arun with OpenAI Codex assistance.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
import json,gzip,hashlib
R=Path(__file__).resolve().parent;O=R/'complex548-exchange-obstruction';O.mkdir(exist_ok=False)
rolefile=R/'source548-review/complex-global/SAT-OWNERS.json.gz';parentfile=R/'pr548-complex314/complex-global/base/split-centres/GLOBAL-TEMPLATE.json.gz'
roles=json.loads(gzip.decompress(rolefile.read_bytes()));parent=json.loads(gzip.decompress(parentfile.read_bytes()))
bins={(z['child'],rep,z['port']):z['rank']for z in parent['idle_children']for rep in range(8)};occupied=defaultdict(list)
for z in roles:
 key=(z['child'],z['owner_replica'],z['port']);bins[key]-=z['width'];occupied[key].append(z)
assert all(v>=0 for v in bins.values())
groups=Counter((z['width'],bins[z['child'],z['owner_replica'],z['port']])for z in roles)
packets=Counter((u['width']+v['width'],bins[key])for key,zs in occupied.items()for u,v in combinations(zs,2))
def prove(left):
 feasible=[];infeasible=0
 for (w,a),count in sorted(left.items()):
  for (v,b),count2 in sorted(groups.items()):
   aa=a+w-v;bb=b+v-w
   if aa<0 or bb<0:infeasible+=1;continue
   assert aa+bb==a+b
   assert min(aa,bb)>=min(a,b),(w,a,v,b,aa,bb)
   assert (aa>0)+(bb>0)>=(a>0)+(b>0)
   feasible.append(dict(width_out=w,width_in=v,before=[a,b],after=[aa,bb],smaller_remainder_change=min(aa,bb)-min(a,b)))
 return dict(shape_combinations=len(left)*len(groups),capacity_infeasible_shapes=infeasible,feasible_shapes=feasible)
r=dict(status='PASS_EXACT_FIXED_MAP_PAIR_AND_TWO_FOR_ONE_OBSTRUCTION',source_head='66dbc2bffc1bfa8d50b3f9a2ac7ccba8fd9f6f36',roles_sha256=hashlib.sha256(rolefile.read_bytes()).hexdigest(),parent_sha256=hashlib.sha256(parentfile.read_bytes()).hexdigest(),role_groups=[dict(width=w,remainder=a,count=n)for(w,a),n in sorted(groups.items())],packet_groups=[dict(width=w,remainder=a,count=n)for(w,a),n in sorted(packets.items())],pair=prove(groups),two_for_one=prove(packets),argument='All represented capacity-feasible exchanges preserve the sum of the two affected remainders and weakly increase their minimum. Concavity of r^(1-b) for every 0<b<1 then makes the paid moment nondecreasing. The count of positive remainder children also cannot fall, so the retained positive per-child fallback charge cannot improve. Windows and physical-family conflicts only restrict this relaxed neighborhood further.',scope='Fixed current owner map, local profiles, widths and data-idle bins. Exchanging one whole helper for one, or two co-located whole helpers for one, between two bins. Does not cover multi-bin cycles, role splitting, multi-role block exchanges, changed call order, local word, stock or geometry. This is not a global allocation optimum or new kappa.')
(O/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],{k:len(r[k]['feasible_shapes'])for k in ['pair','two_for_one']})
