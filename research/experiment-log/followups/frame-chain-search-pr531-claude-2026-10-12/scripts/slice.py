import json,gzip,sys
from fractions import Fraction as Q
src,sel_src,out,out_sel=sys.argv[1:5]
w=json.load(gzip.open(src));sel=json.load(gzip.open(sel_src))
V=len(w['ports']);R=w['report']['R'];n=2*V+R
removed_total=0
while True:
    ops=[('A',i,e) for i,e in enumerate(w['A'])]+[('cut',i,e) for i,e in enumerate(w['cut'])]+[('B',i,e) for i,e in enumerate(w['B'])]
    obs=[{} for _ in range(n)]
    for t in range(V,2*V): obs[t]={t:Q(1)}
    dead=set()
    for sec,i,e in reversed(ops):
        if e[0]=='add':
            _,t,s,a,b=e[:5];q=Q(a,b)
            if not obs[t] and not (V<=t<2*V): dead.add((sec,i))
            for k,x in obs[t].items():
                z=obs[s].get(k,0)+q*x
                if z: obs[s][k]=z
                else: obs[s].pop(k,None)
        else:
            _,t,a,b=e[:4];q=Q(a,b)
            if not obs[t] and not (V<=t<2*V): dead.add((sec,i))
            obs[t]={k:x*q for k,x in obs[t].items()}
    if not dead: break
    removed_total+=len(dead)
    for sec in ('A','B'):
        keep=[i for i in range(len(w[sec])) if (sec,i) not in dead]
        w[sec]=[w[sec][i] for i in keep];sel[sec]=[sel[sec][i] for i in keep]
    assert not any(s=='cut' for s,i in dead)
print('removed',removed_total,'A',len(w['A']),'B',len(w['B']))
for x,o in ((w,out),(sel,out_sel)):
    open(o,'wb').write(gzip.compress(json.dumps(x,sort_keys=True,separators=(',',':')).encode(),mtime=0))
