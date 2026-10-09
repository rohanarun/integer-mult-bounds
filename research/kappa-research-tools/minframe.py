exec(open('maxframe.py').read().split("nxt={}")[0])
jc={}
def join(f,g):
  if f is None:return g
  if g is None or f==g or C.sub(g,f):return f
  if C.sub(f,g):return g
  k=(f,g) if f<g else (g,f)
  if k not in jc:jc[k]=word.register(list(C.B[f])+list(C.B[g]))
  return jc[k]
vc={}
def span(n):
  if n not in vc:
    bits=C.sup[n];rows=[]
    while bits:
      low=bits&-bits;s=low.bit_length()-1;bits-=low;rows.append(C.chi[s])
    vc[n]=word.register(rows)
  return vc[n]
start={b:word.w['source_frame'][x] for x,b in word.source.items()};start.update({b:z['frame'] for b,z in word.gauge.items()})
prv=dict(start);L=[None]*len(ops)
for i in order:
  a,b,n=ops[i]
  L[i]=join(join(prv.get(a),prv.get(b)),span(n));prv[a]=prv[b]=L[i]
bad=sum(not C.sub(L[i],word.opframe[i]) for i in range(len(ops)))
nd=sum(not C.nondeg(L[i]) for i in range(len(ops)))
print('L violations',bad,'degenerate',nd,'changed',sum(L[i]!=word.opframe[i] for i in range(len(ops))))
word.opframe=L
try:
  r=word.row();json.dump(dict(base=base['child_histogram'],new=r['child_histogram']),open('minframe_hist.json','w'))
  print('ok')
except Exception as e:print('row failed',e)
