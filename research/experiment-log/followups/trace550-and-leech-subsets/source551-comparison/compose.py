import gzip,json,sys,copy,difflib,hashlib
from pathlib import Path
from collections import Counter
O=Path(__file__).resolve().parent;ROOT=O.parent
sys.path.insert(0,str(ROOT/'source548-review/complex-local/static44/gk'));import gk_word as g,gk_common as c
g.V=c.V=112;g.DATA=c.DATA=7168
load=lambda p:json.loads(gzip.decompress(p.read_bytes()))
w=load(O/'weighted/FULL-WORD.json.gz');source550=load(ROOT/'pr550-independent314/local/candidate/FULL-WORD.json.gz');own=load(ROOT/'trace550-retimed-candidate/WORD.json.gz');receipt=json.loads((ROOT/'trace550-retimed-candidate/CONSTRUCTION.json').read_text());baseH=g.profile(w);results=[]
def fee(H):return sum(n*r*((73/r)**.001594507308884431-1) for r,n in H.items())
def emit(name,u,meta):
 try:H=g.profile(u)
 except AssertionError as e:results.append({'variant':name,'status':'REJECTED_FRAME_CHAIN','error':str(e),'meta':meta});return
 u['cleanup']=[g.inverse(e,g.FULL) for e in reversed(u['A']+u['B']) if not 112<=e[1]<224];u['report']['local_profile']=dict(H);u['report']['local_rank_mass']=sum(r*n for r,n in H.items())
 delta=Counter(H);delta.subtract(baseH);r={'variant':name,'status':'PASS_LOCAL_FRAME_PROFILE_ONLY','profile':dict(H),'delta':{k:n for k,n in delta.items() if n},'fee_delta':fee(H)-fee(baseH),'meta':meta};results.append(r);(O/(name+'.json.gz')).write_bytes(g.dump(u));print(json.dumps(r),flush=True)
# First compose550 exact scalar expansion with552's improved background.
u=copy.deepcopy(w);p,q=936,1048;e3=u['B'][p];e1=u['B'][q];assert e3[:5]==['add',283,299,1,1] and e1[:5]==['add',616,283,1,1]
new=[['add',616,283,1,1,[290,162,98,24,6]],['add',616,299,1,1,[290,162,98,24,6]],['add',283,299,1,1,[290,162,98,24,6]]]
def commute(e,f):return e[1]!=f[2] and f[1]!=e[2] if e[0]==f[0]=='add' else not set(e[1:3])&set(f[1:3])
assert all(commute(e1,e) for e in u['B'][p+1:q]);u['B']=u['B'][:p]+new+u['B'][p+1:q]+u['B'][q+1:];emit('wave-plus550',u,{'moves':1,'input_pr552_head':'33c33af0b7697155be1ea708e08cbd3f0707d94c'})
# After550 composition B index mapping exactly agrees;552 source substitutions are in A only.
for mode in ('override','only_unconflicted','intersection','union'):
 z=copy.deepcopy(u);applied=[];conflicts=[]
 for ch in receipt['changes']:
  sec,i=ch['section'],ch['index'];assert source550[sec][i][-1]==ch['old'];assert own[sec][i][-1]==ch['new']
  if z[sec][i][:-1]!=source550[sec][i][:-1]:conflicts.append({'section':sec,'index':i,'reason':'scalar_operation_changed'});continue
  F=z[sec][i][-1];conflict=g.basis(F)!=g.basis(ch['old'])
  if conflict:conflicts.append({'section':sec,'index':i,'reason':'frame_background_changed','background':F,'old':ch['old'],'new':ch['new']})
  if mode=='only_unconflicted' and conflict:continue
  if mode=='intersection':newF=g.basis(g.span(F)&g.span(ch['new']))
  elif mode=='union':newF=g.basis(F+ch['new'])
  else:newF=g.basis(ch['new'])
  z[sec][i][-1]=list(newF);applied.append((sec,i))
 emit('wave550-retime-'+mode,z,{'applied':applied,'conflicts':conflicts})
(O/'COMPOSITION-RESULT.json').write_text(json.dumps({'baseline_profile':dict(baseH),'results':results},indent=2)+'\n')
