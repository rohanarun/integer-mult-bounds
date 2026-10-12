"""Necessary fee obstruction for the explicit pure-carrier Leech cubic factory.

No full dense word is emitted. This is not an obstruction to all Leech circuits.
"""
from pathlib import Path
from fractions import Fraction as Q
import hashlib, json, math

O = Path(__file__).resolve().parent
F = O.parent
source = F / 'leech-full-shell-cubic'
data = json.loads((source / 'COMPRESSED-RESULT.json').read_text())
v = data['ports']
centers = data['remaining_centers']
g = data['all_gather_ranks']
h = g + 1
C = centers * g
# One zero-start pure-source clone per port, plus designated gather centers.
# Every center uses the common 25D old-label space. The clones can therefore
# feed all centers, but cannot subsequently serve any native target cap.
R = v + centers
M = 2 * v * (h - 1) + h * R + C

def lower_log(x, terms=128):
    z = (x - 1) / (x + 1)
    out = Q(0)
    term = z
    for j in range(terms):
        out += term / (2*j + 1)
        term *= z*z
    return 2*out

# In the unchanged uniform-stage accounting, m = 1 + (h-1)L.
# For each local rank r<=h, r*((m/r)^b-1)>b*r*log(m/h).
# Thus L*b*M*log(m/h) < ((v-C)*L-v) is necessary.
b = Q(137, 100000)
cutoff = 64
rows = []
for L in range(3, cutoff):
    m = 1 + (h-1)*L
    delta = (v-C)*L-v
    lower = lower_log(Q(m, h))
    margin = L*b*M*lower-delta
    assert margin > 0
    rows.append({'L': L, 'm': m, 'deficit': delta,
                 'strict_lower_fee_margin': float(margin),
                 'positive_exact_numerator': margin.numerator > 0})
# For every L>=64, delta/L < v-C and log(m/h)>=log((1+25*64)/26).
tail = b*M*lower_log(Q(1+(h-1)*cutoff, h))-(v-C)
assert tail > 0
assert all((v-C)*L-v <= 0 for L in (1, 2))

# Negative controls: omission of all source copies invalidates this particular
# rejection test; the optimistic L3 deficit is indeed strictly positive.
wrong_M = 2*v*(h-1)+h*centers+C
assert 10*b*wrong_M*lower_log(Q(251, 26))-((v-C)*10-v) < 0
assert (v-C)*3-v == 1560
proposals = [((v-C-v/L)/(M*math.log((1+(h-1)*L)/h)), L)
             for L in range(3, 10001)]
best = max(proposals)
result = {
    'status': 'PASS_EXACT_FACTORY_FEE_OBSTRUCTION_NOT_GEOMETRY_EXCLUSION',
    'ports': v, 'ambient_dimension': h, 'designated_centers': centers,
    'common_gather_dimension': g, 'copy_rank': C,
    'source_carrier_copies': v, 'helper_stock_lower_bound_this_factory': R,
    'unavoidable_local_rank_mass_this_factory': M,
    'complex_exponent_strict_upper': str(b),
    'complex_exponent_strict_upper_decimal': str(float(b)),
    'all_integer_stage_counts_covered': True,
    'finite_stage_checks': rows,
    'tail_starts_at': cutoff,
    'tail_strict_margin': float(tail),
    'tail_exact_numerator_positive': tail.numerator > 0,
    'log_lower_bound': '128 positive rational atanh-series terms',
    'floating_bound_diagnostic_only': {'maximum': best[0], 'L': best[1]},
    'negative_controls': ['omitting_source_copies_does_not_prove_rejection',
                          'positive_L3_deficit_confirmed'],
    'scope': 'Zero-start, monotone, pure-source-carrier factory with 2600 dedicated centers and common 25D gathers, in uniform-stage accounting m=25L+1. Gives all B corrections for free. Does not exclude mixed/coded carriers, static-frame hosting, different label completions or covers.'
}
(O/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
paths = [source/'COMPRESSED-RESULT.json', source/'compress_sphere.py',
         source/'screen.py', source/'COMPRESSED-GATHER-BASES.json.gz',
         O/'references/build.py', O/'references/audit.py',
         O/'references/price_obstruction.py', O/'references/E7-README.md']
(O/'SOURCES.json').write_text(json.dumps([
    {'path': str(p.relative_to(F)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
    for p in paths], indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='finite_stage_checks'}, indent=2))
