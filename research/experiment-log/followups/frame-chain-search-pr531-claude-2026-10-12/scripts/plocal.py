import json,sys
from price import price
CUR={int(k):v for k,v in json.load(open('/tmp/v531/hosted/HOSTED.json'))['global_profile'].items()}
LOC={1:2028,2:752,3:156,4:392,5:56,6:56,7:8}
def price_local(newloc):
    P=dict(CUR)
    for k,v in LOC.items(): P[k]-=72*v
    for k,v in newloc.items(): P[k]=P.get(k,0)+72*v
    return price({k:v for k,v in P.items() if v})
def from_sa(path):
    d=json.load(open(path));H={int(k):v for k,v in d['chain_profile'].items()};H0={int(k):v for k,v in d['start_chain_profile'].items()}
    new={k:LOC.get(k,0)-H0.get(k,0)+H.get(k,0) for k in set(LOC)|set(H)}
    return new
if __name__=='__main__':
    b0=price(CUR)
    for p in sys.argv[1:]:
        nl=from_sa(p);b=price_local(nl);print(p,nl,b,'%+.4f%%'%((b-b0)/b0*100))
