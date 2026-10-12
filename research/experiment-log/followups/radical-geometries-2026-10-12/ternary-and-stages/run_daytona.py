"""Own one ephemeral sandbox; never list/reconfigure/delete other workers' sandboxes."""
import json,time,hashlib,sys
from pathlib import Path
from daytona import Daytona,DaytonaConfig,CreateSandboxFromImageParams,Resources
ROOT=Path(__file__).resolve().parent
receipt={'campaign':'radical-geometry-stages','created_sandbox':None,'status':'STARTING','sources':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['experiments.py','INPUT.json']}}
def save():(ROOT/'DAYTONA-RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
save();sb=None
try:
 d=Daytona(DaytonaConfig(api_key=Path('/tmp/radical/DAYTONA_KEY').read_text().strip()))
 sb=d.create(CreateSandboxFromImageParams(image='python:3.12',language='python',resources=Resources(cpu=1,memory=2,disk=3),labels={'campaign':'imb-radical-stages','owner':'codex-subagent','source':'pr548'},auto_stop_interval=10,auto_delete_interval=20),timeout=60)
 receipt.update(created_sandbox=sb.id,status='CREATED');save();print('CREATED',sb.id,flush=True)
 for name in ['experiments.py','INPUT.json']:sb.fs.upload_file((ROOT/name).read_bytes(),'/home/daytona/'+name)
 r=sb.process.exec('cd /home/daytona && PYTHONDONTWRITEBYTECODE=1 python -B experiments.py',timeout=60)
 (ROOT/'REMOTE-STDOUT.log').write_text(r.result)
 receipt['exit_code']=r.exit_code;save()
 (ROOT/'RESULT.json').write_bytes(sb.fs.download_file('/home/daytona/RESULT.json'))
 receipt.update(status='EXPERIMENTS_COMPLETE',result_sha256=hashlib.sha256((ROOT/'RESULT.json').read_bytes()).hexdigest());save();print('EXPERIMENTS_COMPLETE',flush=True)
except Exception as e:
 # Exception class only: provider messages may accidentally contain auth/context.
 receipt.update(status='ERROR',error_type=type(e).__name__);save();print('ERROR_CLASS',type(e).__name__,flush=True)
finally:
 if sb is not None:
  try:
   d.delete(sb,timeout=60);receipt['cleanup']='DELETE_CALL_COMPLETED';save();print('DELETE_CALL_COMPLETED',flush=True)
  except Exception as e:receipt['cleanup']='DELETE_ERROR_'+type(e).__name__;save();print(receipt['cleanup'],flush=True)
