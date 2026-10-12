# Joint search: reorder commuting scalar ops inside A and inside B, and lift/lower frames (monotone chains only).
import json,gzip,math,random,sys,time,copy
from collections import Counter
WORD,SEED,SECS,OUT=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
B=float(sys.argv[5]);TEMP0=float(sys.argv[6]);SEL=sys.argv[7];PSWAP=float(sys.argv[8]) if len(sys.argv)>8 else 0.5
random.seed(SEED)
w=json.loads(gzip.decompress(open(WORD,'rb').read()));sel=json.loads(gzip.decompress(open(SEL,'rb').read()))
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
hyper=lambda p: basis([x for x in range(1,512) if not (x&p).bit_count()%2])
starts=[(p,) for p in w['ports']]+[()]*(V+R)
for r,F in w.get('start_extra',{}).items(): starts[int(r)]=basis(F)
levels={int(t):basis(F) for t,F in w.get('target_levels',{}).items()}
nodes=[];head={};tail={}
prv={};nxt={}
def link_append(k,r):
    if r in tail: prv[k,r]=tail[r];nxt[tail[r],r]=k
    else: head[r]=k
    tail[r]=k
def node(regs,F,mut,lo=(),op=None):
    k=len(nodes);nodes.append(dict(regs=list(regs),F=basis(F),mut=mut,lo=basis(lo),op=op))
    for r in regs: link_append(k,r)
    return k
for r,F in enumerate(starts): node([r],F,False)
seq={'A':[],'B':[]}
for section in ('A','B'):
    if section=='B':
        for r,F in zip(w['centers'],w['center_frames']): node([r],F,False)
        for t in range(V): node([V+t],levels.get(t,()),False)
    for i,e in enumerate(w[section]):
        regs=e[1:3] if e[0]=='add' else e[1:2]
        o=sel[section][i]
        # lower bound: constructor frame only if it exceeds the join of the constructor's register frames (8 slack ops)
        seq[section].append(node(regs,e[-1],True,lo=o[-1] if o[-1] and len(basis(o[-1]))==8 else (),op=copy.deepcopy(e)))
for r in range(n): node([r],hyper(w['ports'][r-V]) if V<=r<2*V else FULL,False)
f=lambda r: r*((m/r)**B-1) if r>0 else 0.0
def fee_all():
    tot=0;H=Counter()
    for r in range(n):
        k=head[r]
        while (k,r) in nxt:
            q=nxt[k,r];d=len(nodes[q]['F'])-len(nodes[k]['F']);assert d>=0 and le(nodes[k]['F'],nodes[q]['F']),(r,k,q)
            if d:H[d]+=1
            k=q
    return sum(f(a)*b for a,b in H.items()),H
cur,H0=fee_all();best=cur;print('start',cur,dict(sorted(H0.items())),flush=True)
def edge_fee(edges,frames):
    s=0
    for p,q,_r in edges:
        d=len(frames.get(q,nodes[q]['F']))-len(frames.get(p,nodes[p]['F']))
        if d<0: return None
        s+=f(d)
    return s
def closure(ch):
    queue=list(ch)
    while queue:
        j=queue.pop();Fj=ch[j]
        for r in nodes[j]['regs']:
            q=nxt[j,r];Fq=ch.get(q,nodes[q]['F'])
            if not le(Fj,Fq):
                if not nodes[q]['mut']: return None
                ch[q]=join(Fq,Fj);queue.append(q)
            p=prv[j,r];Fp=ch.get(p,nodes[p]['F'])
            if not le(Fp,Fj):
                if not nodes[p]['mut']: return None
                Np=meet(Fp,Fj)
                if not le(nodes[p]['lo'],Np): return None
                ch[p]=Np;queue.append(p)
        if len(ch)>80: return None
    return ch
def incident(nodeset):
    E=set()
    for j in nodeset:
        for r in nodes[j]['regs']:
            E.add((prv[j,r],j,r));E.add((j,nxt[j,r],r))
    return E
def commute(a,b):
    ea,eb=nodes[a]['op'],nodes[b]['op']
    Wa={ea[1]};Ra={ea[1]}|({ea[2]} if ea[0]=='add' else set())
    Wb={eb[1]};Rb={eb[1]}|({eb[2]} if eb[0]=='add' else set())
    if ea[0]=='add' and eb[0]=='add' and ea[1]==eb[1]: return ea[2]!=eb[1] and eb[2]!=ea[1]
    return not (Wa&Rb) and not (Wb&Ra)
def swap_links(a,b,shared):
    for r in shared:
        p=prv[a,r];q=nxt[b,r]
        nxt[p,r]=b;prv[b,r]=p;nxt[b,r]=a;prv[a,r]=b;nxt[a,r]=q;prv[q,r]=a
