"""Independent scalar and response-column controls for the R480 line-class screen.
Usage: python verify_bit510_response_classes.py WORD ROOTS_JSON NONROOT_JSON OUTPUT_JSON
"""
from pathlib import Path
import gzip,json,sys
w=json.load(gzip.open(sys.argv[1]));V=w['v'];N=2*V+w['R'];first={};resp={h:0 for h in range(2*V,N)}
for ph in ('D','A','B','C'):
 for f,d,ss in w[ph]:
  if w['frames'][f]:
   for h in [d]+ss:
    if h>=2*V:first.setdefault(h,f)
for f,d,ss in w['D']:
 assert f==0 and V<=d<2*V
 for h in ss:resp[h]^=1<<(d-V)
assert all(resp.values())
def rank(cols):
 b={}
 for x in cols:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return len(b)
def alternate(cols):
 piv=[]
 for x in cols:
  for y in piv:x=min(x,x^y)
  if x:piv.append(x)
 return len(piv)
rows=[]
for line in range(V):
 hs=sorted(h for h,f in first.items()if line in w['frames'][f]);rr=rank([resp[h]for h in hs]);assert rr==len(hs);rows.append(dict(line=line,helpers=hs,rank=rr,nullity=0))
x=[1<<i for i in range(N)]
for ph in ('D','A','B','C'):
 if ph=='B':
  vals=[x[h]for h in w['ret']]
  for t,ss in enumerate(w['scatter']):
   for s in ss:x[V+t]^=vals[s]
 for f,d,ss in w[ph]:
  for s in ss:x[d]^=x[s]
assert x==[(1<<i)^((1<<(i-V))if V<=i<2*V else 0)for i in range(N)]
roots=json.load(open(sys.argv[2]));extra=json.load(open(sys.argv[3]));assert roots['root_classes']==rows
for row in rows+extra['classes']:assert alternate([resp[h]for h in row['helpers']])==row['rank']==len(row['helpers'])
res=dict(status='PASS_INDEPENDENT_SCALAR_AND_TWO_GF2_RANK_ENGINES',columns=N,helpers=w['R'],root_classes=len(rows),nonroot_classes=len(extra['classes']),zero_response_helpers=0,scope='Checks scalar word and ranks of the independently enumerated geometric classes. The enumeration completeness is supplied by the exact plane-intersection screen.')
Path(sys.argv[4]).write_text(json.dumps(res,indent=2)+'\n');print(res)
