import json,gzip
from collections import defaultdict,Counter
c=json.load(gzip.open('c112.json.gz')); v=c['v'];R=c['R'];n=2*v+R
par=list(range(n+64))
def f(x):
    while par[x]!=x: par[x]=par[par[x]];x=par[x]
    return x
def u(a,b): par[f(a)]=f(b)
for ph in ('precondition','compensation','A','cut','B'):
    for e in c[ph]:
        if e[0]=='add': u(e[1],e[2])
for t in range(v): u(t,v+t)  # decoder pairs source t with target t
comp=defaultdict(list)
for r in range(n): comp[f(r)].append(r)
sizes=Counter(len(x) for x in comp.values())
print('components by size',sorted(sizes.items())[:10],'num',len(comp))
small=[x for x in comp.values() if len(x)<20]
print('small components',[(len(x),[('S' if r<v else 'T' if r<2*v else 'H') for r in x]) for x in small][:10])
