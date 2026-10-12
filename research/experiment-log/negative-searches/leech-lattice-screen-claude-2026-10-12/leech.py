"""Leech lattice minimal vectors (scaled by sqrt8: norm 32 -> use integer coords, norm 32), structure stats relevant to the
E8 port construction: lines, inner-product classes, frame tightness, binary realisation in Lambda/2Lambda."""
import itertools, json, collections
import numpy as np
# extended binary Golay code from generator (MOG-free: standard [I|A] form)
A=[[0,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,0,1,1,1,0,0,0,1,0],[1,1,0,1,1,1,0,0,0,1,0,1],[1,0,1,1,1,0,0,0,1,0,1,1],
   [1,1,1,1,0,0,0,1,0,1,1,0],[1,1,1,0,0,0,1,0,1,1,0,1],[1,1,0,0,0,1,0,1,1,0,1,1],[1,0,0,0,1,0,1,1,0,1,1,1],
   [1,0,0,1,0,1,1,0,1,1,1,0],[1,0,1,0,1,1,0,1,1,1,0,0],[1,1,0,1,1,0,1,1,1,0,0,0],[1,0,1,1,0,1,1,1,0,0,0,1]]
G=[[int(i==j) for j in range(12)]+A[i] for i in range(12)]
code=set()
for m in range(1<<12):
    w=[0]*24
    for i in range(12):
        if m>>i&1: w=[a^b for a,b in zip(w,G[i])]
    code.add(tuple(w))
wts=collections.Counter(sum(c) for c in code); print('golay weights',dict(sorted(wts.items())))
assert wts=={0:1,8:759,12:2576,16:759,24:1}
octads=[c for c in code if sum(c)==8]
V=set()
# shape (+-2^8,0^16) on octads with even number of minus signs
for o in octads:
    idx=[i for i in range(24) if o[i]]
    for signs in itertools.product([1,-1],repeat=8):
        if signs.count(-1)%2==0:
            v=[0]*24
            for i,s in zip(idx,signs): v[i]=2*s
            V.add(tuple(v))
# shape (-+3, +-1^23): x = (-3,1^23) + 2*codeword-sign pattern: v_i = 1-2c_i ... standard: (∓3,±1^23) with signs from codeword
for c in code:
    base=[(-1 if c[i] else 1) for i in range(24)]
    for j in range(24):
        v=list(base); v[j]=-3*base[j]
        V.add(tuple(v))
# shape (+-4,+-4,0^22)
for i,j in itertools.combinations(range(24),2):
    for s,t in itertools.product([4,-4],repeat=2):
        v=[0]*24; v[i]=s; v[j]=t; V.add(tuple(v))
V=np.array(sorted(V),dtype=np.int64)
print('minimal vectors',len(V),'norms',set((V*V).sum(1).tolist()))
assert len(V)==196560
lines=V[[i for i,v in enumerate(V.tolist()) if next(x for x in v if x)>0]]
print('lines',len(lines))
r=lines[0]; ip=(lines@r)
print('inner products with one line (scaled /8):',dict(sorted(collections.Counter((ip//8).tolist()).items())))
S=lines.T@lines; print('frame tight? diag',set(np.diag(S).tolist()),'offdiag max',np.abs(S-np.diag(np.diag(S))).max())
# Lambda/2Lambda classes: vectors/  (scaled coords are sqrt8*true); class of v mod 2Lambda: use v mod (2*scaled lattice)?
# simpler: minimal vectors are pairwise distinct mod 2Lambda except +-: check v-w in 2Lambda <=> (v-w)/2 in Lambda <=> norm/structure; test via inner products: for v!=±w, v-w in 2Lambda requires |v-w|^2>=4*32 -> only possible if ip<=-... compute max ip
print('max |ip|/8 for distinct lines',int(np.abs(lines[1:]@r).max()//8))
json.dump(dict(min_vectors=196560,lines=int(len(lines)),ip_classes={str(k):int(v) for k,v in collections.Counter((ip//8).tolist()).items()}),open('LEECH-STATS.json','w'),indent=1)
