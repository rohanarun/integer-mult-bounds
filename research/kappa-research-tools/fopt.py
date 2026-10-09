import sys,json,importlib.util,time,math,random,pickle
from collections import Counter,defaultdict
from pathlib import Path
sys.set_int_max_str_digits(0)
P=Path('/home/claude/crocswap/w200/research/paired-cube-diagonal-bit-168')
spec=importlib.util.spec_from_file_location('ad',P/'bit/word.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
word=m.Candidate();word.exact_frames();C=word.C;h=word.h;M=word.module
ops=word.ops;full=word.w['full_frame']
LOG=[0]+[d*math.log(72/d) for d in range(1,73)]
def g(d):return LOG[d] if d>0 else 0.0
# ---- frame algebra
jc={};mc={}
def sub(f,g_):return C.sub(f,g_)
def join(f,g_):
  if f is None:return g_
  if g_ is None or f==g_ or sub(g_,f):return f
  if sub(f,g_):return g_
  k=(f,g_) if f<g_ else (g_,f)
  if k not in jc:jc[k]=word.register(list(C.B[f])+list(C.B[g_]))
  return jc[k]
def meet(f,g_):
  if f==g_ or sub(f,g_):return f
  if sub(g_,f):return g_
  k=(f,g_) if f<g_ else (g_,f)
  if k not in mc:
    K,_=M.kernel(list(C.A[f])+list(C.A[g_]),h);mc[k]=word.register(K)
  return mc[k]
vc={}
def span(n):
  if n not in vc:
    bits=C.sup[n];rows=[]
    while bits:
      low=bits&-bits;s=low.bit_length()-1;bits-=low;rows.append(C.chi[s])
    vc[n]=word.register(rows) if rows else None
  return vc[n]
ndc={}
def nondeg(f):
  if f not in ndc:ndc[f]=C.nondeg(f)
  return ndc[f]
# ---- physical chains: list of slots; slot = ('op',i) or ('fix',frame)
seq=defaultdict(list)
for i,(a,b,x) in enumerate(ops):seq[a].append(('op',i));seq[b].append(('op',i))
rootframe={s:word.w['root_frame'][j] for j,s in enumerate(word.w['rootroles'])}
for s,f in rootframe.items():seq[s].append(('fix',f))
start={b:word.w['source_frame'][x] for x,b in word.source.items()};start.update({b:z['frame'] for b,z in word.gauge.items()})
recipient={d:b for b,d in word.pairs}
chains=[];chainstart=[]
for s in range(word.R):
  if s in word.donor:continue
  ch=list(seq[s])
  if s in recipient:b=recipient[s];ch+=[('fix',word.gauge[b]['frame'])]+seq[b]
  ch.append(('fix',full));chains.append(ch);chainstart.append(start.get(s))
F=list(word.opframe)
where=defaultdict(list)
for c,ch in enumerate(chains):
  for k,(t,r) in enumerate(ch):
    if t=='op':where[r].append((c,k))
assert all(len(v)==2 for v in where.values()) and len(where)==len(ops)
def fr(c,k):
  if k<0:return chainstart[c]
  t,r=chains[c][k];return F[r] if t=='op' else r
def dim(f):return 0 if f is None else C.dimf[f]
def chaincost(c):
  tot=0.0;prev=dim(chainstart[c])
  for k in range(len(chains[c])):
    d=dim(fr(c,k))
    if d>prev:tot+=g(d-prev)
    prev=max(prev,d)
  return tot
def total():return sum(chaincost(c) for c in range(len(chains)))
def hist():
  H=Counter()
  for c in range(len(chains)):
    prev=dim(chainstart[c])
    for k in range(len(chains[c])):
      d=dim(fr(c,k))
      if d>prev:H[d-prev]+=1
      prev=max(prev,d)
  return H
def local(i):
  """cost of the increments touching op i in both chains"""
  tot=0.0
  for c,k in where[i]:
    p=dim(fr(c,k-1));x=dim(F[i]);n=dim(fr(c,k+1)) if k+1<len(chains[c]) else x
    tot+=g(x-p)+g(n-x)
  return tot
def bounds(i):
  lo=span(ops[i][2]);hi=None
  for c,k in where[i]:
    lo=join(lo,fr(c,k-1))
    if k+1<len(chains[c]):
      nx=fr(c,k+1);hi=nx if hi is None else meet(hi,nx)
  return lo,hi
if __name__=='__main__':
  t0=time.time();base=total();H0=hist();print('base cost',round(base,2),sum(H0.values()),time.time()-t0,flush=True)
