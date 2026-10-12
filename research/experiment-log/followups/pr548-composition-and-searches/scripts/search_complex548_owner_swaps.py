"""Two-helper same-call exchange screen on PR548's literal owner map.
Preserve widths, call order, per-family busy sets and allowed pending windows.
Floating cost nominates only; actual global audit and exact pricing required.
Prepared for Rohan Arun with OpenAI Codex assistance.
"""
from pathlib import Path
from collections import defaultdict,Counter
import json,gzip,copy,math,time,hashlib
R=Path(__file__).resolve().parent;O=R/'complex548-owner-swaps';O.mkdir(exist_ok=False);P=R/'source548-review/complex-global';start=time.monotonic()
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
roles=read(P/'SAT-OWNERS.json.gz');plan=read(P/'SAT534-PLAN.json');parent=read(R/'pr548-complex314/complex-global/base/split-centres/GLOBAL-TEMPLATE.json.gz');host=read(R/'pr548-complex314/complex-global/hosted/GLOBAL-TEMPLATE.json.gz');V=112;M=73;T=8;b=float('0.001593519419282306763502');cost=[0]+[r*((M/r)**b-1)for r in range(1,M+1)];side={};pairs={}
for e in parent['execution_schedule']:
 if e['kind']=='idle_cover_sweep':
  for s,ch in enumerate(e['child_indices']):side[ch]=s;pairs[ch]=e['pair']
bins={}
for child in parent['idle_children']:
 for rep in range(T):
  i,port,cap=child['child'],child['port'],child['rank'];key=(i,rep,port);fam=rep*(8*V)+(2*pairs[i]+side[i])*V+port;windows=plan['windows'][f'{rep},{i}'];assert windows[0]==cap
  bins[key]=dict(family=fam,cap=cap,left=cap,times=windows[1])
for z in roles:
 key=(z['child'],z['owner_replica'],z['port']);assert z['family']==bins[key]['family'];bins[key]['left']-=z['width']
assert all(v['left']>=0 for v in bins.values())
busy={c['time']:{x[0]for x in c['owners']}for c in host['calls']};assert all(len(v)==728 for v in busy.values())
buckets=defaultdict(lambda:defaultdict(set))
for key,z in bins.items():
 for t in z['times']:buckets[t][z['left']].add(key)
def update(key,left):
 z=bins[key]
 for t in z['times']:buckets[t][z['left']].remove(key);buckets[t][left].add(key)
 z['left']=left
moves=[];tried=0;improving_shapes=0;families_tested=0
calls=defaultdict(list)
for z in roles:calls[z['time']].append(z)
for sweep in range(8):
 changed=0
 for t,zs in sorted(calls.items()):
  best=None
  for i,u in enumerate(zs):
   uk=(u['child'],u['owner_replica'],u['port']);a=bins[uk]['left'];w=u['width']
   for v in zs[i+1:]:
    tried+=1;vwidth=v['width']
    if w==vwidth:continue
    vk=(v['child'],v['owner_replica'],v['port']);bb=bins[vk]['left'];aa=a+w-vwidth;bc=bb+vwidth-w
    if aa<0 or bc<0:continue
    delta=cost[aa]+cost[bc]-cost[a]-cost[bb]
    if delta>=-1e-12:continue
    improving_shapes+=1
    # Both bins already host this exact call, hence both windows permit it.
    assert t in bins[uk]['times'] and t in bins[vk]['times']
    assert u['family']!=v['family']
    if best is None or delta<best[0]:best=(delta,u,v,uk,vk,aa,bc)
  if best is None:continue
  delta,u,v,uk,vk,aa,bc=best;before=[copy.deepcopy(u),copy.deepcopy(v)]
  for z,key in [(u,vk),(v,uk)]:
   ch,rep,port=key;z.update(child=ch,owner_replica=rep,port=port,copy=rep*V+port,family=bins[key]['family'])
  update(uk,aa);update(vk,bc);moves.append(dict(before=before,after=[copy.deepcopy(u),copy.deepcopy(v)],fee_delta=delta));changed+=1
 if not changed:break
bybin=defaultdict(list)
for z in roles:bybin[z['child'],z['owner_replica'],z['port']].append(z)
for key,zs in bybin.items():
 off=0
 for z in sorted(zs,key=lambda z:(z['time'],z['helper'])):z['offset']=off;off+=z['width']
 assert off==bins[key]['cap']-bins[key]['left']
roles.sort(key=lambda z:(z['time'],z['helper']));local=read(R/'pr548-complex314/complex-local/local/LOCAL-CHECKS.json');H=Counter()
for c in host['calls']:H.update({int(r):n for r,n in local[c['orientation']]['paid_profile'].items()})
for z in bins.values():
 if z['left']:H[z['left']]+=1
assert M*host['live']-sum(r*n for r,n in H.items())==2560;original={int(r):n for r,n in read(R/'source548-review/EXPECTED.json')['complex_global_profile'].items()}
plan['profile']=dict(sorted(H.items()));plan['status']='SAME_CALL_PAIR_EXCHANGE_SCREEN_PENDING_ADMISSION';(O/'OWNERS.json.gz').write_bytes(gzip.compress(json.dumps(roles,sort_keys=True,separators=(',',':')).encode(),mtime=0));(O/'PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
r=dict(status='COMPLETE_BOUNDED_SAME_CALL_PAIR_EXCHANGE_SCREEN',pair_visits=tried,improving_remainder_shapes=improving_shapes,candidate_families_tested=families_tested,moves=moves,profile=dict(sorted(H.items())),baseline_profile=original,seconds=time.monotonic()-start,scope='Fixed actual call order, local word, widths, allowed owner windows and one whole helper per physical family per call. At most eight sweeps, best improving same-call pair per call per sweep; floating cost only. No cross-call exchange, global optimum or new physical admission claim.');(O/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items()if k!='moves'},'moves',len(moves))
