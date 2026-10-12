"""Exact binary subspace single-event endpoint search; floating cost nomination only.
Fixed scalar word, entrances, centre/target barriers and final frames. Full physical
replay remains necessary. Prepared with OpenAI Codex assistance; inherited gk code credited.
"""
from pathlib import Path
import os,json,gzip,sys,time,copy,math,hashlib
from collections import Counter
from functools import lru_cache
R=Path(__file__).resolve().parent; assert os.path.ismount('/Volumes/SP AI 01_16') and os.access(R,os.W_OK)
O=R/'trace550-frame-endpoints';O.mkdir(exist_ok=False)
sys.path.insert(0,str(R/'source550-review/local/vendor/gk'));import gk_word as g,gk_common as c
g.V=c.V=112;g.DATA=c.DATA=7168
source=R/'pr550-independent314/local/candidate/FULL-WORD.json.gz';w=json.load(gzip.open(source));original=copy.deepcopy(w);V=112;N=2*V+w['report']['R'];nodes=[];chains=[[]for _ in range(N)];mutable=[]
@lru_cache(None)
def sp(f):return frozenset(g.span(f))
def join(fs):return g.basis([x for f in fs for x in f])
def meet(fs):
 s=set(sp(fs[0]))
 for f in fs[1:]:s.intersection_update(sp(f))
 return g.basis(sorted(s))
def node(regs,F,sec=None,ix=None):
 k=len(nodes);nodes.append({'regs':regs,'F':g.basis(F),'sec':sec,'ix':ix})
 for r in regs:chains[r].append(k)
 if sec:mutable.append(k)
for r in range(N):node([r],[w['ports'][r]] if r<V else w.get('start_extra',{}).get(str(r),[]))
for sec in ('A','B'):
 if sec=='B':
  for r,f in zip(w['centers'],w['center_frames']):node([r],f)
  for t in range(V):node([V+t],w.get('target_levels',{}).get(str(t),[]))
 for ix,e in enumerate(w[sec]):node(e[1:3]if e[0]=='add'else e[1:2],e[-1],sec,ix)
for r in range(N):node([r],g.perp(w['ports'][r-V])if V<=r<2*V else g.FULL)
prev={};nxt={}
for r,ch in enumerate(chains):
 for a,b in zip(ch,ch[1:]):prev[b,r]=a;nxt[a,r]=b
b=.001593581126479114854212
fee=lambda d:d*math.expm1(b*math.log(73/d))if d else 0
hist0=g.profile(w);changes=[];t0=time.monotonic();probes=0
for sweep in range(30):
 best=None
 for k in mutable:
  z=nodes[k];pred=[nodes[prev[k,r]]['F']for r in z['regs']];succ=[nodes[nxt[k,r]]['F']for r in z['regs']];lo=join(pred);hi=meet(succ);f=z['F'];assert sp(lo)<=sp(f)<=sp(hi)
  old=sum(fee(len(f)-len(a))+fee(len(q)-len(f))for a,q in zip(pred,succ))
  for new in {lo,hi}:
   if new==f:continue
   probes+=1;delta=sum(fee(len(new)-len(a))+fee(len(q)-len(new))for a,q in zip(pred,succ))-old
   if delta<-1e-12 and (best is None or delta<best[0]):best=(delta,k,new)
 if best is None:break
 delta,k,new=best;z=nodes[k];changes.append(dict(section=z['sec'],index=z['ix'],old=list(z['F']),new=list(new),delta=delta));z['F']=new
for z in nodes:
 if z['sec']:w[z['sec']][z['ix']][-1]=list(z['F'])
w['cleanup']=[g.inverse(e,g.FULL)for e in reversed(w['A']+w['B'])if not V<=e[1]<2*V]
hist=g.profile(w);assert sum(r*n for r,n in hist.items())==sum(r*n for r,n in hist0.items());w['report']['local_profile']=dict(hist)
(O/'WORD.json.gz').write_bytes(g.dump(w));res=dict(status='COMPLETE_SINGLE_EVENT_ENDPOINT_SCREEN',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),events=len(mutable),probes=probes,sweeps=sweep+1,changes=changes,before=dict(hist0),after=dict(hist),fee_delta=sum(n*fee(r)for r,n in hist.items())-sum(n*fee(r)for r,n in hist0.items()),terminated_no_strict_endpoint_gain=best is None,seconds=time.monotonic()-t0,scope='Every feasible single-event frame has dimension between join(predecessors) and meet(successors). Concavity makes an endpoint minimize its discovery fee with others fixed. All binary subspace inclusions checked exactly, cost comparison floating. No neutral moves, simultaneous moves, new scalar words, physical admission or kappa claim.')
(O/'RESULT.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
