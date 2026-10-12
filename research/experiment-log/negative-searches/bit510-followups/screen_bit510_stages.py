"""Whole-width8 idle-hosting stage screen; pricing candidates, not operator certificates."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
import json,sys,math,time,importlib.util
R=Path(__file__).resolve().parent;O=R/'bit510-stage-screen';O.mkdir(exist_ok=False);V=R/'bit510-review/research/e8-r480-nine-stage/vendor';sys.path.insert(0,str(V/'e8-r715-eleven-stage-whole/code'));import hosting_k as HK
spec=importlib.util.spec_from_file_location('mom',V/'e8-r740-replica32/code/engines/moment.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
base=json.load(open(R/'bit510-review/research/e8-r480-nine-stage/EXPECTED.json'))['nine'];c=Q(base['bit_lower']);HK.cost=lambda r,m:r*math.expm1(float(c)*math.log(m/r))if r else 0
local=Counter({1:1200,2:1440,4:180,6:120,8:9});rows=[];T=32
def schedule(K):
 ev=[dict(kind='local',stage=0,pair=0)];s=1
 for j in range(K):
  ev.append(dict(kind='local',stage=s,pair=j));s+=1
  if j<K-1:ev.append(dict(kind='bridge',dst=j,src=j+1))
  ev.append(dict(kind='local',stage=s,pair=j));s+=1
  if j<K-1:ev.append(dict(kind='bridge',dst=j,src=j+1))
 for j in reversed(range(K-1)):ev.append(dict(kind='bridge',dst=j+1,src=j))
 out=[];idx=0
 for e in ev:
  out.append(e)
  if e['kind']!='local':continue
  s=e['stage'];idle=[]
  if s%2 and s<=2*K-3:idle=[((s+1)//2,7*(s+1))]
  elif s%2==0 and 2<=s<=2*K-2:idle=[(s//2,7)]
  elif s==2*K:idle=[(j,14*(K-1-j))for j in range(K)]
  for p,r in idle:out.append(dict(kind='idle',pair=p,rank=r,idx=idx));idx+=1
 return out
for L in range(5,32,2):
 t=time.monotonic();K=(L-1)//2;m=1+7*L;W=2*K*120*T;sc=schedule(K);win={i:x for i,x in HK.windows(sc).items()if x[1]>0 and x[2]};row=dict(stages=L,m=m,live=W)
 try:
  ys,zs,val=HK.solve(win,240,{(s,8):480 for s in range(L)},m,host_all=True,maxk=m//8,time_limit=20)
  # Check literal pattern capacities and stage assignment equalities independently.
  for i,(p,r,st)in win.items():
   assert sum(n for (ii,pat),n in ys.items()if ii==i)==240
   assert all(sum(pat)<=r for (ii,pat),n in ys.items()if ii==i)
   assert sum(len(pat)*n for (ii,pat),n in ys.items()if ii==i)==sum(n for(ii,w,s),n in zs.items()if ii==i)
  for s in range(L):assert sum(n for(i,w,ss),n in zs.items()if ss==s)==480
  assert all(s in win[i][2]and w==8 for i,w,s in zs)
  H=Counter({r:n*L*T for r,n in local.items()})
  for e in sc:
   if e['kind']!='idle' or not e['rank']:continue
   i=e['idx'];rank=e['rank']
   if i in win:
    for(ii,pat),n in ys.items():
     if ii==i and rank>sum(pat):H[rank-sum(pat)]+=n*T
   else:H[rank]+=240*T
  assert m*W-sum(r*n for r,n in H.items())==T*(2*K*120-72*L)
  if L==9:assert dict(sorted(H.items()))=={int(k):v for k,v in base['profile'].items()}
  cert=M.certify(H,m,W,True);row.update(status='PASS_AGGREGATE_PATTERN_AND_EXACT_PRICE_ONLY',profile=dict(sorted(H.items())),lower=cert['lower'],beats_bit510=Q(cert['lower'])>c,patterns=[[i,list(p),n]for(i,p),n in ys.items()],assignments=[[i,w,s,n]for(i,w,s),n in zs.items()])
 except AssertionError as e:row.update(status='INFEASIBLE_OR_UNRESOLVED_MODEL',error=repr(e))
 row['seconds']=time.monotonic()-t;rows.append(row);(O/'RESULT.json').write_text(json.dumps(dict(results=rows,scope='Fixed R480 word, odd stage recipe and per-replica width8 whole-owner aggregate model. Exact pricing and integer constraints, no emitted physical certificate or all-size theorem claim.'),indent=2)+'\n');print({k:v for k,v in row.items()if k not in ('profile','patterns','assignments')},flush=True)
