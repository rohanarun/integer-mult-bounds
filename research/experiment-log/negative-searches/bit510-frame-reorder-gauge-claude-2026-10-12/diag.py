exec(open('bsa.py').read().split("mut=[k for k")[0].replace("WORD,SEED,SECS,OUT=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]),sys.argv[4]","WORD='/tmp/w510/research/e8-r480-dead-totals/data/bitE8mut-r480.json.gz';SEED=0;SECS=0;OUT='x'"))
seqs=Counter()
for r in range(n):
    k=head[r];s=[dim(nodes[k]['F'])]
    while (k,r) in nxt:
        k=nxt[k,r];d=dim(nodes[k]['F'])
        if d!=s[-1]: s.append(d)
    kind='x' if r<v else 'y' if r<2*v else 'h'
    seqs[(kind,tuple(s))]+=1
for k,vv in sorted(seqs.items()): print(k,vv)
