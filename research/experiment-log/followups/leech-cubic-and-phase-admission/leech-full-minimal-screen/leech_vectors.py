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
wts=collections.Counter(sum(c) for c in code); 
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