t0=time.time();it=0;acc=0;swaps=0
while time.time()-t0<SECS:
    it+=1;T=TEMP0*(1-(time.time()-t0)/SECS)+1e-9
    if random.random()<PSWAP:
        sec='A' if random.random()<len(seq['A'])/(len(seq['A'])+len(seq['B'])) else 'B'
        S=seq[sec];i=random.randrange(len(S)-1);a,b=S[i],S[i+1]
        shared=set(nodes[a]['regs'])&set(nodes[b]['regs'])
        if not shared:
            S[i],S[i+1]=b,a;continue   # free move, no chain change
        if not commute(a,b): continue
        oldE=incident({a,b});oldf=edge_fee(oldE,{})
        swap_links(a,b,shared)
        best_opt=None
        for ch0 in ({a:join(nodes[a]['F'],nodes[b]['F'])},{b:meet(nodes[a]['F'],nodes[b]['F'])}):
            if not le(nodes[ch0.get(b,b) if False else b]['lo'],ch0.get(b,nodes[b]['F'])): continue
            ch=closure(dict(ch0))
            if ch is None: continue
            E=incident(set(ch)|{a,b});
            nf=edge_fee(E,ch)
            if nf is None: continue
            # old fee over the same edge set needs old links: approximate by recomputing with links swapped back
            best_opt=(ch,E,nf) if best_opt is None or nf<best_opt[2] else best_opt
        if best_opt is None: swap_links(b,a,shared);continue
        ch,E,nf=best_opt
        swap_links(b,a,shared);oE=incident(set(ch)|{a,b});of=edge_fee(oE,{});swap_links(a,b,shared)
        d=nf-of
        if d<-1e-12 or random.random()<math.exp(-d/T):
            for j,G in ch.items(): nodes[j]['F']=G
            S[i],S[i+1]=b,a;cur+=d;acc+=1;swaps+=1
        else: swap_links(b,a,shared)
    else:
        sec=None;k=random.randrange(len(nodes))
        z=nodes[k]
        if not z['mut']: continue
        F=z['F']
        if random.random()<0.5:
            Gm=FULL
            for r in z['regs']: Gm=meet(Gm,nodes[nxt[k,r]]['F'])
            cand=[x for x in sp(Gm) if x not in sp(F)] if random.random()<0.7 else [x for x in range(1,512) if x not in sp(F)]
            if not cand: continue
            G=join(F,(random.choice(cand),))
        else:
            if not F: continue
            Fb=list(F);coeffs=[random.randint(0,1) for _ in Fb]
            if not any(coeffs): continue
            vecs=[]
            for mask in range(1<<len(Fb)):
                v=0;par=0
                for ii,bb in enumerate(Fb):
                    if mask>>ii&1: v^=bb;par^=coeffs[ii]
                if par==0: vecs.append(v)
            G=basis(vecs)
            if not le(z['lo'],G): continue
        ch=closure({k:G})
        if ch is None: continue
        E=incident(set(ch));nf=edge_fee(E,ch)
        if nf is None: continue
        d=nf-edge_fee(E,{})
        if d<-1e-12 or random.random()<math.exp(-d/T):
            for j,G2 in ch.items(): nodes[j]['F']=G2
            cur+=d;acc+=1
    if cur<best-1e-9:
        best=cur;snap=(copy.deepcopy(seq),[z['F'] for z in nodes]);
        if it%1==0: bestsnap=snap
if best<fee_all()[0]+1e-6 and 'bestsnap' in dir(): pass
chk,H=fee_all()
print('iters',it,'acc',acc,'swaps',swaps,'cur',cur,'check',chk,'best',best,flush=True)
# write current state (final) -- also consistent
out=copy.deepcopy(w)
for sec in ('A','B'):
    ops=[]
    for k in seq[sec]:
        e=copy.deepcopy(nodes[k]['op']);e[-1]=list(nodes[k]['F']);ops.append(e)
    out[sec]=ops
def inverse(e):
    e=copy.deepcopy(e)
    if e[0]=='add': e[3]*=-1
    else: e[2],e[3]=e[3],e[2]
    e[-1]=list(FULL);return e
out['cleanup']=[inverse(e) for e in reversed(out['A']+out['B']) if not V<=e[1]<2*V]
json.dump(dict(fee=chk,start=fee_all and None,chain_profile=dict(sorted(H.items())),start_chain_profile=dict(sorted(H0.items()))),open(OUT+'.json','w'))
open(OUT+'.gz','wb').write(gzip.compress(json.dumps(out,sort_keys=True,separators=(',',':')).encode(),mtime=0))
