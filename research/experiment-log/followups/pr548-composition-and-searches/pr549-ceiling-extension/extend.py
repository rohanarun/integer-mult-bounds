"""Reuse PR549's credited rational dual for the independently replayed PR548 word.
No edits to the original author's package. Decimal nominates; two exact engines prove.
Prepared for Rohan Arun with OpenAI Codex assistance. Dual/proof/verifier chafreaky,
Apache-2.0; original notices and source package retained separately.
"""
from pathlib import Path
from decimal import Decimal,localcontext,ROUND_CEILING
from fractions import Fraction as Q
from collections import Counter
import json,sys,hashlib
R=Path(__file__).resolve().parent;O=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else R/'complex548-pr549-dual-retry';assert O.is_relative_to(R);O.mkdir(exist_ok=False)
p=R/'source549-review/verify.py';prefix=p.read_text().split('\nb,receipts=prove(cert)')[0];sys.argv=[str(p),str(O/'RESULT.json')];ns={'__file__':str(p),'__name__':'pr549_fixed_dual_extension'};exec(compile(prefix,str(p),'exec'),ns)
read=lambda p:json.loads(p.read_bytes());plan=read(R/'source548-review/complex-global/SAT534-PLAN.json');assert plan['windows']==ns['plan']['windows'] and Counter(plan['baseline_widths'])==ns['widths'];assert len(plan['order'])==ns['calls']
local=read(R/'pr548-complex314/complex-local/local/LOCAL-CHECKS.json');H=Counter()
import gzip
host=json.loads(gzip.decompress((R/'pr548-complex314/complex-global/hosted/GLOBAL-TEMPLATE.json.gz').read_bytes()))
for c in host['calls']:H.update({int(r):n for r,n in local[c['orientation']]['paid_profile'].items()})
assert len(host['calls'])==ns['calls'] and host['live']==ns['W'];assert sum(r*n for r,n in H.items())+sum(r*n for r,n in ns['stock'].items())-sum(w*n for w,n in ns['demand'].items())==ns['m']*ns['W']-ns['deficit']
# Bind actual fresh replay receipt, profile and current composition arithmetic.
fresh=read(R/'pr548-complex314/RESULT.json');cp=read(R/'source548-review/EXPECTED.json');assert fresh['template_sha256']==cp['complex_template_sha256']==hashlib.sha256(gzip.decompress((R/'pr548-complex314/complex-global/hosted/GLOBAL-TEMPLATE.json.gz').read_bytes())).hexdigest();assert fresh['profile']==cp['complex_global_profile']
ns['H']=H;ns['used_ranks']=sorted(({left for _,_,left in ns['patterns']}|set(H))-{0})
cert=ns['cert'].copy();dual=list(map(Q,cert['dual']));objective=sum(ns['stock'][r]*v for r,v in zip(ns['ranks'],dual))+sum(ns['demand'][w]*v for w,v in zip(ns['ws'],dual[len(ns['ranks']):]));current=Q(cp['complex_lower'])
with localcontext()as ctx:
 ctx.prec=70;decimal=lambda q:Decimal(q.numerator)/Decimal(q.denominator);dd=decimal(objective);lo=decimal(current);hi=Decimal('.0017');m=Decimal(ns['m']);terms=[(Decimal(r*n),(m/Decimal(r)).ln())for r,n in H.items()];fallback=Decimal(32*ns['m']**2*sum(H.values()))/Decimal(10**16);lm=m.ln()
 for _ in range(160):
  b=(lo+hi)/2;gap=sum(co*((b*lr).exp()-1)for co,lr in terms)+fallback*(b*lm).exp()-ns['deficit']+b*dd
  if gap>0:hi=b
  else:lo=b
 ticks=int((hi*Decimal(10**15)).to_integral_value(rounding=ROUND_CEILING));cert['excluded_b']=str(Q(ticks,10**15))
excluded,receipts=ns['prove'](cert)
controls=[]
for name,c in [('current_admitted_b',dict(cert,excluded_b=str(current))),('inflated_stock_dual',dict(cert,dual=[str(Q(cert['dual'][0])+1),*cert['dual'][1:]]))]:
 try:ns['prove'](c)
 except AssertionError:controls.append(name)
 else:raise AssertionError('invalid control accepted '+name)
k=Q(read(R/'r420-pr548-price314.json')['kappa']);limit=excluded/(1+excluded)
def dec(q):
 with localcontext()as ctx:ctx.prec=60;return str(Decimal(q.numerator)/Decimal(q.denominator))
r=dict(status='PASS_EXACT_PR548_POOLED_HOSTING_CEILING_USING_PR549_DUAL',source_heads={'PR548':fresh['source_head'],'PR549':'a248674ccdf0ed32f3a122f594b54524c90e4654'},source_verifier_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),current_kappa=dec(k),current_b=dec(current),excluded_b=str(excluded),excluded_b_decimal=dec(excluded),strict_kappa_ceiling=str(limit),strict_kappa_ceiling_decimal=dec(limit),kappa_headroom_upper=dec(limit-k),relative_kappa_headroom_percent_upper=dec(100*(limit/k-1)),patterns_checked=len(ns['patterns']),moment_engines=receipts,negative_controls=controls,local_profile_72_calls=dict(sorted(H.items())),stock=dict(ns['stock']),demands=ns['demand'],scope='All fractional whole-helper packings of this fixed PR548 local word, 72 calls, eight replicas, idle stock, helper widths and retained per-child bad charge. Relaxes chronology, ownership, per-call exclusion and integrality. Fixed-word packing ceiling, not a feasible supplier or new kappa. Changed words, widths, chain, stock, banks and compiler/outer assumptions are outside scope.')
(O/'CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n');(O/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print({k:r[k]for k in['status','excluded_b_decimal','strict_kappa_ceiling_decimal','relative_kappa_headroom_percent_upper']})
