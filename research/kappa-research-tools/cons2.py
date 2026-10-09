exec(open('cons.py').read().split("st=Counter()")[0])
order=word.phase1+word.rest;pos={i:k for k,i in enumerate(order)}
print('ops',len(ops),'ordered',len(order))
dist=Counter();clean=Counter();fully=0;perroot=[]
wr_by=defaultdict(list)
for i,(a,b,n) in enumerate(ops):wr_by[a].append(pos[i])
for j in only:
  s=rr[j];W=sorted(writes[s],key=pos.get);good=True
  for u in uses[s]:
    pre=[w for w in W if pos[w]<pos[u]];dist[len(pre)]+=1
    ok=all(not any(pos[w]<p<pos[u] for p in wr_by[ops[w][1]]) for w in pre)
    clean[ok]+=1;good&=ok and len(pre)>=1
  perroot.append(good)
print('preceding writes per read',dist,'sources unchanged',clean,'roots all-clean',sum(perroot))
print('sample ops',ops[:5], 'n range',min(o[2] for o in ops),max(o[2] for o in ops))
