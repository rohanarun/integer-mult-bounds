"""Repair full-span center gathering by exact additive center splitting.
This preserves the transfer and correction graph; it is not a scheduled word.
"""
from pathlib import Path
import gzip,json
import numpy as np
ROOT=Path(__file__).resolve().parent
base=json.load(gzip.open(ROOT/'SLICE-GRAM-WITNESSES.json.gz'));labels=json.loads((ROOT/'LABEL-WITNESSES.json').read_text());Y=np.array(json.load(gzip.open(ROOT/'SOURCE-LINES.json.gz'))['Y'])
def basis(xs):
 p={}
 for x in xs:
  while x:
   k=x.bit_length()-1
   if k in p:x^=p[k]
   else:p[k]=x;break
 return p
def normal(xs,h):
 p=basis(xs);f=next(i for i in range(h)if i not in p);z=1<<f
 for k in sorted(p):
  if(z&p[k]).bit_count()%2:z^=1<<k
 assert z and all((z&x).bit_count()%2==0 for x in xs);return z
results=[];witness=[]
for ll in labels:
 b=base[ll['source_witness_index']];A=Y[b['ports_original']];B=np.array(b['B_scaled']);P=ll['labels'];h=ll['dimension'];N=len(P)
 aa=[];bb=[];normals=[];splits={};initial=sum(bool(np.any(row))for row in B)
 for k,row in enumerate(B):
  idx=np.flatnonzero(row).tolist()
  if not idx:continue
  parts=[];cur=[]
  for i in idx:
   if len(basis([P[j]for j in cur+[i]]))==h:parts.append(cur);cur=[]
   cur.append(i)
  if cur:parts.append(cur)
  splits[str(k)]=len(parts)
  for part in parts:
   aa.append(A[:,k]);r=np.zeros(N,dtype=np.int64);r[part]=row[part];bb.append(r);normals.append(normal([P[i]for i in part],h))
 AA=np.array(aa).T;BB=np.array(bb);assert np.array_equal(AA@BB,A@B)
 assert all((P[i]&n).bit_count()%2==0 for r,n in zip(BB,normals)for i in np.flatnonzero(r))
 results.append({'ports':N,'binary_dimension':h,'initial_nonzero_centers':initial,'centers_after_split':len(bb),'splits_by_original_coordinate':splits,'all_centers_gather_in_proper_hyperplanes':True,'transfer_preserved_exactly':True,'scope':'Exact scalar factorization and binary cap witnesses; no chronological dirty-word/frame/phase/global admission.'})
 witness.append({'ports':N,'A':AA.tolist(),'B_scaled':BB.tolist(),'scale':b['scale'],'labels':P,'dimension':h,'center_normals':normals})
(ROOT/'SPLIT-CENTERS.json').write_text(json.dumps(results,indent=2)+'\n')
(ROOT/'SPLIT-CENTERS-WITNESSES.json.gz').write_bytes(gzip.compress(json.dumps(witness,separators=(',',':')).encode(),mtime=0));print(json.dumps(results,indent=2))
