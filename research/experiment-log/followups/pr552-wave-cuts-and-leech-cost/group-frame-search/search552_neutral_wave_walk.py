"""Global s-t cut nominations for one common hyperplane contraction or line extension.
All group sizes allowed; exact binary frame legality, floating fee rounded to integer
capacities for discovery. Full scalar/phase/global replay required for improvements.
Prepared with OpenAI Codex assistance, inherited gk primitives retain source notices.
"""
from pathlib import Path
import json,gzip,sys,os,time,copy,math,hashlib
from collections import Counter,defaultdict,deque
from functools import lru_cache
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
R=Path(__file__).resolve().parent;assert os.path.ismount('/Volumes/SP AI 01_16')and os.access(R,os.W_OK)
O=R/'trace552-neutral-wave-walk-anchor-fixed';O.mkdir(exist_ok=False)
sys.path.insert(0,str(R/'source550-review/local/vendor/gk'));import gk_word as g,gk_common as c;g.V=c.V=112;g.DATA=c.DATA=7168
src=R/'pr552-independent314/complex-local/weighted/FULL-WORD.json.gz';w=json.load(gzip.open(src));base=copy.deepcopy(w);n=224+w['report']['R'];b=.001594507308884431019637;SCALE=10**7;INF=10**15
cost=lambda d:d*math.expm1(b*math.log(73/d))+32*73**2*73**b/10**16 if d else 0
@lru_cache(None)
def sp(F):return frozenset(g.span(F))
@lru_cache(None)
def contract(F,v):return g.basis(x for x in sp(F)if not(x&v).bit_count()%2)
@lru_cache(None)
def extend(F,v):return g.basis((*F,v))
def context(w):
 nodes=[];chains=[[]for _ in range(n)];edges=[]
 def node(rs,F,sec=None,ix=None,anchor=False):
  k=len(nodes);nodes.append(dict(regs=rs,F=g.basis(F),sec=sec,ix=ix,fixed=sec is None))
  for r in rs:
   if chains[r]:
    if anchor:
     prev=nodes[chains[r][-1]];assert prev['F']==g.basis(F)
     prev['fixed']=True
    edges.append((chains[r][-1],k))
   chains[r].append(k)
 for r in range(n):node([r],[w['ports'][r]]if r<112 else w.get('start_extra',{}).get(str(r),[]))
 for sec in ('A','B'):
  if sec=='B':
   for r,F in zip(w['centers'],w['center_frames']):node([r],F,anchor=True)
   for t in range(112):node([112+t],w.get('target_levels',{}).get(str(t),[]),anchor=True)
  for ix,e in enumerate(w[sec]):node(e[1:3]if e[0]=='add'else e[1:2],e[-1],sec,ix)
 for r in range(n):node([r],g.perp(w['ports'][r-112])if 112<=r<224 else g.FULL)
 return nodes,edges
