"""Greedy whole-owner realization for retired-pivot candidates; discovery only."""
import sys,json,gzip,copy,math
from pathlib import Path
from collections import Counter,defaultdict
S,C,O=map(lambda x:Path(x).resolve(),sys.argv[1:]);O.mkdir(exist_ok=False)
read=lambda p:json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
base=read(S/'inputs/OWNER-PLAN.json');base_roles=read(S/'inputs/OWNERS.json.gz');rows=read(C/'RESULT.json')['rows'];fee=lambda H:sum(int(k)*v*math.log(73/int(k)) for k,v in H.items());results=[]
for row in rows:
 p=copy.deepcopy(base);zs=copy.deepcopy(base_roles);case=C/f"case-{row['case']:03d}";w=read(case/'coalesced/FULL-WORD.json.gz');widths=[9-len(w.get('start_extra',{}).get(str(224+h),[])) for h in range(504)]
 groups=defaultdict(list);calls=defaultdict(list)
 def key(z):return(z['owner_replica'],z['child'],z['port'])
 for z in zs:groups[key(z)].append(z);calls[z['time']].append(z)
 left={};available=defaultdict(list)
 for k,(rank,times)in p['windows'].items():
  rep,ch=map(int,k.split(','))
  for port in range(112):
   g=(rep,ch,port);left[g]=rank-sum(z['width']for z in groups[g])
   for tm in times:available[tm].append(g)
 def family(g):return g[0]*896+(2*p['pairs'][str(g[1])]+p['sides'][str(g[1])])*112+g[2]
 moved=0
 for t,rr in sorted(calls.items()):
  used={z['family'] for z in rr}
  for z in rr:
   nw=widths[z['helper']];old=z['width'];k=key(z)
   if nw==old:continue
   assert nw>old
   if left[k]>=nw-old:left[k]-=nw-old;z['width']=nw;continue
   possible=[g for g in available[t] if left[g]>=nw and family(g) not in used]
   if not possible:raise RuntimeError(('no whole owner',row['case'],t,z['helper']))
   def score(g):
    a=left[g];return (a-nw)*math.log(73/(a-nw)) - a*math.log(73/a) if a>nw else -a*math.log(73/a)
   g=min(possible,key=lambda g:(score(g),g))
   left[k]+=old;left[g]-=nw;groups[k].remove(z);groups[g].append(z);used.remove(z['family']);used.add(family(g))
   z.update(owner_replica=g[0],child=g[1],port=g[2],copy=g[0]*112+g[2],family=family(g),width=nw);moved+=1
 for g,rs in groups.items():
  off=0
  for z in sorted(rs,key=lambda z:(z['time'],z['helper'])):z['offset']=off;off+=z['width']
 H=Counter({int(k):72*v for k,v in w['report']['local_profile'].items()});H.update(x for x in left.values() if x)
 assert sum(k*v for k,v in H.items())==73*7168-2560
 out=O/f"case-{row['case']:03d}";out.mkdir();p.update(profile=dict(sorted(H.items())),baseline_widths=widths,local_profile=w['report']['local_profile'],status='GREEDY_REALIZATION_PENDING_AUDIT')
 (out/'PLAN.json').write_text(json.dumps(p,indent=2)+'\n');(out/'OWNERS.json.gz').write_bytes(gzip.compress(json.dumps(zs,sort_keys=True,separators=(',',':')).encode(),mtime=0))
 result=dict(case=row['case'],moved=moved,entropy_delta=fee(H)-fee(base['profile']),profile=dict(sorted(H.items())),scope='Unaudited literal nomination')
 results.append(result);print(result,flush=True)
 (O/'RESULT.json').write_text(json.dumps(dict(status='GREEDY_REALIZATION_DISCOVERY',rows=results),indent=2)+'\n')
