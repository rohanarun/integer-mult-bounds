"""Bounded exact phases for alternative label lane's retained23D106-port witness."""
from pathlib import Path
import gzip,json,time,hashlib
import clifford_exact as ce
from symbolic_phase import lower_child,same,amplitude,support_point
r=Path(__file__).resolve().parent;started=time.time();w=json.loads(gzip.decompress((r/'REPAIRED23-WITNESS.json.gz').read_bytes()));n=w['dimension'];assert n==23;P=w['labels'];vectors=w['vectors'];frames=[tuple(x) for x in w['gather_frames']];F=ce.fourier(n);recipes=[];framechecks=0;cache={}
def frame(V):
 global framechecks
 V=tuple(V)
 if V not in cache:
  op=ce.canonical_frame(n,V);L=[x|(x<<n) for x in V]+[y<<n for y in ce.nullspace(V,n)];pre=[x|(z<<n) for x,z,p in ce.inverse(op.tab)[n:]]
  assert ce.rank(L)==ce.rank(L+pre)==n;assert ce.rank([x for x,z,p in op.tab[n:]])==len(V)
  cache[V]=op;framechecks+=1
 return cache[V]
def admit(name,op,degree):
 rec,out=lower_child(op);assert rec['rank']==degree
 point=support_point(op);recipes.append({'name':name,'rank':degree,'recipe':rec,'phase_witness':{'point':point,'amplitude':amplitude(op,point)}})
for i,p in enumerate(P):
 assert p.bit_count()%2
 source=frame((p,));target=frame(ce.nullspace([p],n));native_target=ce.cgate(n,p).adjoint().then(F)
 admit('source_endpoint_%d'%i,ce.cgate(n,p).adjoint().then(source),0)
 admit('target_endpoint_%d'%i,native_target.adjoint().then(target),0)
for j,U in enumerate(frames):
 Tu=frame(U);assert len(U)<n
 admit('zero_to_gather_%d'%j,Tu,len(U));admit('gather_to_zero_%d'%j,Tu.adjoint(),len(U));admit('gather_tail_%d'%j,Tu.adjoint().then(F),n-len(U))
 for i,p in enumerate(P):
  if vectors[i][j]:
   assert ce.rank(list(U)+[p])==len(U)
   admit('source_%d_to_gather_%d'%(i,j),frame((p,)).adjoint().then(Tu),len(U)-1)
 print('gather',j+1,'recipes',len(recipes),'seconds',round(time.time()-started,3),flush=True)
raw=json.dumps({'source_seed':w['source_seed'],'dimension':n,'recipes':recipes},separators=(',',':')).encode();(r/'REPAIRED23-PHASE-RECIPES.json.gz').write_bytes(gzip.compress(raw,mtime=0))
res={'status':'PASS_EXACT_REPAIRED23_LEECH106_FRAME_PHASES','dimension':n,'source_seed':w['source_seed'],'ports':len(P),'coordinate_gathers':24,'gather_rank_sum':sum(map(len,frames)),'gather_rank_histogram':{str(k):sum(len(U)==k for U in frames) for k in sorted(set(map(len,frames)))},'unique_general_frame_preimage_checks':framechecks,'phase_lowered_children_and_adapters':len(recipes),'phase_rank_histogram':{str(k):sum(x['rank']==k for x in recipes) for k in sorted(set(x['rank'] for x in recipes))},'all_equalities_include_global_phase':True,'hilbert_state_vectors_allocated':0,'recipe_uncompressed_sha256':hashlib.sha256(raw).hexdigest(),'seconds':time.time()-started,'scope':'Finite native23D frame/adapter feasibility for every nonzero coordinate gather incidence in the retained witness, not a full chronological scalar word or dirty-helper/global supplier admission.'}
(r/'REPAIRED23-RESULT.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res),flush=True)
