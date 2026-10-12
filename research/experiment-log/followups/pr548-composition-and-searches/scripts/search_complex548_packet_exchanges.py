"""Two-for-one whole-helper packet exchange screen on PR548's literal owner map.
Preserve widths, call order, per-family busy sets and allowed pending windows.
Floating cost nominates only; actual global audit and exact pricing required.
Prepared for Rohan Arun with OpenAI Codex assistance.
"""
from pathlib import Path
from collections import defaultdict,Counter
import json,gzip,copy,math,time,hashlib
R=Path(__file__).resolve().parent;O=R/'complex548-packet-exchanges';O.mkdir(exist_ok=False);P=R/'source548-review/complex-global';start=time.monotonic()
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
from itertools import combinations
for sweep in range(32):
 occupied=defaultdict(list);singles=defaultdict(list)
 for z in roles:
  key=(z['child'],z['owner_replica'],z['port']);occupied[key].append(z);singles[z['width'],bins[key]['left']].append(z)
 chosen=None
 for uk,us in sorted(occupied.items()):
  a=bins[uk]['left'];uf=bins[uk]['family']
  for u1,u2 in combinations(us,2):
   tried+=1;w=u1['width']+u2['width'];opts=[]
   for (vw,bb),vs in singles.items():
    aa=a+w-vw;bc=bb+vw-w
    if aa<0 or bc<0:continue
    delta=cost[aa]+cost[bc]-cost[a]-cost[bb]
    if delta < -1e-12:opts.append((delta,vw,bb,aa,bc))
   for delta,vw,bb,aa,bc in sorted(opts):
    improving_shapes+=1
    for v in singles[vw,bb]:
     families_tested+=1;vk=(v['child'],v['owner_replica'],v['port']);vf=v['family']
     if vk==uk:continue
     assert u1['time']!=u2['time']
     if any(u['time'] not in bins[vk]['times'] for u in [u1,u2]) or v['time'] not in bins[uk]['times']:continue
     # At each call, remove all exchanged roles before testing destination ownership.
     removed=defaultdict(set)
     for z in [u1,u2,v]:removed[z['time']].add(z['family'])
     if any(vf in busy[u['time']]-removed[u['time']] for u in [u1,u2]):continue
     if uf in busy[v['time']]-removed[v['time']]:continue
     chosen=(u1,u2,v,uk,vk,aa,bc,delta);break
    if chosen:break
   if chosen:break
  if chosen:break
 if chosen is None:break
 u1,u2,v,uk,vk,aa,bc,delta=chosen;before=[copy.deepcopy(z)for z in [u1,u2,v]]
 for z in [u1,u2,v]:busy[z['time']].remove(z['family'])
 for z,key in [(u1,vk),(u2,vk),(v,uk)]:
  ch,rep,port=key;z.update(child=ch,owner_replica=rep,port=port,copy=rep*V+port,family=bins[key]['family']);busy[z['time']].add(z['family'])
 update(uk,aa);update(vk,bc);moves.append(dict(before=before,after=[copy.deepcopy(z)for z in [u1,u2,v]],fee_delta=delta))
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
plan['profile']=dict(sorted(H.items()));plan['status']='PACKET_EXCHANGE_SCREEN_PENDING_ADMISSION';(O/'OWNERS.json.gz').write_bytes(gzip.compress(json.dumps(roles,sort_keys=True,separators=(',',':')).encode(),mtime=0));(O/'PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
r=dict(status='COMPLETE_BOUNDED_TWO_FOR_ONE_PACKET_EXCHANGE_SCREEN',role_visits=tried,improving_remainder_shapes=improving_shapes,candidate_families_tested=families_tested,moves=moves,profile=dict(sorted(H.items())),baseline_profile=original,seconds=time.monotonic()-start,scope='Fixed actual call order, local word, widths, allowed owner windows and one whole helper per physical family per call. Up to 32 first-improving exchanges of two whole helpers in one bin for one in another. Check every affected call busy set and allowed window. Floating screen only; no global optimum or physical admission claimed.');(O/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items()if k!='moves'},'moves',len(moves))
