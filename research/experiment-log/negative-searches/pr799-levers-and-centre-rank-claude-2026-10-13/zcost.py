import sys
sys.argv=['x','/tmp/g44/x4/jx/FULL-WORD.json.gz','1','0','/tmp/sa3/zz','0.00166','0','0.3']
src=open('/tmp/sa3/sa3z.py').read().split("t0=time.time()")[0]
exec(src)
res=[]
for q in sorted(ZERO):
    # lines in the helper's eventual frames: try each line in its end frame
    best=None
    for x in sp(end[q]):
        if not x: continue
        ch=closure({q:(x,)})
        if ch is None: continue
        E=incident(set(ch));nf=efee(E,ch)
        if nf is None: continue
        d=nf-efee(E,{})
        if best is None or d<best[0]: best=(d,x,len(ch))
    res.append((q,best))
import collections
print(collections.Counter(None if b is None else round(b[0],4) for q,b in res).most_common(10))
print('unit fee f(1)=',f(1))
