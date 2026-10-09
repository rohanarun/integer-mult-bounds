import sys,json,importlib.util
from collections import Counter,defaultdict
from pathlib import Path
sys.set_int_max_str_digits(0)
P=Path('/home/claude/crocswap/w200/research/paired-cube-diagonal-bit-168')
sys.path.insert(0,str(P/'bit'))
spec=importlib.util.spec_from_file_location('ad',P/'bit/word.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
word=m.Candidate();word.exact_frames()
C=word.C;h,v=word.h,word.v;ops=word.ops
phase=set(word.phase1);position={i:j for j,i in enumerate(word.rest)}
sources=set(word.source.values());alias=set(word.donor)|set(word.donor.values())
writes=defaultdict(list);uses=defaultdict(list);rootids=defaultdict(list)
for i,(a,b,n) in enumerate(ops):writes[a].append(i);uses[b].append(i)
for j,s in enumerate(word.w['rootroles']):rootids[s].append(j)
first=[len(word.rest)+1]*v
for s in word.order:
  for t in word.gauge[s]['targets']:first[t]=min(first[t],word.readtime[s])
fail=Counter();ok=[];kinds=Counter()
for j,r in enumerate(word.g['roots']):
  s=word.w['rootroles'][j];U=word.w['root_frame'][j];kinds[r['kind']]+=1
  reasons=[]
  if r['kind']!='side':reasons.append('kind:'+r['kind'])
  if s in sources:reasons.append('source')
  if s in alias:reasons.append('alias')
  if s in word.gauge:reasons.append('gauged')
  if rootids[s]!=[j]:reasons.append('multiroot')
  if uses[s]:reasons.append('consumers')
  if not writes[s]:reasons.append('nowrites')
  if any(i in phase for i in writes[s]):reasons.append('center')
  if writes[s] and not all(C.sub(word.opframe[i],U) for i in writes[s]):reasons.append('cap')
  piv=[t for t in r['targets'] if writes[s] and all(i in position for i in writes[s]) and first[t]>max(position[i] for i in writes[s])]
  if not piv:reasons.append('nopivot')
  for x in reasons:fail[x]+=1
  if not reasons:ok.append((j,piv,r['targets'],C.dimf[U]))
  elif len(reasons)==1:fail['ONLY:'+reasons[0]]+=1
print('roots',len(word.g['roots']),kinds);print(fail);print('eligible',len(ok))
json.dump([dict(root=j,pivots=p,targets=t,rank=d) for j,p,t,d in ok],open('elig.json','w'))
