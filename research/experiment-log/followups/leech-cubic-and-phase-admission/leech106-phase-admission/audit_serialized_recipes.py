"""Decode saved phase recipes without calling either recipe constructor/lower_child."""
from pathlib import Path
import json,gzip,time
import clifford_exact as ce
from symbolic_phase import amplitude
r=Path(__file__).resolve().parent;started=time.time();out=[]
for name in ['ORIGINAL25','REPAIRED23']:
 payload=json.loads(gzip.decompress((r/(name+'-PHASE-RECIPES.json.gz')).read_bytes()));n=payload['dimension'];F=ce.fourier(n);cache={}
 if name=='ORIGINAL25':
  w=next(x for x in json.loads(gzip.decompress((r/'PUNCTURED-WITNESSES.json.gz').read_bytes())) if x['seed']==55026);frames=[tuple(payload['gather_basis'])]
 else:w=json.loads(gzip.decompress((r/'REPAIRED23-WITNESS.json.gz').read_bytes()));frames=list(map(tuple,w['gather_frames']))
 P=w['labels']
 def frame(U):
  U=tuple(U)
  if U not in cache:cache[U]=ce.canonical_frame(n,U)
  return cache[U]
 def mon(rec):
  op=ce.diag(n,tuple(rec['quadratic_rows']),tuple(rec['linear_Z4'])).then(ce.perm(n,tuple(rec['matrix_rows']))).then(ce.xgate(n,rec['offset']))
  return op.then(ce.Op(n,ce.identity(n),[('phase',rec['phase'])]))
 def expected(tag):
  if tag.startswith('source_endpoint_'):
   i=int(tag.rsplit('_',1)[1]);return ce.cgate(n,P[i]).adjoint().then(frame((P[i],)))
  if tag.startswith('target_endpoint_'):
   i=int(tag.rsplit('_',1)[1]);old=ce.cgate(n,P[i]).adjoint().then(F);return old.adjoint().then(frame(ce.nullspace([P[i]],n)))
  if tag.startswith('source_'):
   pieces=tag.split('_');i=int(pieces[1]);j=int(pieces[-1]) if name=='REPAIRED23' else 0;return frame((P[i],)).adjoint().then(frame(frames[j]))
  if name=='ORIGINAL25':
   U=frame(frames[0]);return {'empty_to_gather':U,'gather_to_empty':U.adjoint(),'gather_to_full':U.adjoint().then(F),'full_to_gather':F.adjoint().then(U)}[tag]
  j=int(tag.rsplit('_',1)[1]);U=frame(frames[j])
  if tag.startswith('zero_to_gather_'):return U
  if tag.startswith('gather_to_zero_'):return U.adjoint()
  if tag.startswith('gather_tail_'):return U.adjoint().then(F)
  raise AssertionError(tag)
 for record in payload['recipes']:
  rec=record['recipe'];op=expected(record['name']);degree=ce.rank([x for x,z,p in op.tab[n:]]);assert rec['rank']==degree
  compiled=mon(rec['left']) if degree==0 else mon(rec['right']).then(ce.fourier(n,range(degree))).then(mon(rec['left']))
  assert compiled.tab==op.tab
  point=record['phase_witness']['point'];a=amplitude(op,point);assert a[:2]!=(0,0);assert a==amplitude(compiled,point)==tuple(record['phase_witness']['amplitude'])
 out.append({'package':name,'recipes_independently_decoded':len(payload['recipes']),'exact_tableaus_and_global_phases':True})
 print(out[-1],flush=True)
res={'status':'PASS_INDEPENDENT_SERIALIZED_RECIPE_DECODING','results':out,'constructor_or_lower_child_called':False,'hilbert_state_vectors_allocated':0,'seconds':time.time()-started};(r/'SERIALIZED-AUDIT.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res),flush=True)
