"""Exact necessary fee inequality in unchanged nine-stage complex cover ansatz."""
from fractions import Fraction as Q
from pathlib import Path
import json
O=Path(__file__).resolve().parent;r=json.loads((O/'RESULT.json').read_text());H={int(k):v for k,v in r['local_profile'].items()};m=73;L=9;V=63;cop=49;deficit=(L-1)*V-L*cop
# ln(x) =2 sum z^(2k+1)/(2k+1); finite positive partial sum strictly below log.
def loglower(x,N=256):
 z=(x-1)/(x+1);power=z;ans=Q(0)
 for k in range(N):ans+=power/(2*k+1);power*=z*z
 return 2*ans
T=sum(z*k*loglower(Q(m,k)) for k,z in H.items());upper=Q(deficit,L)/T
# At any b>=upper: L sum H[r]*r*((m/r)^b-1) > L*b*T >=deficit.
# Padding/idle terms are nonnegative. This is optimistic: no fallback, no overhead.
endpoint=Q(1,5000);margin=L*endpoint*T-deficit;assert margin>0
Tall=sum(z*k*loglower(Q(41,k)) for k,z in H.items());allupper=Q(V-cop)/Tall
out={'all_uniform_odd_stage_counts_ge5_root_upper':str(allupper),'all_uniform_odd_stage_counts_ge5_root_upper_float':float(allupper),'status':'EXACT_NINE_STAGE_LOCAL_FEE_OBSTRUCTION','fixed_local_profile':H,'copy_rank_charge':cop,'per_replica_deficit':deficit,'linear_fee_coefficient_lower':str(T),'conditional_complex_root_strict_upper':str(upper),'conditional_complex_root_strict_upper_float':float(upper),'rejected_b':str(endpoint),'strict_lower_fee_margin_at_rejected_b':str(margin),'strict_lower_fee_margin_float':float(margin),'scope':'Applies to this explicit E7 word in same9stagecover accounting. Not a bound on E7 geometry or different circuits/covers. No exact feasible global price claimed.'}
(O/'PRICE-OBSTRUCTION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if not k.endswith('lower') and not k.endswith('upper') and k!='strict_lower_fee_margin_at_rejected_b'},indent=2))
