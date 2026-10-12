import json,itertools
from ortools.linear_solver import pywraplp
from price import price
b=0.00152
f=lambda r: r*((73/r)**b-1) if r else 0
ranks=[8,16,32,48];cnt=[672,448,448,448];dem={9:352*9,8:152*9}
pats=[]
for r in ranks:
  for n9 in range(r//9+1):
    for n8 in range((r-9*n9)//8+1):
      pats.append((r,n8,n9,r-8*n8-9*n9))
s=pywraplp.Solver.CreateSolver('GLOP');x=[s.NumVar(0,s.infinity(),'') for p in pats]
for r,c in zip(ranks,cnt): s.Add(sum(x[i] for i,p in enumerate(pats) if p[0]==r)==c)
s.Add(sum(x[i]*p[1] for i,p in enumerate(pats))==dem[8]); s.Add(sum(x[i]*p[2] for i,p in enumerate(pats))==dem[9])
s.Minimize(sum(x[i]*f(p[3]) for i,p in enumerate(pats)));s.Solve()
sol={pats[i]:x[i].solution_value() for i in range(len(pats)) if x[i].solution_value()>1e-9}
print(sol)
rem={}
for p,v in sol.items():
  if p[3]: rem[p[3]]=rem.get(p[3],0)+8*v
print('remainders x8 replicas',rem)
loc={1:2028,2:752,3:156,4:392,5:56,6:56,7:8}
P={k:72*v for k,v in loc.items()};P[32]=1
for k,v in rem.items(): P[k]=P.get(k,0)+v
cur={int(k):v for k,v in json.load(open('/tmp/v531/hosted/HOSTED.json'))['global_profile'].items()}
print('cur rem',{k:cur[k]-72*loc.get(k,0) for k in cur})
# fractional pricing: scale by 2
import math
P2={k:round(2*v) for k,v in P.items()}
print('ceiling b (x2 scaled approx)',price(P2,73,2*7168), 'cur',price(cur))
