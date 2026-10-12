"""Independent rational rejection and actual hosted-profile normalization check."""
from pathlib import Path
from fractions import Fraction as Q
import json
O=Path(__file__).resolve().parent
r=json.loads((O/'RESULT.json').read_text())
v,h,c=98280,26,2600
R=v+c; C=25*c; mass=2*v*25+26*R+C
assert mass==r['unavoidable_local_rank_mass_this_factory']==7601880
def loglower(x):
    z=(x-1)/(x+1)
    return sum((2*z**(2*j+1)/Q(2*j+1) for j in range(128)),Q(0))
b=Q(r['complex_exponent_strict_upper'])
for L in range(3,64):
    assert b*mass*loglower(Q(25*L+1,26)) > Q(33280*L-98280,L)
assert b*mass*loglower(Q(1601,26))>33280

# The already admitted controller contributes 9*8 copies of the LOCAL
# histogram and has deficit 8*((9-1)*112-9*64). Only local ranks have the
# bound h=9. Its leftover owner calls include rank48 and are nonnegative.
receipt=O/'references/OWNERS-AND-PROFILE.json'
j=json.loads(receipt.read_text()); H={int(k):v for k,v in j['paid_profile'].items()}
local={1:2316,2:424,3:464,4:192,5:56,6:56,8:8}
left={k:H.get(k,0)-72*local.get(k,0) for k in H.keys()|local.keys()}
assert all(n>=0 for n in left.values())
assert sum(k*n for k,n in H.items())==j['rank_mass']
assert 73*j['live']-j['rank_mass']==8*(8*112-9*64)==2560
assert left[48]>0
(O/'VERIFIED.json').write_text(json.dumps({
    'status':'PASS_INDEPENDENT_RATIONAL_FACTORY_BOUND_AND_REFERENCE_NORMALIZATION',
    'strict_b_upper':str(b),'L3_through63_checked':61,'tail_L_ge64_checked':True,
    'reference_source':str(receipt.relative_to(O.parent)),
    'reference_local_calls':72,'reference_replica_multiplier':8,
    'reference_deficit':2560,'reference_idle_profile':left,
    'important_scope':'h bounds LOCAL transition ranks only; nonlocal idle children can exceed h. The general h26 uniform-stage controller is a prospective accounting extension, not an emitted admitted controller.'
},indent=2)+'\n')
print('PASS independent rational bound and actual 72-call normalization')
