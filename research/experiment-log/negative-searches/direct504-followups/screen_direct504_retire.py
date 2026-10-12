"""Exact local candidate construction; optimistic remainder pricing is discovery only."""
import sys,json,gzip,copy,subprocess,math
from pathlib import Path
from collections import Counter,defaultdict
S,O=map(lambda x:Path(x).resolve(),sys.argv[1:]);O.mkdir(exist_ok=False)
sys.path.insert(0,str(S/'vendor/gk'));import gk_common as c;import gk_word as g
c.V=g.V=112;c.DATA=g.DATA=7168
read=lambda p:json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
w=read(S.parent/'pr531-independent311/reconstructed/raw/FULL-WORD.json.gz');sel=read(S/'inputs/SELECTION.json');col=g.responses(w)
# Exact response graph components: retiring a component cannot break another pivot relation.
components=[]
for i,cl in enumerate(sel['kernel']):
 adj=defaultdict(set)
 for p in cl['pivots']:
  rel=g.solve_relation(col,cl['donors'],p);assert rel is not None
  for d in rel:adj[p].add(d);adj[d].add(p)
 seen=set()
 for p in cl['pivots']:
  if p in seen:continue
  st=[p];nodes=set()
  while st:
   v=st.pop()
   if v in nodes:continue
   nodes.add(v);st.extend(adj[v]-nodes)
  seen|=nodes;components.append((i,sorted(nodes&set(cl['pivots']))))
print('components',[(i,len(p)) for i,p in components],flush=True)
base=read(S/'EXPECTED.json');bp={int(k):v for k,v in base['global_profile'].items()};bl={int(k):v for k,v in base['local_profile'].items()};br=Counter(bp)
for k,v in bl.items():br[k]-=72*v
fee=lambda H:sum(n*r*math.log(73/r) for r,n in H.items())
rows=[]
for idx,(i,ps) in enumerate(components):
 out=O/f'case-{idx:03d}';out.mkdir();selection=copy.deepcopy(sel);selection['kernel'][i]['pivots']=[p for p in selection['kernel'][i]['pivots'] if p not in ps]
 changed=g.build(w,selection,check=True);changed['report'].update(v=112,h=9,R=504)
 (out/'SELECTION.json').write_text(json.dumps(selection,indent=2)+'\n');(out/'SELECTED.json.gz').write_bytes(g.dump(changed))
 with (out/'coalescing.log').open('w') as f:subprocess.run([sys.executable,'-B',str(S/'code/coalesce_frames.py'),'--word',str(out/'SELECTED.json.gz'),'--out',str(out/'coalesced')],check=True,stdout=f,stderr=subprocess.STDOUT)
 candidate=read(out/'coalesced/FULL-WORD.json.gz');local={int(k):v for k,v in candidate['report']['local_profile'].items()};extra=72*len(ps);rem=Counter(br)
 # Optimistic mass removal from the smallest remainders, unconstrained by windows/helper IDs.
 for rank in sorted(list(rem)):
  if rank<=0 or rem[rank]<=0:continue
  while extra and rem[rank]:
   take=min(extra,rank);rem[rank]-=1
   if rank>take:rem[rank-take]+=1
   extra-=take
  if not extra:break
 assert not extra
 H=Counter({k:72*v for k,v in local.items()});H.update(rem);assert sum(k*v for k,v in H.items())==73*7168-2560
 row=dict(case=idx,kernel=i,retired_pivots=ps,local_profile=local,optimistic_global_profile=dict(H),entropy_delta=fee(H)-fee(bp),scope='Unrealized optimistic packing screen; no certified global gain')
 rows.append(row);print(idx,len(ps),row['entropy_delta'],flush=True)
 (O/'RESULT.json').write_text(json.dumps(dict(status='LOCAL_CONSTRUCTIONS_OPTIMISTIC_SCREEN',rows=rows),indent=2)+'\n')
