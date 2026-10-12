"""Exact exhaustive obstruction for arbitrary whole-helper subset exchanges
between two distinct bins in the frozen PR548 owner map. Includes empty subsets.
Prepared for Rohan Arun with OpenAI Codex assistance.
"""
from pathlib import Path
from collections import defaultdict
import json,gzip,hashlib
R=Path(__file__).resolve().parent;O=R/'complex548-two-bin-obstruction';O.mkdir(exist_ok=False)
rf=R/'source548-review/complex-global/SAT-OWNERS.json.gz';pf=R/'pr548-complex314/complex-global/base/split-centres/GLOBAL-TEMPLATE.json.gz'
roles=json.loads(gzip.decompress(rf.read_bytes()));parent=json.loads(gzip.decompress(pf.read_bytes()))
bins={(z['child'],rep,z['port']):[z['rank'],[]]for z in parent['idle_children']for rep in range(8)}
for z in roles:
 key=(z['child'],z['owner_replica'],z['port']);bins[key][0]-=z['width'];bins[key][1].append(z['width'])
groups=defaultdict(set);subsets=0
for key,(a,ws)in bins.items():
 assert a>=0
 for mask in range(1<<len(ws)):
  w=sum(v for i,v in enumerate(ws)if mask>>i&1);groups[w,a].add(key);subsets+=1
proof=[];excluded=[];infeasible=0
for (w,a),us in sorted(groups.items()):
 for (v,b),vs in sorted(groups.items()):
  aa=a+w-v;bb=b+v-w
  if min(aa,bb)<0:infeasible+=1;continue
  # There exist distinct source bins unless both groups are the same singleton.
  distinct=not(len(us)==len(vs)==1 and us==vs)
  row=dict(before=[a,b],after=[aa,bb],exchanged_widths=[w,v])
  if not distinct:
   row['only_bin']=list(next(iter(us)));excluded.append(row);continue
  assert aa+bb==a+b and min(aa,bb)>=min(a,b),row
  assert (aa>0)+(bb>0)>=(a>0)+(b>0)
  proof.append(row)
# Control: the tempting move requires two different bins with remainder39.
# There is only one. Adding a fictional second one must expose the improvement.
assert len(groups[0,39])==len(groups[9,39])==1 and groups[0,39]==groups[9,39]
assert min(39+0-9,39+9-0)<39
r=dict(status='PASS_EXACT_ALL_TWO_BIN_WHOLE_HELPER_SUBSET_EXCHANGE_OBSTRUCTION',source_head='66dbc2bffc1bfa8d50b3f9a2ac7ccba8fd9f6f36',roles_sha256=hashlib.sha256(rf.read_bytes()).hexdigest(),parent_sha256=hashlib.sha256(pf.read_bytes()).hexdigest(),bins=len(bins),roles=len(roles),maximum_helpers_in_bin=max(len(z[1])for z in bins.values()),enumerated_subsets=subsets,group_count=len(groups),groups=[dict(exchanged_width=w,remainder=a,bin_count=len(keys))for(w,a),keys in sorted(groups.items())],capacity_infeasible_shape_pairs=infeasible,excluded_same_singleton_bin=excluded,feasible_distinct_bin_shapes=proof,control='A fabricated second remainder39 bin would permit a 9-wide move changing (39,39) to (30,48); the actual map has only one such bin, so this is rejected as a same-bin exchange.',argument='For every realizable capacity-feasible pair of whole-helper subsets in two distinct bins, including empty subsets, the sum of the two residual ranks is conserved and their minimum cannot decrease. For all 0<b<1 concavity of r^(1-b) makes the paid moment nondecreasing. Positive residual-child count cannot decrease, so the retained positive per-child fallback charge also cannot improve. Ignoring window and family constraints only enlarges the neighborhood.',scope='Exact obstruction at the pinned fixed owner map for all two-bin whole-helper subset exchanges, including single moves and arbitrary block swaps. Does not exclude multi-bin exchanges, non-improving preparatory moves followed by a gain, changed call order, helper splitting, changed local words, stocks or geometry. Not a global allocation optimum or new kappa.')
(O/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],{k:r[k]for k in ['bins','roles','enumerated_subsets','group_count']},'feasible_shapes',len(proof))
