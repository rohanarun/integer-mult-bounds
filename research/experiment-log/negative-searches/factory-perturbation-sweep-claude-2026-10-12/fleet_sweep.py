import sys,time,json,threading,traceback
from pathlib import Path
from daytona import Daytona, DaytonaConfig, CreateSandboxFromImageParams, Resources
d=Daytona(DaytonaConfig(api_key=open('/tmp/radical/DAYTONA_KEY').read().strip()))
N=int(sys.argv[1]); PER=int(sys.argv[2]); START=int(sys.argv[3]) if len(sys.argv)>3 else 1
OUT=Path('/tmp/fleet_out');OUT.mkdir(exist_ok=True)
pkg=open('/tmp/swpkg.tgz','rb').read()
lock=threading.Lock(); status={}
def job(k):
    seed=START+k; sb=None
    try:
        sb=d.create(CreateSandboxFromImageParams(image='python:3.12',language='python',resources=Resources(cpu=1,memory=2,disk=3),labels={'campaign':'factory-sweep'}),timeout=600)
        sb.fs.upload_file(pkg,'/home/daytona/swpkg.tgz')
        r=sb.process.exec('cd /home/daytona && tar xzf swpkg.tgz && pip install -q numpy scipy 2>&1|tail -1',timeout=900)
        r=sb.process.exec('cd /home/daytona/swpkg && python3 -B sweep.py %d %d /home/daytona/out > run.log 2>&1; echo EXIT $?; tail -c 300 run.log'%(seed,PER),timeout=5400)
        data=sb.fs.download_file('/home/daytona/out/results.json')
        (OUT/('res_%d.json'%seed)).write_bytes(data)
        with lock: status[seed]='ok'
    except Exception as e:
        with lock: status[seed]='fail:'+repr(e)[:200]
    finally:
        if sb:
            try: sb.delete()
            except Exception: pass
ths=[threading.Thread(target=job,args=(k,)) for k in range(N)]
for i,t in enumerate(ths): t.start(); time.sleep(1.5)
for t in ths: t.join()
json.dump(status,open(OUT/('status_%d.json'%START),'w'),indent=1)
print('done',sum(1 for v in status.values() if v=='ok'),'ok of',N)
