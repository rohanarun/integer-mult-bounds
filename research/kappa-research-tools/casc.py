import sys
exec(open('lbound.py').read().split("lb=0.0")[0])
import pickle
def cur(j,ch):return ch.get(j,F[j])
def frc(c,k,ch):
  if k<0:return chainstart[c]
  t,r=chains[c][k];return cur(r,ch) if t=='op' else r
def raise_(i,X):
  ch={};q=[(i,X)]
  while q:
    j,X=q.pop();o=cur(j,ch);nf=join(o,X)
    if nf==o:continue
    if not nondeg(nf):return None
    ch[j]=nf
    for c,k in where[j]:
      if k+1<len(chains[c]):
        t,r=chains[c][k+1]
        if t=='op':
          if not sub(nf,cur(r,ch)):q.append((r,nf))
        elif not sub(nf,r):return None
      if len(ch)>400:return None
  return ch
def lower_(i,Y):
  ch={};q=[(i,Y)]
  while q:
    j,Y=q.pop();o=cur(j,ch);nf=meet(o,Y)
    if nf==o:continue
    if not sub(span(ops[j][2]) or nf,nf) or not nondeg(nf):return None
    ch[j]=nf
    for c,k in where[j]:
      if k==0:
        if chainstart[c] is not None and not sub(chainstart[c],nf):return None
        continue
      t,r=chains[c][k-1]
      if t=='op':
        if not sub(cur(r,ch),nf):q.append((r,nf))
      elif not sub(r,nf):return None
    if len(ch)>400:return None
  return ch
def chaincost2(c,ch):
  tot=0.0;prev=dim(chainstart[c])
  for k in range(len(chains[c])):
    d=dim(frc(c,k,ch))
    if d>prev:tot+=g(d-prev)
    prev=max(prev,d)
  return tot
def delta(ch):
  cs={c for j in ch for c,k in where[j]}
  return sum(chaincost2(c,ch)-chaincost2(c,{}) for c in cs)
if len(sys.argv)>1:F[:]=pickle.load(open(sys.argv[1],'rb'))
t0=time.time();tc=total();print('start',round(tc,2),flush=True)
for it in range(30):
  acc=0;gain=0.0;order2=list(range(len(ops)));random.Random(100+it).shuffle(order2)
  for i in order2:
    best=None;bd=-1e-9;cand=[]
    for c,k in where[i]:
      if k+1<len(chains[c]):cand.append(('r',frc(c,k+1,{})))
      cand.append(('l',frc(c,k-1,{})))
    cand+= [('r',U[i]),('l',L[i])]
    for typ,X in cand:
      if X is None:continue
      ch=raise_(i,X) if typ=='r' else lower_(i,X)
      if not ch:continue
      d=delta(ch)
      if d<bd:bd,best=d,ch
    if best:
      for j,f in best.items():F[j]=f
      acc+=1;gain+=bd
  tc=total();print(it,'accepted',acc,'gain',round(gain,2),'cost',round(tc,2),round(time.time()-t0),flush=True)
  pickle.dump(F,open('F_casc.pkl','wb'))
  if acc==0:break
