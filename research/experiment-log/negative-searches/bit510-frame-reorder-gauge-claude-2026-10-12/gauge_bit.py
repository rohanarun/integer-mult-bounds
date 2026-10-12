exec(open('bsa.py').read().split("mut=[k for k")[0].replace("WORD,SEED,SECS,OUT=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]),sys.argv[4]","WORD='/tmp/w510/research/e8-r480-dead-totals/data/bitE8mut-r480.json.gz';SEED=0;SECS=0;OUT='x'"))
from collections import defaultdict
resp=defaultdict(set)
for g in c['D']:
    for s in g[2]: resp[s].add(g[1]-v)
# first frame of helper after D: next node after the D node / start
first={}
for r in range(2*v,n):
    k=head[r]
    while (k,r) in nxt:
        k=nxt[k,r]
        if nodes[k]['F']: first[r]=nodes[k]['F'];break
def ipl(a,b): return sum(x*y for x,y in zip(L[a],L[b]))
# y first nonzero frame (in B) and final cap
yfirst={}
for t in range(v):
    r=v+t;k=head[r]
    while (k,r) in nxt:
        k=nxt[k,r]
        if nodes[k]['F']: yfirst[t]=nodes[k]['F'];break
cnt=Counter();ok=[]
for h in range(2*v,n):
    F=first.get(h)
    if F is None or dim(F)!=1: cnt['first dim %s'%(dim(F) if F else None)]+=1;continue
    T=resp[h]
    l=next(iter(F)) if len(F)==1 else None
    good=all(F<=yfirst[t] and all(ipl(x,t)==0 for x in F) for t in T)
    cnt['line-first, resp %d, compatible %s'%(len(T),good)]+=1
    if good: ok.append(h)
print(cnt)
# nesting: targets shared by gauges with different lines
lines_at=defaultdict(set)
for h in ok:
    for t in resp[h]: lines_at[t].add(first[h])
print('targets with >1 distinct gauge line',sum(1 for t,s in lines_at.items() if len(s)>1),'of',len(lines_at))
