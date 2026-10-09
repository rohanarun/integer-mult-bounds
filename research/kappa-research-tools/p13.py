import sys,json,math,os
sys.argv=['x'];sys.path.insert(0,'/home/claude/crocswap/w168/research/paired-cube-bit')
import paired_cube_bit_word as B
p=int(os.environ.get('P','13'))
arcsf='/home/claude/crocswap/w168/research/paired-cube-bit/data/arcs_p%d.json'%p
arcs=json.load(open(arcsf)) if os.path.exists(arcsf) else None
if os.environ.get('FULLTECH'):
    src=open(B.__file__).read()
    src=src.replace("abo = pinned_all_but_one(QMODULES[p], p - 2) if p in QMODULES else all_but_one(p - 2)","abo = pinned_all_but_one(QMODULES[p], p - 2) if p in QMODULES else nested_prefix(p - 2)")
    src=src.replace("g = BitGraph(p).finish(mod, abo, merge=p == 12, l1=p == 12)","g = BitGraph(p).finish(mod, abo, merge=True, l1=True)")
    ns=dict(B.__dict__);exec(compile(src[src.index('def build('):src.index('def export(')],'b','exec'),ns);B.build=ns['build'];arcs=None
out,prf,arcs2,exp=B.build(p,arcs,log=print)
h=2*p;m=3*h;v=prf['v'];R=prf['R']
C={int(k):n for k,n in prf['child_histogram'].items()}
gh={int(k):n for k,n in prf['selected_rank_histogram'].items()}
for d,n in gh.items(): C[3*d]-=n
C={k:n for k,n in C.items() if n}
Wp=2*v+R-sum(d*n for d,n in gh.items())/h
def root(C,W):
    lo,hi=0.,.1
    for _ in range(80):
        a=(lo+hi)/2
        if math.fsum(n*(r/m)**(1-a) for r,n in C.items())<W: lo=a
        else: hi=a
    return lo
print('p',p,'h',h,'v',v,'R',R,'R/v %.3f'%(R/v),'gauges',gh,'unpacked %.6e'%B.float_root(prf['child_histogram'],prf['W_per_vertex'],m),'packed-virtual %.6e'%root(C,Wp))
