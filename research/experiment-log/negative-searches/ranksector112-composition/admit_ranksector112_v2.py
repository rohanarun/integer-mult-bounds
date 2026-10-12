"""Fresh global admission of source522 rank-sector factory on source523 ports."""
from pathlib import Path
import subprocess,sys,os,json,time,hashlib
R=Path(__file__).resolve().parent;P=R/'source523-review';V=P/'vendor/pr514';G=V/'vendor/complex/e8-complex-gauge-kernel';C=R/'pr472-delivery-publication/research/ranksector112-async/code';F=R/'pr522-independent-full314/base';L=R/'ranksector112-local-admission/local';O=R/'ranksector112-global-admission-v2';O.mkdir(exist_ok=False);B=O/'base';H=O/'hosted';A=O/'audit';A.mkdir();steps=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0',TMPDIR=str(R/'tmp401'));env.pop('PYTHONOPTIMIZE',None);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert json.load(open(R/'pr522-independent-full314/RESULT.json'))['status']=='PASS_CONDITIONAL_ASYNCHRONOUS_COMPLEX_DERIVATIVE'
assert json.load(open(R/'ranksector112-local-admission/RECEIPT.json'))['status']=='PASS_RANKSECTOR112_LOCAL_ONLY'
jobs=[('restrict-global',P/'code/restrict_global.py',[F,L,B]),('audit-restriction',R/'ranksector112-adapted-code/audit_global_restriction.py',[F,B,A/'GLOBAL-RESTRICTION-AUDIT.json']),('emit',P/'code/emit_async.py',[G,B,R/'ranksector112-owner-transport/OWNERS.json.gz',R/'ranksector112-owner-transport/PLAN.json',H]),('audit',P/'code/audit_async.py',[B,H,A/'ASYNC-AUDIT.json']),('raw-independent',C/'audit_112_independent.py',['--original-base',F,'--local',L,'--owners',R/'ranksector112-owner-transport/OWNERS.json.gz','--out',A]),('invoice',C/'audit_async_invoice.py',[A,B,H]),('assembly',P/'code/assemble.py',[A,B,H,V/'inputs/PR493-EXPECTED.json'])]
try:
 for name,script,args in jobs:
  print('RUN',name,flush=True);start=time.monotonic();log=O/(name+'.log')
  with log.open('w')as f:p=subprocess.run([sys.executable,'-B',str(script),*map(str,args)],stdout=f,stderr=subprocess.STDOUT,env=env)
  steps.append(dict(name=name,returncode=p.returncode,seconds=time.monotonic()-start,log_sha256=sha(log)));(O/'STEPS.json').write_text(json.dumps(steps,indent=2)+'\n');assert p.returncode==0,(name,log.read_text()[-6000:]);print('PASS',name,flush=True)
 x=json.load(open(A/'EXACT-ASSEMBLY.json'));expected=json.load(open(R/'ranksector112-arithmetic/EXACT-ARITHMETIC.json'));assert all(x[k]==expected[k]for k in ['kappa','complex_lower','bit_lower'])
 (O/'RECEIPT.json').write_text(json.dumps(dict(status='PASS_RANKSECTOR112_FINITE_COMPOSITION',kappa=x['kappa'],kappa_decimal=x['kappa_decimal'],complex_lower=x['complex_lower'],complex_template_sha256=x['complex_template_sha256'],steps=steps,source522_receipt_sha256=sha(R/'pr522-independent-full314/RESULT.json'),local_receipt_sha256=sha(R/'ranksector112-local-admission/RECEIPT.json'),scope='Fresh source522 complex replay, changed local112 checks, global restriction, independent actual whole owners, invoice and exact assembly. Bit493 operator cited/repriced; inherited all-size and analytic interfaces remain conditional.'),indent=2)+'\n');print('PASS_RANKSECTOR112_FINITE_COMPOSITION',x['kappa_decimal'],flush=True)
except BaseException as e:
 (O/'FAILURE.json').write_text(json.dumps(dict(error=repr(e),steps=steps),indent=2)+'\n');raise
