import sys,json
from fractions import Fraction as Q
from pathlib import Path
sys.set_int_max_str_digits(0)
sys.path.insert(0,'/home/claude/crocswap/w197/research/packed-source-assisted-bit')
import arithmetic as AR
im=AR.load('interval_moment',Path('/home/claude/crocswap/w187')/'research/paired-cube-local-bit-168/arithmetic/interval_moment.py')
c200=json.load(open('/home/claude/crocswap/w200/research/paired-cube-diagonal-bit-168/certificate.json'))
A0=Q(c200['bit']['coarse']['ordinary_saving'])
def kappa(hist,nphys=17114,ngauge=2200,v=1760,den=10**15,sinkdelta=True):
    H={int(k):3*n for k,n in hist.items()}
    if sinkdelta: H[21]-=102*3 if False else 0
    assert H.pop(60)==3*ngauge
    W=3*2*v+(9*(nphys-ngauge)+9*ngauge*4//24)//3 if False else 3*2*v+ (9*ngauge//6) + (9*(nphys-ngauge)-2*(9*ngauge//6))//3
    mass=sum(r*n for r,n in H.items())
    row=dict(m=72,W=W,child_multiplicities=H,N=72*W-mass,L=0,total_rank=mass,maxchild=max(H))
    def paid(a):
        r=im.moment(row,a);l,u=im.log_interval(Q(72));e,f=im.exp_interval(a*l,a*u)
        w=Q(1,10**16)*Q(32*72*sum(H.values()),W);return r['upper']+w*f,r['lower']+w*e
    lo=0;hi=den//100
    while hi-lo>1:
        mid=(lo+hi)//2;u,l=paid(Q(mid,den))
        if u<1:lo=mid
        elif l>1:hi=mid
        else:break
    c=Q(lo,den);a=A0
    for _ in range(3):a=(1-c)*c+c*a
    return float(c),float(a/(1+a)),W,72*W-mass
if __name__=='__main__':
    p=c200['bit']['profile']
    print('PR200 terminal',kappa(p['child_histogram']))
    d=json.load(open(sys.argv[1]))
    def sink(hh):
        hh={int(k):n for k,n in hh.items()};hh[21]-=102;hh[3]-=102;return hh
    print('base (pre-sink, +sink delta)',kappa(sink(d['base']),17114))
    print('new  (+same sink delta)',kappa(sink(d['new']),17114))
