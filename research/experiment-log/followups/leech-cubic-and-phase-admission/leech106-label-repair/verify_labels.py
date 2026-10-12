"""Independent saved-witness audit. Imports neither coloring nor label constructors."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import os,gzip,json,hashlib
from sympy import Matrix
P=Path(__file__).resolve().parent;assert os.path.ismount('/Volumes/SP AI 01_16') and os.access(P,os.W_OK)
source={w['seed']:w for w in json.load(gzip.open(P.parent/'leech-full-minimal-screen/PUNCTURED-WITNESSES.json.gz'))};ws=json.load(gzip.open(P/'REPAIRED-WITNESSES.json.gz'))
def span(xs):
 rows={}
 for x in xs:
  for k in sorted(rows,reverse=True):
   if x>>k&1:x^=rows[k]
  if x:rows[x.bit_length()-1]=x
 return rows
def inside(x,rows):
 for k in sorted(rows,reverse=True):
  if x>>k&1:x^=rows[k]
 return x==0
records=[]
for w in ws:
 old=source[w['source_seed']];assert w['vectors']==old['vectors'];U=Matrix(w['vectors']);G=U*U.T;N=U.rows;labels=w['labels'];h=w['dimension'];assert N==106 and U.to_DM().rank()==24
 assert w['transfer_scaled']==G.tolist() and w['transfer_denominator']==32
 def check(ls):
  assert len(set(ls))==N and all(0<x<1<<h and x.bit_count()%2 for x in ls)
  assert all(G[i,j]==0 or i==j or (ls[i]&ls[j]).bit_count()%2==0 for i in range(N) for j in range(N))
 check(labels)
 assert all(G[i,i]==32 for i in range(N));assert all(Fraction(int(z),32).denominator in [1,4] for z in G)
 frames=w['gather_frames'];assert len(frames)==24
 for j,F in enumerate(frames):
  S=span(F);ids=[i for i in range(N) if U[i,j]];V=span(labels[i] for i in ids);assert len(S)==len(F)==len(V)<h;assert all(inside(x,S) for x in V.values())
 gram=[sum(((labels[i]&labels[j]).bit_count()%2)<<j for j in range(N)) for i in range(N)];grank=len(span(gram));lrank=len(span(labels));q=max(w['coloring'])+1;assert grank==q
 assert all(((labels[i]&labels[j]).bit_count()%2)==int(w['coloring'][i]==w['coloring'][j]) for i in range(N) for j in range(N))
 maxclass=max(Counter(w['coloring']).values());radlower=(maxclass-1).bit_length();assert h==q+2*radlower
 controls=[]
 for kind in ['even','duplicate','orthogonality']:
  bad=labels[:]
  if kind=='even':bad[0]^=1
  elif kind=='duplicate':bad[0]=bad[1]
  else:
   i,j=next((i,j) for i in range(N) for j in range(i+1,N) if G[i,j]);one=next(k for k in range(h) if labels[j]>>k&1);zero=next(k for k in range(h) if not(labels[j]>>k&1));bad[i]^=(1<<one)|(1<<zero)
  try:check(bad)
  except AssertionError:controls.append(kind)
  else:raise AssertionError('bad labels accepted')
 records.append(dict(source_seed=w['source_seed'],ambient_dimension=h,gram_rank=grank,label_span_rank=lrank,max_color_class=maxclass,minimum_dimension_for_this_color_gram_with_distinct_ports=q+2*radlower,gather_ranks=list(map(len,frames)),copied_rank=sum(map(len,frames)),exact_scalar_rank=24,all_caps_pass=True,negative_controls=controls))
ans=dict(status='PASS_INDEPENDENT_FINITE_LABEL_AND_GATHER_AUDIT',witness_sha256=hashlib.sha256((P/'REPAIRED-WITNESSES.json.gz').read_bytes()).hexdigest(),records=records,scope='Checks exact fixed scalar Gram transfer, distinct odd labels, every nonzero offdiagonal correction, and exact proper gather spans. Selected color-block Gram optimal ambient dimension only, not a lower bound over alternative completions; no physical/global admission.')
(P/'VERIFIED.json').write_text(json.dumps(ans,indent=2)+'\n');print(json.dumps(ans,indent=2))
