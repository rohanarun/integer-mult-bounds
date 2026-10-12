"""Exact arithmetic screen; zero complex contamination term requires source-scope review."""
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal,localcontext
import importlib.util,json,hashlib,time
R=Path(__file__).resolve().parent;ROOT=R.parent;start=time.monotonic()
def load(n):
 p=ROOT/'source552-review/engines'/(n+'.py');s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M,B,A=[load(n)for n in ['moment','base_two_moment','outer']]
parent=json.loads((ROOT/'pr552-independent314/RESULT.json').read_text());P={int(r):n for r,n in parent['complex_global_profile'].items()};m=73;W=7168;c=Q(parent['bit_lower']);oldb=Q(parent['complex_lower']);oldk=Q(parent['kappa']);assert m*W-sum(r*n for r,n in P.items())==2560
baseline=M.certify(P,m,W,True);assert Q(baseline['lower'])==oldb
cert=M.certify(P,m,W,False);b=Q(cert['lower']);assert b>oldb
checks=[]
for endpoint,ok in [(b,True),(b+Q(1,10**24),False)]:
 l,h=M.moment(P,m,W,endpoint,False);u,v=B.moment(m,W,list(P.items()),endpoint);assert(h<1 and v<1)if ok else(l>1 and u>1);checks.append(dict(endpoint=str(endpoint),accept=ok,mercator=[str(l-1),str(h-1)],base_two=[str(u-1),str(v-1)]))
assert M.moment(P,m,W,b,True)[0]>1
eta=beta=Q(1,10**18);grid=Q(1,10**18);bridge={'semantic':{'C0':{'base':2,'exponent':210000},'strict_literal_gap':1},'rows':{'degree_gap':Q(10**6)-Q(51*20161,25)}}
def assemble(bb):
 s=min(c,(1-beta)*bb)-Q(1,10**24);assert 0<s<c and s<(1-beta)*bb;chain=[Q(384599,10**10)];cuts=[]
 for _ in range(6):
  old=chain[-1];a=(1-s)*s+s*old;gap=min(s-a,1-a-s,1-a-s*(1-old),1-s);assert old<a<s<1-a and gap>0;ceil=lambda x:-(-x.numerator//x.denominator);cut=max(ceil(36/gap**2),ceil(2*(4+512)/gap));assert cut*gap**2>=36 and cut*gap>=2*(4+512);cuts.append(dict(exponent=str(a),gap=str(gap),cutoff_log2=str(cut)));chain.append(a)
 q=chain[-1]*(1-2*eta);margin=(1-eta)*q/(1+q);ticks=margin/grid;k=grid*((ticks.numerator-1)//ticks.denominator);a=A.assembly(chain[-1],bb,bridge,k,eta=eta,beta=beta);assert len(a['strict_constraints'])==47 and all(v>0 for v in a['strict_constraints'].values());return k,chain,cuts,a
assert assemble(oldb)[0]==oldk
k,chain,cuts,a=assemble(b);controls=['new_endpoint_rejected_by_old_charge']
for name,kk,ee,bbeta in [('next_grid',k+grid,eta,beta),('zero_eta',k,Q(0),beta),('zero_beta',k,eta,Q(0)),('unit_beta',k,eta,Q(1))]:
 try:A.assembly(chain[-1],b,bridge,kk,eta=ee,beta=bbeta)
 except AssertionError:controls.append(name)
 else:raise AssertionError(name)
def dec(v):
 with localcontext()as ctx:ctx.prec=70;return str(Decimal(v.numerator)/Decimal(v.denominator))
r=dict(status='EXACT_ARITHMETIC_PASS_NATIVE_COMPLEX_SCOPE_UNDER_REVIEW',baseline_kappa=str(oldk),baseline_kappa_decimal=dec(oldk),candidate_kappa=str(k),candidate_kappa_decimal=dec(k),old_complex_lower=str(oldb),complex_lower=str(b),complex_decimal=dec(b),absolute_gain=str(k-oldk),relative_gain_percent=dec(100*(k/oldk-1)),profile=P,live=W,m=m,rank_deficit=2560,bit_lower=str(c),moments=checks,outer={n:str(v)for n,v in a['strict_constraints'].items()},bootstrap=cuts,controls=controls,seconds=time.monotonic()-start,scope='Numerical zero-contamination moment only. Do not claim admitted result until actual complex compiler/all-size interface is checked to have no GL residue selector. Existing profiles, invoices and physical operators unchanged.')
(R/'NATIVE-MOMENT-SCREEN.json').write_text(json.dumps(r,indent=2)+'\n');print({key:r[key]for key in ['status','candidate_kappa_decimal','complex_decimal','relative_gain_percent','seconds']})
