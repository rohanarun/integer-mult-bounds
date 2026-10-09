import sys
exec(open('casc.py').read().split("if len(sys.argv)>1")[0])
import json
def moves(i):
  cand=[]
  for c,k in where[i]:
    if k+1<len(chains[c]):cand.append(('r',frc(c,k+1,{})))
    cand.append(('l',frc(c,k-1,{})))
  cand+=[('r',U[i]),('l',L[i])]
  return cand
def sweep(seed,T=0.0):
  acc=0;gain=0.0;o=list(range(len(ops)));rng=random.Random(seed);rng.shuffle(o)
  for i in o:
    opts=[]
    for typ,X in moves(i):
      if X is None:continue
      ch=raise_(i,X) if typ=='r' else lower_(i,X)
      if ch:opts.append((delta(ch),ch))
    if not opts:continue
    d,ch=min(opts,key=lambda z:z[0])
    if T>0 and d>=-1e-9:
      d,ch=rng.choice(opts)
      if d<=1e-9 or rng.random()>=math.exp(-d/T):continue
    elif d>=-1e-9:continue
    for j,f in ch.items():F[j]=f
    acc+=1;gain+=d
  return acc,gain
t0=time.time();print('start',round(total(),2),flush=True)
best=total();bestF=list(F)
sched=[0]*4+[0.5,0]*3+[1.0,0,0]*3+[0.3,0,0]*3+[0]*4
for it,T in enumerate(sched):
  acc,gain=sweep(it,T);tc=total()
  if tc<best-1e-9:best=tc;bestF=list(F)
  print(it,'T',T,'acc',acc,'cost',round(tc,2),'best',round(best,2),round(time.time()-t0),flush=True)
F[:]=bestF
json.dump({str(i):[list(r) for r in C.B[F[i]]] for i in range(len(ops)) if F[i]!=word.opframe[i]},open('F_rows.json','w'))
word.opframe=list(F);word.changed_frames=[i for i,(a,b) in enumerate(zip(word.original_opframe,word.opframe)) if a!=b]
word.exact_frames();r=word.row();print('row ok',r['W_per_vertex'],r['deficit_per_vertex'],'changed vs PR200',sum(F[i]!=m.Candidate.__dict__ and F[i]!=0 for i in []),flush=True)
sys.path.insert(0,str(P/'bit'))
from terminal import prove
sel=json.loads((P/'selected/bit/sinks.json').read_text())
import contextlib,io
with contextlib.redirect_stdout(io.StringIO()):tp=prove(word,sel)
json.dump(dict(hist=tp['profile']['child_histogram'],R=tp['profile']['R']),open('opt_profile.json','w'))
print('terminal',tp['status'],tp['profile']['W_per_vertex'],flush=True)
import evalh
print('kappa',evalh.kappa(tp['profile']['child_histogram']),flush=True)
