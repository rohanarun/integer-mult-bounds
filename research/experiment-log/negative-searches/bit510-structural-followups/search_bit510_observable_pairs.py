"""Exact F2 suffix-response retarget screen on the R480 bit circuit.
Same-frame whole-gate retargeting and zero-response deletions; discovery only.
Prepared for rohanarun with OpenAI Codex assistance. Apache-2.0.
"""
from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction as Q
import gzip,json,math,time,copy,hashlib
import sympy as S
R=Path(__file__).resolve().parent;O=R/'bit510-observable-pairs';O.mkdir(exist_ok=False);t=time.monotonic();p=R/'bit510-review/research/e8-r480-dead-totals/data/bitE8mut-r480.json.gz';w=json.load(gzip.open(p));v=w['v'];n=2*v+w['R'];Zregs=list(range(v))+list(range(2*v,n));mask=[sum(1<<i for i in f)for f in w['frames']];dims=[S.Matrix([w['lines'][i]for i in f]).rank()if f else 0 for f in w['frames']];le=lambda a,b:mask[a]&mask[b]==mask[a];full=next(i for i,d in enumerate(dims)if d==8);fee=lambda k:k*math.expm1(.001587447108*math.log(64/k))if k else 0
original=copy.deepcopy(w);moves=[];trials=Counter();best_negative=[]
def scalar(word):
 z=[1<<r for r in range(n)]
 for sec in ['D','A','B','C']:
  if sec=='B':
   held=[z[r]for r in word['ret']]
   for j,cs in enumerate(word['scatter']):
    for c in cs:z[v+j]^=held[c]
  for f,d,ss in word[sec]:
   for s in ss:z[d]^=z[s]
 assert all(z[r]==((1<<r)|(1<<(r-v))if v<=r<2*v else 1<<r)for r in range(n))
def profiles(word):
 cur=list(word['start']);h=Counter()
 def go(r,f):
  a=cur[r];assert le(a,f)
  if a!=f:h[int(dims[f]-dims[a])]+=1;cur[r]=f
 for sec in ['D','A','B','C']:
  if sec=='B':
   for r in word['ret']:go(r,full);h[8]+=1
  for f,d,ss in word[sec]:
   for r in [d]+ss:go(r,f)
 for r,f in enumerate(word['final']):go(r,f)
 return h
base=profiles(w);scalar(w)
# Delete all zero-target-response instructions together; individually neutral deletions
# may expose a frame transition only after the whole dead segment disappears.
resp=[0]*n
for j in range(v):resp[v+j]=1<<j
for f,d,ss in reversed(w['B']):
 for q in ss:resp[q]^=resp[d]
for j,cs in enumerate(w['scatter']):
 for c in cs:resp[w['ret'][c]]^=resp[v+j]
dead=[]
for i in reversed(range(len(w['A']))):
 f,d,ss=w['A'][i]
 if resp[d]==0:dead.append(i)
 for q in ss:resp[q]^=resp[d]
oldA=copy.deepcopy(w['A']);deadset=set(dead);w['A']=[g for i,g in enumerate(w['A'])if i not in deadset]
w['C']=[[full,d,list(ss)]for f,d,ss in reversed(w['A'])];scalar(w);sliced=profiles(w)
used=set(w['ret'])
for sec in ['D','A','B','C']:
 for f,d,ss in w[sec]:used.update([d]+ss)
unused=sorted(set(range(2*v,n))-used)
slice_record=dict(removed_indices=sorted(dead),removed_gates=[oldA[i]for i in sorted(dead)],old_profile=dict(base),sliced_profile=dict(sliced),unused_helpers=unused)
(O/'SLICE.json').write_text(json.dumps(slice_record,indent=2)+'\n');print('SIMULTANEOUS_SLICE',len(dead),dict(sliced),'unused',unused,flush=True)
# Group equal rank-one changes in the final target matrix.
resp=[0]*n
for j in range(v):resp[v+j]=1<<j
for f,d,ss in reversed(w['B']):
 for q in ss:resp[q]^=resp[d]
for j,cs in enumerate(w['scatter']):
 for c in cs:resp[w['ret'][c]]^=resp[v+j]
suffix=[]
for f,d,ss in reversed(w['A']):
 suffix.append(resp[d])
 for q in ss:resp[q]^=resp[d]
suffix.reverse();z=[1<<r for r in range(n)];groups=defaultdict(list)
for i,(f,d,ss)in enumerate(w['A']):
 inp=0
 for q in ss:inp^=z[q]
 if suffix[i] and inp:groups[(suffix[i],inp)].append(i)
 z[d]^=inp
import itertools
candidates=[(i,j)for ids in groups.values()for i,j in itertools.combinations(ids,2)]
records=[];best=None;H0=profiles(w);fee0=sum(fee(r)*c for r,c in H0.items())
for i,j in candidates:
 trial=copy.deepcopy(w);trial['A']=[g for k,g in enumerate(w['A'])if k not in (i,j)];trial['C']=[[full,d,list(ss)]for f,d,ss in reversed(trial['A'])]
 row=dict(indices=[i,j])
 try:scalar(trial);hh=profiles(trial)
 except AssertionError:row['status']='REJECT_SECOND_ORDER_OR_FRAME_INTERACTION'
 else:
  delta=sum(fee(r)*c for r,c in hh.items())-fee0;row.update(status='PASS_SCALAR_AND_FRAME',profile=dict(hh),fee_delta=delta)
  if delta < -1e-12 and (best is None or delta<best[0]):best=(delta,trial,row)
 records.append(row)
if best:
 (O/'WORD.json.gz').write_bytes(gzip.compress(json.dumps(best[1],sort_keys=True,separators=(',',':')).encode(),mtime=0))
res=dict(status='COMPLETE_SCOPED_OBSERVABLE_TWO_GATE_SCREEN',source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),slice_count=len(dead),equal_rank_one_effect_pairs=len(candidates),records=records,profitable=sum(x.get('fee_delta',0)<-1e-12 for x in records),best=best[2]if best else None,seconds=time.monotonic()-t,scope='Pairs of whole A gates with identical nonzero rank-one target-matrix effects on the simultaneously sliced word. Each removal pair checked by fresh720-column F2 replay and nested frames. Equal first-order effects alone do not prove joint deletion; exact replay tests cross terms. No arbitrary pairs, wider rewrites, physical emission or exponent claim.')
(O/'RESULT.json').write_text(json.dumps(res,indent=2)+'\n');print({k:v for k,v in res.items()if k!='records'},flush=True)
