import itertools, json, math
from collections import Counter
# E8 roots (coords x2 to stay integral): D8 roots + half-integer even-sign vectors
R=[]
for i,j in itertools.combinations(range(8),2):
    for s,t in itertools.product((2,-2),repeat=2):
        v=[0]*8; v[i]=s; v[j]=t; R.append(tuple(v))
for sg in itertools.product((1,-1),repeat=8):
    if sg.count(-1)%2==0: R.append(sg)
assert len(R)==240
lines=[v for v in R if v>tuple(-x for x in v)]
ip=lambda a,b:sum(x*y for x,y in zip(a,b))
c=Counter(ip(lines[0],w)//4 for w in R)
st=json.load(open('/tmp/leech/LEECH-STATS.json'))
def welch(N,d): return math.sqrt((N-d)/(d*(N-1)))
L=st['ip_classes']; nzL=sum(v for k,v in L.items() if k in('1','2'))  # per line: count lines (ip>0 reps)
out={
 "E8":{"dim":8,"lines":120,"ip_classes_vs_roots":dict(c),"nonzero_neighbour_lines":56,"zero_lines":63,
       "coherence":0.5,"welch_bound":welch(120,8),"lines_per_dim":15,"quotient_2":"E8/2E8: 1+120+135=256"},
 "Leech":{"dim":24,"lines":98280,"nonzero_neighbour_lines":23552+2300+0,  # per line, lines (not vectors)
          "zero_lines":46575-0,"coherence":0.5,"welch_bound":welch(98280,24),"lines_per_dim":98280/24,
          "quotient_2":"Lambda/2Lambda: 1+98280+8386560+8292375=2^24; distinct minimal lines never congruent mod 2Lambda since |v-w|^2=64-2ip<128"},
}
out["Leech"]["nonzero_neighbour_lines"]=23552+2300+23552+2300 >>1 <<0
# vectors with ip!=0 to fixed line rep: 51704 vectors = 25852 lines... but sign pairs: +k and -k both counted
out["Leech"]["nonzero_neighbour_lines"]=(23552+2300)  # each line contributes one of ±
out["Leech"]["zero_lines"]=46575//1
out["Leech"]["nonzero_fraction"]=(98279-46575+0)/98279
out["E8"]["nonzero_fraction"]=56/119
print(json.dumps(out,indent=1))
