# Frame-lift local search for 'bitE8/1+mut' words: frames = root-closed subspaces of the E8 root lines.
import json,gzip,math,random,sys,time,copy
from collections import Counter
WORD,SEED,SECS,OUT=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
CAT_ONLY=len(sys.argv)>5 and sys.argv[5]=='cat'
TEMP0=float(sys.argv[6]) if len(sys.argv)>6 else 0.0
random.seed(SEED)
c=json.load(gzip.open(WORD))
v,h,R=c['v'],c['h'],c['R'];n=2*v+R;m=64;B=0.0015874
L=[tuple(x) for x in c['lines']];P=2147483647
def rank_and_basis(idx):
    rows=[];piv=[]
    for i in idx:
        r=[x%P for x in L[i]]
        for (pc,pr) in zip(piv,rows):
            if r[pc]:
                f=r[pc];r=[(a-f*b)%P for a,b in zip(r,pr)]
        nz=next((k for k,x in enumerate(r) if x),None)
        if nz is not None:
            inv=pow(r[nz],P-2,P);r=[x*inv%P for x in r]
            for j in range(len(rows)):
                if rows[j][nz]:
                    f=rows[j][nz];rows[j]=[(a-f*b)%P for a,b in zip(rows[j],r)]
            rows.append(r);piv.append(nz)
    return rows,piv
CL={}
def close(idx):
    key=frozenset(idx)
    if key in CL: return CL[key]
    rows,piv=rank_and_basis(sorted(key))
    out=[]
    for i in range(v):
        r=[x%P for x in L[i]]
        for pc,pr in zip(piv,rows):
            if r[pc]: f=r[pc];r=[(a-f*b)%P for a,b in zip(r,pr)]
        if not any(r): out.append(i)
    F=frozenset(out);CL[key]=F;CL[F]=F;DIM[F]=len(rows);return F
DIM={}
def dim(F): 
    if F not in DIM: close(F)
    return DIM[F]
cat=[close(f) for f in c['frames']]
catset=set(cat)
def join(F,G): return close(F|G)
def meet(F,G): return close(F&G)
def le(F,G): return F<=G
nodes=[];head={};tail={};prv={};nxt={}
def node(regs,F,mut,gate=None):
    k=len(nodes);nodes.append(dict(regs=list(regs),F=F,mut=mut,gate=gate))
    for r in regs:
        if r in tail: prv[k,r]=tail[r];nxt[tail[r],r]=k
        else: head[r]=k
        tail[r]=k
    return k
for r in range(n): node([r],cat[c['start'][r]],False)
for g in c['D']: node([g[1]]+g[2],cat[g[0]],False)
seq={'A':[],'B':[]}
for i,g in enumerate(c['A']): seq['A'].append(node([g[1]]+g[2],cat[g[0]],True,('A',i)))
# scatter barrier: y at 0, ret registers frozen at their current frame (centre ranks fixed)
cur={}
for r in range(n):
    k=tail[r];cur[r]=nodes[k]['F']
for t in range(v): node([v+t],frozenset(),False)
for q in c['ret']: node([q],cur[q],False)
for i,g in enumerate(c['B']): seq['B'].append(node([g[1]]+g[2],cat[g[0]],True,('B',i)))
for g in c['C']: node([g[1]]+g[2],cat[g[0]],False)
for r in range(n): node([r],cat[c['final'][r]],False)
f=lambda r: r*((m/r)**B-1) if r>0 else 0.0
def chain_H():
    H=Counter()
    for r in range(n):
        k=head[r]
        while (k,r) in nxt:
            q=nxt[k,r];a,b=nodes[k]['F'],nodes[q]['F'];assert a<=b,(r,k,q)
            d=dim(b)-dim(a)
            if d:H[d]+=1
            k=q
    return H
H0=chain_H();cent=Counter(dim(cur[q]) for q in c['ret'])
print('chain',dict(sorted(H0.items())),'centre',dict(cent),'local',dict(sorted((H0+cent).items())),flush=True)
fee=lambda H: sum(f(a)*b for a,b in H.items())
curfee=fee(H0);best=curfee;bestF=[z['F'] for z in nodes];bestseq=None
def closure(ch):
    queue=list(ch)
    while queue:
        j=queue.pop();Fj=ch[j]
        for r in nodes[j]['regs']:
            q=nxt[j,r];Fq=ch.get(q,nodes[q]['F'])
            if not Fj<=Fq:
                if not nodes[q]['mut']: return None
                ch[q]=join(Fq,Fj);queue.append(q)
            p=prv[j,r];Fp=ch.get(p,nodes[p]['F'])
            if not Fp<=Fj:
                if not nodes[p]['mut']: return None
                ch[p]=meet(Fp,Fj);queue.append(p)
        if len(ch)>100: return None
    if CAT_ONLY and any(F not in catset for F in ch.values()): return None
    return ch
