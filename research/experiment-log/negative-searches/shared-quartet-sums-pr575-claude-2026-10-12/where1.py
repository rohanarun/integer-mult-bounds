import json,gzip,sys
from collections import Counter
sys.path.insert(0,'/tmp/w531/research/direct-delivery504-global/vendor/gk')
import gk_common as common
w=json.load(gzip.open(sys.argv[1]));basis=common.basis
V=len(w['ports']);R=w['report']['R'];n=2*V+R
cur={}
for r in range(n):
    cur[r]=(w['ports'][r],) if r<V else ((basis(w['start_extra'][str(r)]) if str(r) in w.get('start_extra',{}) else ()) if r>=2*V else ())
lev={int(t):basis(E) for t,E in w.get('target_levels',{}).items()}
kind=lambda r:'src' if r<V else 'tgt' if r<2*V else 'hlp'
C=Counter()
def climb(r,F,where):
    F=basis(F);d=len(F)-len(cur[r])
    if d>0: C[(where,kind(r),d)]+=1
    cur[r]=F
for part in ('A','B'):
    if part=='B':
        for r,f in zip(w['centers'],w['center_frames']): cur[r]=basis(f)
        for t in range(V): cur[V+t]=lev.get(t,())
    for i,e in enumerate(w[part]):
        regs=[e[1]]+([e[2]] if e[0]=='add' else [])
        for r in regs: climb(r,e[-1],part)
FULL=basis([1<<i for i in range(9)])
for r in range(n): climb(r,FULL if (r<V or r>=2*V) else basis([x for x in range(1,512) if not (x&w['ports'][r-V]).bit_count()%2]),'final')
tot=Counter()
for (wh,k,d),c in C.items(): tot[d]+=c
print('profile',dict(sorted(tot.items())))
print('rank-1 climbs by section/register:',{f'{wh}:{k}':c for (wh,k,d),c in sorted(C.items()) if d==1})
print('rank-2:',{f'{wh}:{k}':c for (wh,k,d),c in sorted(C.items()) if d==2})
# per-register step sequences (helpers and targets)
seqs={'hlp':Counter(),'tgt':Counter(),'src':Counter()}
cur2={}
for r in range(n):
    cur2[r]=[len(cur[r])]
