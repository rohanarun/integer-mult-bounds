import json,gzip,sys,copy,subprocess
from fractions import Fraction as F
from collections import Counter
W=sys.argv[1]
w0=json.load(gzip.open(W))
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
def contained(a,b): return basis(list(a)+list(b))==basis(b)
regs=lambda e:[e[1]]+([e[2]] if e[0]=='add' else [])
def apply(e,rows,inv=False):
    if e[0]=='scale':
        q=F(e[2],e[3]); q=1/q if inv else q
        rows[e[1]]={k:q*x for k,x in rows[e[1]].items()}
    else:
        q=F(e[3],e[4]); q=-q if inv else q
        for k,x in list(rows[e[2]].items()):
            z=rows[e[1]].get(k,F(0))+q*x
            if z: rows[e[1]][k]=z
            else: rows[e[1]].pop(k,None)
V=len(w0['ports']);R=w0['report']['R'];n=2*V+R;h=9
FULL=basis([1<<i for i in range(h)])
prefix=w0['precondition']+w0['A']+w0['cut']+w0['B']
p=[{k:F(1)} for k in range(n)]
for e in prefix: apply(e,p)
pinv=[{k:F(1)} for k in range(n)]
for e in reversed(prefix): apply(e,pinv,inv=True)
col={}
for k in range(n):
    for j in p[k]: col.setdefault(j,set()).add(k)
def simulate(w):
    """returns paid profile, endB, end frames, width inventory, or raises"""
    start=[(pp,) for pp in w['ports']]+[()]*(V+R)
    for q,U in w.get('start_extra',{}).items(): start[int(q)]=basis(U)
    end=[FULL]*V+[basis([x for x in range(1,1<<h) if (x&pp).bit_count()%2==0]) for pp in w['ports']]+[FULL]*R
    for q,U in w.get('helper_final',{}).items(): end[int(q)]=basis(U)
    cur=list(start);paid=Counter()
    def climb(q,U):
        U=basis(U);assert contained(cur[q],U),('nonmono',q)
        d=len(U)-len(cur[q])
        if d: paid[d]+=1
        cur[q]=U
    for sec in ('A','B'):
        if sec=='B':
            for q,U in zip(w['centers'],w['center_frames']):
                U=basis(U);served={()}
                for T in sorted(served,key=lambda x:-len(x)):
                    if T!=U: paid[len(U)-len(T)]+=1
                    U=T
        for e in w[sec]:
            for q in regs(e): climb(q,e[-1])
    endB=list(cur)
    tail=[w['cleanup'][i][:-1]+[U] for i,U in w['early_cleanup']]
    for e in tail:
        for q in regs(e): climb(q,e[-1])
    for q,U in enumerate(end): climb(q,U)
    inv=Counter(len(end[q])-len(start[q]) for q in range(2*V,n))
    return paid,endB,end,inv,cur
paid0,endB,end0,inv0,_=simulate(w0)
assert dict(paid0)=={int(k):v for k,v in w0['report']['local_profile'].items()},(paid0,w0['report']['local_profile'])
early={i for i,U in w0['early_cleanup']}
low=set(map(int,w0.get('helper_final',{})))
results=[]
for q in range(2*V,n):
    if q in low: continue
    G=[i for i,e in enumerate(w0['cleanup']) if i not in early and q in regs(e)]
    w=copy.deepcopy(w0)
    # tail frames sequentially from endB plus existing tail
    paid,eB,end,inv,cur=simulate(w0)
    newtail=[]
    for i in G:
        e=w0['cleanup'][i];U=basis([x for r in regs(e) for x in cur[r]])
        for r in regs(e): cur[r]=U
        newtail.append([i,list(U)])
    ks=(col.get(q,set())|set(pinv[q]))-{q}
    Uq=basis([x for k in ks for x in endB[k]]+list(cur[q]))
    results.append(("dim",q,len(Uq),len(G)))
    if len(Uq)>=9: continue
    w['early_cleanup']=w0['early_cleanup']+newtail
    w['helper_final'][str(q)]=list(Uq)
    try: paid,eB,end,inv,_=simulate(w)
    except AssertionError as ex: results.append((q,'sim-fail',str(ex)[:60]));continue
    w['report']['local_profile']={str(k):v for k,v in sorted(paid.items())}
    w['report']['width_inventory']={str(k):v for k,v in sorted(inv.items())}
    out='/tmp/sa3/le_%d.json.gz'%q
    open(out,'wb').write(gzip.compress(json.dumps(w,sort_keys=True,separators=(',',':')).encode(),mtime=0))
    r=subprocess.run([sys.executable,'-B','research/gauge44-frames-x/independent/audit_local.py','--word',out,'--output','/tmp/sa3/le_%d.audit.json'%q],cwd='/tmp/wmain',capture_output=True,text=True)
    ok='PASS_INDEPENDENT' in r.stdout
    d={k:paid.get(k,0)-paid0.get(k,0) for k in set(paid)|set(paid0) if paid.get(k,0)!=paid0.get(k,0)}
    di={k:inv.get(k,0)-inv0.get(k,0) for k in set(inv)|set(inv0) if inv.get(k,0)!=inv0.get(k,0)}
    results.append((q,len(G),len(Uq),ok,d,di,(r.stdout+r.stderr).strip().splitlines()[-1][:100] if not ok else ''))
for x in results: print(x)
