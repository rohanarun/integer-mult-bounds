"""Four-register exact control with only an interior insertion permitted."""
from fractions import Fraction as Q
from pathlib import Path
import json
O=Path(__file__).resolve().parent
# i=0,j=1,k=2,l=3. Coefficients intentionally non-unit and signed dyadics.
e=['add',0,1,3,2,[]];u=['add',3,1,-5,4,[]];v=['add',3,0,7,2,[]];f=['add',1,2,-1,2,[]];old=[e,u,v,f]
def commute(e,f):return e[1]!=f[2] and f[1]!=e[2]
def replay(es):
 rows=[[Q(i==j) for j in range(4)] for i in range(4)]
 for _,t,s,a,b,_ in es:rows[t]=[x+Q(a,b)*y for x,y in zip(rows[t],rows[s])]
 return rows
legal=[a for a in range(1,4) if all(commute(e,z) for z in old[1:a]) and all(commute(f,z) for z in old[a:3])];assert legal==[2]
a=Q(3,2);b=Q(-1,2);terms=[f,e,['add',0,2,(-a*b).numerator,(-a*b).denominator,[]]];rewritten=[u,*terms,v];assert replay(old)==replay(rewritten)
# Reject both endpoint gathers and wrong bridge sign.
assert not all(commute(f,z) for z in old[1:3]);assert not all(commute(e,z) for z in old[1:3]);wrong=[list(z) for z in rewritten];wrong[3][3]*=-1;assert replay(old)!=replay(wrong)
r={'status':'PASS_EXACT_INTERIOR_ONLY_STEINBERG_CONTROL','permitted_gap_indices':legal,'old_word':old,'new_word':rewritten,'exact_four_by_four_equal':True,'negative_controls_rejected':3,'scope':'Algebraic movement/indexing control only; not a physical supplier.'};(O/'INTERIOR-CONTROL.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
