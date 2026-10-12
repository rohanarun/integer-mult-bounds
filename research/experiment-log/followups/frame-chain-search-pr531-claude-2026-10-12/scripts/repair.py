import sys
sys.path.insert(0,'/tmp/k531')
from evalsel import *
def repair(w):
    """lift every op frame to the join with its registers' current frames (monotone lifts); None if barriers/finals break"""
    basis=g.basis;span=g.span
    P=w['ports'];n=2*V+R
    cur={}
    for r in range(n):
        cur[r]=(P[r],) if r<V else ((basis(w['start_extra'][str(r)]) if str(r) in w.get('start_extra',{}) else ()) if r>=2*V else ())
    lev={int(t):basis(E) for t,E in w.get('target_levels',{}).items()}
    lifted=0
    for part in ('A','B'):
        if part=='B':
            for r,f in zip(w['centers'],w['center_frames']):
                if cur[r]!=basis(f): return None,('centre',r)
            for t in range(V):
                if cur[V+t]!=lev.get(t,()): return None,('target barrier',t,cur[V+t],lev.get(t,()))
        for e in w[part]:
            regs=[e[1]]+([e[2]] if e[0]=='add' else [])
            F=basis(list(e[-1])+[x for r in regs for x in cur[r]])
            if F!=basis(e[-1]): lifted+=1;e[-1]=list(F)
            for r in regs: cur[r]=F
    FULL=g.FULL
    for r in range(n):
        fin=FULL if (r<V or r>=2*V) else g.perp(P[r-V])
        if not span(cur[r])<=span(fin): return None,('final',r)
    return lifted,None
def evaluate2(sel):
    try: w=g.build(word,sel,check=False)
    except AssertionError as e: return None,str(e)[:80]
    lifted,err=repair(w)
    if lifted is None: return None,err
    try: prof=g.profile(w)
    except AssertionError as e: return None,str(e)[:80]
    wc=Counter(widths_of(w))
    if set(wc)-{7,8,9}: return None,'width'
    Pp=hostlp.full(dict(prof),wc[8],wc[9],wc[7])
    if Pp is None: return None,'host'
    return price(Pp),(dict(prof),lifted,w)
