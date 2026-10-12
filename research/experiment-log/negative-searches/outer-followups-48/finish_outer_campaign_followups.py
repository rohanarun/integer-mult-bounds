"""Close bounded versions of campaign ideas28 and54 on pinned PR523 arithmetic."""
from pathlib import Path
from fractions import Fraction as Q
import json,importlib.util,hashlib
R=Path(__file__).resolve().parent;O=R/'findings-outer-followups';O.mkdir(exist_ok=False);P=R/'source523-review/evidence/EXACT-ASSEMBLY.json';x=json.load(open(P));b=Q(x['complex_lower']);c=Q(x['bit_lower']);engine=R/'source523-review/vendor/pr514/vendor/complex/split-centres-global/vendor/engines/outer.py'
if not engine.exists():engine=R/'source507-review/vendor/complex/split-centres-global/vendor/engines/outer.py'
spec=importlib.util.spec_from_file_location('outer',engine);Outer=importlib.util.module_from_spec(spec);spec.loader.exec_module(Outer);rows=[]
for digits in [18,20,24,30]:
 eta=beta=Q(1,10**digits);s=min(c,(1-beta)*b)-Q(1,10**24);a=Q(384599,10**10)
 for step in range(1,13):
  old=a;a=(1-s)*s+s*old;gap=min(s-a,1-a-s,1-a-s*(1-old),1-s);assert old<a<s<1-a and gap>0
  q=a*(1-2*eta);margin=(1-eta)*q/(1+q);tick=margin*10**18;k=Q((tick.numerator-1)//tick.denominator,10**18)
  bridge={'semantic':{'C0':{'base':2,'exponent':210000},'strict_literal_gap':1},'rows':{'degree_gap':Q(10**6)-Q(51*20161,25)}};out=Outer.assembly(a,b,bridge,k,eta=eta,beta=beta);assert len(out['strict_constraints'])==47 and all(v>0 for v in out['strict_constraints'].values());rejected=[]
  for label,kap,e,be in [('next_grid',k+Q(1,10**18),eta,beta),('zero_eta',k,Q(0),beta),('zero_beta',k,eta,Q(0))]:
   try:Outer.assembly(a,b,bridge,kap,eta=e,beta=be)
   except AssertionError:rejected.append(label)
   else:raise AssertionError(label)
  cut=max(-(- (36/gap**2).numerator//(36/gap**2).denominator),-(-(2*(4+6464)/gap).numerator//(2*(4+6464)/gap).denominator))
  rows.append(dict(bootstrap_steps=step,eta=str(eta),beta=str(beta),kappa=str(k),difference_from_six_step_published=str(k-Q(x['kappa'])),strict_constraints=47,controls=rejected,sufficient_log2_cutoff=str(cut)))
report=dict(status='PASS_48_EXACT_OUTER_ASSEMBLY_SCREENS',source_sha256=hashlib.sha256(P.read_bytes()).hexdigest(),engine_sha256=hashlib.sha256(engine.read_bytes()).hexdigest(),rows=rows,positive_gain_cases=sum(Q(z['difference_from_six_step_published'])>0 for z in rows),scope='Bounded exact arithmetic screen only. Does not prove all-size/compiler hypotheses, optimality over the full outer polytope, or any practical runtime crossover. Original historical campaign records remain unchanged.')
(O/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],'gains',report['positive_gain_cases'])
