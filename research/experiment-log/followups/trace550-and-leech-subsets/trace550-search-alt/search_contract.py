"""All-distance exact-commuting 2to3 trace search on PR550; no supplier edits."""
import json,gzip,sys,copy,math,bisect,time,hashlib
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter,defaultdict
O=Path(__file__).resolve().parent;ROOT=O.parent
sys.path.insert(0,str(ROOT/'source550-review/local/vendor/gk'))
import gk_word as g,gk_common as c
g.V=c.V=112;g.DATA=c.DATA=7168
src=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'pr550-independent314/local/candidate/FULL-WORD.json.gz';O=Path(sys.argv[2]) if len(sys.argv)>2 else O;raw=src.read_bytes();w=json.loads(gzip.decompress(raw));base=g.profile(w);n=224+w['report']['R'];A=len(w['A']);trace=w['A']+w['B'];stats=Counter();wins=[];start=time.monotonic()
def regs(e):return e[1:3] if e[0]=='add' else e[1:2]
def commute(e,f):return (e[1]!=f[2] and f[1]!=e[2]) if e[0]==f[0]=='add' else not(set(regs(e))&set(regs(f)))
chains=[[] for _ in range(n)]
for p,e in enumerate(trace):
 for r in regs(e):chains[r].append((p,g.basis(e[-1])))
initial=[((w['ports'][r],) if r<112 else g.basis(w.get('start_extra',{}).get(str(r),[]))) for r in range(n)]
final=[g.perp(w['ports'][r-112]) if 112<=r<224 else g.FULL for r in range(n)]
cache={}
def span(F):
 F=tuple(F)
 if F not in cache:cache[F]=g.span(F)
 return cache[F]
def hist(Fs):
 H=Counter();last=Fs[0]
 for f in Fs[1:]:
  if not span(last)<=span(f):return None
  if f!=last:H[len(f)-len(last)]+=1
  last=f
 return H
oldH=[hist([initial[r]]+[f for p,f in chains[r]]+[final[r]]) for r in range(n)]
assert all(H is not None for H in oldH)
def interval_frames(lo,hi,extras):
 dim=len(hi)-len(lo);pool={lo,hi}
 if dim<=3:
  sub={lo};todo=[lo]
  while todo:
   cur=todo.pop()
   for x in span(hi)-span(cur):
    nxt=g.basis((*cur,x))
    if nxt not in sub:sub.add(nxt);todo.append(nxt)
  return sorted(sub,key=lambda x:(len(x),x))
 stats['interval_dim_gt3_partial']+=1
 for f in extras:
  z=g.basis((*lo,*f))
  if span(z)<=span(hi):pool.add(z)
 return sorted(pool,key=lambda x:(len(x),x))
def exact(events,rs):
 pos={r:i for i,r in enumerate(rs)};rows=[{i:Q(1)} for i in range(3)]
 for e in events:
  _,t,s,a,b,_=e;t=pos[t];s=pos[s];q=Q(a,b)
  for j,x in rows[s].copy().items():
   z=rows[t].get(j,0)+q*x
   if z:rows[t][j]=z
   else:rows[t].pop(j,None)
 return rows
