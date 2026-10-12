"""Relaxed fixed-local-word owner ceiling, not a feasible allocation.
For 0<b<1, each idle rank r<=R satisfies r^(1-b)>=r*R^(-b).
With total idle mass divisible by R, all mass at R minimizes the relaxed moment.
Prepared for Rohan Arun with OpenAI Codex assistance.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
from decimal import Decimal,localcontext
import json,gzip,importlib.util
R=Path(__file__).resolve().parent;O=R/'static44-owner-headroom';assert not O.exists();O.mkdir();P=R/'r420-static44-publication/research/r420-static44-composition'
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def load(n):
 s=importlib.util.spec_from_file_location(n,P/'engines'/(n+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=load('moment');B=load('base_two_moment');t=read(R/'pr544-independent314/complex-hosted/GLOBAL-TEMPLATE.json.gz');checks=read(R/'pr544-independent314/complex-local/LOCAL-CHECKS.json');h=Counter()
for c in t['calls']:h.update({int(r):n for r,n in checks[c['orientation']]['paid_profile'].items()})
actual=Counter({int(r):n for r,n in read(R/'source544-review/EXPECTED.json')['complex_global_profile'].items()});idle=actual.copy();idle.subtract(h);assert all(n>=0 for n in idle.values());mass=sum(r*n for r,n in idle.items());parent=read(R/'pr544-independent314/complex-base/split-centres/GLOBAL-TEMPLATE.json.gz');cap=max(c['rank']for c in parent['idle_children']);assert cap==48 and mass%cap==0
ideal=h.copy();ideal[cap]+=mass//cap
# Drop fallback costs as a further relaxation; its rejected grid endpoint
# bounds any positive saving admitted by this fixed word/idle-cap envelope.
z=M.certify(dict(ideal),73,t['live'],False);upper=Q(z['upper']);lo,hi=M.moment(dict(ideal),73,t['live'],upper,False);bl,bh=B.moment(73,t['live'],list(ideal.items()),upper);assert lo>1 and bl>1
out=dict(status='PASS_RELAXED_FIXED_WORD_OWNER_CEILING_NOT_FEASIBILITY',source_head='4858bb38da10cd8a1cd25ef85e7c14f4e2b529dd',idle_mass=mass,maximum_idle_rank=cap,ideal_idle_count=mass//cap,actual_idle_profile=dict(+idle),relaxed_global_profile=dict(sorted(ideal.items())),complex_saving_strict_upper=str(upper),scope='Fixed 72-call static44 local profiles, fixed live stock, deficit and original data idle children of rank<=48. Arbitrarily concentrate residual mass into rank48 children and omit fallback charges. This is an optimistic ceiling, not a schedulable owner map or improved kappa.')
with localcontext()as c:c.prec=50;out['complex_saving_strict_upper_decimal']=str(Decimal(upper.numerator)/Decimal(upper.denominator))
(O/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
