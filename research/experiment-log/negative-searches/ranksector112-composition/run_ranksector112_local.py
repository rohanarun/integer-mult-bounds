"""Fresh local check of PR522 rank-sector factory restricted by PR523's port rule."""
from pathlib import Path
import subprocess,sys,os,json,time
R=Path(__file__).resolve().parent;P=R/'source523-review';V=P/'vendor/pr514';C=V/'vendor/complex';G=C/'e8-complex-gauge-kernel';O=R/'ranksector112-local-admission';O.mkdir(exist_ok=False);L=O/'local';steps=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0',TMPDIR=str(R/'tmp401'));env.pop('PYTHONOPTIMIZE',None)
for name,script,args in [('restrict',P/'code/build_port112.py',[R/'pr522-independent-full314/base/split-centres',L]),('transport',P/'code/audit_port112_transport.py',[L]),('emit',P/'code/emit_local112.py',[L]),('local',P/'code/audit_local112.py',[L]),('phases',P/'code/phases_local112.py',[L,C/'split-centres-global/vendor']),('wrappers',G/'code/adapters_gk.py',[L/'CANONICAL-WORD.json.gz',L/'RESIDUAL-ADAPTERS.json',L/'LEMMA-A.json'])]:
 print('RUN',name,flush=True);start=time.monotonic()
 with(O/(name+'.log')).open('w')as f:p=subprocess.run([sys.executable,'-B',str(script),*map(str,args)],stdout=f,stderr=subprocess.STDOUT,env=env)
 steps.append(dict(name=name,returncode=p.returncode,seconds=time.monotonic()-start));(O/'STEPS.json').write_text(json.dumps(steps,indent=2)+'\n')
 if p.returncode:raise SystemExit(p.returncode)
 print('PASS',name,flush=True)
(O/'RECEIPT.json').write_text(json.dumps(dict(status='PASS_RANKSECTOR112_LOCAL_ONLY',steps=steps,scope='Fresh restricted local scalar transport, both orientation column/frame checks, exact phases and residual wrappers. Global ownership and exact composition remain separate.'),indent=2)+'\n')
