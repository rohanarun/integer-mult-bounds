"""Exact Gaussian-dyadic Clifford amplitudes by quadratic path sums.
No Hilbert-space vector is allocated. Tableau operations are pinned compiler code;
phase path sums and their Gaussian elimination are implemented independently here.
"""
import clifford_exact as ce

def bits(m):
 while m:b=m&-m;yield b.bit_length()-1;m^=b
class Poly:
 def __init__(self,n):self.n=n;self.c=0;self.a=[0]*n;self.edges=set()
 def pair(self,i,j):
  if i==j:self.a[i]=(self.a[i]+2)%4;return
  e=(min(i,j),max(i,j))
  if e in self.edges:self.edges.remove(e)
  else:self.edges.add(e)
 def form(self,c,m,k):
  k%=4
  if c:self.c=(self.c+k)%4;k=(-k)%4
  ids=list(bits(m))
  for i in ids:self.a[i]=(self.a[i]+k)%4
  if k%2:
   for ii,i in enumerate(ids):
    for j in ids[ii+1:]:self.pair(i,j)
 def product2(self,c,m,d,l):
  self.c=(self.c+2*c*d)%4
  if c:self.form(0,l,2)
  if d:self.form(0,m,2)
  for i in bits(m):
   for j in bits(l):self.pair(i,j)
 def substitute(self,images,n):
  p=Poly(n);p.c=self.c
  for i,a in enumerate(self.a):p.form(*images[i],a)
  for i,j in self.edges:p.product2(*images[i],*images[j])
  return p
 def val(self,x):return (self.c+sum(self.a[i] for i in bits(x))+2*sum(bool(x>>i&1 and x>>j&1) for i,j in self.edges))%4

