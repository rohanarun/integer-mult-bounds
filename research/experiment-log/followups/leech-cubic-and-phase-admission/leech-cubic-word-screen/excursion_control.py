"""Exact arbitrary-dirt control for source excursions; no native compiler claim."""
from pathlib import Path
from fractions import Fraction as Q
import json
O=Path(__file__).resolve().parent
# x0,x1,y0,y1,z0,z1. Gathers z=Gx, scatter y=Sz.
G=[[Q(1),Q(1)],[Q(1),Q(-1)]]
S=[[Q(3,4),Q(1,4)],[Q(1,4),Q(-3,4)]]
T=[[sum(S[t][k]*G[k][i] for k in range(2)) for i in range(2)] for t in range(2)]
assert T==[[1,Q(1,2)],[Q(-1,2),1]]
pre=[(2+t,4+k,-S[t][k]) for t in range(2) for k in range(2)]
A=[(4+k,i,G[k][i]) for k in range(2) for i in range(2)]
scatter=[(2+t,4+k,S[t][k]) for t in range(2) for k in range(2)]
B=[(2+t,i,-T[t][i]) for t in range(2) for i in range(2) if i!=t]
cleanup=[(t,s,-q) for t,s,q in reversed(A)]
program=pre+A+scatter+B+cleanup
def replay(events):
    rows=[[Q(i==j) for j in range(6)] for i in range(6)]
    for t,s,q in events:rows[t]=[a+q*b for a,b in zip(rows[t],rows[s])]
    return rows
expected=[[Q(i==j) for j in range(6)] for i in range(6)]
for i in range(2):expected[2+i][i]=1
assert replay(program)==expected
assert replay(program[1:])!=expected
assert replay(program[:-1])!=expected
# h3 toy: native lines p1,p2 sit in common 2D U. Each roundtrip adds2
# to the unchanged endpoint climb2. Descending U->p violates monotone
# inclusion but is a legitimate prospective general frame transition.
def span(F):
    z={0}
    for x in F:z|={y^x for y in list(z)}
    return z
p=span([1]);U=span([1,2]);full=span([1,2,4])
assert p<U<full and not U<=p
def distance(a,b):return (len(a).bit_length()-1)+(len(b).bit_length()-1)-2*(len(a&b).bit_length()-1)
assert distance(p,U)+distance(U,p)+distance(p,full)==4
v=98280;extra=2*(25-1)*v
slope=33280-extra
assert slope<0
result={'status':'PASS_SCALAR_EXCURSION_IDENTITY_BUT_NEGATIVE_RANK_DEFICIT',
 'arbitrary_columns_checked':6,'toy_scalar_operations':len(program),
 'negative_controls':['missing_dirty_precompensation_rejected','missing_cleanup_rejected','nonmonotone_U_to_p_rejected_by_inclusion'],
 'source_roundtrip_cost_each':48,'extra_rank_per_local_invocation':extra,
 'deficit_after_one_excursion_per_source':f'{slope}*L-98280',
 'second_inverse_excursion_extra_if_used':extra,
 'minimal_local_rank_mass_with_one_excursion':2*v*25+26*2600+65000+extra,
 'scope':'Scalar toy identity only. Current monotone local profiler cannot admit U->p. A generalized frame implementation must pay the extra distance; unchanged cover already has negative rank deficit for all positive L. No 26D phase replay or full scalar word generated.'}
(O/'EXCURSION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
