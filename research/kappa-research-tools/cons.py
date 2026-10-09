exec(open('sinkenum.py').read().split("fail=Counter()")[0])
from collections import Counter
roots=word.g['roots'];rr=word.w['rootroles']
role2root={s:j for j,s in enumerate(rr)}
def reasons(j):
  r=roots[j];s=rr[j];U=word.w['root_frame'][j];R=[]
  if r['kind']!='side':R.append('kind')
  if s in sources:R.append('source')
  if s in alias:R.append('alias')
  if s in word.gauge:R.append('gauged')
  if rootids[s]!=[j]:R.append('multi')
  if uses[s]:R.append('consumers')
  if not writes[s]:R.append('nowrites')
  if any(i in phase for i in writes[s]):R.append('center')
  if writes[s] and not all(C.sub(word.opframe[i],U) for i in writes[s]):R.append('cap')
  piv=[t for t in r['targets'] if writes[s] and all(i in position for i in writes[s]) and first[t]>max(position[i] for i in writes[s])]
  if not piv:R.append('nopivot')
  return R
only=[j for j in range(len(roots)) if reasons(j)==['consumers']]
st=Counter();nc=Counter();dst=Counter()
for j in only[:518]:
  s=rr[j];lw=max(writes[s]);U=[i for i in uses[s]]
  nc[len(U)]+=1
  for i in U:
    a,b,n=ops[i];st['after_last_write' if i>lw else 'before']+=1
    dst['root' if a in role2root else ('gauge' if a in word.gauge else ('source' if a in sources else 'other'))]+=1
    st['phase' if i in phase else 'rest']+=1
print(len(only),nc,st,dst)
j=only[0];s=rr[j];print('example',j,roots[j]['targets'],'writes',[(i,ops[i]) for i in writes[s]],'uses',[(i,ops[i]) for i in uses[s]])
