"""Exact collective span of the already-certified proper-hyperplane directions."""
from pathlib import Path
from sympy import Matrix,Rational
from collections import Counter
import json
p=Path(__file__).resolve().parent
w=json.loads((p/'TERNARY126-HYPERPLANE-WITNESSES.json').read_text());S=w['survivors']
B=Matrix.hstack(*[Matrix([Rational(z) for z in d['coefficients']]) for h in S for d in h['directions']])
_,piv=B.to_DM().rref()
sums=Counter(str(sum(Rational(z) for z in d['port_values'])) for h in S for d in h['directions'])
norms=Counter(sum(x*x for x in h['normal'])%3 for h in S)
r={'surviving_normal_norms':dict(norms),'number_directions':B.cols,'coefficient_span_rank':len(piv),'independent_direction_indices':list(piv),'direction_coordinate_sum_histogram':dict(sums)}
(p/'TERNARY126-HYPERPLANE-SPAN.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
