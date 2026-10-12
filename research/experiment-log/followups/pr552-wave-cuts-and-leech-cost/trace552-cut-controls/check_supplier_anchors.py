"""Minimal calls to the pinned GK profiler exposing equality-only boundaries."""
from pathlib import Path
import sys,json,copy,hashlib,os
P=Path(__file__).resolve().parent;assert os.path.ismount('/Volumes/SP AI 01_16') and os.access(P,os.W_OK)
sys.path.insert(0,str(P.parent/'source550-review/local/vendor/gk'))
import gk_word as g
# Tiny supplier-shaped profiler controls only; these are not physical words.
g.V=1
base={'report':{'R':1},'ports':[1],'centers':[2],'center_frames':[[2]],'target_levels':{'0':[2]},'cut':[['add',1,2,1,1,[2]]],'A':[['scale',2,1,1,[2]],['scale',1,1,1,[2]]],'B':[]}
old=dict(g.profile(base));results=[]
for ix,expected in [(0,'centre frame'),(1,'target level at the centre scatter')]:
 w=copy.deepcopy(base);w['A'][ix][-1]=[]
 try:g.profile(w)
 except AssertionError as e:
  assert str(e)==expected,(str(e),expected);results.append({'event':ix,'expected_error':expected,'observed_error':str(e),'rejected':True})
 else:raise AssertionError('invalid equality anchor was accepted')
ans={'status':'PASS_REAL_GK_PROFILE_ANCHOR_NEGATIVE_CONTROLS','baseline_profile':old,'mutation_controls':results,'source_gk_word_sha256':hashlib.sha256(Path(g.__file__).read_bytes()).hexdigest(),'scope':'Tiny profiler-shaped fixtures; not scalar/physical/global supplier admission.'}
(P/'SUPPLIER-ANCHOR-CONTROLS.json').write_text(json.dumps(ans,indent=2)+'\n');print(json.dumps(ans,indent=2))
