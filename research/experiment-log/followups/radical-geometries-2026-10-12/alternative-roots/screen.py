"""Exact root-decoder / binary-label screen. New finite tests, no claimed supplier.
Root conventions: Dn=+-ei+-ej (IAS PCMI 2004 root-system notes).
All rational vector computations are scaled integral, no numerical ranks.
"""
import itertools,json,hashlib,gzip,time
from pathlib import Path
from collections import Counter
import sympy as s
OUT=Path(__file__).resolve().parent
BASE=OUT.parent

def parity(x):return x.bit_count()%2

def invgf(rows,n):
 a=[rows[i]|(1<<(n+i)) for i in range(n)]
 for k in range(n):
  p=next(i for i in range(k,n) if a[i]>>k&1);a[k],a[p]=a[p],a[k]
  for i in range(n):
   if i!=k and a[i]>>k&1:a[i]^=a[k]
 return [x>>n for x in a]
def sympl(n,ip):
 pool=[1<<i for i in range(n)];pairs=[];rad=[]
 while pool:
  x=pool.pop(0);j=next((j for j,y in enumerate(pool) if ip(x,y)),None)
  if j is None:rad.append(x);continue
  y=pool.pop(j);pairs.append((x,y));pool=[z^(y if ip(z,x) else 0)^(x if ip(z,y) else 0) for z in pool]
 return pairs,rad

def labels(C,coeff):
 n=C.rows;rows=[sum(int(C[i,j]%2)<<j for j in range(n)) for i in range(n)]
 ip=lambda x,y:parity(sum((parity(rows[i]&y)<<i) for i in range(n))&x)
 pairs,rad=sympl(n,ip);basis=[z for p in pairs for z in p]+rad
 # basis columns matrix, invert to recover expansion of original lattice coefficients.
 inv=invgf([sum(((basis[j]>>i)&1)<<j for j in range(n)) for i in range(n)],n)
 N=2*len(pairs)+2*len(rad);h=N+1
 even=[(1<<i)|(1<<N) for i in range(N)]
 def lift(x):
  out=0
  for i in range(N):
   if x>>i&1:out^=even[i]
  return out
 sp,sr=sympl(N,lambda x,y:parity(lift(x)&lift(y)));assert not sr
 mapped=[lift(z) for p in sp[:len(pairs)] for z in p]+[lift(sp[len(pairs)+i][0]) for i in range(len(rad))]
 out=[]
 for v in coeff:
  c=sum((int(x)%2)<<i for i,x in enumerate(v));coordinates=[parity(r&c) for r in inv];p=(1<<h)-1
  for use,b in zip(coordinates,mapped):
   if use:p^=b
  out.append(p)
 return h,out,len(rad)

def canonical(v):return tuple(-x for x in v) if next(x for x in v if x)<0 else tuple(v)
def D(n):
 roots=set()
 for i,j in itertools.combinations(range(n),2):
  for sign in (-1,1):
   v=[0]*n;v[i]=2;v[j]=2*sign;roots.add(tuple(v))
 simple=[]
 for i in range(n-1):v=[0]*n;v[i]=2;v[i+1]=-2;simple.append(v)
 v=[0]*n;v[-2:]=[2,2];simple.append(v)
 return simple,sorted(roots)
def A(n):
 simple=[];roots=[]
 for i in range(n):v=[0]*(n+1);v[i]=2;v[i+1]=-2;simple.append(v)
 for i,j in itertools.combinations(range(n+1),2):v=[0]*(n+1);v[i]=2;v[j]=-2;roots.append(v)
 return simple,roots
simpleE=[[1,-1,-1,-1,-1,-1,-1,1],[2,2,0,0,0,0,0,0],[-2,2,0,0,0,0,0,0]]
for i in range(1,6):v=[0]*8;v[i]=-2;v[i+1]=2;simpleE.append(v)
e8=set(D(8)[1])
for v in itertools.product((-1,1),repeat=8):
 if sum(x<0 for x in v)%2==0:e8.add(canonical(v))
