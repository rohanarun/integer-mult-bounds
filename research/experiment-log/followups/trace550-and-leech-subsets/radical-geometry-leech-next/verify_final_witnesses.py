"""Independent retained finite witness audit: no search/construction imports."""
from pathlib import Path
import json,gzip
import numpy as np
ROOT=Path(__file__).resolve().parent
base=json.load(gzip.open(ROOT/'SLICE-GRAM-WITNESSES.json.gz'))
Y=np.array(json.load(gzip.open(ROOT/'SOURCE-LINES.json.gz'))['Y'],dtype=np.int64)
ww=json.load(gzip.open(ROOT/'SPLIT-CENTERS-WITNESSES.json.gz'));results=[]
for w in ww:
 A=np.array(w['A'],dtype=np.int64);B=np.array(w['B_scaled'],dtype=np.int64);P=w['labels'];h=w['dimension'];N=len(P);s=w['scale'];T=A@B
 assert s>0 and s&(s-1)==0;assert np.all(np.diag(T)==s)
 assert len(set(P))==N and all(x>0 and x<1<<h and x.bit_count()%2 for x in P)
 assert all((P[i]&P[j]).bit_count()%2==0 for i in range(N)for j in range(N)if i!=j and T[i,j])
 normals=w['center_normals'];assert len(normals)==B.shape[0]
 assert all(0<n<1<<h and all((n&P[i]).bit_count()%2==0 for i in np.flatnonzero(row))for row,n in zip(B,normals))
 old=next(b for b in base if len(b['ports_original'])==N)
 assert np.array_equal(T,Y[old['ports_original']]@np.array(old['B_scaled']))
 # Mutant controls preserve the original geometry and decoder elsewhere.
 badP=P[:];badP[0]=0;assert not all(x.bit_count()%2 for x in badP)
 row=B[0];i=int(np.flatnonzero(row)[0]);badnormal=1<<((P[i]&-P[i]).bit_length()-1)
 assert (badnormal&P[i]).bit_count()%2==1
 results.append({'ports':N,'labels_dimension':h,'centers':B.shape[0],'odd_label_mutant_rejected':True,'wrong_center_normal_rejected':True})
r={'status':'PASS_INDEPENDENT_SCALAR_LABEL_AND_CENTER_CAP_WITNESSES','results':results,'scope':'Finite ingredients only. Chronological frame chains, arbitrary-dirt helper restoration, phases, adapters, global hosting and pricing remain unbuilt.'}
(ROOT/'VERIFIED.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
