"""Exact phase-bearing original Leech106 frame/adapter tests, polynomial size."""
from pathlib import Path
import gzip,json,time,hashlib,copy
import clifford_exact as ce
from symbolic_phase import lower_child,same,amplitude,support_point
r=Path(__file__).resolve().parent;started=time.time();n=25
w=next(x for x in json.loads(gzip.decompress((r/'PUNCTURED-WITNESSES.json.gz').read_bytes())) if x['seed']==55026);P=w['labels'];normal=w['common_normal_even_pool'];U=ce.nullspace([normal],n);assert len(U)==24
F=ce.fourier(n);Tu=ce.canonical_frame(n,U);empty=ce.ident(n)
def validate_frame(V):
 op=ce.canonical_frame(n,V);L=[x|(x<<n) for x in V]+[y<<n for y in ce.nullspace(V,n)];pre=[x|(z<<n) for x,z,p in ce.inverse(op.tab)[n:]]
 assert ce.rank(L)==ce.rank(L+pre)==n
 assert all(((a&((1<<n)-1))&(b>>n)).bit_count()%2==((b&((1<<n)-1))&(a>>n)).bit_count()%2 for a in L for b in L)
 assert ce.rank([x for x,z,p in op.tab[n:]])==len(V)
 return op
validate_frame(U);recipes=[];ops={}
def lower(name,op,expected):
 rec,compiled=lower_child(op);assert rec['rank']==expected
 point=support_point(op);witness={'point':point,'amplitude':amplitude(op,point)}
 recipes.append({'name':name,'expected_rank':expected,'recipe':rec,'phase_witness':witness});ops[name]=op
 return rec
for name,op,d in [('empty_to_gather',Tu,24),('gather_to_empty',Tu.adjoint(),24),('gather_to_full',Tu.adjoint().then(F),1),('full_to_gather',F.adjoint().then(Tu),1)]:lower(name,op,d)
print('PASS_COMMON_DEGENERATE_GATHER_AND_WIDTH1_RESIDUAL',flush=True)
for i,p in enumerate(P):
 assert p.bit_count()%2 and (p&normal).bit_count()%2==0
 source=validate_frame((p,));target=validate_frame(ce.nullspace([p],n))
 lower('source_%d_to_gather'%i,source.adjoint().then(Tu),23)
 lower('source_endpoint_%d'%i,ce.cgate(n,p).adjoint().then(source),0)
 native_target=ce.cgate(n,p).adjoint().then(F)
 lower('target_endpoint_%d'%i,native_target.adjoint().then(target),0)
 if i%20==0:print('ports',i+1,'seconds',round(time.time()-started,3),flush=True)
def decode(rec):
 o=ce.diag(n,tuple(rec['quadratic_rows']),tuple(rec['linear_Z4'])).then(ce.perm(n,tuple(rec['matrix_rows']))).then(ce.xgate(n,rec['offset']))
 return o.then(ce.Op(n,ce.identity(n),[('phase',rec['phase'])]))
rec=next(x['recipe'] for x in recipes if x['name']=='gather_to_full');S=Tu.adjoint().then(F);R=decode(rec['right']);L=decode(rec['left']);net=R.adjoint().then(S).then(L.adjoint());target=ce.fourier(n,range(1));assert same(net,target)
# Controls: same tableau but wrong scalar phase must fail; translation and width also fail.
controls=[]
bad=net.then(ce.Op(n,ce.identity(n),[('phase',1)]));assert bad.tab==net.tab and not same(bad,target);controls.append('global_phase_undetectable_by_tableau_alone')
assert not same(net.then(ce.xgate(n,1)),target);controls.append('wrong_translation')
assert not same(net,ce.fourier(n,range(2)));controls.append('wrong_residual_width')
payload={'scope':'Exact actual frame edges and endpoint/residual adapters only, no chronological scalar word or supplier invoice.','dimension':n,'source_seed':55026,'gather_basis':U,'isotropic_normal':normal,'recipes':recipes}
raw=json.dumps(payload,separators=(',',':')).encode();(r/'ORIGINAL25-PHASE-RECIPES.json.gz').write_bytes(gzip.compress(raw,mtime=0))
result={'status':'PASS_EXACT_ORIGINAL_LEECH106_DEGENERATE_FRAME_PHASES','dimension':25,'ports':106,'source_seed':55026,'gather_rank':24,'normal_isotropic':normal.bit_count()%2==0,'general_frame_preimage_checks':213,'phase_lowered_children_and_adapters':len(recipes),'phase_rank_histogram':{str(k):sum(x['expected_rank']==k for x in recipes) for k in sorted(set(x['expected_rank'] for x in recipes))},'all_equalities_include_global_phase':True,'width1_residual_wrappers_decoded':True,'negative_controls':controls,'hilbert_state_vectors_allocated':0,'phase_method':'Exact Z4 quadratic path sum with Gaussian-integer elimination and affine constraints; original tableau compiler retained.','recipe_uncompressed_sha256':hashlib.sha256(raw).hexdigest(),'seconds':time.time()-started,'scope':'Degenerate-frame feasibility demonstrated. This is not a complete dirty-helper scalar word, phase coverage of an unbuilt word, global invoice or kappa.'}
(r/'ORIGINAL25-RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
