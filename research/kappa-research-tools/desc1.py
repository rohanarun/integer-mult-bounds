from fopt import *
def cands(i):
  lo,hi=bounds(i);S={lo,hi}
  for c,k in where[i]:
    S.add(fr(c,k-1))
    if k+1<len(chains[c]):S.add(fr(c,k+1))
  return [f for f in S if f is not None and sub(lo,f) and sub(f,hi) and nondeg(f)]
t0=time.time();cur=total();print('start',round(cur,2),flush=True)
for it in range(20):
  imp=0;order=list(range(len(ops)));random.Random(it).shuffle(order)
  for i in order:
    old=F[i];best=local(i);bf=old
    for f in cands(i):
      F[i]=f;v=local(i)
      if v<best-1e-9:best,bf=v,f
    F[i]=bf
    if bf!=old:imp+=1
  cur=total();print(it,'moves',imp,'cost',round(cur,2),round(time.time()-t0),flush=True)
  if not imp:break
pickle.dump(F,open('F_desc1.pkl','wb'))
