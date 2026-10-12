from pathlib import Path
import subprocess,json,sys
R=Path(__file__).resolve().parent;O=R/'direct504-random-coalescing';O.mkdir(exist_ok=False)
base=json.load(open(R/'source531-review/EXPECTED.json'))['local_profile'];rows=[]
for seed in range(40):
 out=O/f'seed-{seed:03d}'
 with (O/f'seed-{seed:03d}.log').open('w')as f:
  subprocess.run([sys.executable,'-B',str(R/'search_direct504_random_coalesce.py'),'--word',str(R/'pr531-independent311/reconstructed/selected/FULL-WORD.json.gz'),'--out',str(out),'--seed',str(seed)],stdout=f,stderr=subprocess.STDOUT,check=True)
 d=json.load(open(out/'COALESCING.json'));row=dict(seed=seed,profile=d['local_profile_after'],fee=d['local_entropy_after'],moves=d['moves']);rows.append(row)
 print(seed,row['fee'],row['profile'],flush=True)
 (O/'RESULT.json').write_text(json.dumps(dict(status='DISCOVERY_LOCAL_PROFILES',baseline=base,rows=rows),indent=2)+'\n')
