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
 if dim<=4:
  sub={lo};todo=[lo]
  while todo:
   cur=todo.pop()
   for x in span(hi)-span(cur):
    nxt=g.basis((*cur,x))
    if nxt not in sub:sub.add(nxt);todo.append(nxt)
  return sorted(sub,key=lambda x:(len(x),x))
 stats['interval_dim_gt4_partial']+=1
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
 bysource=defaultdict(list);bytarget=defaultdict(list)
 for q,e in enumerate(events):
  if e[0]=='add':bysource[e[2]].append(q);bytarget[e[1]].append(q)
 for p,e in enumerate(events):
  if e[0]!='add':continue
  candidates=set(bysource[e[1]])|set(bytarget[e[2]])
  for q in sorted(x for x in candidates if x>p):
   f=events[q]
   if e[1]==f[2] and e[2]!=f[1]:
    # j+=b*k then i+=a*j
    j,k=e[1:3];i=f[1];b=Q(e[3],e[4]);a=Q(f[3],f[4]);terms=[(i,j,a),(i,k,a*b),(j,k,b)]
   elif e[2]==f[1] and e[1]!=f[2]:
    # i+=a*j then j+=b*k
    i,j=e[1:3];k=f[2];a=Q(e[3],e[4]);b=Q(f[3],f[4]);terms=[(j,k,b),(i,j,a),(i,k,-a*b)]
   else:continue
   stats['algebraic_pairs']+=1;rs=(i,j,k);P=p+off;QQ=q+off
   for direction,anchor,moving in [('later_left',P,f),('earlier_right',QQ,e)]:
    if not all(commute(moving,z) for z in events[p+1:q]):stats['commutation_rejected']+=1;continue
    stats['commuting_pairs_directions']+=1
    prev=[];nxt=[];newchains={}
    for r in rs:
     rem=[(x,F) for x,F in chains[r] if x not in (P,QQ)];before=[F for x,F in rem if x<anchor];after=[F for x,F in rem if x>anchor];prev.append(before[-1] if before else initial[r]);nxt.append(after[0] if after else final[r]);newchains[r]=(before,after)
    prevmap=dict(zip(rs,prev));nextmap=dict(zip(rs,nxt));upperall=g.basis(set.intersection(*(span(F) for F in nxt)))
    t1,s1,_=terms[0];t2,s2,_=terms[1];t3,s3,_=terms[2]
    lo1=g.basis((*prevmap[t1],*prevmap[s1]));loall=g.basis(x for F in prev for x in F)
    if not span(lo1)<=span(upperall) or not span(loall)<=span(upperall):stats['empty_interval']+=1;continue
    upperlast=g.basis(span(nextmap[t3])&span(nextmap[s3]))
    assignments=[]
    extras=[g.basis(e[-1]),g.basis(f[-1]),*prev,*nxt]
    for F1 in interval_frames(lo1,upperall,extras):
     lo2=g.basis((*F1,*loall))
     for F2 in interval_frames(lo2,upperall,extras):
      for F3 in interval_frames(F2,upperlast,extras):assignments.append((F1,F2,F3))
    for Fs in assignments:
     stats['frame_assignments']+=1;delta=Counter()
     for r in rs:
      before,after=newchains[r];middle=[F for (t,s,q),F in zip(terms,Fs) if r in (t,s)];H=hist([initial[r],*before,*middle,*after,final[r]])
      assert H is not None
      delta.update(H);delta.subtract(oldH[r])
     delta={r:z for r,z in delta.items() if z};fee=sum(z*r*((73/r)**.0015935194192823068-1) for r,z in delta.items())
     if fee>=-1e-11:continue
     new=[['add',t,s,z.numerator,z.denominator,list(F)] for (t,s,z),F in zip(terms,Fs)];assert exact([e,f],rs)==exact(new,rs)
     u=copy.deepcopy(w)
     if direction=='later_left':u[section]=events[:p]+new+events[p+1:q]+events[q+1:]
     else:u[section]=events[:p]+events[p+1:q]+new+events[q+1:]
     u['cleanup']=[g.inverse(z,g.FULL) for z in reversed(u['A']+u['B']) if not 112<=z[1]<224]
     try:H=g.profile(u)
     except AssertionError as err:stats['full_profile_rejected']+=1;continue
     actual=Counter(H);actual.subtract(base);actual={r:z for r,z in actual.items() if z};assert delta==actual
     stats['positive_full_profile_nominations']+=1
     win={'section':section,'positions':[p,q],'direction':direction,'registers':rs,'old':[e,f],'new':new,'delta':delta,'fee_delta':fee,'profile':dict(H),'distance':q-p,'scalar_3x3_exact':True}
     index=len(wins);wins.append(win);u['report']['local_profile']=dict(H);(O/f'chain4-candidate-{index:03d}.json.gz').write_bytes(g.dump(u));print('GAIN',json.dumps(win),flush=True)
 print(section,dict(stats),time.monotonic()-start,flush=True)
result={'status':'COMPLETE_ALL_DISTANCE_TWO_TO_THREE_SCREEN','source_sha256':hashlib.sha256(raw).hexdigest(),'source_pr550_head':'c7337040822978f1611ce9d9d44e7bb96d887e23','stats':dict(stats),'nominations':wins,'seconds':time.monotonic()-start,'scope':'Both exact-commuting placements for all algebraic pairs; distinct nested replacement frames, exhaustive intervals through quotient dimension4. Positive full gk.profile candidates still require independent scalar/physical/price admission.'};(O/'CHAIN4-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
