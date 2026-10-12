from pathlib import Path
import json,subprocess,base64,hashlib,concurrent.futures
R=Path(__file__).resolve().parent;known={}
for base in ['source531-review','source535-review','source541-static44','source493','source510','source541-method','r480-minimal-publication','source543-review','source544-review','source548-review']:
 p=R/base
 if not p.exists():continue
 for f in p.rglob('*'):
  if f.is_file()and '__pycache__'not in f.parts:
   raw=f.read_bytes();known[hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()]=f
for n in [550]:
 x=json.loads((R/f'source{n}-tree-selection.json').read_text());out=R/f'source{n}-review';assert not out.exists();out.mkdir();rows=x['files'];prefix=x['prefix']
 def fetch(e):
  if e['sha']in known:raw=known[e['sha']].read_bytes()
  else:
   obj=json.loads(subprocess.check_output(['gh','api','repos/'+x['repo']+'/git/blobs/'+e['sha']]));raw=base64.b64decode(obj['content'])
  assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==e['sha'];p=out/e['path'][len(prefix):];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw);return e['sha']in known
 with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:reused=sum(pool.map(fetch,rows))
 (R/f'source{n}-acquisition.json').write_text(json.dumps(dict(repo=x['repo'],head=x['head'],prefix=prefix,files=len(rows),reused=reused,status='PASS_EXACT_GIT_BLOBS',blobs={e['path'][len(prefix):]:e['sha']for e in rows}),indent=2)+'\n');print(n,'acquired',len(rows),'reused',reused,flush=True)