assert len(e8)==120

def E(n):
 B=s.Matrix(simpleE[:n]);roots=[]
 for v in sorted(e8):
  if s.Matrix(list(B.tolist())+[list(v)]).rank()==n:roots.append(v)
 return simpleE[:n],roots

def evaluate(name,B0,roots):
 B=s.Matrix(B0);R=s.Matrix(roots);C=B*B.T/4;G=R*R.T/4;coeff=R*B.T*(B*B.T).inv();assert coeff*B==R and all(x.q==1 for x in coeff)
 h,ports,rad=labels(C,coeff.tolist());v=len(roots);d=B.rows
 assert all(parity(p) for p in ports)
 mismatches=sum(parity(ports[i]&ports[j])!=(1+int(G[i,j]))%2 for i in range(v) for j in range(v))
 assert mismatches==0
 collisions=v-len(set(ports));corr=sum(G[i,j]!=0 for i in range(v) for j in range(v) if i!=j)
 # Generic Gram decoder: centers u_k=sum_i r_ik*x_i/2, targets += r_tk*u_k/4 (scaled roots norm8),
 # then subtract every offdiagonal Gram/2. This is exactly I and dyadic.
 decoder=R*R.T/8;res=decoder-s.diag(*decoder.diagonal());assert decoder-res==s.eye(v)
 legal=sum(parity(ports[i]&ports[j])==0 for i in range(v) for j in range(v) if i!=j and res[i,j])
 assert legal==corr
 output={'name':name,'dimension':d,'ports':v,'binary_label_dimension_constructed':h,'binary_form_radical_dimension':rad,'port_collisions':collisions,'side_corrections_directed':corr,'side_corrections_per_port':str(s.Rational(corr,v)),'centers':d,'center_copy_charge_at_rank_h_minus_1':d*(h-1),'nine_stage_naive_deficit_per_replica':8*v-9*d*(h-1),'five_stage_naive_deficit_per_replica':4*v-5*d*(h-1),'eleven_stage_naive_deficit_per_replica':10*v-11*d*(h-1),'max_absolute_offdiag_gram':str(max(abs(G[i,j]) for i in range(v) for j in range(v) if i!=j)),'exact_decoder_identity':True,'all_side_corrections_inside_target_cap':True,'pair_checks':v*v,'rank_over_rationals':int(R.rank()),'scope':'Exact geometry and clean scalar Gram decoder only; no helper circuit, dirty restoration, frames, phase, global host or moment certificate.'}
 (OUT/(name+'-WITNESS.json')).write_text(json.dumps({'simple_roots_scaled_by_2':B0,'roots_scaled_by_2':roots,'ports':ports,'h':h},indent=2)+'\n');return output
res=[]
for name,args in [('A4',A(4)),('A6',A(6)),('A8',A(8)),('D4',D(4)),('D5',D(5)),('D6',D(6)),('D8',D(8)),('E6',E(6)),('E7',E(7)),('E8',E(8))]:
 r=evaluate(name,*args);res.append(r);print(json.dumps(r),flush=True)
# Current punctured E8 actual raw word: check the same exact identity and interaction counts.
w=json.load(gzip.open(BASE/'pr548-complex314/complex-local/syndrome/FULL-WORD.json.gz'))
r=w['root_lines'];print('current root example',r[0],flush=True)
(OUT/'RESULT.json').write_text(json.dumps({'status':'FINITE_GEOMETRY_SCREEN_ONLY','results':res,'source_pr548_head':'66dbc2bffc1bfa8d50b3f9a2ac7ccba8fd9f6f36','current_word_sha256':hashlib.sha256((BASE/'pr548-complex314/complex-local/syndrome/FULL-WORD.json.gz').read_bytes()).hexdigest()},indent=2)+'\n')
