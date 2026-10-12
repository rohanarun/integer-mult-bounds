"""Exact correction-support screen of Smith-based Leech decoder, not full admission."""
from pathlib import Path
import json,gzip,itertools
import numpy as np
ROOT=Path(__file__).resolve().parent
w=json.load(gzip.open(ROOT/'DYADIC-DECODER-WITNESS.json.gz'))
A=np.array(w['A'],dtype=np.int64);B8=np.array(w['eight_B'],dtype=np.int64)
Q8=A@B8;assert np.array_equal(Q8@Q8,8*Q8)
active=np.flatnonzero(np.any(B8!=0,axis=0));inactive=[i for i in range(276) if i not in active]
E=(Q8!=0)|(Q8.T!=0);np.fill_diagonal(E,False)
# Branch-and-bound maximum clique on core27: all remaining vertices independent.
def maximum_clique(vertices):
 adj={i:{j for j in vertices if E[i,j]} for i in vertices};best=[]
 def search(chosen,candidates):
  nonlocal best
  if len(chosen)+len(candidates)<=len(best):return
  if not candidates:
   if len(chosen)>len(best):best=chosen[:]
   return
  while candidates:
   if len(chosen)+len(candidates)<=len(best):return
   v=max(candidates,key=lambda x:len(adj[x]&candidates));candidates.remove(v)
   search(chosen+[v],candidates&adj[v])
  if len(chosen)>len(best):best=chosen[:]
 search([],set(vertices));return best
best=maximum_clique(list(map(int,active)))
# Any clique has at most one inactive vertex, hence exact full graph max clique.
for i in inactive:
 cand=maximum_clique([int(j) for j in active if E[i,j]])+[i]
 if len(cand)>len(best):best=cand
# Safe exact explicit h=36 label upper construction: e_i for 27 active,
# and 249 distinct odd 9bit suffixes for inactive. This checks only corrections.
labels=[0]*276
for k,i in enumerate(active):labels[int(i)]=1<<k
odd=[x for x in range(1,512) if x.bit_count()%2]
for i,x in zip(inactive,odd):labels[i]=x<<len(active)
assert len(set(labels))==276 and all(x.bit_count()%2 for x in labels)
assert all((labels[i]&labels[j]).bit_count()%2==0 for i in range(276) for j in range(276) if E[i,j])
res={'status':'PASS_EXACT_CORRECTION_SUPPORT_SCREEN_NOT_FULL_WORD',
 'low_rank_projector':'Q=A B, Q^2=Q; denominator at most8',
 'active_decoder_columns':len(active),'directed_offdiagonal_correction_nonzeros':int(np.count_nonzero(Q8-np.diag(np.diag(Q8)))),
 'required_orthogonality_edges':int(E.sum())//2,
 'exact_maximum_required_orthogonal_clique':len(best),'clique_port_indices':list(map(int,best)),
 'label_dimension_lower_bound':len(best),'label_dimension_explicit_upper_bound':len(active)+9,
 'label_construction':str(len(active))+' separate active axes and9 new axes carrying'+str(len(inactive))+' distinct odd suffixes',
 'scope':'Only necessary orthogonal-cap condition for corrections I-Q. No center gathering hyperplanes, phase or cost admission. A failed low dimension rules out this specific decoder, not all Leech decoders.',
 'natural_projector_lower_bound':276,'diagonal_Q8_histogram':{str(int(x)):int(np.sum(np.diag(Q8)==x)) for x in np.unique(np.diag(Q8))},'diagonal_identity_pass':bool(np.all(np.diag(Q8)==8)),'diagonal_failure_scope':'A B is a coordinate reconstruction projector, not a port transfer with diagonal1. It cannot be inserted as the supplier low-rank transfer with only orthogonal-cap offdiagonal correction.'}
(ROOT/'DECODER-CAPS.json').write_text(json.dumps(res,indent=2)+'\n')
(ROOT/'DECODER-CAPS-WITNESS.json.gz').write_bytes(gzip.compress(json.dumps({'Q8':Q8.tolist(),'labels_h36':labels},separators=(',',':')).encode(),mtime=0))
print(json.dumps(res,indent=2))