for section,events,off in [('A',w['A'],0),('B',w['B'],A)]:
 lookup=defaultdict(list);bytarget=defaultdict(list)
 for p,e in enumerate(events):
  if e[0]=='add':lookup[(e[1],e[2],Q(e[3],e[4]))].append(p);bytarget[e[1]].append(p)
 seen=set()
 for x,e in enumerate(events):
  if e[0]!='add':continue
  # e is i<-j; f is j<-k at arbitrary distance.
  i,j=e[1:3];a=Q(e[3],e[4])
  for y in bytarget[j]:
   f=events[y];k=f[2]
   if k==i:continue
   b=Q(f[3],f[4]);bridge=a*b if x<y else -a*b
   for z in lookup[(i,k,bridge)]:
    positions=tuple(sorted((x,y,z)))
    if positions in seen:continue
    seen.add(positions);stats['exact_coefficient_triples']+=1;old=[events[t] for t in positions];rs=(i,j,k)
    terms=[(j,k,b),(i,j,a)] if x<y else [(i,j,a),(j,k,b)]
    dummy=[['add',t,s,q.numerator,q.denominator,[]] for t,s,q in terms];assert exact(old,rs)==exact(dummy,rs)
    for direction,anchor_local in [('all_left',positions[0]),('all_right',positions[-1])]:
     ok=True
     for index in positions:
      interval=range(anchor_local,index) if direction=='all_left' else range(index+1,anchor_local+1)
      if not all(t in positions or commute(events[index],events[t]) for t in interval):ok=False;break
     if not ok:stats['commutation_rejected']+=1;continue
     stats['commuting_triples_directions']+=1;anchor=anchor_local+off;removed={t+off for t in positions};prev={};nxt={};newchains={}
     for r in rs:
      rem=[(p,F) for p,F in chains[r] if p not in removed];before=[F for p,F in rem if p<anchor];after=[F for p,F in rem if p>anchor];prev[r]=before[-1] if before else initial[r];nxt[r]=after[0] if after else final[r];newchains[r]=(before,after)
     t1,s1,_=terms[0];t2,s2,_=terms[1];lo1=g.basis((*prev[t1],*prev[s1]));hi1=g.basis(set.intersection(*(span(F) for F in nxt.values())));hi2=g.basis(span(nxt[t2])&span(nxt[s2]))
     if not span(lo1)<=span(hi1):stats['empty_first_interval']+=1;continue
     extras=[g.basis(e[-1]) for e in old]+list(prev.values())+list(nxt.values())
     for F1 in interval_frames(lo1,hi1,extras):
      lo2=g.basis((*F1,*prev[t2],*prev[s2]))
      if not span(lo2)<=span(hi2):stats['empty_second_interval']+=1;continue
      for F2 in interval_frames(lo2,hi2,extras):
       Fs=(F1,F2);stats['frame_assignments']+=1;delta=Counter()
       for r in rs:
        before,after=newchains[r];middle=[F for (t,s,q),F in zip(terms,Fs) if r in (t,s)];H=hist([initial[r],*before,*middle,*after,final[r]]);assert H is not None;delta.update(H);delta.subtract(oldH[r])
       delta={r:z for r,z in delta.items() if z};fee=sum(z*r*((73/r)**.0015935194192823068-1) for r,z in delta.items())
       if fee>=-1e-11:continue
       new=[['add',t,s,q.numerator,q.denominator,list(F)] for (t,s,q),F in zip(terms,Fs)];u=copy.deepcopy(w);modified=[]
       for p,e in enumerate(events):
        if p==anchor_local:modified.extend(new)
        if p not in positions:modified.append(e)
       u[section]=modified;u['cleanup']=[g.inverse(e,g.FULL) for e in reversed(u['A']+u['B']) if not 112<=e[1]<224]
       try:H=g.profile(u)
       except AssertionError:stats['full_profile_rejected']+=1;continue
       actual=Counter(H);actual.subtract(base);assert {r:z for r,z in actual.items() if z}==delta
       stats['positive_full_profile_nominations']+=1;win={'section':section,'positions':positions,'direction':direction,'registers':rs,'old':old,'new':new,'delta':delta,'fee_delta':fee,'profile':dict(H),'scalar_3x3_exact':True};index=len(wins);wins.append(win);u['report']['local_profile']=dict(H);(O/f'contract-candidate-{index:03d}.json.gz').write_bytes(g.dump(u));print('GAIN',json.dumps(win),flush=True)
 print(section,dict(stats),time.monotonic()-start,flush=True)
(O/'CONTRACT-RESULT.json').write_text(json.dumps({'status':'COMPLETE_ALL_DISTANCE_THREE_TO_TWO_SCREEN','stats':dict(stats),'nominations':wins,'seconds':time.monotonic()-start,'scope':'Exact coefficient and3x3identity triples; all-left/all-right exact commuting gathers; nested two-frame intervals exhaustive quotientdim<=3, larger intervals selected frames only; no physical admission.'},indent=2)+'\n')
