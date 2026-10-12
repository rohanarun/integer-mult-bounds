exec(open('ip9.py').read().split("idx={}")[0])
idx={}
for i,(p,r,st) in win.items():
    for pat in patterns(r):
        if len(pat)<=len(st):
            idx[('y',i,pat)]=len(idx)
            for s_ in st:
                for w in set(pat): idx[('a',i,pat,s_,w)]=len(idx)
n=len(idx);c=np.zeros(n)
for k,j in idx.items():
    if k[0]=='y': r=win[k[1]][1]; c[j]=cost(r-sum(k[2]))-cost(r)
rows=[];lo=[];hi=[]
for i,(p,r,st) in win.items():
    rows.append({j:1 for k,j in idx.items() if k[0]=='y' and k[1]==i});lo.append(V*T);hi.append(V*T)
ys=[k for k in idx if k[0]=='y']
for k in ys:
    _,i,pat=k; st=win[i][2]
    for w in set(pat):
        e={idx['a',i,pat,s_,w]:1 for s_ in st}; e[idx[k]]=-pat.count(w); rows.append(e);lo.append(0);hi.append(0)
    for s_ in st:
        e={idx['a',i,pat,s_,w]:1 for w in set(pat)}; e[idx[k]]=-1; rows.append(e);lo.append(-np.inf);hi.append(0)
PEN=float(sys.argv[2]) if len(sys.argv)>2 else 1e5
for s_ in range(L):
    for w in widths:
        idx[('u',s_,w)]=len(idx)
c=np.concatenate([c,np.zeros(len(idx)-len(c))])
for k,j in idx.items():
    if k[0]=='u': c[j]=PEN
n=len(idx)
for s_ in range(L):
    for w in widths:
        e={j:1 for k,j in idx.items() if k[0]=='a' and k[3]==s_ and k[4]==w}; e[idx['u',s_,w]]=8
        rows.append(e);lo.append(supply[w]);hi.append(supply[w])
A=lil_matrix((len(rows),n))
for ri,e in enumerate(rows):
    for j,x in e.items(): A[ri,j]=x
res=milp(c,constraints=LinearConstraint(A.tocsr(),lo,hi),integrality=np.ones(n),bounds=Bounds(0,np.inf),options=dict(time_limit=1200))
print(res.status,res.message)
x=[int(round(q)) for q in res.x]
paid=Counter()
for r,k in loc.items(): paid[r]+=k*L*T
for ch,rk in allch.items():
    if ch not in win: paid[rk]+=V*T
for k,j in idx.items():
    if k[0]=='y' and x[j]:
        rr=win[k[1]][1]-sum(k[2])
        if rr: paid[rr]+=x[j]
banks=sum(x[j] for k,j in idx.items() if k[0]=='u')
W=W+banks
for k,j in idx.items():
    if k[0]=='u' and x[j]: paid[M-8*k[2]]+=x[j]
print('banks',banks,{k:x[j] for k,j in idx.items() if k[0]=='u' and x[j]})
print('profile',dict(sorted(paid.items())),'deficit',M*W-sum(r*v for r,v in paid.items()))
json.dump(dict(y=[[k[1],list(k[2]),x[j]] for k,j in idx.items() if k[0]=='y' and x[j]],a=[[k[1],list(k[2]),k[3],k[4],x[j]] for k,j in idx.items() if k[0]=='a' and x[j]]),open('sel9c.json','w'))
print('b',float(Q(MM.certify(dict(paid),M,W,True)['lower'])))
