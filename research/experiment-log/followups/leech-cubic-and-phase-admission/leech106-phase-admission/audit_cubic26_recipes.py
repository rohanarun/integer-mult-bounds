"""Independently decode saved 26D recipes; no lower_child or constructor call."""
from pathlib import Path
import json,gzip,time
import clifford_exact as ce
from symbolic_phase import amplitude
r=Path(__file__).resolve().parent;started=time.time();payload=json.loads(gzip.decompress((r/'CUBIC26-PHASE-RECIPES.json.gz').read_bytes()));P=json.loads(gzip.decompress((r/'CUBIC26-ALL-QUOTIENT-LABELS.json.gz').read_bytes()))['odd_labels'];n=payload['dimension'];F=ce.fourier(n);U=ce.canonical_frame(n,tuple(payload['gather_basis']));cache={}
def frame(basis):
 basis=tuple(basis)
 if basis not in cache:cache[basis]=ce.canonical_frame(n,basis)
 return cache[basis]
def mon(rec):
 op=ce.diag(n,tuple(rec['quadratic_rows']),tuple(rec['linear_Z4'])).then(ce.perm(n,tuple(rec['matrix_rows']))).then(ce.xgate(n,rec['offset']))
 return op.then(ce.Op(n,ce.identity(n),[('phase',rec['phase'])]))
def expected(tag):
 if tag.startswith('source_endpoint_'):
  i=int(tag.rsplit('_',1)[1]);return ce.cgate(n,P[i]).adjoint().then(frame((P[i],)))
 if tag.startswith('target_endpoint_'):
  i=int(tag.rsplit('_',1)[1]);old=ce.cgate(n,P[i]).adjoint().then(F);return old.adjoint().then(frame(ce.nullspace([P[i]],n)))
 if tag.startswith('source_'):
  i=int(tag.split('_')[1]);return frame((P[i],)).adjoint().then(U)
 return {'empty_to_gather':U,'gather_to_empty':U.adjoint(),'gather_to_full':U.adjoint().then(F),'full_to_gather':F.adjoint().then(U)}[tag]
for record in payload['recipes']:
 rec=record['recipe'];op=expected(record['name']);degree=ce.rank([x for x,z,p in op.tab[n:]]);assert rec['rank']==degree
 compiled=mon(rec['left']) if degree==0 else mon(rec['right']).then(ce.fourier(n,range(degree))).then(mon(rec['left']))
 assert compiled.tab==op.tab
 point=record['phase_witness']['point'];a=amplitude(op,point);assert a[:2]!=(0,0);assert a==amplitude(compiled,point)==tuple(record['phase_witness']['amplitude'])
res={'status':'PASS_INDEPENDENT_CUBIC26_SERIALIZED_RECIPE_DECODING','dimension':n,'sampled_ports':len(payload['sample_port_indices']),'recipes_independently_decoded':len(payload['recipes']),'exact_tableaus_and_global_phases':True,'constructor_or_lower_child_called':False,'hilbert_state_vectors_allocated':0,'seconds':time.time()-started};(r/'CUBIC26-SERIALIZED-AUDIT.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res),flush=True)
