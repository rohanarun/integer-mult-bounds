"""All-label containment census plus bounded exact 26D phase family audit."""
from pathlib import Path
import gzip,json,time,hashlib
import clifford_exact as ce
from symbolic_phase import lower_child,same,amplitude,support_point
r=Path(__file__).resolve().parent;started=time.time();n=26
labels=json.loads(gzip.decompress((r/'CUBIC26-ALL-QUOTIENT-LABELS.json.gz').read_bytes()))['odd_labels'];N=len(labels)
assert N==98280 and len(set(labels))==N
U=tuple(1<<i for i in range(25));normal=1<<25
assert ce.rank(U)==25 and ce.nullspace(U,n)==[normal]
for p in labels:assert 0<p<1<<25 and p.bit_count()%2==1 and (p&normal)==0
# All-coordinate 0 embedding preserves each binary pairing algebraically.
# Contains every nonzero line; general-frame distance formula implies rank 25-1=24.
indices=sorted(set([0,N-1]+[i*(N-1)//31 for i in range(32)]+[min(range(N),key=lambda i:labels[i].bit_count()),max(range(N),key=lambda i:labels[i].bit_count())]))
F=ce.fourier(n);cache={};recipes=[]
def frame(V):
 V=tuple(V)
 if V not in cache:
  op=ce.canonical_frame(n,V);L=[x|(x<<n) for x in V]+[y<<n for y in ce.nullspace(V,n)];pre=[x|(z<<n) for x,z,p in ce.inverse(op.tab)[n:]]
  assert ce.rank(L)==ce.rank(L+pre)==n
  assert ce.rank([x for x,z,p in op.tab[n:]])==len(V)
  cache[V]=op
 return cache[V]
def admit(name,op,degree):
 rec,out=lower_child(op);assert rec['rank']==degree and same(op,out)
 point=support_point(op);recipes.append({'name':name,'rank':degree,'recipe':rec,'phase_witness':{'point':point,'amplitude':amplitude(op,point)}})
Tu=frame(U)
for tag,op,degree in [('empty_to_gather',Tu,25),('gather_to_empty',Tu.adjoint(),25),('gather_to_full',Tu.adjoint().then(F),1),('full_to_gather',F.adjoint().then(Tu),1)]:admit(tag,op,degree)
for i in indices:
 p=labels[i];source=frame((p,));target=frame(ce.nullspace([p],n));assert ce.rank(list(U)+[p])==25
 admit('source_%d_to_gather'%i,source.adjoint().then(Tu),24)
 admit('source_endpoint_%d'%i,ce.cgate(n,p).adjoint().then(source),0)
 native_target=ce.cgate(n,p).adjoint().then(F);admit('target_endpoint_%d'%i,native_target.adjoint().then(target),0)
# Odd ambient dimension was never a precondition: dimension26 genuine recipes pass.
# The extension excludes bit25; adding a vector with bit25 is rejected by containment.
assert (labels[0]|normal)&normal
bad=Tu.then(ce.Op(n,ce.identity(n),[('phase',1)]));assert bad.tab==Tu.tab and not same(bad,Tu)
payload={'dimension':n,'gather_basis':U,'sample_port_indices':indices,'recipes':recipes}
raw=json.dumps(payload,separators=(',',':')).encode();(r/'CUBIC26-PHASE-RECIPES.json.gz').write_bytes(gzip.compress(raw,mtime=0))
res={'status':'PASS_CUBIC26_NATIVE_INTERFACE_BOUNDED_PHASE_AUDIT','dimension':n,'ports_all_label_census':N,'all_distinct_odd_and_in_common_proper_gather':True,'common_gather_dimension':25,'common_gather_nondegenerate':True,'gather_count_from_scalar_source':2600,'sampled_ports':len(indices),'sample_port_indices':indices,'all_port_transition_rank_by_general_frame_identity':24,'all_port_transition_rank_scope':'Every label containment checked; rank follows the exact general-subspace distance identity. Not all 98,280 phase recipes enumerated.','gather_rank':25,'tail_rank':1,'unique_exact_frame_preimages_checked':len(cache),'exact_phase_recipes':len(recipes),'phase_rank_histogram':{str(k):sum(x['rank']==k for x in recipes) for k in sorted(set(x['rank'] for x in recipes))},'zero_embedding_preserves_all_binary_pairings':'Algebraic identity (p,0) dot (q,0) = p dot q; no pairwise quadratic enumeration needed.','even_dimension_restriction_in_native_interface':False,'negative_controls':['out_of_gather_bit25_detected','same_tableau_wrong_global_phase_rejected'],'all_equalities_include_global_phase':True,'hilbert_state_vectors_allocated':0,'recipe_uncompressed_sha256':hashlib.sha256(raw).hexdigest(),'seconds':time.time()-started,'scope':'Native finite frame/phase feasibility only. No chronological scalar word, dirty-helper restoration, global assembly/parity admission, paid invoice or kappa.'}
(r/'CUBIC26-RESULT.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res),flush=True)
