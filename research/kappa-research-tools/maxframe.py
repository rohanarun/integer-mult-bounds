import sys,json,importlib.util,time
from collections import Counter,defaultdict
from fractions import Fraction as Q
from pathlib import Path
sys.set_int_max_str_digits(0)
P=Path('/home/claude/crocswap/w200/research/paired-cube-diagonal-bit-168')
spec=importlib.util.spec_from_file_location('ad',P/'bit/word.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
word=m.Candidate();word.exact_frames();C=word.C;h=word.h;M=word.module
t0=time.time();base=word.row();print('base row',base['W_per_vertex'],base['deficit_per_vertex'],time.time()-t0)
ops=word.ops;order=word.phase1+word.rest
full=word.w['full_frame']
term={}
for j,s in enumerate(word.w['rootroles']):term[s]=word.w['root_frame'][j]
for b,d in word.pairs:term[d]=word.gauge[b]['frame']
mc={}
def meet(f,g):
  if f==g or C.sub(f,g):return f
  if C.sub(g,f):return g
  k=(f,g) if f<g else (g,f)
  if k not in mc:
    K,_=M.kernel(list(C.A[f])+list(C.A[g]),h);mc[k]=word.register(K)
  return mc[k]
nxt={}  # role -> upper bound from the future
U=[None]*len(ops)
for i in reversed(order):
  a,b,n=ops[i]
  ua=nxt.get(a,term.get(a,full));ub=nxt.get(b,term.get(b,full))
  U[i]=meet(ua,ub);nxt[a]=U[i];nxt[b]=U[i]
bad=sum(not C.sub(word.opframe[i],U[i]) for i in range(len(ops)))
nd=[i for i in range(len(ops)) if not C.nondeg(U[i])]
print('violations',bad,'degenerate',len(nd),'changed',sum(U[i]!=word.opframe[i] for i in range(len(ops))),time.time()-t0)
# starts: gauge/source frames within first op frame
start={b:word.w['source_frame'][x] for x,b in word.source.items()};start.update({b:z['frame'] for b,z in word.gauge.items()})
print('start violations',sum(1 for s,f in start.items() if s in nxt and not C.sub(f,nxt[s])))
old=word.opframe;word.opframe=U
try:
  r=word.row();print('max row W',r['W_per_vertex'],'def',r['deficit_per_vertex'])
  json.dump(dict(base=base['child_histogram'],new=r['child_histogram']),open('maxframe_hist.json','w'),default=str)
except Exception as e:print('row failed',e)
