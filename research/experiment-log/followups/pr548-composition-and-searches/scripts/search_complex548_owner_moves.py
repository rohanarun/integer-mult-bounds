"""Single whole-helper relocation screen on PR548's literal owner map.
Preserve widths, call order, per-family busy sets and allowed pending windows.
Floating cost nominates only; actual global audit and exact pricing required.
Prepared for Rohan Arun with OpenAI Codex assistance.
"""
from pathlib import Path
from collections import defaultdict,Counter
import json,gzip,copy,math,time,hashlib
R=Path(__file__).resolve().parent;O=R/'complex548-owner-moves';O.mkdir(exist_ok=False);P=R/'source548-review/complex-global';start=time.monotonic()
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
# One complete greedy pass, then repeat only if an improving relocation occurred.
for sweep in range(8):
 changed=0
 for z in sorted(roles,key=lambda z:(-bins[z['child'],z['owner_replica'],z['port']]['left'],z['time'],z['helper'])):
  tried+=1;oldkey=(z['child'],z['owner_replica'],z['port']);old=bins[oldkey];left=old['left'];w=z['width'];t=z['time'];options=[]
  for otherleft,keys in buckets[t].items():
   if otherleft<w or not keys:continue
   delta=cost[left+w]+cost[otherleft-w]-cost[left]-cost[otherleft]
   if delta < -1e-12:options.append((delta,otherleft));improving_shapes+=1
  chosen=None
  for delta,otherleft in sorted(options):
   for key in sorted(buckets[t][otherleft]):
    families_tested+=1
    if key==oldkey:continue
    fam=bins[key]['family']
    if fam in busy[t]and fam!=z['family']:continue
    chosen=(key,delta);break
   if chosen:break
  if chosen is None:continue
  key,delta=chosen;before=copy.deepcopy(z);new=bins[key];busy[t].remove(z['family']);busy[t].add(new['family']);update(oldkey,left+w);update(key,new['left']-w)
  ch,rep,port=key;z.update(child=ch,owner_replica=rep,port=port,copy=rep*V+port,family=new['family']);moves.append(dict(before=before,after=copy.deepcopy(z),fee_delta=delta));changed+=1
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
plan['profile']=dict(sorted(H.items()));plan['status']='SINGLE_HELPER_RELOCATION_SCREEN_PENDING_ADMISSION';(O/'OWNERS.json.gz').write_bytes(gzip.compress(json.dumps(roles,sort_keys=True,separators=(',',':')).encode(),mtime=0));(O/'PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
r=dict(status='COMPLETE_BOUNDED_SINGLE_WHOLE_HELPER_RELOCATION_SCREEN',role_visits=tried,improving_remainder_shapes=improving_shapes,candidate_families_tested=families_tested,moves=moves,profile=dict(sorted(H.items())),baseline_profile=original,seconds=time.monotonic()-start,scope='Fixed actual call order, local word, widths, allowed owner windows and one whole helper per physical family per call. Bounded greedy whole-role moves; floating cost only. No two-role exchange, global optimum or new physical admission claim.');(O/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items()if k!='moves'},'moves',len(moves))
