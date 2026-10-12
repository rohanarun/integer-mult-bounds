import sys,json,gzip,copy,subprocess,os
sys.path.insert(0,'/tmp/geo')
from share import *
W0=sys.argv[1];OUTD=sys.argv[2];os.makedirs(OUTD,exist_ok=True)
w=load(W0);V=len(w['ports']);R=w['report']['R']
seq,hist,cands=candidates(w)
print('candidate shared sums',len(cands))
# For each candidate: provider A = first register to hold S; consumer B = later register that BUILDS S itself.
# Build segment of B: the ops on t=B since B last had empty data part, ending at position posB. Requires those ops to read only sources (<V).
plans=[]
for k,regs in cands:
    posA,A,dA=regs[0]
    for posB,B,dB in regs[1:]:
        if B<2*V: continue          # only rebuild helpers
        # walk back B's ops
        ops=[];ok=True
        for pos in range(posB,-1,-1):
            sec,i,t,d=hist[pos]
            if t!=B: continue
            e=seq[pos][2]
            if not d and pos!=posB: break
            if e[0]!='add' or e[2]>=V: ok=False;break
            ops.append(pos)
            if len(d)==0: break
        if not ok or len(ops)<2: continue
        # B's data before the first op must be empty
        firstpos=min(ops)
        prevd=None
        for pos in range(firstpos-1,-1,-1):
            if hist[pos][2]==B: prevd=hist[pos][3];break
        if prevd: continue
        # A must hold S (same data) at posB: last write to A before posB
        holdA=None
        for pos in range(posB-1,-1,-1):
            if hist[pos][2]==A: holdA=hist[pos][3];break
        if holdA is None or key(holdA)!=k: continue
        # coefficient c with dB = c*holdA
        j=min(dB);c=dB[j]/holdA[j]
        if c.denominator&(c.denominator-1): continue
        plans.append(dict(sum=len(k),A=A,B=B,ops=sorted(ops),pos=posB,c=(c.numerator,c.denominator),saved=len(ops)-1))
print('rewrite plans',len(plans),Counter(p['sum'] for p in plans))
json.dump(plans,open(OUTD+'/plans.json','w'))