def cmul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def iphase(k):return[(1,0),(0,1),(-1,0),(0,-1)][k%4]
def gauss(p):
 """Sum i^p(x) over all binary x, returning two exact integers."""
 fac=(1,0)
 while p.n:
  i=next((i for i,a in enumerate(p.a) if a%2),0);a=p.a[i]
  neigh=[j if k==i else k for k,j in p.edges if k==i or j==i]
  keep=[j for j in range(p.n) if j!=i];pos={j:k for k,j in enumerate(keep)}
  imgs=[(0,0) if j==i else (0,1<<pos[j]) for j in range(p.n)]
  q=p.substitute(imgs,len(keep))
  if a%2:
   q.form(0,sum(1<<pos[j] for j in neigh),-a)
   z=iphase(a);fac=cmul(fac,(1+z[0],z[1]));p=q
  else:
   fac=(2*fac[0],2*fac[1])
   if not neigh:
    if a==2:return(0,0)
    p=q;continue
   pivot=pos[neigh[0]];other=[pos[j] for j in neigh[1:]];rest=[j for j in range(q.n) if j!=pivot];rp={j:k for k,j in enumerate(rest)}
   imgs=[(a//2,sum(1<<rp[j] for j in other)) if j==pivot else (0,1<<rp[j]) for j in range(q.n)]
   p=q.substitute(imgs,len(rest))
 return cmul(fac,iphase(p.c))

def solve(rows,rhs,n):
 a=[int(z)|(int(v)<<n) for z,v in zip(rows,rhs)];piv=[];k=0
 for j in range(n):
  z=next((i for i in range(k,len(a)) if a[i]>>j&1),None)
  if z is None:continue
  a[k],a[z]=a[z],a[k]
  for i in range(len(a)):
   if i!=k and a[i]>>j&1:a[i]^=a[k]
  piv.append(j);k+=1
 if any((x&((1<<n)-1))==0 and x>>n&1 for x in a):return None
 y0=sum(((a[i]>>n)&1)<<j for i,j in enumerate(piv));free=[j for j in range(n) if j not in piv]
 basis=[(1<<j)|sum(((a[i]>>j)&1)<<v for i,v in enumerate(piv)) for j in free]
 return y0,basis

def amplitude(op,target,basis=0):
 forms=[((basis>>i)&1,0) for i in range(op.n)];poly=Poly(0);fac=(1,0);den=0
 for e in op.circuit:
  if e[0]=='C':
   q,s=e[1:];m=poly.n;poly.n+=1;poly.a.append((-s)%4);fac=cmul(fac,(1,s));den+=1
   forms=[(c,mask^(1<<m)) if q>>i&1 else(c,mask) for i,(c,mask) in enumerate(forms)]
  elif e[0]=='X':forms=[(c^((e[1]>>i)&1),m) for i,(c,m) in enumerate(forms)]
  elif e[0]=='P':
   new=[]
   for row in e[1]:
    c=m=0
    for i in bits(row):c^=forms[i][0];m^=forms[i][1]
    new.append((c,m))
   forms=new
  elif e[0]=='D':
   Q,alpha=e[1:]
   for i,a in enumerate(alpha):poly.form(*forms[i],a)
   for i in range(op.n):
    for j in range(i+1,op.n):
     if Q[i]>>j&1:poly.product2(*forms[i],*forms[j])
  elif e[0]=='phase':poly.c=(poly.c+e[1])%4
  else:raise AssertionError(e)
 solved=solve([m for c,m in forms],[c^((target>>i)&1) for i,(c,m) in enumerate(forms)],poly.n)
 if solved is None:return(0,0,0)
 y0,bs=solved;images=[((y0>>i)&1,sum(((v>>i)&1)<<j for j,v in enumerate(bs))) for i in range(poly.n)]
 total=cmul(fac,gauss(poly.substitute(images,len(bs))));a,b=total
 while den and a%2==b%2==0:a//=2;b//=2;den-=1
 return a,b,den

def support_point(op):
 """Support affine equations from diagonal products of output stabilizers."""
 n=op.n;st=op.tab[n:];xrows=ce.transpose([x for x,z,p in st],n);coeffs=ce.nullspace(xrows,n);rows=[];rhs=[]
 for mask in coeffs:
  out=(0,0,0)
  for j in bits(mask):out=ce.pmul(out,st[j])
  x,z,p=out;assert x==0 and p%2==0;rows.append(z);rhs.append(p//2)
 sol=solve(rows,rhs,n);assert sol is not None
 return sol[0]
def same(op,other):
 if op.tab!=other.tab:return False
 x=support_point(op);a=amplitude(op,x);assert a[:2]!=(0,0)
 return a==amplitude(other,x)

def monomial(op):
 n=op.n;T=op.tab;assert all(x==0 and p%2==0 for x,z,p in T[n:]);G=ce.transpose([x for x,z,p in T[:n]],n);b=ce.mv(G,sum((p//2)<<i for i,(x,z,p) in enumerate(T[n:])))
 gt=ce.transpose(G,n);cols=[ce.mv(gt,z) for x,z,p in T[:n]];Q=ce.transpose(cols,n);alpha=[(p-2*ce.parity(b&z))%4 for x,z,p in T[:n]]
 out=ce.diag(n,Q,alpha).then(ce.perm(n,G)).then(ce.xgate(n,b));assert out.tab==T
 a,im,den=amplitude(op,b);assert den==0;phase=[(1,0),(0,1),(-1,0),(0,-1)].index((a,im));out=out.then(ce.Op(n,ce.identity(n),[('phase',phase)]));assert same(out,op)
 return out,dict(matrix_rows=G,offset=b,quadratic_rows=Q,linear_Z4=alpha,phase=phase)
def lower_child(op):
 """Pinned elimination algebra, with phase-sensitive polynomial-size amplitude checks."""
 n=op.n;Bcols=[x for x,z,p in op.tab[n:]];r=ce.rank(Bcols)
 if not r:
  mon,rec=monomial(op);return dict(rank=0,left=rec,right=None),mon
 G=ce.transpose(ce.basis_extend(Bcols,n),n);A=ce.inv(G,n);PA=ce.perm(n,A);part=op.then(PA);Bcols=[x for x,z,p in part.tab[n:]];Dcols=[z for x,z,p in part.tab[n:]]
 picks=[];selected=[]
 for j,x in enumerate(Bcols):
  if ce.rank(selected+[x])>len(selected):picks.append(j);selected.append(x)
 assert len(picks)==r and all(x>>r==0 for x in Bcols)
 Br=ce.transpose(selected,r);Bi=ce.inv(Br,r);Dr=ce.transpose([Dcols[j]&((1<<r)-1) for j in picks],r)
 Qsmall=tuple(sum(ce.parity(row&col)<<j for j,col in enumerate(ce.transpose(Bi,r))) for row in Dr);Q=Qsmall+(0,)*(n-r);DQ=ce.diag(n,Q)
 V=part.then(DQ).then(ce.hadamard(n,range(r)));assert all(x==0 for x,z,p in V.tab[n:]);Vmon,Vrec=monomial(V)
 S=ce.diag(n,tuple(1<<i if i<r else 0 for i in range(n)))
 left=S.adjoint().then(DQ.adjoint()).then(PA.adjoint());right=Vmon.then(S.adjoint()).then(ce.xgate(n,(1<<r)-1))
 lmon,lrec=monomial(left);rmon,rrec=monomial(right);compiled=rmon.then(ce.fourier(n,range(r))).then(lmon)
 assert same(compiled,op)
 return dict(rank=r,left=lrec,right=rrec),compiled
