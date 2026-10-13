# Joint reorder + frame-lift search for gauge44-lineage words (helper_final, early_cleanup tails, centre barriers).
# Swaps only pairs where >=1 gate writes a target (cleanup subsequence unchanged). Frames never drop below the input word's frames.
import json,gzip,math,random,sys,time,copy
from collections import Counter
WORD,SEED,SECS,OUT,B,TEMP0,PSWAP=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]),sys.argv[4],float(sys.argv[5]),float(sys.argv[6]),float(sys.argv[7])
random.seed(SEED)
w=json.loads(gzip.decompress(open(WORD,'rb').read()))
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
SP={}
def sp(F):
    s=SP.get(F)
    if s is None:
        s={0}
        for y in F: s|={x^y for x in s}
        s=frozenset(s);SP[F]=s
    return s
def join(F,G): return basis(list(F)+list(G))
def meet(F,G): return basis(sorted(sp(F)&sp(G)))
def le(F,G): return sp(F)<=sp(G)
V,R=len(w['ports']),w['report']['R'];m=73;n=2*V+R
FULL=basis([1<<i for i in range(9)])
start=[(p,) for p in w['ports']]+[()]*(V+R)
for q,U in w.get('start_extra',{}).items(): start[int(q)]=basis(U)
end=[FULL]*V+[basis([x for x in range(1,512) if (x&p).bit_count()%2==0]) for p in w['ports']]+[FULL]*R
for q,U in w.get('helper_final',{}).items(): end[int(q)]=basis(U)
lev={int(t):basis(U) for t,U in w.get('target_levels',{}).items()}
nodes=[];head={};tail={};prv={};nxt={}
def node(regs,F,mut,op=None,tag=None):
    k=len(nodes);nodes.append(dict(regs=list(regs),F=basis(F),mut=mut,lo=basis(F),op=op,tag=tag))
    for r in regs:
        if r in tail: prv[k,r]=tail[r];nxt[tail[r],r]=k
        else: head[r]=k
        tail[r]=k
    return k
regsof=lambda e:[e[1]]+([e[2]] if e[0]=='add' else [])
ZERO=set(json.load(open('/tmp/sa3/zero_cold.json')))
for r in range(n): node([r],start[r],r in ZERO)
for r in ZERO: nodes[r]['lo']=()
seq={'A':[],'B':[]}
for i,e in enumerate(w['A']): seq['A'].append(node(regsof(e),e[-1],True,copy.deepcopy(e),('A',i)))
for q,U in zip(w['centers'],w['center_frames']): node([q],U,False)
for t in range(V): node([V+t],lev.get(t,()),False)
for i,e in enumerate(w['B']): seq['B'].append(node(regsof(e),e[-1],True,copy.deepcopy(e),('B',i)))
tailn=[]
for j,(i,U) in enumerate(w.get('early_cleanup',[])): tailn.append(node(regsof(w['cleanup'][i]),U,True,None,('T',j)))
for r in range(n): node([r],end[r],False)
f=lambda r: r*((m/r)**B-1) if r>0 else 0.0
def chainH():
    H=Counter()
    for r in range(n):
        k=head[r]
        while (k,r) in nxt:
            q=nxt[k,r];d=len(nodes[q]['F'])-len(nodes[k]['F']);assert d>=0 and le(nodes[k]['F'],nodes[q]['F']),(r,k,q,nodes[k]['F'],nodes[q]['F'])
            if d:H[d]+=1
            k=q
    return H
H0=chainH();fee=lambda H:sum(f(a)*b for a,b in H.items());cur=fee(H0);best=cur
print('start',dict(sorted(H0.items())),cur,flush=True)
def closure(ch):
    for j in ch:
        if j<n and j not in ZERO: return None
    queue=list(ch)
    while queue:
        j=queue.pop();Fj=ch[j]
        for r in nodes[j]['regs']:
            q=nxt[j,r];Fq=ch.get(q,nodes[q]['F'])
            if not le(Fj,Fq):
                if not nodes[q]['mut']: return None
                ch[q]=join(Fq,Fj);queue.append(q)
            if (j,r) not in prv: continue
            p=prv[j,r];Fp=ch.get(p,nodes[p]['F'])
            if not le(Fp,Fj):
                if not nodes[p]['mut']: return None
                Np=meet(Fp,Fj)
                if not le(nodes[p]['lo'],Np): return None
                ch[p]=Np;queue.append(p)
        if len(ch)>80: return None
    return ch
def incident(S):
    E=set()
    for j in S:
        for r in nodes[j]['regs']:
            if (j,r) in prv: E.add((prv[j,r],j,r))
            E.add((j,nxt[j,r],r))
    return E
def efee(E,ch):
    s=0
    for p,q,_ in E:
        d=len(ch.get(q,nodes[q]['F']))-len(ch.get(p,nodes[p]['F']))
        if d<0: return None
        s+=f(d)
    return s
