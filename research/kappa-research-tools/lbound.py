from fopt import *
order=word.phase1+word.rest
# global L (forward, minimal) and U (backward, maximal) per op, on physical chains
L=[None]*len(ops);U=[None]*len(ops)
pos={}
for c,ch in enumerate(chains):
  for k,(t,r) in enumerate(ch):
    if t=='op':pos.setdefault(r,[]).append((c,k))
# forward: process ops in execution order; prev element frame on chain
def prevL(c,k):
  # nearest previous slot frame under L
  if k==0:return chainstart[c]
  t,r=chains[c][k-1]
  return L[r] if t=='op' else join(r, prevL(c,k-1)) if False else (r if t=='fix' else None)
for i in order:
  f=span(ops[i][2])
  for c,k in where[i]:
    if k==0:f=join(f,chainstart[c])
    else:
      t,r=chains[c][k-1];f=join(f,L[r] if t=='op' else r)
  L[i]=f
for i in reversed(order):
  f=None
  for c,k in where[i]:
    if k+1<len(chains[c]):
      t,r=chains[c][k+1];x=U[r] if t=='op' else r
      f=x if f is None else meet(f,x)
  U[i]=f
assert all(sub(L[i],F[i]) and sub(F[i],U[i]) for i in range(len(ops)))
print('L,U ok',flush=True)
lb=0.0;cur=0.0;inc=0
for c,ch in enumerate(chains):
  Ls=[];Us=[]
  for t,r in ch:
    if t=='op':Ls.append(L[r]);Us.append(U[r])
    else:Ls.append(r);Us.append(r)
  n=len(ch);J=[None]*n;Mx=[None]*n;j=chainstart[c]
  for k in range(n):j=join(j,Ls[k]);J[k]=j
  mm=Us[-1]
  for k in range(n-1,-1,-1):mm=meet(mm,Us[k]);Mx[k]=mm
  d0=dim(chainstart[c]);best=[math.inf]*(n+1);best[0]=0.0
  for k1 in range(n):
    if best[k1]==math.inf:continue
    base=dim(J[k1-1]) if k1>0 else d0
    for k2 in range(k1,n):
      if not sub(J[k2],Mx[k1]):break
      v=best[k1]+g(dim(J[k2])-base)
      if v<best[k2+1]:best[k2+1]=v
  lb+=best[n];cur+=chaincost(c)
print('current',round(cur,1),'per-chain relaxation lower bound',round(lb,1),'ratio',lb/cur)
