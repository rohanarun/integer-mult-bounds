import sys,json
from fractions import Fraction as Q
from pathlib import Path
sys.set_int_max_str_digits(0)
sys.path.insert(0,'/home/claude/crocswap/w197/research/packed-source-assisted-bit')
import arithmetic as AR
ROOT=Path('/home/claude/crocswap/w193');BIT=Path('/home/claude/crocswap/w187')
c200=json.load(open('/home/claude/crocswap/w200/research/paired-cube-diagonal-bit-168/certificate.json'))
p=c200['bit']['profile'];H={int(k):3*v for k,v in p['child_histogram'].items()}
assert H.pop(60)==6600
W=3*2*1760+3300+(9*(17114-2200)-6600)//3
mass=sum(r*n for r,n in H.items());print('W',W,'deficit',72*W-mass)
phys=dict(W=W,child_histogram=H,deficit=72*W-mass,conservative_selector_calls=10**10)
im=AR.load('interval_moment',BIT/'research/paired-cube-local-bit-168/arithmetic/interval_moment.py')
def profile(m,W,H,delta):
    return dict(m=m,W=W,child_multiplicities=H,N=delta,L=0,total_rank=sum(r*n for r,n in H.items()),maxchild=max(H))
packed=profile(72,W,H,72*W-mass)
def paid(row,a):
    r=im.moment(row,a);l,u=im.log_interval(Q(row['m']));e,f=im.exp_interval(a*l,a*u)
    w=Q(1,10**16)*Q(32*row['m']*sum(row['child_multiplicities'].values()),row['W'])
    return r['upper']+w*f, r['lower']+w*e
den=10**18;lo=0;hi=den//100
while hi-lo>1:
    mid=(lo+hi)//2;u,l=paid(packed,Q(mid,den))
    if u<1:lo=mid
    elif l>1:hi=mid
    else:raise SystemExit('inconclusive')
c=Q(lo,den);print('packed coarse c',float(c),c)
a0=Q(c200['bit']['coarse']['ordinary_saving']);print('a0 (#200 ordinary)',float(a0))
ch=[a0]
for _ in range(3): ch.append((1-c)*c+c*ch[-1])
print('a3',float(ch[-1]))
c191=json.load(open(ROOT/'research/source-assisted-v4/certificate.json'));print('complex profile W',c191['complex_profile']['W_per_vertex'])
beta=eta=Q(1,10**24);weak=Q(1,10**30)
b=Q(700918443859411,10**18)
a=min(ch[-1],(1-beta)*b-weak);q=a*(1-2*eta);bound=(1-eta)*q/(1+q);z=bound*den
k=Q((z.numerator-1)//z.denominator,den);print('kappa',float(k),k,'vs #202 6.768823e-4: %+.3f%%'%(100*(float(k)/6.768823e-4-1)))
