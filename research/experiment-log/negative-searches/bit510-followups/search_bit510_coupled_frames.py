"""Bounded monotone lift search on R480; exact rational catalogue, floating discovery fee.
No physical or theorem claim until independent emitted operator admission.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import json,gzip,sys,math,time,copy,random
R=Path(__file__).resolve().parent;O=R/'bit510-coupled-frame-search';O.mkdir(exist_ok=False);t0=time.monotonic()
w=json.load(gzip.open(R/'bit510-review/research/e8-r480-dead-totals/data/bitE8mut-r480.json.gz'));lines=w['lines']
def rref(vs):
 b={}
 for row in vs:
  x=list(map(Q,row))
  for p,y in sorted(b.items()):
   if x[p]:a=x[p];x=[s-a*t for s,t in zip(x,y)]
  if any(x):
   p=next(j for j,a in enumerate(x)if a);a=x[p];x=[v/a for v in x]
   for q,y in list(b.items()):
    if y[p]:a=y[p];b[q]=[s-a*t for s,t in zip(y,x)]
   b[p]=x
 return b
def contains(b,row):
 x=list(map(Q,row))
 for p,y in sorted(b.items()):
  if x[p]:a=x[p];x=[s-a*t for s,t in zip(x,y)]
 return not any(x)
bs=[rref([lines[i]for i in f])for f in w['frames']];dim=[len(b)for b in bs];masks=[]
for f,b in zip(w['frames'],bs):
 closed={i for i,x in enumerate(lines)if contains(b,x)};assert set(f)==closed,'catalogue is not root-closed';masks.append(sum(1<<i for i in closed))
le=lambda a,b: masks[a]&masks[b]==masks[a]
N=2*w['v']+w['R'];nodes=[];chains=[[]for _ in range(N)];mutable=[]
def node(regs,frame,sec=None,idx=None):
 k=len(nodes);nodes.append(dict(regs=regs,F=frame,lo=frame,sec=sec,idx=idx))
 for r in regs:chains[r].append(k)
 if sec in ('A','B'):mutable.append(k)
 return k
for r,f in enumerate(w['start']):node([r],f)
for sec in ['D','A','B','C']:
 if sec=='B':
  for r in w['ret']:node([r],nodes[chains[r][-1]]['F'])
  for r in range(w['v'],2*w['v']):node([r],0)
 for i,(f,d,ss)in enumerate(w[sec]):node([d]+ss,f,sec,i)
for r,f in enumerate(w['final']):node([r],f)
prev={};nxt={}
for r,ch in enumerate(chains):
 for a,b in zip(ch,ch[1:]):prev[b,r]=a;nxt[a,r]=b
b=.001587447106092548;fee=lambda k:k*math.expm1(b*math.log(64/k)) if k else 0
def profile():
 h=Counter()
 for r,ch in enumerate(chains):
  for a,z in zip(ch,ch[1:]):
   fa,fz=nodes[a]['F'],nodes[z]['F'];assert le(fa,fz)
   if dim[fz]>dim[fa]:h[dim[fz]-dim[fa]]+=1
 return h
H0=profile();print('CATALOGUE',len(bs),'profile',dict(H0),'seconds',time.monotonic()-t0,flush=True)

from functools import lru_cache
@lru_cache(None)
def upper(mask):
 options=[f for f in range(len(bs))if mask&masks[f]==mask]
 return min(options,key=lambda f:(dim[f],f))
trials=0;valid=0;moves=[];bestdelta=0;winner=None
for k in reversed(mutable):
 z=nodes[k]
 for f in range(len(bs)):
  if f==z['F']or not le(z['F'],f):continue
  trials+=1;changed={k:f};queue=[k];bad=False
  while queue and not bad:
   j=queue.pop();fj=changed[j]
   for r in nodes[j]['regs']:
    q=nxt[j,r];fq=changed.get(q,nodes[q]['F'])
    if not le(fj,fq):
     if nodes[q]['sec']not in ('A','B'):bad=True;break
     changed[q]=upper(masks[fq]|masks[fj]);queue.append(q)
  if bad:continue
  valid+=1;edges=set()
  for j in changed:
   for r in nodes[j]['regs']:edges.add((prev[j,r],j,r));edges.add((j,nxt[j,r],r))
  dh=Counter()
  for p,q,r in edges:
   old=dim[nodes[q]['F']]-dim[nodes[p]['F']];new=dim[changed.get(q,nodes[q]['F'])]-dim[changed.get(p,nodes[p]['F'])]
   assert new>=0
   if old:dh[old]-=1
   if new:dh[new]+=1
  d=sum(fee(r)*n for r,n in dh.items())
  if d<bestdelta-1e-12:bestdelta=d;winner=(k,f,changed,dh);print('BEST',trials,'delta',d,'nodes',len(changed),flush=True)
if winner:
 k,f,ch,dh=winner
 for j,f in ch.items():nodes[j]['F']=f
 moves=[dict(section=nodes[j]['sec'],index=nodes[j]['idx'],frame=f)for j,f in ch.items()]
H=profile();out=copy.deepcopy(w)
for k in mutable:
 z=nodes[k];out[z['sec']][z['idx']][0]=z['F']
(O/'WORD.json.gz').write_bytes(gzip.compress(json.dumps(out,sort_keys=True,separators=(',',':')).encode(),mtime=0));res=dict(status='COMPLETE_CATALOGUE_FORWARD_CLOSURE_SCREEN',trials=trials,valid=valid,moves=moves,baseline_chain_profile=dict(H0),new_chain_profile=dict(H),best_fee_delta=bestdelta,seconds=time.monotonic()-t0,scope='Exact root catalogue containment; each seed frame lift propagated forward using a minimum-rank catalogue upper frame. Bounded catalogue screen, floating pricing. Not all rational subspaces, no optimality or global admission claim.');(O/'RESULT.json').write_text(json.dumps(res,indent=2)+'\n');print(res,flush=True)
