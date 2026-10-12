from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import sys,json
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'source550-review/engines'));import moment,base_two_moment
s=json.loads((R/'trace550-frame-single-certificate/RESULT.json').read_text());p=json.loads((R/'pr550-independent314/local/PRICE.json').read_text());H=Counter({int(r):n for r,n in p['global_profile'].items()});b=Q(p['complex_lower']);rows=[]
for shape in s['shapes']:
 d=Counter(x for x in shape['new']if x);d.subtract(x for x in shape['old']if x)
 if not any(d.values()):rows.append(dict(shape=shape,status='IDENTICAL_COMPLETE_PROFILE'));continue
 new=H.copy();new.update({r:72*n for r,n in d.items()});new={r:n for r,n in new.items()if n};assert all(n>0 for n in new.values())
 a,z=moment.moment(new,73,7168,b,True)
 c,e=base_two_moment.moment(73,7168,list(new.items()),b);fl,fu=base_two_moment.moment(73,7168,[(1,32*73**2*sum(new.values()))],b);c+=fl/10**16;e+=fu/10**16
 assert a>1 and c>1
 rows.append(dict(shape=shape,status='REJECTED_AT_BASELINE_ADMITTED_B_BY_BOTH_ENGINES',engine1_lower_minus_one=str(a-1),engine2_lower_minus_one=str(c-1)))
res=dict(status='PASS_ALL_SINGLE_EVENT_FRAME_ENDPOINTS_NO_HIGHER_B',b=str(b),endpoint_probes=s['endpoint_probes'],shapes=len(rows),receipts=rows,scope='Frozen PR550 word and all other frames; fixed valid owner remainder. Exact endpoint moment comparisons plus concavity exclude all intermediate single-event dimensions. Does not exclude neutral paths or simultaneous changes.')
(R/'trace550-frame-single-certificate/EXACT-PRICES.json').write_text(json.dumps(res,indent=2)+'\n');print(res['status'],len(rows))
