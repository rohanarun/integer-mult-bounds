"""Label-independent lower bound on copied center ranks for fixed decoder supports.
Required correction edges force pairwise orthogonal odd labels; a clique is independent.
"""
from pathlib import Path
import gzip,json,itertools
import numpy as np
ROOT=Path(__file__).resolve().parent
w=json.load(gzip.open(ROOT/'COLOR-WITNESS.json.gz'));A=np.array(w['A']);B=np.array(w['source']['B_scaled']);T=A@B;N=len(T)
E=(T!=0)|(T.T!=0);np.fill_diagonal(E,False);adj=[{j for j in range(N)if E[i,j]}for i in range(N)]
def maxclique(vertices):
 best=[]
 def search(cur,can):
  nonlocal best
  if len(cur)+len(can)<=len(best):return
  if not can:
   if len(cur)>len(best):best=cur[:]
   return
  while can:
   if len(cur)+len(can)<=len(best):return
   i=max(can,key=lambda i:len(adj[i]&can));can.remove(i);search(cur+[i],can&adj[i])
 search([],set(vertices));return best
bounds=[]
for k,row in enumerate(B):
 support=np.flatnonzero(row).tolist()
 if not support:continue
 clique=maxclique(support)
 assert set(clique)<=set(support)and all(E[i,j]for i,j in itertools.combinations(clique,2))
 bounds.append({'center_coordinate':k,'support_ports':support,'forced_orthogonal_clique':clique,'copied_rank_lower_bound':len(clique),'distinct_colors_on_support':len({w['coloring'][i]for i in support})})
C=sum(x['copied_rank_lower_bound']for x in bounds)
r={'status':'PASS_EXACT_LABEL_INDEPENDENT_CENTER_RANK_LOWER_BOUND','ports':N,'center_bounds':bounds,'total_copied_rank_lower_bound':C,'deficit_upper_polynomial':{'coefficient_of_L':N-C,'constant':-N},'rules_out_positive_deficit_for_all_positive_L':C>=N,'scope':'Every ordinary-dot-product odd-label realization preserving all required correction caps, with this fixed decoder and separately copied centers. Free Gram entries, ambient dimension, label distinctness encoding and proper cap choices do not weaken the clique witnesses. Does not rule out changing scalar decoder/factorization or eliminating copied centers.'}
(ROOT/'CENTER-CLIQUE-BOUND.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
