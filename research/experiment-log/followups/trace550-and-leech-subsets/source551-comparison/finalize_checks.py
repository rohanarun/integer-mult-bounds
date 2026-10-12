from pathlib import Path
import json,gzip,sys,hashlib
O=Path(__file__).resolve().parent;ROOT=O.parent;sys.path.insert(0,str(ROOT/'source548-review/complex-local/static44/gk'));import gk_word as g,gk_common as c
g.V=c.V=112;g.DATA=c.DATA=7168
source=json.load(gzip.open(O/'weighted/FULL-WORD.json.gz'));base=g.profile(source);res=[]
for seed in [55201,55202]:
 word=json.load(gzip.open(O/f'anneals552/seed{seed}.gz'));H=g.profile(word);assert H==base;assert all(source[k]==word[k] for k in source if k not in ('report',));res.append({'seed':seed,'status':'PASS_FULL_PROFILE_RECOUNT_NO_GAIN','exact_word_structure_unchanged':True,'local_profile':dict(H),'raw_output_sha256':hashlib.sha256((O/f'anneals552/seed{seed}.gz').read_bytes()).hexdigest()})
(O/'ANNEAL-RECOUNT.json').write_text(json.dumps(res,indent=2)+'\n')
# Bind unchanged compiler primitives to both downloaded exact Git trees.
records=[]
for n,prefix in [(551,'research/subspace16-r420/vendor/static44/gk/'),(552,'research/filtration-wavefront/complex-local/static44/gk/')]:
 tree={x['path']:x['sha'] for x in json.load(open(O/f'TREE{n}.json'))}
 for name in ['gk_common.py','gk_word.py']:
  data=(ROOT/'source548-review/complex-local/static44/gk'/name).read_bytes();sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert sha==tree[prefix+name];records.append({'pr':n,'path':prefix+name,'git_blob':sha})
(O/'COMPILER-SOURCE-BINDING.json').write_text(json.dumps(records,indent=2)+'\n');print('PASS anneal full profiles and shared compiler Git blobs')
