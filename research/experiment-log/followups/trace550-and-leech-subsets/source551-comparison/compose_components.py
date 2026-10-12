exec(compile((__import__('pathlib').Path(__file__).resolve().parent/'compose.py').read_text().split('# First compose550')[0], 'compose-prefix','exec'))
# Test phase-separated changes directly on552; old550 B alignment handled against wave-plus550.
wave550=load(O/'wave-plus550.json.gz')
for sec in ('A','B'):
 z=copy.deepcopy(wave550);changes=[ch for ch in receipt['changes'] if ch['section']==sec]
 for ch in changes:
  i=ch['index'];assert z[sec][i][:-1]==source550[sec][i][:-1];z[sec][i][-1]=ch['new']
 emit('only-phase-'+sec,z,{'applied':len(changes)})
# Connected components of affected-register graph, tested full overrides and meets.
changes=receipt['changes'];adj=[set() for _ in changes]
def regs(ch):return set(source550[ch['section']][ch['index']][1:3])
for i,ch in enumerate(changes):
 for j in range(i):
  if ch['section']==changes[j]['section'] and regs(ch)&regs(changes[j]):adj[i].add(j);adj[j].add(i)
seen=set();groups=[]
for i in range(len(changes)):
 if i in seen:continue
 group=set();todo=[i]
 while todo:
  q=todo.pop()
  if q in group:continue
  group.add(q);todo.extend(adj[q]-group)
 seen|=group;groups.append(sorted(group))
for gi,group in enumerate(groups):
 for mode in ('override','intersection'):
  z=copy.deepcopy(wave550)
  for j in group:
   ch=changes[j];sec,i=ch['section'],ch['index'];F=ch['new'] if mode=='override' else g.basis(g.span(z[sec][i][-1])&g.span(ch['new']));z[sec][i][-1]=list(F)
  emit(f'component{gi:02d}-{mode}',z,{'change_indices':group,'size':len(group)})
(O/'COMPONENT-RESULT.json').write_text(json.dumps({'groups':groups,'results':results},indent=2)+'\n')
