"""Exact ceiling for deleting all fallback charge from the fixed PR510 profile.
A relaxation, not a feasible new supplier or unconditional theorem.
Prepared for rohanarun with OpenAI Codex assistance. Apache-2.0.
"""
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal,localcontext
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent;O=R/'bit510-fallback-ceiling';O.mkdir(exist_ok=False)
p=R/'r480-sharp535-publication/research/r480-sharp-charge535'
def load(n):
 s=importlib.util.spec_from_file_location(n,p/'engines'/(n+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M,B=load('moment'),load('base_two_moment')
x=json.loads((p/'inputs/PR510-EXPECTED.json').read_text())['nine'];H={int(k):v for k,v in x['profile'].items()};m=x['m'];W=x['bit']['live'];old=Q(json.loads((p/'EXPECTED.json').read_text())['kappa'])
r=M.certify(H,m,W,False);lo,hi=Q(r['lower']),Q(r['upper']);checks=[]
for c,ok in [(lo,True),(hi,False)]:
 a,z=M.moment(H,m,W,c,False);b,y=B.moment(m,W,list(H.items()),c)
 assert (z<1 and y<1) if ok else (a>1 and b>1)
 checks.append(dict(endpoint=str(c),accept=ok,mercator=[str(a-1),str(z-1)],base_two=[str(b-1),str(y-1)]))
ceiling=hi/(1+hi)
def dec(v):
 with localcontext()as ctx:
  ctx.prec=60;return str(Decimal(v.numerator)/Decimal(v.denominator))
out=dict(status='PASS_FIXED_PROFILE_ZERO_FALLBACK_RELAXATION',profile=H,m=m,live=W,baseline_kappa=str(old),zero_fallback_bit_interval=[str(lo),str(hi)],strict_kappa_ceiling=str(ceiling),strict_kappa_ceiling_decimal=dec(ceiling),absolute_headroom_upper=dec(ceiling-old),relative_percent_headroom_upper=dec(100*(ceiling-old)/old),checks=checks,input_sha256=hashlib.sha256((p/'inputs/PR510-EXPECTED.json').read_bytes()).hexdigest(),scope='Fixed PR510 histogram and m64/live30720. Remove all nonnegative fallback cost and all outer bootstrap/parameter loss. Moment strictly increases with c, hence c<upper and kappa<c/(1+c)<the displayed ceiling in the inherited outer formula. This does not bound changed histograms, hosting, local words, geometry or outer theorems; zero fallback is not claimed realizable.')
(O/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items()if k not in ['profile','checks','input_sha256']})
