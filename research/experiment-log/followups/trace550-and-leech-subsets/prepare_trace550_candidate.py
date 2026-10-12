from pathlib import Path
import json,gzip,sys,copy,hashlib
from fractions import Fraction as Q
from collections import Counter
R=Path(__file__).resolve().parent;O=R/'trace550-retimed-candidate';O.mkdir(exist_ok=False)
sys.path.insert(0,str(R/'source550-review/local/vendor/gk'));import gk_word as g,gk_common as c;g.V=c.V=112;g.DATA=c.DATA=7168
sys.path.insert(0,str(R/'source550-review/engines'));import moment,base_two_moment,outer
w=json.load(gzip.open(R/'trace550-frame-anneals/seed55001.gz'));orig=json.load(gzip.open(R/'pr550-independent314/local/candidate/FULL-WORD.json.gz'))
changes=[]
for sec in ('A','B'):
 assert len(w[sec])==len(orig[sec])
 for ix,(a,b)in enumerate(zip(orig[sec],w[sec])):
  assert a[:-1]==b[:-1]
  if a[-1]!=b[-1]:changes.append(dict(section=sec,index=ix,old=a[-1],new=b[-1]))
for k in ('ports','cut','precondition','centers','center_frames','scatter','start_extra','target_levels'):assert w[k]==orig[k]
w['cleanup']=[g.inverse(e,g.FULL)for e in reversed(w['A']+w['B'])if not 112<=e[1]<224]
H=g.profile(w);w['report']['local_profile']=dict(H);data=g.dump(w);(O/'WORD.json.gz').write_bytes(data)
p=json.loads((R/'pr550-independent314/local/PRICE.json').read_text());old=g.profile(orig);globalH=Counter({int(r):n for r,n in p['global_profile'].items()});globalH.subtract({r:72*n for r,n in old.items()});globalH.update({r:72*n for r,n in H.items()});assert min(globalH.values())>=0;globalH=Counter({r:n for r,n in globalH.items()if n})
cert=moment.certify(globalH,73,7168,True);b=Q(cert['lower']);checks=[]
for q,accept in [(b,True),(b+Q(1,10**24),False)]:
 lo,hi=base_two_moment.moment(73,7168,list(globalH.items()),q);fl,fh=base_two_moment.moment(73,7168,[(1,32*73**2*sum(globalH.values()))],q);lo+=fl/10**16;hi+=fh/10**16;assert hi<1 if accept else lo>1;checks.append(dict(point=str(q),accept=accept,lower_minus_one=str(lo-1),upper_minus_one=str(hi-1)))
bit=json.loads((R/'source550-review/inputs/PR543-EXPECTED.json').read_text())['nine'];c=Q(bit['bit_lower']);eta=beta=Q(1,10**18);s=min(c,(1-beta)*b)-Q(1,10**24);a=Q(384599,10**10)
for _ in range(6):a=(1-s)*s+s*a
q=a*(1-2*eta);margin=(1-eta)*q/(1+q);ticks=margin*10**18;k=Q((ticks.numerator-1)//ticks.denominator,10**18)
bridge={'semantic':{'C0':{'base':2,'exponent':210000},'strict_literal_gap':1},'rows':{'degree_gap':Q(10**6)-Q(51*20161,25)}};o=outer.assembly(a,b,bridge,k,eta=eta,beta=beta);assert all(v>0 for v in o['strict_constraints'].values())
price=dict(status='PASS_TWO_ENGINE_PROFILE_NOMINATION_NOT_PHYSICAL_ADMISSION',global_profile=dict(sorted(globalH.items())),local_profile=dict(sorted(H.items())),complex_lower=str(b),b_decimal=cert['lower'],kappa=str(k),kappa_decimal=moment.decimal(k),moment=cert,independent_base_two=checks,outer={key:str(v)for key,v in o['strict_constraints'].items()},scope='Candidate unchanged scalar instructions and entrances with changed monotone frames. Exact frozen-owner-profile price only; independent phase, owner and fresh invoice admission pending.')
(O/'PRICE.json').write_text(json.dumps(price,indent=2)+'\n');plan=json.loads((R/'source550-review/physical/data/SAT534-PLAN.json').read_text());plan['profile']=price['global_profile'];(O/'PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
(O/'CONSTRUCTION.json').write_text(json.dumps(dict(status='PASS_SAME_SCALAR_WORD_AND_EXACT_FRAME_PROFILE',source_pr=550,source_head='c7337040822978f1611ce9d9d44e7bb96d887e23',word_sha256=hashlib.sha256(data).hexdigest(),changes=changes,local_profile_before=dict(old),local_profile_after=dict(H),scope='Full physical admission pending'),indent=2)+'\n');print(price['b_decimal'],price['kappa_decimal'],'changes',len(changes))
