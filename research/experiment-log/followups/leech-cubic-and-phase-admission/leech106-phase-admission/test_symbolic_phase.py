from pathlib import Path
import random,json,itertools,time
import clifford_exact as ce
from symbolic_phase import Poly,gauss,iphase,amplitude,lower_child,same
r=Path(__file__).resolve().parent;rng=random.Random(10625);started=time.time();sums=amps=lowers=0
for n in range(9):
 for case in range(20):
  p=Poly(n);p.c=rng.randrange(4);p.a=[rng.randrange(4) for _ in range(n)];p.edges={(i,j) for i in range(n) for j in range(i+1,n) if rng.randrange(2)}
  terms=[iphase(p.val(x)) for x in range(1<<n)];expected=tuple(sum(a[i] for a in terms) for i in range(2));assert gauss(p)==expected;sums+=1
for n in range(1,6):
 for case in range(12):
  op=ce.ident(n)
  for _ in range(8):
   k=rng.randrange(4)
   if k==0:op=op.then(ce.cgate(n,rng.randrange(1,1<<n),rng.choice([-1,1])))
   elif k==1:
    rows=list(range(n));rng.shuffle(rows);op=op.then(ce.perm(n,tuple(1<<j for j in rows)))
   elif k==2:
    q=[0]*n
    for i in range(n):
     for j in range(i,n):
      if rng.randrange(2):q[i]|=1<<j;q[j]|=1<<i
    alpha=[((q[i]>>i)&1)+2*rng.randrange(2) for i in range(n)];op=op.then(ce.diag(n,q,alpha))
   else:op=op.then(ce.xgate(n,rng.randrange(1<<n)))
  vector,den=op.zero_state()
  for x,(a,b) in enumerate(vector):
   actual=amplitude(op,x);d=den
   while d and a%2==b%2==0:a//=2;b//=2;d-=1
   assert actual==(a,b,d),(n,case,x,actual,(a,b,d));amps+=1
  rec,compiled=lower_child(op);assert compiled.zero_state()==op.zero_state();ref,_=ce.lower_child(op);assert rec==ref;lowers+=1
result={'status':'PASS_LITERAL_CROSSCHECK_OF_SYMBOLIC_PHASE_COMPILER','quadratic_gauss_sums_exhaustively_compared':sums,'literal_amplitudes_compared':amps,'lowered_recipe_matches_original_compiler':lowers,'seed':10625,'seconds':time.time()-started};(r/'SYMBOLIC-CROSSCHECK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
