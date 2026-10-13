import json,gzip,sys
from fractions import Fraction as F
from collections import Counter
w=json.load(gzip.open(sys.argv[1]))
def basis(vs):
    b={}
    for x in vs:
        for p in sorted(b,reverse=True):
            if x>>p&1:x^=b[p]
        if x:
            p=x.bit_length()-1
            for q in b:
                if b[q]>>p&1:b[q]^=x
            b[p]=x
    return tuple(b[p] for p in sorted(b,reverse=True))
regs=lambda e:[e[1]]+([e[2]] if e[0]=='add' else [])
V=len(w['ports']);R=w['report']['R'];n=2*V+R
def apply(e,rows):
    if e[0]=='scale': rows[e[1]]={k:F(e[2],e[3])*x for k,x in rows[e[1]].items()}
    else:
        q=F(e[3],e[4])
        for k,x in list(rows[e[2]].items()):
            z=rows[e[1]].get(k,F(0))+q*x
            if z: rows[e[1]][k]=z
            else: rows[e[1]].pop(k,None)
raw=[{k:F(1)} for k in range(n)]
for e in w['A']+w['cut']+w['B']: apply(e,raw)
dirt=[{} for _ in range(n)]
for y in range(V,2*V): dirt[y]={k:a for k,a in raw[y].items() if k>=2*V}
for e in w['precondition']: apply(e,dirt)
resp=Counter(k for y in range(V,2*V) for k in dirt[y])
entering=set(map(int,w['start_extra']))
first={}
for sec in ('A','B'):
    for e in w[sec]:
        for q in regs(e):
            if q>=2*V and q not in first: first[q]=basis(e[-1])
low=set(map(int,w['helper_final']))
pre={q for e in w['precondition'] for q in regs(e)}
c=Counter()
for q in range(2*V,n):
    st=basis(w['start_extra'].get(str(q),[]))
    fr=first.get(q,())
    c[('entering' if q in entering else 'plain','zero-resp' if resp[q]==0 else 'resp','in-precond' if q in pre else '-','start',len(st),'first',len(fr))]+=1
for k,v in sorted(c.items(),key=str): print(k,v)
cold=[q for q in range(2*V,n) if q not in entering and resp[q]==0]
print('cold zero-resp helpers',len(cold),'in helper_final',sum(1 for q in cold if q in low),
      'end dims',Counter(len(basis(w['helper_final'].get(str(q),[1<<i for i in range(9)]))) for q in cold))
# gates touching a cold helper, in order, with frames, first 8 per helper (show one)
q0=cold[0]
seqq=[(sec,i,e) for sec in ('A','B') for i,e in enumerate(w[sec]) if q0 in regs(e)]
for s in seqq[:12]: print(s)
print('early tail gates on q0',[ (i,U) for i,U in w['early_cleanup'] if q0 in regs(w['cleanup'][i])][:5])
zf=Counter()
for q in cold:
    gs=[(sec,i,e) for sec in ('A','B') for i,e in enumerate(w[sec]) if q in regs(e)]
    zf[(sum(1 for s in gs if not s[2][-1]),len(gs))]+=1
print('cold helpers: (#zero-frame gates, #gates)',zf.most_common(6))
