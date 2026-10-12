import copy,json,gzip,sys
from pathlib import Path
from collections import Counter
O=Path(__file__).resolve().parent;ROOT=O.parent;sys.path.insert(0,str(ROOT/'source548-review/complex-local/static44/gk'));import gk_word as g,gk_common as c
g.V=c.V=112;g.DATA=c.DATA=7168
load=lambda p:json.load(gzip.open(O/p));a=load('framed551/FULL-WORD.json.gz');b=load('weighted/FULL-WORD.json.gz');base=g.profile(b);indices=[i for i in range(len(b['B'])) if a['B'][i][-1]!=b['B'][i][-1]];results=[]
def check(name,w):
 try:H=g.profile(w)
 except AssertionError as e:results.append({'name':name,'status':'REJECT','error':str(e)});return
 delta=Counter(H);delta.subtract(base);fee=sum(z*r*((73/r)**.001594507308884431-1) for r,z in delta.items());r={'name':name,'status':'LEGAL','profile':dict(H),'delta':{k:z for k,z in delta.items() if z},'fee_delta':fee};results.append(r)
 if fee<0:
  w['cleanup']=[g.inverse(e,g.FULL) for e in reversed(w['A']+w['B']) if not 112<=e[1]<224];w['report']['local_profile']=dict(H);(O/(name+'.json.gz')).write_bytes(g.dump(w));print('GAIN',json.dumps(r),flush=True)
for mode in ['all551','meet','join']:
 w=copy.deepcopy(b)
 for i in indices:
  x=a['B'][i][-1];y=b['B'][i][-1];F=x if mode=='all551' else g.basis(g.span(x)&g.span(y)) if mode=='meet' else g.basis(x+y);w['B'][i][-1]=list(F)
 check('mix-'+mode,w)
for i in indices:
 w=copy.deepcopy(b);w['B'][i][-1]=a['B'][i][-1];check(f'mix-single-{i}',w)
# components under shared affected registers, allowing exact independence of profile deltas.
regs={i:set(b['B'][i][1:3]) for i in indices};seen=set();groups=[]
for i in indices:
 if i in seen:continue
 group={i};todo=[i]
 while todo:
  j=todo.pop()
  for k in indices:
   if k not in group and regs[j]&regs[k]:group.add(k);todo.append(k)
 seen|=group;groups.append(sorted(group))
for gi,group in enumerate(groups):
 for mode in ['override','meet','join']:
  w=copy.deepcopy(b)
  for i in group:
   x=a['B'][i][-1];y=b['B'][i][-1];F=x if mode=='override' else g.basis(g.span(x)&g.span(y)) if mode=='meet' else g.basis(x+y);w['B'][i][-1]=list(F)
  check(f'mix-group{gi}-{mode}',w)
(O/'MIX551552-RESULT.json').write_text(json.dumps({'differences':indices,'groups':groups,'results':results},indent=2)+'\n');print('tests',len(results),'legal',sum(r['status']=='LEGAL' for r in results),'gains',sum(r.get('fee_delta',0)<0 for r in results))
