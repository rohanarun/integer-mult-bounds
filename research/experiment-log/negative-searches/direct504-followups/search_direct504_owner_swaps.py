"""Discovery: whole-owner helper swaps preserving every per-call physical family.
Inputs are frozen PR531 slots; outputs require independent emission and auditing.
"""
from pathlib import Path
from collections import defaultdict,Counter
import json,gzip,math,sys
S,O=map(Path,sys.argv[1:]);O.mkdir(exist_ok=False)
def read(p):return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
p=read(S/'inputs/OWNER-PLAN.json');roles=read(S/'inputs/OWNERS.json.gz');groups=defaultdict(list);calls=defaultdict(list)
def key(z):return(z['owner_replica'],z['child'],z['port'])
for z in roles:groups[key(z)].append(z);calls[z['time']].append(z)
left={k:p['windows'][f'{k[0]},{k[1]}'][0]-sum(z['width'] for z in zs) for k,zs in groups.items()}
trace=[]
for sweep in range(100):
 changed=0
 for t,zs in sorted(calls.items()):
  while True:
   small=sorted((z for z in zs if z['width']==8 and left[key(z)]>0),key=lambda z:left[key(z)])
   large=sorted((z for z in zs if z['width']==9),key=lambda z:-left[key(z)])
   best=None
   for a in small:
    for b in large:
     x,y=left[key(a)],left[key(b)]
     if y<x:break
     if key(a)==key(b):continue
     best=(a,b,x,y);break
    if best:break
   if best is None:break
   a,b,x,y=best
   trace.append(dict(time=t,a=key(a),b=key(b),remainders_before=[x,y],helpers=[a['helper'],b['helper']]))
   a['helper'],b['helper']=b['helper'],a['helper'];a['width'],b['width']=b['width'],a['width']
   left[key(a)]-=1;left[key(b)]+=1;changed+=1
 if not changed:break
for k,zs in groups.items():
 off=0
 for z in sorted(zs,key=lambda z:(z['offset'],z['time'])):z['offset']=off;off+=z['width']
 assert off<=p['windows'][f'{k[0]},{k[1]}'][0]
H=Counter({int(r):72*n for r,n in p['local_profile'].items()})
for k,(rank,window) in p['windows'].items():
 rep,child=map(int,k.split(','))
 for port in range(112):
  rem=left.get((rep,child,port),rank)
  if rem:H[rem]+=1
assert sum(r*n for r,n in H.items())==73*7168-2560
base=p['profile'];p['profile']=dict(sorted(H.items()));p['status']='DISCOVERY_OWNER_EXCHANGES_PENDING_PHYSICAL_REPLAY'
(O/'PLAN.json').write_text(json.dumps(p,indent=2)+'\n')
(O/'OWNERS.json.gz').write_bytes(gzip.compress(json.dumps(roles,sort_keys=True,separators=(',',':')).encode(),mtime=0))
r=dict(status='DISCOVERY_ONLY',swaps=len(trace),sweeps=sweep+1,baseline=base,profile=p['profile'],trace=trace)
(O/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print('swaps',len(trace),'profile',dict(sorted(H.items())),flush=True)
