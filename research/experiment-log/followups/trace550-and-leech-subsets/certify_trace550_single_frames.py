"""Exact binary subspace single-event endpoint search; floating cost nomination only.
Fixed scalar word, entrances, centre/target barriers and final frames. Full physical
replay remains necessary. Prepared with OpenAI Codex assistance; inherited gk code credited.
"""
from pathlib import Path
import os,json,gzip,sys,time,copy,math,hashlib
from collections import Counter
from functools import lru_cache
R=Path(__file__).resolve().parent; assert os.path.ismount('/Volumes/SP AI 01_16') and os.access(R,os.W_OK)
O=R/'trace550-frame-single-certificate';O.mkdir(exist_ok=False)
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

shapes={};inc=[]
for k in mutable:
 z=nodes[k];pred=[nodes[prev[k,r]]['F']for r in z['regs']];succ=[nodes[nxt[k,r]]['F']for r in z['regs']];lo=join(pred);hi=meet(succ);f=z['F']
 old=sorted([d for a,q in zip(pred,succ)for d in (len(f)-len(a),len(q)-len(f))],reverse=True)
 for new in {lo,hi}:
  if new==f:continue
  nw=sorted([d for a,q in zip(pred,succ)for d in (len(new)-len(a),len(q)-len(new))],reverse=True)
  assert sum(nw)==sum(old)
  ok=all(sum(old[:j])>=sum(nw[:j])for j in range(1,len(old)+1))
  key=(tuple(old),tuple(nw));shapes.setdefault(key,dict(count=0,old=old,new=nw,old_majorizes_new=ok));shapes[key]['count']+=1
  if not ok:inc.append(dict(section=z['sec'],index=z['ix'],old=old,new=nw))
r=dict(status='PASS_ALL_ENDPOINTS_NONDECREASING_FOR_0_LT_B_LT_1'if not inc else 'PARTIAL_MAJORISATION_SCREEN',events=len(mutable),endpoint_probes=sum(x['count']for x in shapes.values()),shapes=list(shapes.values()),incomparable=inc,proof='f(d)=73^b*d^(1-b)-d is concave for0<b<1, with f(0)=0. Old majorizes new, so new sum f>=old. For intermediate frame dimension the sum of increment fees is concave in dimension, hence at least the minimum endpoint fee. Fixed scalar instruction and all other frames; excludes simultaneous/neutral-path changes.',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
(O/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],r['endpoint_probes'],len(shapes),'incomparable',len(inc))
