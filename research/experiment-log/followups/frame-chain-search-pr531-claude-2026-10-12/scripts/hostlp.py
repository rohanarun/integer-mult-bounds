from ortools.sat.python import cp_model
from price import price
import json
CUR={int(k):v for k,v in json.load(open('/tmp/v531/hosted/HOSTED.json'))['global_profile'].items()}
LOC={1:2028,2:752,3:156,4:392,5:56,6:56,7:8}
def host(n8,n9,n7=0,b=0.00152):
  f=lambda r: r*((73/r)**b-1) if r else 0
  ranks=[8,16,32,48];cnt=[672*8,448*8,448*8,448*8]
  pats=[(r,a,c,e,r-8*a-9*c-7*e) for r in ranks for c in range(r//9+1) for a in range((r-9*c)//8+1) for e in range((r-9*c-8*a)//7+1 if n7 else 1)]
  m=cp_model.CpModel();x=[m.NewIntVar(0,30000,'') for p in pats]
  for r,c in zip(ranks,cnt): m.Add(sum(x[i] for i,p in enumerate(pats) if p[0]==r)==c)
  m.Add(sum(x[i]*p[1] for i,p in enumerate(pats))==n8*72); m.Add(sum(x[i]*p[2] for i,p in enumerate(pats))==n9*72); m.Add(sum(x[i]*p[3] for i,p in enumerate(pats))==n7*72)
  m.Minimize(sum(x[i]*int(f(p[4])*1e9) for i,p in enumerate(pats)))
  s=cp_model.CpSolver();s.parameters.max_time_in_seconds=20;s.parameters.num_workers=8;st=s.Solve(m)
  if st not in (cp_model.OPTIMAL,cp_model.FEASIBLE): return None
  rem={}
  for i,p in enumerate(pats):
    v=s.Value(x[i])
    if v and p[4]: rem[p[4]]=rem.get(p[4],0)+v
  return rem
REM0=host(152,352)
def full(loc,n8,n9,n7=0):
  rem=host(n8,n9,n7)
  if rem is None: return None
  P=dict(CUR)
  for k,v in LOC.items(): P[k]-=72*v
  for k,v in REM0.items(): P[k]-=v
  for k,v in loc.items(): P[k]=P.get(k,0)+72*v
  for k,v in rem.items(): P[k]=P.get(k,0)+v
  assert min(P.values())>=0,P
  return {k:v for k,v in P.items() if v}
if __name__=='__main__':
  print('REM0',REM0)
  base=price(CUR);print('base',base, price(full(LOC,152,352)))
  for d in [1,4,16]:
    L=dict(LOC);L[1]+=d
    P=full(L,152+d,352-d);print(d,'w9->w8 +d rank1', (price(P)-base)/base*100)
    L=dict(LOC);L[2]+=d
    P=full(L,152+2*d,352-2*d);print(d,'2x w9->w8 +d rank2', (price(P)-base)/base*100)