def incident(S):
    E=set()
    for j in S:
        for r in nodes[j]['regs']: E.add((prv[j,r],j,r));E.add((j,nxt[j,r],r))
    return E
def efee(E,ch):
    s=0
    for p,q,r in E:
        d=dim(ch.get(q,nodes[q]['F']))-dim(ch.get(p,nodes[p]['F']))
        if d<0: return None
        s+=f(d)
    return s
mut=[k for k,z in enumerate(nodes) if z['mut']]
PSWAP=float(sys.argv[7]) if len(sys.argv)>7 else 0.6
def commute(a,b):
    ga,gb=nodes[a]['regs'],nodes[b]['regs']
    da,sa=ga[0],set(ga[1:]);db,sb=gb[0],set(gb[1:])
    return da not in sb and db not in sa
def swap_links(a,b,shared):
    for r in shared:
        p=prv[a,r];q=nxt[b,r]
        nxt[p,r]=b;prv[b,r]=p;nxt[b,r]=a;prv[a,r]=b;nxt[a,r]=q;prv[q,r]=a
swaps=0

t0=time.time();it=0;acc=0
while time.time()-t0<SECS:
    it+=1;T=TEMP0*(1-(time.time()-t0)/SECS)+1e-12
    if random.random()<PSWAP:
        sec='A' if random.random()<0.9 else 'B'
        S=seq[sec];i=random.randrange(len(S)-1);a,b=S[i],S[i+1]
        shared=set(nodes[a]['regs'])&set(nodes[b]['regs'])
        if not shared: S[i],S[i+1]=b,a;continue
        if not commute(a,b): continue
        swap_links(a,b,shared);bo=None
        for ch0 in ({a:join(nodes[a]['F'],nodes[b]['F'])},{b:meet(nodes[a]['F'],nodes[b]['F'])}):
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
            for j,G2 in ch.items(): nodes[j]['F']=G2
            S[i],S[i+1]=b,a;curfee+=d;acc+=1;swaps+=1
            if curfee<best-1e-12: best=curfee;bestF=[z['F'] for z in nodes];bestseq=copy.deepcopy(seq)
        else: swap_links(b,a,shared)
        continue
    k=random.choice(mut);z=nodes[k];F=z['F']
    if random.random()<0.5:
        Gm=frozenset(range(v))
        for r in z['regs']: Gm=Gm&nodes[nxt[k,r]]['F']
        cand=list(Gm-F) if random.random()<0.8 else [x for x in range(v) if x not in F]
        if not cand: continue
        G=join(F,{random.choice(cand)})
    else:
        if not F: continue
        # lower: join of predecessors plus a random sub-collection of F's lines, closed
        J=frozenset()
        for r in z['regs']: J=J|nodes[prv[k,r]]['F']
        keep=[x for x in F if random.random()<0.5]
        G=close(J|frozenset(keep))
        if G==F or not G<=F: continue
    ch=closure({k:G})
    if ch is None: continue
    E=incident(set(ch));nf=efee(E,ch)
    if nf is None: continue
    d=nf-efee(E,{})
    if d<-1e-12 or (TEMP0>0 and random.random()<math.exp(-d/T)) or (d<=1e-12 and TEMP0==0):
        for j,G2 in ch.items(): nodes[j]['F']=G2
        curfee+=d;acc+=1
        if curfee<best-1e-12: best=curfee;bestF=[z['F'] for z in nodes];bestseq=copy.deepcopy(seq)
H=chain_H();print('final fee',fee(H),'best seen',best,'swaps',swaps)
newframes=set(z['F'] for z in nodes)-catset
print('iters',it,'acc',acc,'best',fee(H),'start',fee(H0),'chain',dict(sorted(H.items())),'local',dict(sorted((H+cent).items())),'new frames',len(newframes),Counter(dim(F) for F in newframes),flush=True)
json.dump(dict(best=fee(H),start=fee(H0),local=dict(sorted((H+cent).items())),start_local=dict(sorted((H0+cent).items())),new_frames=len(newframes)),open(OUT+'.json','w'))
# write word
out=copy.deepcopy(c);frames=[sorted(F) for F in cat];idx={F:i for i,F in enumerate(cat)}
# keep original lists for catalogue frames
frames=[list(fr) for fr in c['frames']]
def fid(F):
    if F not in idx: idx[F]=len(frames);frames.append(sorted(F))
    return idx[F]
for sec in ('A','B'):
    out[sec]=[[fid(nodes[k]['F']),nodes[k]['regs'][0],nodes[k]['regs'][1:]] for k in seq[sec]]
out['C']=[[c['C'][0][0],g[1],list(g[2])] for g in reversed(out['A'])]

out['frames']=frames
open(OUT+'.gz','wb').write(gzip.compress(json.dumps(out,separators=(',',':')).encode(),mtime=0))
