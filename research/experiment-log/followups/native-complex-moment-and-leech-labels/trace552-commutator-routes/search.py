"""Bounded contiguous one-add to four-add commutator routes on exact PR552."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from functools import lru_cache
import sys,os,json,gzip,time,bisect,hashlib,copy,math
P=Path(__file__).resolve().parent;R=P.parent;assert os.path.ismount('/Volumes/SP AI 01_16') and os.access(P,os.W_OK)
sys.path.insert(0,str(R/'source550-review/local/vendor/gk'));import gk_word as g;g.V=112
src=R/'pr552-independent314/complex-local/weighted/FULL-WORD.json.gz';raw=src.read_bytes();w=json.loads(gzip.decompress(raw));base=g.profile(w);n=224+w['report']['R'];A=len(w['A']);events=w['A']+w['B'];cost=lambda d:d*math.expm1(.001594507308884431019637*math.log(73/d))+32*73**2*73**.001594507308884431019637/10**16 if d else 0
@lru_cache(None)
def span(F):return frozenset(g.span(F))
@lru_cache(None)
def bits(F):return sum(1<<z for z in span(F))
@lru_cache(None)
def join(F,G):return g.basis((*F,*G))
def meet(F,G):return g.basis(span(F)&span(G))
def sub(F,G):return bits(F)&~bits(G)==0
stats=Counter();wins=[];errors=[];started=time.monotonic()
@lru_cache(None)
def spaces(L,U):
 assert sub(L,U);d=len(U)-len(L)
 if d>3:
  stats['partial_large_quotient_intervals']+=1
  return tuple(sorted({L,U}|{F for F in catalog if sub(L,F) and sub(F,U)},key=lambda x:(len(x),x)))
 seen={L};todo=[L]
 while todo:
  F=todo.pop()
  for z in span(U)-span(F):
   H=g.basis((*F,z))
   if H not in seen:seen.add(H);todo.append(H)
 return tuple(sorted(seen,key=lambda x:(len(x),x)))

def regs(e):return e[1:3] if e[0]=='add' else e[1:2]
chains=[[] for _ in range(n)]
for r in range(n):chains[r].append((-1,(w['ports'][r],) if r<112 else g.basis(w.get('start_extra',{}).get(str(r),[])),'fixed'))
for p,e in enumerate(events):
 if p==A:
  for r,F in zip(w['centers'],w['center_frames']):chains[r].append((p-.5,g.basis(F),'anchor'))
  for t in range(112):chains[112+t].append((p-.5,g.basis(w.get('target_levels',{}).get(str(t),[])),'anchor'))
 for r in regs(e):chains[r].append((p,g.basis(e[-1]),'event'))
for r in range(n):chains[r].append((len(events),g.perp(w['ports'][r-112]) if 112<=r<224 else g.FULL,'fixed'))
positions=[[t for t,F,k in ch] for ch in chains];catalog={F for ch in chains for t,F,k in ch}
def bounds(r,p,remove):
 ix=bisect.bisect_left(positions[r],p);before=chains[r][ix-1];after=chains[r][ix+1 if remove else ix];return before[1],after[1],after[2]
def matrix(word):
 M=[[Q(i==j) for j in range(3)] for i in range(3)]
 for t,s,k in word:M[t]=[x+k*y for x,y in zip(M[t],M[s])]
 return M
controls=[]
for k in [Q(1),Q(-1),Q(3,2),Q(-5,8)]:
 for u in [Q(1),Q(-2),Q(1,4)]:
  v=k/u
  for order,ops in [('ab-first',[(0,1,u),(1,2,-v),(0,1,-u),(1,2,v)]),('bc-first',[(1,2,v),(0,1,u),(1,2,-v),(0,1,-u)])]:
   assert matrix(ops)==matrix([(0,2,k)]);bad=list(ops);t,s,q=bad[-1];bad[-1]=(t,s,-q);assert matrix(bad)!=matrix([(0,2,k)]);controls.append(dict(k=str(k),u=str(u),order=order,all_arbitrary_dirt_columns_exact=True,wrong_sign_rejected=True))
(P/'EXACT-CONTROLS.json').write_text(json.dumps(controls,indent=2)+'\n')
# Most expensive endpoint profile transitions first, with deterministic index tie break.
ranked=[]
for p,e in enumerate(events):
 if e[0]!='add':continue
 F=g.basis(e[-1]);bd=[bounds(r,p,True) for r in regs(e)];old=sum(cost(len(F)-len(lo))+cost(len(hi)-len(F)) for lo,hi,kind in bd);ranked.append((-old,p))
ranked.sort();selected=ranked[:384]
for gate_no,(_,p) in enumerate(selected):
 if time.monotonic()-started>150:stats['time_budget_stop']=1;break
 e=events[p];a,c=e[1:3];k=Q(e[3],e[4]);F=g.basis(e[-1]);ca=bounds(a,p,True);cc=bounds(c,p,True);stats['gates_screened']+=1
 helpers=[]
 for breg in range(224,n):
  if breg in (a,c):continue
  cb=bounds(breg,p,False);L=join(join(ca[0],cc[0]),cb[0]);U=meet(meet(ca[1],cc[1]),cb[1]);stats['helper_intervals_screened']+=1
  if not sub(L,U):continue
  helpers.append((len(U)-len(L),-len(cb[0]),breg,cb));stats['compatible_helper_intervals']+=1
 helpers.sort();stats['warm_helpers_selected']+=min(12,len(helpers))
 for _,__,breg,cb in helpers[:12]:
  old=sum(cost(len(F)-len(lo))+cost(len(hi)-len(F)) for lo,hi,typ in (ca,cc))+cost(len(cb[1])-len(cb[0]))
  for order in [0,1]:
   # The first/third endpoint is x; the second/fourth endpoint is z.
   x,z=(a,c) if order==0 else (c,a);bx,bz=(ca,cc) if order==0 else (cc,ca);L1=join(bx[0],cb[0]);Lall=join(L1,bz[0]);Uall=meet(meet(bx[1],cb[1]),bz[1]);Ulast=meet(cb[1],bz[1]);assert sub(Lall,Uall)
   first=spaces(L1,Uall);mid=spaces(Lall,Uall);last=spaces(Lall,Ulast);best=None;count=0
   for f1 in first:
    d1=len(f1);part1=cost(d1-len(bx[0]))+cost(d1-len(cb[0]))
    for f2 in mid:
     if not sub(f1,f2):continue
     d2=len(f2);part2=part1+cost(d2-d1)+cost(d2-len(bz[0]))
     for f3 in mid:
      if not sub(f2,f3) or (bx[2]=='anchor' and f3!=bx[1]):continue
      d3=len(f3);part3=part2+cost(d3-d1)+cost(d3-d2)+cost(len(bx[1])-d3)
      for f4 in last:
       if not sub(f3,f4) or (cb[2]=='anchor' and f4!=cb[1]) or (bz[2]=='anchor' and f4!=bz[1]):continue
       d4=len(f4);fee=part3+cost(d4-d3)+cost(d4-d2)+cost(len(cb[1])-d4)+cost(len(bz[1])-d4)-old;count+=1
       if best is None or fee<best[0]:best=(fee,(f1,f2,f3,f4))
   stats['nested_frame_assignments']+=count;stats['helper_orientations']+=1
   if best is None:stats['no_legal_frame_assignment']+=1;continue
   if best[0]>=-1e-11:continue
   stats['positive_local_fee_nominations']+=1;fee,Fs=best
   rawops=[(a,breg,Q(1)),(breg,c,-k),(a,breg,Q(-1)),(breg,c,k)] if order==0 else [(breg,c,k),(a,breg,Q(1)),(breg,c,-k),(a,breg,Q(-1))]
   new=[['add',t,s,q.numerator,q.denominator,list(F)] for (t,s,q),F in zip(rawops,Fs)];u=copy.deepcopy(w);sec='A' if p<A else 'B';ix=p if p<A else p-A;u[sec][ix:ix+1]=new
   try:prof=g.profile(u)
   except AssertionError as err:errors.append(dict(p=p,b=breg,order=order,fee=fee,error=str(err)));stats['full_profile_rejected']+=1;continue
   actual=sum(n*cost(r) for r,n in prof.items())-sum(n*cost(r) for r,n in base.items());assert abs(actual-fee)<1e-9
   u['cleanup']=[g.inverse(v,g.FULL) for v in reversed(u['A']+u['B']) if not 112<=v[1]<224];u['report']['local_profile']=dict(prof);fn=f'CANDIDATE-{len(wins):03d}.json.gz';(P/fn).write_bytes(g.dump(u));row=dict(p=p,section=sec,index=ix,helper=breg,order=order,fee_delta=actual,old=e,new=new,profile=dict(prof),candidate=fn);wins.append(row);print('GAIN',json.dumps(row),flush=True)
 if gate_no%24==0:print('PROGRESS',gate_no,dict(stats),time.monotonic()-started,flush=True)
result=dict(status='BOUNDED_CONTIGUOUS_COMMUTATOR_SCREEN_COMPLETE',source_pr552_head='33c33af0b7697155be1ea708e08cbd3f0707d94c',source_sha256=hashlib.sha256(raw).hexdigest(),stats=dict(stats),nominations=wins,rejected_nominations=errors,seconds=time.monotonic()-started,scope='Top384 endpoint-fee gates, up to12 warm compatible existing helpers each, two commutator orientations, fixed contiguous location. Nested frame intervals complete through quotient dimension3; larger intervals use existing frame catalog and endpoints only. Coefficients use u=1,v=k, with general signed dyadic identity controls. Full profile checked only positive nominations; all require independent physical/exact price admission.')
(P/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
