"""Random-perturbation sweep of the PR522 complex factory (pair matchings per block x packet-orientation seed).
Each candidate: rebuild factory -> transfer PR514/522 retimed frames -> keep or rescan gauge/kernel -> local profile + widths
-> proxy price b (nine-stage one-owner hosting IP, banks allowed; same proxy for the baseline).  usage: sweep.py SEED N OUTDIR"""
import sys,os,json,gzip,copy,difflib,subprocess,random,time,math,shutil,importlib.util
from collections import Counter,defaultdict
from fractions import Fraction as Q
from pathlib import Path
H=Path(__file__).resolve().parent; sys.path.insert(0,str(H/'gk')); sys.path.insert(0,str(H))
import gk_word as g
import hosting_core as HC
s=importlib.util.spec_from_file_location('mom',str(H/'moment.py'));MM=importlib.util.module_from_spec(s);s.loader.exec_module(MM)
read=lambda f:json.loads(gzip.decompress(Path(f).read_bytes()) if str(f).endswith('.gz') else Path(f).read_bytes())
REF=read(H/'ref_factory.json.gz'); RET=read(H/'ref_retimed.json.gz'); SEL0=read(H/'PAIR-SELECTION.json'); SPEC0=read(H/'PAIR-SPEC.json')
GR=json.load(open(H/'cgrad.json'))
def hamming_dir(seed,work):
    if seed is None: return H/'hamming'
    d=work/('ham%d'%seed)
    if (d/'work/complex-network/hamming/PACKET-PROGRAMS.json.gz').exists(): return d/'work/complex-network/hamming'
    (d/'work/pr370-source/research/e8-bit/data/bit').mkdir(parents=True,exist_ok=True)
    shutil.copy(H/'e8/e8-r865.json.gz',d/'work/pr370-source/research/e8-bit/data/bit/bitE8-r865.json.gz')
    src=(H/'hamming_packets.py').read_text().replace('rng=random.Random(38639)','rng=random.Random(%d)'%seed)
    (d/'hp.py').write_text(src)
    subprocess.run([sys.executable,'-B','hp.py'],cwd=d,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return d/'work/complex-network/hamming'
def factory(spec,seed,work,tag):
    out=work/('f_'+tag); sp=work/('spec_'+tag+'.json'); sp.write_text(json.dumps(spec))
    hd=hamming_dir(seed,work)
    r=subprocess.run([sys.executable,'-B',str(H/'run_portable.py'),str(H/'construct_ranksector.py'),str(hd),str(out),str(sp)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    if r.returncode: return None,'factory:'+r.stderr[-200:]
    b=read(out/'FULL-WORD.json.gz'); shutil.rmtree(out,ignore_errors=True); return b,None
def transfer(b):
    for part in ['A','B']:
        aa=[json.dumps(e[:-1]) for e in REF[part]];bb=[json.dumps(e[:-1]) for e in b[part]]
        for ia,ib,n in difflib.SequenceMatcher(a=aa,b=bb,autojunk=False).get_matching_blocks():
            for d in range(n):
                if REF[part][ia+d][-1]!=RET[part][ia+d][-1]: b[part][ib+d][-1]=copy.deepcopy(RET[part][ia+d][-1])
    b['cleanup']=[g.inverse(e,g.FULL) for e in reversed(b['A']+b['B']) if not 120<=e[1]<240]
    return b
def rank_indep(col,ds):
    piv={}
    out=[]
    for d in ds:
        row=dict(col[d])
        while row:
            k=min(row)
            if k in piv:
                pr=piv[k];q=row[k]/pr[k]
                for j,x in pr.items():
                    z=row.get(j,Q(0))-q*x
                    if z:row[j]=z
                    else:row.pop(j,None)
            else: piv[k]=row; out.append(d); break
    return out
def rescan(b,rng):
    col=g.responses(b); first=g.first_frames(b)
    gauge={h:E for h,E in SEL0['gauge'].items() if g.span(g.basis(E))<=g.span(first[int(h)])}
    used=set(int(h) for h in gauge); classes=[]
    for cl in SEL0['kernel']:
        E=g.basis(cl['E'])
        cand=[x for x in range(560) if x not in used and col[x] and g.span(E)<=g.span(first[x])]
        pref=rank_indep(col,[x for x in cl['donors'] if x in cand]); rest=[x for x in cand if x not in pref]; rng.shuffle(rest)
        donors=list(pref)
        piv=[x for x in cand if x not in donors and g.solve_relation(col,donors,x) is not None]
        # greedy extension: add one extra donor only if it brings >= 2 new pivots
        for d in rest:
            if d in piv or d in donors: continue
            if len(rank_indep(col,donors+[d]))<=len(donors): continue
            nd=donors+[d]; npv=[x for x in cand if x not in nd and g.solve_relation(col,nd,x) is not None]
            if len(npv)>=len(piv)+2: donors,piv=nd,npv
        if piv:
            classes.append(dict(E=cl['E'],donors=donors,pivots=piv)); used|=set(donors)|set(piv)
    return dict(kernel=classes,gauge=gauge)
# ---------------- proxy price: nine-stage one-owner hosting with banks
SCH=json.load(open(H/'sched9.json'))
def windows():
    rank={}
    for it in SCH['idle_children']: rank.setdefault(it['child'],it['rank'])
    pos={e['stage']:e['pair'] for e in SCH['recipe'] if e['kind']=='local'}
    sched=[]
    for e in SCH['execution_schedule']:
        if e['kind']=='local_cover_sweep': sched.append(dict(kind='local',stage=e['stage'],pair=pos[e['stage']]))
        elif e['kind']=='bridge': sched.append(dict(kind='bridge',dst=e['dst'],src=e['src']))
        elif e['kind']=='idle_cover_sweep':
            for sd,ch in enumerate(e['child_indices']):
                if ch in rank: sched.append(dict(kind='idle',pair=e['pair'],rank=rank[ch],idx=ch))
    return {k:x for k,x in HC.windows(sched).items() if x[2]},rank
WIN,RANK=windows()
def price(local,widths):
    import numpy as np
    from scipy.optimize import milp,LinearConstraint,Bounds
    from scipy.sparse import lil_matrix
    V,T,L,M=120,8,9,73; W=2*4*V*T
    wd=Counter(widths); ws=sorted(wd)
    cost=lambda r: -GR[str(r)]/1e-9 if 0<r<89 else 0.0
    def pats(r,st):
        out=[]
        def rec(i,cur,tot,spec):
            if i==len(ws): out.append(tuple(cur)); return
            w=ws[i];k=0
            while tot+k*w<=r and 9*(len(cur)+k)<=M and spec+k*(9-w)<=M-r and len(cur)+k<=len(st):
                rec(i+1,cur+[w]*k,tot+k*w,spec+k*(9-w));k+=1
        rec(0,[],0,0); return out
    idx={}
    for i,(p,r,st) in WIN.items():
        for pat in pats(r,st):
            idx[('y',i,pat)]=len(idx)
            for s_ in st:
                for w in set(pat): idx[('a',i,pat,s_,w)]=len(idx)
    for s_ in range(L):
        for w in ws: idx[('u',s_,w)]=len(idx)
    n=len(idx);c=np.zeros(n)
    for k,j in idx.items():
        if k[0]=='y': r=WIN[k[1]][1]; c[j]=cost(r-sum(k[2]))-cost(r)
        if k[0]=='u': c[j]=1e5
    rows=[];lo=[];hi=[]
    for i in WIN: rows.append({j:1 for k,j in idx.items() if k[0]=='y' and k[1]==i});lo.append(V);hi.append(V)
    for k in [k for k in idx if k[0]=='y']:
        _,i,pat=k; st=WIN[i][2]
        for w in set(pat):
            e={idx['a',i,pat,s_,w]:1 for s_ in st}; e[idx[k]]=-pat.count(w); rows.append(e);lo.append(0);hi.append(0)
        for s_ in st:
            e={idx['a',i,pat,s_,w]:1 for w in set(pat)}; e[idx[k]]=-1; rows.append(e);lo.append(-np.inf);hi.append(0)
    for s_ in range(L):
        for w in ws:
            e={j:1 for k,j in idx.items() if k[0]=='a' and k[3]==s_ and k[4]==w}; e[idx['u',s_,w]]=1; rows.append(e);lo.append(wd[w]);hi.append(wd[w])
    A=lil_matrix((len(rows),n))
    for ri,e in enumerate(rows):
        for j,x in e.items(): A[ri,j]=x
    res=milp(c,constraints=LinearConstraint(A.tocsr(),lo,hi),integrality=np.ones(n),bounds=Bounds(0,np.inf),options=dict(time_limit=300))
    x=[int(round(q)) for q in res.x]
    paid=Counter()
    for r,k in local.items(): paid[int(r)]+=k*L*T
    for ch,rk in RANK.items():
        if ch not in WIN: paid[rk]+=V*T
    for k,j in idx.items():
        if k[0]=='y' and x[j]:
            rr=WIN[k[1]][1]-sum(k[2])
            if rr: paid[rr]+=x[j]*T
    banks=0
    for k,j in idx.items():
        if k[0]=='u' and x[j]: banks+=x[j]; paid[M-8*k[2]]+=x[j]
    W+=banks
    assert M*W-sum(r*v for r,v in paid.items())==2496
    return float(Q(MM.certify(dict(paid),M,W,True)['lower'])),banks
def evaluate(spec,seed,work,tag,rng):
    t0=time.time()
    b,err=factory(spec,seed,work,tag)
    if b is None: return dict(tag=tag,status='factory_fail',err=err)
    raw=copy.deepcopy(b); raw['cleanup']=[g.inverse(e,g.FULL) for e in reversed(raw['A']+raw['B']) if not 120<=e[1]<240]
    best=None; errs=[]
    for label,base in (('retimed',transfer(b)),('raw',raw)):
        for mode in ('frozen','rescan'):
            try:
                sel=SEL0 if mode=='frozen' else rescan(base,rng)
                w=g.build(base,sel); prof=g.profile(w)
                best=(label+'/'+mode,w,prof); break
            except AssertionError as e: errs.append(label+'/'+mode+':'+str(e)[:80])
        if best: break
    if not best: return dict(tag=tag,status='kernel_fail',err=' | '.join(errs)[:300])
    mode,w,prof=best
    widths=g.widths_of(w)
    try: b_,banks=price(prof,widths)
    except Exception as e: return dict(tag=tag,status='price_fail',err=repr(e)[:200])
    return dict(tag=tag,status='ok',mode=mode,b_proxy=b_,banks=banks,profile={str(k):v for k,v in sorted(prof.items())},widths=dict(Counter(widths)),entering=sum(1 for x in widths if x<9),seconds=round(time.time()-t0,1),spec=spec,seed=seed)
if __name__=='__main__':
    seed,N,outdir=int(sys.argv[1]),int(sys.argv[2]),Path(sys.argv[3]); outdir.mkdir(parents=True,exist_ok=True)
    rng=random.Random(seed); work=outdir/'work'; work.mkdir(exist_ok=True)
    res=[]
    if seed==0: res.append(evaluate(SPEC0,None,work,'baseline',rng)); print(json.dumps(res[-1]),flush=True)
    keys=sorted(SPEC0)
    for i in range(N):
        spec={k:list(v) for k,v in SPEC0.items()}
        nflip=rng.choice([1,1,2,3,4])
        for _ in range(nflip):
            k=rng.choice(keys); p=rng.randrange(2); spec[k][p]=rng.randrange(3)
        pseed=None if rng.random()<0.6 else rng.randrange(1,10**6)
        res.append(evaluate(spec,pseed,work,'s%d_%d'%(seed,i),rng)); print(json.dumps(res[-1]),flush=True)
        json.dump(res,open(outdir/'results.json','w'))
    json.dump(res,open(outdir/'results.json','w'))