def istarget(k): e=nodes[k]['op'];return e is not None and V<=e[1]<2*V
def commute(a,b):
    ea,eb=nodes[a]['op'],nodes[b]['op']
    Wa={ea[1]};Ra=set(regsof(ea));Wb={eb[1]};Rb=set(regsof(eb))
    if ea[0]=='add' and eb[0]=='add' and ea[1]==eb[1]: return ea[2]!=eb[1] and eb[2]!=ea[1]
    return not (Wa&Rb) and not (Wb&Ra)
def swap_links(a,b,shared):
    for r in shared:
        p=prv[a,r];q=nxt[b,r]
        nxt[p,r]=b;prv[b,r]=p;nxt[b,r]=a;prv[a,r]=b;nxt[a,r]=q;prv[q,r]=a
mut=[k for k,z in enumerate(nodes) if z['mut']]
t0=time.time();it=acc=swaps=0
while time.time()-t0<SECS:
    it+=1;T=TEMP0*(1-(time.time()-t0)/SECS)+1e-12
    if random.random()<PSWAP:
        sec='A' if random.random()<0.5 else 'B'
        S=seq[sec];i=random.randrange(len(S)-1);a,b=S[i],S[i+1]
        if not(istarget(a) or istarget(b)): continue
        shared=set(nodes[a]['regs'])&set(nodes[b]['regs'])
        if not shared: S[i],S[i+1]=b,a;continue
        if not commute(a,b): continue
        oE=incident({a,b});of=efee(oE,{})
        swap_links(a,b,shared);bo=None
        for ch0 in ({a:join(nodes[a]['F'],nodes[b]['F'])},{b:meet(nodes[a]['F'],nodes[b]['F'])}):
            if not le(nodes[b]['lo'],ch0.get(b,nodes[b]['F'])): continue
            ch=closure(dict(ch0))
            if ch is None: continue
            E=incident(set(ch)|{a,b});nf=efee(E,ch)
            if nf is None: continue
            if bo is None or nf<bo[1]: bo=(ch,nf)
        if bo is None: swap_links(b,a,shared);continue
        ch,nf=bo
        swap_links(b,a,shared);of=efee(incident(set(ch)|{a,b}),{});swap_links(a,b,shared)
        d=nf-of
        if d<-1e-12 or (d<=1e-12 and TEMP0==0) or (TEMP0>0 and random.random()<math.exp(-d/T)):
            for j,G in ch.items(): nodes[j]['F']=G
            S[i],S[i+1]=b,a;cur+=d;acc+=1;swaps+=1
        else: swap_links(b,a,shared)
    else:
        k=random.choice(mut);z=nodes[k];F=z['F']
        if random.random()<0.6:
            Gm=FULL
            for r in z['regs']: Gm=meet(Gm,nodes[nxt[k,r]]['F'])
            cand=[x for x in sp(Gm) if x not in sp(F)] if random.random()<0.8 else [x for x in range(1,512) if x not in sp(F)]
            if not cand: continue
            G=join(F,(random.choice(cand),))
        else:
            if len(F)==len(z['lo']): continue
            Fb=list(F);co=[random.randint(0,1) for _ in Fb]
            if not any(co): continue
            vecs=[]
            for mask in range(1<<len(Fb)):
                v=0;par=0
                for ii,bb in enumerate(Fb):
                    if mask>>ii&1: v^=bb;par^=co[ii]
                if par==0: vecs.append(v)
            G=basis(vecs)
            if not le(z['lo'],G): continue
        ch=closure({k:G})
        if ch is None: continue
        E=incident(set(ch));nf=efee(E,ch)
        if nf is None: continue
        d=nf-efee(E,{})
        if d<-1e-12 or (d<=1e-12 and TEMP0==0) or (TEMP0>0 and random.random()<math.exp(-d/T)):
            for j,G2 in ch.items(): nodes[j]['F']=G2
            cur+=d;acc+=1
    if cur<best-1e-9: best=cur
H=chainH()
print('starts',{r:nodes[r]['F'] for r in ZERO if nodes[r]['F']});print('iters',it,'acc',acc,'swaps',swaps,'fee',fee(H),'start',fee(H0),'chain',dict(sorted(H.items())),flush=True)
out=copy.deepcopy(w)
for sec in ('A','B'):
    out[sec]=[]
    for k in seq[sec]:
        e=copy.deepcopy(nodes[k]['op']);e[-1]=list(nodes[k]['F']);out[sec].append(e)
out['early_cleanup']=[[i,list(nodes[tailn[j]]['F'])] for j,(i,U) in enumerate(w.get('early_cleanup',[]))]
json.dump(dict(fee=fee(H),start=fee(H0),chain=dict(sorted(H.items())),chain0=dict(sorted(H0.items()))),open(OUT+'.json','w'))
open(OUT+'.gz','wb').write(gzip.compress(json.dumps(out,sort_keys=True,separators=(',',':')).encode(),mtime=0))
