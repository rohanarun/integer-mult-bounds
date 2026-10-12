from repair import *
G=[int(h) for h in SEL['gauge']]
P=word['ports']
feas={}
for h in G:
    S=set(g.span(first[h]))
    for t in col[h]: S&=set(g.span(g.perp(P[t])))
    feas[h]=sorted(S-{0,6})
print(Counter(len(v) for v in feas.values()))
b0,_=evaluate(SEL)
cnt=Counter(g.basis([6,y]) for h in G for y in feas[h])
print(cnt.most_common(8))
best=[]
for E,c in cnt.most_common(20):
    s=copy.deepcopy(SEL);hs=[h for h in G if g.span(E)<=g.span(first[h]) and all(x in feas[h] or x in (0,6) for x in g.span(E))]
    for h in hs: s['gauge'][str(h)]=list(E)
    b,info=evaluate2(s)
    print(E,len(hs),None if b is None else '%+.4f%%'%((b-b0)/b0*100),info if b is None else (info[0],info[1]))
