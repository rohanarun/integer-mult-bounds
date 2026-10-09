import sys,json,math,collections,os
sys.argv=['x'];sys.path.insert(0,'/home/claude/crocswap/w168/research/paired-cube-bit')
import paired_cube_bit_word as B
MODE=os.environ.get('MODE','base')
src=open(B.__file__).read()
s0=src.index('def select_gauges');s1=src.index('def profile(')
fn=src[s0:s1]
if MODE=='relax':
    fn=fn.replace("if delta >= -1e-12 or not nondeg_id","if not nondeg_id")
elif MODE.startswith('packed'):
    # packed-aware objective: value of a gauge of dim d = removal of d/24 of a chain (W) plus local shift; target costs unchanged
    lam=float(MODE[6:] or '1')
    fn=fn.replace("delta = 3 * (excess(r - d) - excess(r)) + excess(3 * d)","delta = 3 * (excess(r - d) - excess(r)) - lam * 3 * d * trial_a")
ns=dict(B.__dict__);ns['lam']=float(MODE[6:] or '1') if MODE.startswith('packed') else 1.0
exec(compile(fn,'sel','exec'),ns)
B.select_gauges=ns['select_gauges']
arcs=json.load(open('/home/claude/crocswap/w168/research/paired-cube-bit/data/arcs_p12.json'))
out,prf,arcs2,exp=B.build(12,arcs,log=lambda *a:None)
h=24;m=72;v=prf['v'];R=prf['R']
C={int(k):n for k,n in prf['child_histogram'].items()}
gh={int(k):n for k,n in prf['selected_rank_histogram'].items()}
for d,n in gh.items(): C[3*d]-=n
C={k:n for k,n in C.items() if n}
Wp=2*v+R-sum(d*n for d,n in gh.items())/24
mass=sum(r*n for r,n in C.items())
def root(C,W):
    lo,hi=0.,.1
    for _ in range(80):
        a=(lo+hi)/2
        if math.fsum(n*(r/m)**(1-a) for r,n in C.items())<W: lo=a
        else: hi=a
    return lo
print(MODE,'R',R,'gauges',gh,'unpacked root %.6e'%B.float_root(prf['child_histogram'],prf['W_per_vertex'],m),'packed-virtual W %.1f root %.6e'%(Wp,root(C,Wp)),'deficit',m*Wp-mass)
