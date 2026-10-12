"""Independent exhaustive binary-subspace controls for the frozen root cut model."""
import os,json,hashlib,math,itertools,random,time
from pathlib import Path
from collections import defaultdict
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow
P=Path(__file__).resolve().parent;assert os.path.ismount('/Volumes/SP AI 01_16') and os.access(P,os.W_OK)
SCALE=10**7;INF=10**15;b=.001594507308884431019637
cost=lambda d:d*math.expm1(b*math.log(73/d))+32*73**2*73**b/10**16 if d else 0

def span(vs):
 out={0}
 for v in vs:out|={x^v for x in out}
 return frozenset(out)
def rank(F):return len(F).bit_length()-1
def change(F,v,kind):return frozenset(x for x in F if not (x&v).bit_count()%2) if kind=='contract' else F|frozenset(x^v for x in F)
def reach(mat,start,reverse=False):
 a=mat.transpose().tocsr() if reverse else mat.tocsr();seen={start};todo=[start]
 while todo:
  u=todo.pop()
  for k in range(a.indptr[u],a.indptr[u+1]):
   q=int(a.indices[k])
   if a.data[k]>0 and q not in seen:seen.add(q);todo.append(q)
 return seen

def run(Fs,edges,fixed,kind,v,name):
 N=len(Fs);s=N;t=N+1;new=[change(F,v,kind) for F in Fs];active=[new[i]!=Fs[i] for i in range(N)];caps=defaultdict(int);constant=0.;floating=[]
 def arc(a,z,fee):
  assert fee>=0
  floating.append((a,z,fee));caps[a,z]+=round(fee*SCALE)
 for k in fixed:
  if active[k]:caps[k,t]+=INF
 for p,q in edges:
  F,G=Fs[p],Fs[q];assert F<=G;d=rank(G)-rank(F)
  if active[p] and active[q]:
   if kind=='contract':caps[q,p]+=INF;arc(p,q,cost(d+1)-cost(d))
   else:caps[p,q]+=INF;arc(q,p,cost(d+1)-cost(d))
  elif active[p]:
   assert kind=='extend';delta=cost(d-1)-cost(d);arc(s,p,-delta);constant+=delta
  elif active[q]:
   assert kind=='contract';delta=cost(d-1)-cost(d);arc(s,q,-delta);constant+=delta
 hard=sum(z for (a,c),z in caps.items() if a==s)+1;assert hard<2**31-1
 caps={k:hard if z>=INF else z for k,z in caps.items() if z};assert all(z<2**31-1 for z in caps.values())
 rr=[a for a,z in caps];cc=[z for a,z in caps];vv=list(caps.values());mat=csr_matrix((np.array(vv,dtype=np.int64),(rr,cc)),shape=(N+2,N+2));flow=maximum_flow(mat,s,t,method='dinic');res=mat-flow.flow
 amin=reach(res,s);amax=set(range(N+2))-reach(res,t,True);assert t not in amin and s in amax
 ids=[i for i in range(N) if active[i]];ex=[];invalid=0;invalid_fixed=0;max_error=0.
 for mask in range(1<<len(ids)):
  sel={i for j,i in enumerate(ids) if mask>>j&1};S=sel|{s};real=[new[i] if i in sel else F for i,F in enumerate(Fs)];legal=not(sel&fixed) and all(real[p]<=real[q] for p,q in edges)
  cut=sum(z for (a,c),z in caps.items() if a in S and c not in S)
  if not legal:
   invalid+=1;invalid_fixed+=bool(sel&fixed);assert cut>=hard;continue
  delta=sum(cost(rank(real[q])-rank(real[p]))-cost(rank(Fs[q])-rank(Fs[p])) for p,q in edges)
  model=constant+sum(z for a,c,z in floating if a in S and c not in S)
  assert abs(delta-model)<1e-12,(name,delta,model)
  err=abs(delta-(constant+cut/SCALE));max_error=max(max_error,err);assert err<=len(floating)*.5/SCALE+1e-12
  ex.append((sel,cut,delta))
 best=min(z for _,z,_ in ex);opts=[sel for sel,z,d in ex if z==best];assert best==flow.flow_value
 union=set().union(*opts);inter=set.intersection(*opts)
 selmin={i for i in amin if i<N and active[i]};selmax={i for i in amax if i<N and active[i]};assert selmin==inter and selmax==union,(name,selmin,inter,selmax,union)
 dmin=next(d for sel,z,d in ex if sel==selmin);dmax=next(d for sel,z,d in ex if sel==selmax);dexact=min(d for sel,z,d in ex)
 assert dmin-dexact<=len(floating)/SCALE+1e-12 and dmax-dexact<=len(floating)/SCALE+1e-12
 return dict(name=name,kind=kind,v=v,legal_subsets=len(ex),invalid_subsets=invalid,invalid_fixed_subsets=invalid_fixed,edges=len(edges),repeated_edges=len(edges)-len(set(edges)),min_selected=sorted(selmin),max_selected=sorted(selmax),minimum_cut_fee=dmin,maximum_cut_fee=dmax,exact_min_fee=dexact,max_rounding_error=max_error,plateau_distinct=selmin!=selmax)