history=[];ledger=[];visited=set();start=time.monotonic();baseline=g.profile(w);visited.add(hashlib.sha256(json.dumps([w['A'],w['B']],sort_keys=True).encode()).hexdigest())
for sweep in range(8):
 nodes,edges=context(w);frames=[z['F']for z in nodes];N=len(nodes);source=N;sink=N+1;best=None
 for kind,transform in [('contract',contract),('extend',extend)]:
  for v in range(1,512):
   changed={F:transform(F,v)for F in set(frames)};active=[changed[F]!=F for F in frames];caps=defaultdict(int);constant=0.0
   def arc(a,b,fee):
    if fee>0:caps[a,b]+=int(round(fee*SCALE))
   for k,z in enumerate(nodes):
    if active[k]and z['fixed']:caps[k,sink]+=INF
   for p,q in edges:
    F,G=frames[p],frames[q];d=len(G)-len(F);assert sp(F)<=sp(G)
    if active[p]and active[q]:
     if kind=='contract':caps[q,p]+=INF;arc(p,q,cost(d+1)-cost(d))
     else:caps[p,q]+=INF;arc(q,p,cost(d+1)-cost(d))
    elif active[p]:
     # Only extension can encounter active predecessor / inactive successor.
     assert kind=='extend';delta=cost(d-1)-cost(d);assert delta<=0
     arc(source,p,-delta);constant+=delta
    elif active[q]:
     assert kind=='contract';delta=cost(d-1)-cost(d);assert delta<=0
     arc(source,q,-delta);constant+=delta
   if not any(a==source for a,z in caps):continue
   # SciPy returns int32 flows even for int64 input. Choose hard capacity
   # above the all-unselected feasible cut and bound every stored capacity.
   hard_cap=sum(cap for (a,z),cap in caps.items() if a==source)+1
   assert hard_cap < 2**31-1, hard_cap
   rr=[];cc=[];vv=[]
   for (a,z),cap in caps.items():
    if cap:
     cap=hard_cap if cap>=INF else cap
     assert cap<2**31-1
     rr.append(a);cc.append(z);vv.append(cap)
   mat=csr_matrix((np.array(vv,dtype=np.int64),(rr,cc)),shape=(N+2,N+2));result=maximum_flow(mat,source,sink,method='dinic');residual=(mat-result.flow).tocsr();seen={sink};todo=[sink];residual=residual.transpose().tocsr()
   while todo:
    a=todo.pop()
    for pos in range(residual.indptr[a],residual.indptr[a+1]):
     z=int(residual.indices[pos])
     if residual.data[pos]>0 and z not in seen:seen.add(z);todo.append(z)
   selected=[k for k in range(N) if k not in seen and active[k]];assert all(not nodes[k]['fixed']for k in selected)
   delta=0.;selected_set=set(selected)
   for p,q in edges:
    F=changed[frames[p]]if p in selected_set else frames[p];G=changed[frames[q]]if q in selected_set else frames[q];assert sp(F)<=sp(G),(kind,v,p,q)
    delta+=cost(len(G)-len(F))-cost(len(frames[q])-len(frames[p]))
   row=dict(sweep=sweep,kind=kind,covector_or_vector=v,selected=len(selected),fee_delta=delta,rounded_cut_bound=result.flow_value/SCALE+constant);ledger.append(row)
   if delta<=1e-10 and selected:
    sig=hashlib.sha256(json.dumps([[nodes[k]['sec'],nodes[k]['ix'],list(changed[frames[k]])] for k in selected],sort_keys=True).encode()).hexdigest()
    if sig not in visited and (best is None or delta<best[0]-1e-10 or(abs(delta-best[0])<1e-10 and len(selected)>len(best[3]))):best=(delta,kind,v,selected,changed,sig)
  print('SWEEP',sweep,kind,'best',best[0]if best else None,'seconds',time.monotonic()-start,flush=True)
 if best is None:break
 delta,kind,v,selected,changed,sig=best;visited.add(sig);old=g.profile(w);moves=[]
 for k in selected:
  z=nodes[k];F=list(changed[z['F']]);moves.append(dict(section=z['sec'],index=z['ix'],old=list(z['F']),new=F));w[z['sec']][z['ix']][-1]=F
 new=g.profile(w);actual=sum(z*cost(r)for r,z in new.items())-sum(z*cost(r)for r,z in old.items());assert abs(actual-delta)<1e-8
 history.append(dict(sweep=sweep,kind=kind,v=v,delta=delta,moves=moves,profile=dict(new)));print('MOVE',delta,kind,v,len(moves),dict(new),flush=True)
 w['cleanup']=[g.inverse(e,g.FULL)for e in reversed(w['A']+w['B'])if not 112<=e[1]<224]
 w['report']['local_profile']=dict(new);(O/f'CANDIDATE-{sweep}.json.gz').write_bytes(g.dump(w));(O/'HISTORY.json').write_text(json.dumps(history,indent=2)+'\n')
ans=dict(status='COMPLETE_MAXIMAL_CUT_NEUTRAL_WALK_DISCOVERY',baseline_profile=dict(baseline),final_profile=dict(g.profile(w)),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),sweeps=sweep+1,nominations=sum(h['delta']<-1e-10 for h in history),neutral_moves=sum(abs(h['delta'])<=1e-10 for h in history),seconds=time.monotonic()-start,capacity_scale=SCALE,scope='For each nonzero F2^9 covector/extension line, min-cut searches all legal selected event groups with fixed boundaries. Integer-rounded floating fees nominate only; no exact optimality or full physical admission claimed. Maximal source-side minimum cut; up to8 best-improvement/neutral sweeps; multiple different directions jointly are outside one cut.')
(O/'RESULT.json').write_text(json.dumps(ans,indent=2)+'\n');(O/'LEDGER.json').write_text(json.dumps(ledger,indent=2)+'\n');print(ans,flush=True)
