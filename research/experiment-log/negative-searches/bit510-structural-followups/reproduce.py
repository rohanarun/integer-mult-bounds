"""Replay the frozen structural screens in a fresh output directory.
Prepared for rohanarun with OpenAI Codex assistance. Apache-2.0.
"""
from pathlib import Path
import sys,shutil,json,tarfile,subprocess,os,hashlib,time
if not __debug__:raise RuntimeError('Assertions must be enabled')
r=Path(__file__).resolve().parent;o=Path(sys.argv[1]).resolve()
assert not o.exists() and not o.is_relative_to(r)
o.mkdir(parents=True);(o/'tmp').mkdir();env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0',TMPDIR=str(o/'tmp'))
w=o/'bit510-review/research/e8-r480-dead-totals/data/bitE8mut-r480.json.gz';w.parent.mkdir(parents=True);shutil.copyfile(r/'input-word.json.gz',w)
assert hashlib.sha256(w.read_bytes()).hexdigest()==json.loads((r/'bit510-native-fusion/RESULT.json').read_text())['word_sha256']
with tarfile.open(r/'native521.tar.gz')as t:
 for item in t:
  if not item.isfile():continue
  p=o/item.name;assert p.resolve().is_relative_to(o/'source521-review')
  p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(t.extractfile(item).read())
def run(script,name):
 start=time.monotonic()
 with (o/(name+'.log')).open('w')as f:subprocess.run([sys.executable,'-B',str(script)],cwd=o,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 return time.monotonic()-start
receipts=[];secs=run(o/'source521-review/check.py','native-packet')
assert json.loads((o/'native-packet.log').read_text())['status']=='PASS_EXACT_LOCAL_NATIVE_FUSION';receipts.append(dict(name='native-packet',status='PASS',seconds=secs))
jobs=[('screen_bit510_native_fusion.py','native-fusion')]+[('search_bit510_observable_'+x+'.py','observable-'+x)for x in ['retarget','slice','reframe','pairs']]
for script,label in jobs:
 shutil.copyfile(r/script,o/script);secs=run(o/script,label);actual=json.loads((o/('bit510-'+label)/'RESULT.json').read_text());expected=json.loads((r/('bit510-'+label)/'RESULT.json').read_text())
 assert {k:v for k,v in actual.items()if k!='seconds'}=={k:v for k,v in expected.items()if k!='seconds'},label
 receipts.append(dict(name=label,status='PASS_IDENTICAL_MATHEMATICAL_RESULT',seconds=secs));print(label,'PASS',flush=True)
(o/'RECEIPT.json').write_text(json.dumps(dict(status='PASS_ALL_FIVE_SCREENS_AND_NATIVE_PACKET',python=sys.version,runs=receipts,scope='Frozen finite search and rational compatibility replay. Excludes the separately recorded3.11 supplier check, emitted physical phases and all-size theorem.'),indent=2)+'\n')
