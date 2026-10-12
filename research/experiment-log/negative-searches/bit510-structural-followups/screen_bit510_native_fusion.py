"""Exact compatibility screen for PR521 fusion on unchanged R480 frame chains.
This tests consecutive same-register orthogonal frame jumps, not arbitrary rewrites.
Prepared for rohanarun with OpenAI Codex assistance. Apache-2.0.
"""
from pathlib import Path
from collections import Counter
import gzip,json,hashlib,time
import sympy as S
R=Path(__file__).resolve().parent;O=R/'bit510-native-fusion';O.mkdir(exist_ok=False);t=time.monotonic()
p=R/'bit510-review/research/e8-r480-dead-totals/data/bitE8mut-r480.json.gz';w=json.load(gzip.open(p));v=w['v'];n=2*v+w['R'];h=w['h'];Z=S.zeros(h);I=S.eye(h)
proj=[];dim=[]
for f in w['frames']:
 if not f:P=Z
 else:
  rows=S.Matrix([w['lines'][i]for i in f]);basis=S.Matrix.vstack(*rows.rowspace());P=basis.T*(basis*basis.T).inv()*basis
 assert P==P.T and P*P==P
 proj.append(P);dim.append(int(S.trace(P)))
cur=list(w['start']);chains=[[]for _ in range(n)];values=[1<<i for i in range(n)];touchA=set();H=Counter();unique={}
def climb(r,f,loc):
 a=cur[r]
 if a==f:return
 E=proj[f]-proj[a];assert E*E==E and proj[a]*E==Z and E*proj[a]==Z
 rank=dim[f]-dim[a];assert rank>0 and E.rank()==rank
 chains[r].append((a,f,loc));H[rank]+=1;cur[r]=f
for sec in ['D','A','B','C']:
 if sec=='B':
  copied=[values[r]for r in w['ret']]
  for j,cs in enumerate(w['scatter']):
   for c in cs:values[v+j]^=copied[c]
 for k,(f,d,ss)in enumerate(w[sec]):
  for r in [d]+ss:
   if sec=='A'and r>=2*v:touchA.add(r)
   climb(r,f,[sec,k])
  for s in ss:values[d]^=values[s]
for r,f in enumerate(w['final']):climb(r,f,['final',r])
for r in range(n):assert values[r]==((1<<r)|(1<<(r-v))if v<=r<2*v else 1<<r)
assert dict(H)=={1:1200,2:1440,4:180,6:120}
pairs=Counter();rows=[]
for reg,ch in enumerate(chains):
 for left,right in zip(ch,ch[1:]):
  a,b,_=left;c,d,_=right;assert b==c;key=(a,b,d);pairs[key]+=1
for (a,b,c),count in sorted(pairs.items()):
 P=proj[b]-proj[a];Q=proj[c]-proj[b];assert P*Q==Z and Q*P==Z
 product=(I-2*P)*(I-2*Q)
 assert product==I-2*(P+Q) and product*product==I
 assert (product-I).rank()==int(S.trace(P)+S.trace(Q))>=2
 assert P*Q!=Q and (product-I)*(product-I)!=Z
 rows.append(dict(frames=[a,b,c],multiplicity=count,ranks=[int(S.trace(P)),int(S.trace(Q))],product_displacement_rank=(product-I).rank()))
# Positive control: distinct oblique projectors sharing an image meet the fusion criterion.
p0=S.Matrix([[1,0],[0,0]]);q0=S.Matrix([[1,1],[0,0]]);i2=S.eye(2);g=(i2-2*p0)*(i2-2*q0)
assert p0*p0==p0 and q0*q0==q0 and p0*q0==q0 and q0*p0==p0
assert g!=i2 and (g-i2).rank()==1 and (g-i2)**2==S.zeros(2) and g*g!=i2
out=dict(status='PASS_SCOPED_NATIVE_FUSION_COMPATIBILITY_OBSTRUCTION',word_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),registers=n,scalar_basis_columns=n,projectors=len(proj),climb_profile=dict(H),consecutive_pairs=sum(pairs.values()),distinct_pairs=len(rows),compatible_PR521_pairs=0,helpers_untouched_before_B=sorted(set(range(2*v,n))-touchA),pair_certificates=rows,positive_control='Oblique common-image rank-one projectors yield a nontrivial rank-one unipotent product',seconds=time.monotonic()-t,scope='Unchanged R480 same-register consecutive positive frame jumps only; center copies excluded. Intervening scalar interactions ignored as a relaxation. Orthogonal nested flags force disjoint jump images, so this specific common-image rank-one fusion does not apply. All480 helpers touched in A: PR535 untouched-before-B template also cannot transfer directly. No claim about redesigned charts, nonorthogonal frames, cross-register modules, changed words, or global impossibility.')
(O/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items()if k!='pair_certificates'},flush=True)
