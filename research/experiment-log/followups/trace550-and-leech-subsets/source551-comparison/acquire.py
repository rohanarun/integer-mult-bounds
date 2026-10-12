import json,subprocess,hashlib,urllib.request,concurrent.futures
from pathlib import Path
O=Path(__file__).resolve().parent
spec=[(551,'chafreaky/integer-mult-bounds','e7faafc4fec401d24080e5b2df12f964f1cfe123','research/subspace16-r420/',['code/build_frames.py','code/slice.py','code/run.py','data/RECIPE.json','EXPECTED.json','proof/SUBSPACE16.md']),(552,'Dugongue/integer-mult-bounds','33c33af0b7697155be1ea708e08cbd3f0707d94c','research/filtration-wavefront/',['code/build_wave.py','inputs/WAVES.json','response/build_weighted_coset.py','response/WEIGHTED-COSET-SELECTION.json','EXPECTED.json','verify.py','complex-local/run_local.py'])]
jobs=[]
for n,repo,head,prefix,paths in spec:
 tree={z['path']:z for z in json.loads((O/f'TREE{n}.json').read_text())}
 for rel in paths:jobs.append((n,repo,head,prefix+rel,rel,tree[prefix+rel]['sha']))
def download(job):
 n,repo,head,path,rel,sha=job;data=urllib.request.urlopen(f'https://raw.githubusercontent.com/{repo}/{head}/{path}').read();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==sha;dest=O/f'pr{n}'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);return {'pr':n,'head':head,'path':path,'sha':sha,'bytes':len(data)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:results=list(ex.map(download,jobs))
(O/'ACQUISITION.json').write_text(json.dumps(results,indent=2)+'\n');print(len(results))
