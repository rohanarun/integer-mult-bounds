from pathlib import Path
import json,shutil,hashlib
R=Path(__file__).resolve().parent;D=R/'trace550-retiming-publication/research/complex-trace-joint-retiming'
s=(D/'upstream550/assemble.py').read_text().replace("P/'engines'","P/'upstream550/engines'").replace("P/'inputs/PR543-EXPECTED.json'","P/'upstream550/inputs/PR543-EXPECTED.json'").replace("P/'engines'/(name+'.py')","P/'upstream550/engines'/(name+'.py')").replace('z[\'events\']==22109','z[\'events\']==22111').replace("b=Q(398395281619778713553,250000000000000000000000)","b=Q(read(P/'PRICE.json')['complex_lower'])")
start=s.index(' expected={');end=s.index('\n H=',start);s=s[:start]+" expected={int(r):n for r,n in read(P/'PRICE.json')['global_profile'].items()}"+s[end:]
s=s.replace('PASS_FRESH_TRACE_EXPANSION_EXACT_ASSEMBLY','PASS_FRESH_JOINT_FRAME_RETIMING_EXACT_ASSEMBLY').replace('gain_over_pinned547_percent','gain_over_pinned550_percent').replace("Q('0.001590984155135328')","Q('0.001591045666134196')")
(D/'assemble.py').write_text(s)
shutil.copy2(D/'upstream550/assembly_controls.py',D/'assembly_controls.py')
(D/'verify.py').write_text('''"""Reconstruct frozen120-frame change, admit full physical supplier and exact assembly.
OpenAI Codex assistance for Rohan Arun; inherited verifier notices preserved.
"""
from pathlib import Path
import argparse,json,gzip,hashlib,os,subprocess,sys,copy
P=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);a=ap.parse_args();W=a.work.resolve();assert __debug__ and not W.exists() and not W.is_relative_to(P)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
for f,h in read(P/'MANIFEST.json').items():assert sha(P/f)==h,f
W.mkdir(parents=True);env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0');env.pop('PYTHONOPTIMIZE',None)
stages=[]
def run(name,script,*args):
 print('RUN',name,flush=True)
 with (W/(name+'.log')).open('w')as log:r=subprocess.run([sys.executable,'-B',str(P/script),*map(str,args)],stdout=log,stderr=subprocess.STDOUT,env=env)
 stages.append(dict(name=name,exit_code=r.returncode,log_sha256=sha(W/(name+'.log'))));(W/'STAGES.json').write_text(json.dumps(stages,indent=2)+'\\n');assert r.returncode==0,(name,(W/(name+'.log')).read_text()[-3000:])
run('rebuild-upstream550','upstream550/local/construct.py','--input',P/'upstream550/local/inputs/PR548-FULL-WORD.json.gz','--gk',P/'upstream550/local/vendor/gk','--out',W/'baseline')
sys.path.insert(0,str(P/'upstream550/local/vendor/gk'));import gk_word as g,gk_common as c;g.V=c.V=112;g.DATA=c.DATA=7168
w=json.load(gzip.open(W/'baseline/FULL-WORD.json.gz'));before=copy.deepcopy(w)
for z in read(P/'CONSTRUCTION.json')['changes']:
 e=w[z['section']][z['index']];assert e[-1]==z['old'];e[-1]=z['new']
w['cleanup']=[g.inverse(e,g.FULL)for e in reversed(w['A']+w['B'])if not 112<=e[1]<224];w['report']['local_profile']=dict(g.profile(w))
assert json.loads(gzip.decompress(g.dump(w)))==json.load(gzip.open(P/'WORD.json.gz'))
assert w['report']['local_profile']=={int(r):n for r,n in read(P/'PRICE.json')['local_profile'].items()}
run('scalar-and44controls','upstream550/local/audit_scalar.py',P/'WORD.json.gz',P/'upstream550/local/inputs/STATIC44-SELECTION.json',W/'SCALAR.json')
run('physical','upstream550/physical/replay.py','--word',P/'WORD.json.gz','--word-sha256',sha(P/'WORD.json.gz'),'--expected-price',P/'PRICE.json','--plan',P/'PLAN.json','--out',W/'physical')
A=W/'physical/complex-audit'
run('assembly','assemble.py','--owner',A/'OWNERS-AND-PROFILE.json','--invoice',A/'PREFIX-AND-INVOICE.json','--out',W/'ASSEMBLY.json')
run('admission-controls','assembly_controls.py','--owner',A/'OWNERS-AND-PROFILE.json','--invoice',A/'PREFIX-AND-INVOICE.json','--out',W/'CONTROLS.json')
x=read(W/'ASSEMBLY.json');assert x['kappa']==read(P/'PRICE.json')['kappa']
receipt=dict(status='PASS_FROZEN_JOINT_RETIMING_FULL_ADMISSION_AND_ASSEMBLY',kappa=x['kappa'],kappa_decimal=x['kappa_decimal'],python=sys.version,stages=stages,manifest_sha256=sha(P/'MANIFEST.json'),assembly_sha256=sha(W/'ASSEMBLY.json'),physical_receipt_sha256=sha(W/'physical/RECEIPT.json'),scope=x['scope'])
(W/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\\n');print(receipt['status'],x['kappa_decimal'],flush=True)
''')
# Keep initial publication status as a durable receipt.
shutil.copy2(D/'STATUS.json',D/'DRAFT-STATUS.json')
(D/'evidence').mkdir()
for src,dest in [('pr550-independent314/RECEIPT.json','UPSTREAM550-INDEPENDENT-REPLAY.json'),('trace550-retimed-candidate/SCALAR-AUDIT.json','SCALAR-AUDIT.json'),('trace550-retimed-physical314/RESULT.json','PHYSICAL-RESULT.json'),('trace550-retimed-physical314/RECEIPT.json','PHYSICAL-RECEIPT.json')]:shutil.copy2(R/src,D/'evidence'/dest)
(D/'discovery').mkdir();shutil.copy2(R/'source534-method/frame_chain_search.py',D/'discovery/frame_chain_search.py');shutil.copy2(R/'minimum_trace550_frames.py',D/'discovery/minimum_trace550_frames.py');shutil.copy2(R/'trace550-frame-anneals/seed55001.json',D/'discovery/seed55001.json');shutil.copy2(R/'trace550-frame-anneals/seed55001.log',D/'discovery/seed55001.log');shutil.copy2(R/'trace550-frame-anneals/seed55002.json',D/'discovery/seed55002.json')
(D/'MANIFEST.json').write_text(json.dumps({f.relative_to(D).as_posix():hashlib.sha256(f.read_bytes()).hexdigest()for f in sorted(D.rglob('*'))if f.is_file()and f!=D/'MANIFEST.json'},indent=2)+'\n')
print('Prepared candidate verifier and exact assembly')
