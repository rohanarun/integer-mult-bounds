import sys,json
from fractions import Fraction as Q
from pathlib import Path
sys.set_int_max_str_digits(0)
sys.path.insert(0,'/home/claude/crocswap/w197/research/packed-source-assisted-bit')
import arithmetic as AR
BIT=Path('/home/claude/crocswap/w187')
c200=json.load(open('/home/claude/crocswap/w200/research/paired-cube-diagonal-bit-168/certificate.json'))
p=c200['bit']['profile'];im=AR.load('interval_moment',BIT/'research/paired-cube-local-bit-168/arithmetic/interval_moment.py')
def kap(extra):
    H={int(k):3*v for k,v in p['child_histogram'].items()};H.pop(60)
    H[21]-=9*extra;H[3]-=9*extra
    W=3*2*1760+3300+(9*(17114-extra-2200)-6600)//3
    mass=sum(r*n for r,n in H.items())
    row=dict(m=72,W=W,child_multiplicities=H,N=72*W-mass,L=0,total_rank=mass,maxchild=max(H))
    def paid(a):
        r=im.moment(row,a);l,u=im.log_interval(Q(72));e,f=im.exp_interval(a*l,a*u)
        w=Q(1,10**16)*Q(32*72*sum(H.values()),W);return r['upper']+w*f,r['lower']+w*e
    den=10**15;lo=0;hi=den//100
    while hi-lo>1:
        mid=(lo+hi)//2;u,l=paid(Q(mid,den))
        if u<1:lo=mid
        elif l>1:hi=mid
        else:break
    c=Q(lo,den);a=Q(c200['bit']['coarse']['ordinary_saving'])
    for _ in range(3):a=(1-c)*c+c*a
    return float(a/(1+a))
for e in [0,30,100,300]:print(e,kap(e))
