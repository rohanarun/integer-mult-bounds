import itertools,json
from collections import Counter
# Reed-Muller RM(1,4): affine functions on F2^4, length 16
pts=list(itertools.product((0,1),repeat=4))
def aff(a,c): return tuple((sum(x*y for x,y in zip(a,p))+c)%2 for p in pts)
RM1=set(aff(a,c) for a in itertools.product((0,1),repeat=4) for c in (0,1))
w8=[w for w in RM1 if sum(w)==8]
mins=[]
for w in w8:
    S=[i for i in range(16) if w[i]]
    for sg in itertools.product((1,-1),repeat=8):
        if sg.count(-1)%2==0:
            v=[0]*16
            for i,s in zip(S,sg): v[i]=s
            mins.append(tuple(v))
for i,j in itertools.combinations(range(16),2):
    for s,t in itertools.product((2,-2),repeat=2):
        v=[0]*16;v[i]=s;v[j]=t;mins.append(tuple(v))
print('BW16 minimal vectors',len(mins),'norms',Counter(sum(x*x for x in v) for v in mins))
ip=lambda a,b:sum(x*y for x,y in zip(a,b))
lines=[v for v in mins if v>tuple(-x for x in v)]
c=Counter(ip(lines[0],w) for w in lines[1:]);print('lines',len(lines),'ip classes vs one line',dict(c))
nz=sum(v for k,v in c.items() if k!=0)
# second representative of the other orbit type
l2=next(v for v in lines if 2 in v or -2 in v);c2=Counter(ip(l2,w) for w in lines if w!=l2)
print('ip classes vs a (2,2) line',dict(c2))
coh=max(abs(k) for k in c)/8
import math
N,d=len(lines),16
res=dict(BW16=dict(dim=16,min_vectors=len(mins),lines=N,lines_per_dim=N/d,coherence=coh,welch=math.sqrt((N-d)/(d*(N-1))),
  nonzero_neighbour_fraction=nz/(N-1),nonzero_fraction_type2=sum(v for k,v in c2.items() if k)/(N-1)),
  E8=dict(dim=8,min_vectors=240,lines=120,lines_per_dim=15,coherence=0.5,welch=0.343,nonzero_neighbour_fraction=56/119))
# nested flat chain in AG(4,2): sizes of RM-supported blocks
flats={k:0 for k in (1,2,4,8,16)}
import itertools as it
def is_flat(S):
    S=list(S)
    if len(S)&(len(S)-1): return False
    o=pts[S[0]];D={tuple((a+b)%2 for a,b in zip(pts[s],o)) for s in S}
    return all(tuple((a+b)%2 for a,b in zip(x,y)) in D for x in D for y in D)
for k in (2,4,8):
    flats[k]=sum(1 for S in it.combinations(range(16),k) if is_flat(S)) if k<8 else len(w8)
res['AG42_flats_by_size']={'1':16,'2':120,'4':flats[4],'8':flats[8],'16':1}
res['AG32_flats_by_size(E8/[8,4,4])']={'1':8,'2':28,'4':14,'8':1}
print(json.dumps(res,indent=1));json.dump(res,open('/tmp/geo/BW16-STATS.json','w'),indent=1)