start=time.monotonic();rows=[];empty=span([]);line=span([1]);plane=span([1,2]);full=span([1,2,4])
for kind in ('contract','extend'):
 rows.append(run([empty,line,plane],[(0,1),(1,2)],{0,2},kind,1 if kind=='contract' else 2,'positive-'+kind));assert rows[-1]['minimum_cut_fee']<0
 rows.append(run([empty,line,plane],[(0,1),(1,2)],{0,1,2},kind,1 if kind=='contract' else 2,'fixed-no-gain-'+kind));assert rows[-1]['min_selected']==[] and rows[-1]['max_selected']==[]
 rows.append(run([empty,line,plane],[(0,1),(1,2)],{0,2},kind,4 if kind=='contract' else 0,'inactive-no-gain-'+kind));assert rows[-1]['exact_min_fee']==0
 # Equal rank gap permutation produces a true neutral alternative.
 rows.append(run([empty,line,line,plane],[(0,1),(1,2),(2,3)],{0,3},kind,1 if kind=='contract' else 2,'duplicate-frames-'+kind))
 # Active isolated optional node demonstrates minimal/maximal residual plateau.
 rows.append(run([empty,line,plane,line],[(0,1),(1,2)],{0,1,2},kind,1 if kind=='contract' else 2,'neutral-isolated-'+kind));assert rows[-1]['plateau_distinct']

rng=random.Random(5522026)
for case in range(500):
 dim=3 if case<400 else 4;D=1<<dim;Fs=[empty]+sorted([span(rng.sample(range(1,D),rng.randrange(dim+1))) for _ in range(5)],key=lambda F:(len(F),sorted(F)))+[span([1<<k for k in range(dim)])]
 edges=[(p,q) for p in range(len(Fs)) for q in range(p+1,len(Fs)) if Fs[p]<=Fs[q] and rng.random()<.45]
 if edges:edges+=rng.choices(edges,k=rng.randrange(4))
 fixed={0,len(Fs)-1}|{k for k in range(1,len(Fs)-1) if rng.random()<.25}
 for kind in ('contract','extend'):
  for v in range(1,D):rows.append(run(Fs,edges,fixed,kind,v,f'random-{case}'))
ans=dict(status='PASS',root_source_sha256=hashlib.sha256((P/'ROOT-SOURCE.py.txt').read_bytes()).hexdigest(),cases=len(rows),legal_subsets=sum(r['legal_subsets'] for r in rows),invalid_subsets=sum(r['invalid_subsets'] for r in rows),invalid_fixed_subsets=sum(r['invalid_fixed_subsets'] for r in rows),cases_with_repeated_edges=sum(bool(r['repeated_edges']) for r in rows),distinct_optimal_plateau_cases=sum(r['plateau_distinct'] for r in rows),max_rounding_error=max(r['max_rounding_error'] for r in rows),seconds=time.monotonic()-start,scope='Every legal subset of every sampled finite DAG checked against floating pairwise energy and rounded s-t mincut. Minimal and maximal residual cuts equal intersection and union of all rounded optimum active selections. Sampled DAGs do not certify source552 global optimality or physical admission.')
(P/'RESULT.json').write_text(json.dumps(ans,indent=2)+'\n');(P/'CASES.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(ans,indent=2))
# Root context uses a monotone edge for an equality-only scatter boundary.
# The ordinary cut is internally correct but its maximal neutral selection can
# violate the supplier's required current-frame equality.
Fs=[empty,line,line,plane];edges=[(0,1),(1,2),(2,3)]
relaxed=run(Fs,edges,{0,2,3},'contract',1,'scatter-anchor-relaxed')
fixed=run(Fs,edges,{0,1,2,3},'contract',1,'scatter-anchor-equality-fixed')
assert relaxed['min_selected']==[] and relaxed['max_selected']==[1]
assert relaxed['maximum_cut_fee']==0 and fixed['max_selected']==[]
assert change(Fs[1],1,'contract')<Fs[2]
witness=dict(status='CONFIRMED_ROOT_CONTEXT_EQUALITY_GAP',frames=[sorted(F) for F in Fs],edges=edges,scatter_anchor=2,preceding_event=1,relaxed=relaxed,equality_fixed=fixed,explanation='Contracting event1 below fixed anchor2 is monotone and neutral under fictitious climb pricing, but gk.profile requires exact current-frame equality at scatter. Freezing preceding event excludes it; unchanged original remains feasible.',effect='No positive result invalidated: root selected nothing. Maximal neutral cuts can nominate this invalid equality case. Full profile catches it.')
(P/'ANCHOR-GAP.json').write_text(json.dumps(witness,indent=2)+'\n')
print('CONFIRMED_ROOT_CONTEXT_EQUALITY_GAP; exact synthetic maximal-cut witness retained.')
