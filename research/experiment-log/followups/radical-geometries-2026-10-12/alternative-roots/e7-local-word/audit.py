"""Independent stdlib replay of generated scalar E7 word and monotone frames."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import gzip,json,time,hashlib
O=Path(__file__).resolve().parent;raw=(O/'WORD.json.gz').read_bytes();w=json.loads(gzip.decompress(raw));v=w['v'];h=w['h'];R=w['R'];n=2*v+R;begin=time.monotonic()
def apply(e,rows):
 _,t,r,a,b,_=e;q=Q(a,b)
 for j,x in list(rows[r].items()):
  z=rows[t].get(j,Q(0))+q*x
  if z:rows[t][j]=z
  else:rows[t].pop(j,None)
def inverse(e):
 z=list(e);z[3]=-z[3];return z
def dual(e):
 z=inverse(e);z[1],z[2]=z[2],z[1];return z
def ident():return [{i:Q(1)} for i in range(n)]
main=w['A']+w['cut']+w['B'];rows=ident()
for e in main:apply(e,rows)
# clean source response exactly identity, separately before any compensator exists
for t in range(v):assert {j:q for j,q in rows[v+t].items() if j<v}=={t:Q(1)}
comp=[['add',v+t,j,-q.numerator,q.denominator,[]] for t in range(v) for j,q in sorted(rows[v+t].items()) if j>=2*v]
cleanup=[inverse(e) for e in reversed(w['A'])]
for e in cleanup:e[-1]=[1<<i for i in range(h-1,-1,-1)]
program=comp+main+cleanup
for backward in (False,True):
 actual=ident()
 for e in program:apply(dual(e) if backward else e,actual)
 expected=ident()
 for t in range(v):expected[t if backward else v+t][v+t if backward else t]=Q(-1 if backward else 1)
 assert actual==expected,('full arbitrary-dirt identity',backward)
# Independent binary elimination gives complete spans; compare support subsets, no constructor import.
def span(F):
 out={0}
 for p in F:out|={x^p for x in out}
 return out
full=set(range(1<<h));current=[{0,p} for p in w['ports']]+[{0} for _ in range(v+R)];paid=Counter()
def move(r,F):
 new=span(F);assert current[r]<=new
 a=len(current[r]).bit_length()-1;b=len(new).bit_length()-1
 if a!=b:paid[b-a]+=1;current[r]=new
for e in comp:assert current[e[1]]==current[e[2]]=={0}
for e in w['A']:move(e[1],e[-1]);move(e[2],e[-1])
for r,F in zip(w['centers'],w['center_frames']):assert current[r]==span(F);paid[len(current[r]).bit_length()-1]+=1
assert all(current[v+t]=={0} for t in range(v))
for e in w['B']:move(e[1],e[-1]);move(e[2],e[-1]);assert all((w['ports'][e[1]-v]&x).bit_count()%2==0 for x in current[e[1]])
for r in range(n):
 if v<=r<2*v:
  p=w['ports'][r-v];F=[x for x in range(1<<h) if (p&x).bit_count()%2==0]
 else:F=[1<<i for i in range(h)]
 move(r,F)
assert dict(sorted(paid.items()))=={int(k):z for k,z in w['profile'].items()}
# Explicit arbitrary dirt negative: omit first compensator and check a one-column input.
assert comp
badrows=ident()
for e in comp[1:]+main+cleanup:apply(e,badrows)
assert badrows!=expected # expected here backward; explicitly check forward too
want=ident()
for t in range(v):want[v+t][t]=Q(1)
assert badrows!=want
# Frame mutation: a source initially at p cannot participate at zero frame.
assert any(e[2]<v for e in w['A']);first=next(e for e in w['A'] if e[2]<v);assert not {0,w['ports'][first[2]]}<={0}
w['precondition']=comp;w['cleanup']=cleanup;out=gzip.compress(json.dumps(w,sort_keys=True,separators=(',',':')).encode(),mtime=0);(O/'COMPLETE-WORD.json.gz').write_bytes(out)
r={'status':'PASS_EXACT_SCALAR_AND_MONOTONE_FRAMES_ONLY','R':R,'v':v,'h':h,'centers':len(w['centers']),'center_copy_rank_total':sum(map(len,w['center_frames'])),'complete_scalar_operations':len(program),'factory_and_gather_operations':len(w['A']),'center_scatter_operations':len(w['cut']),'side_correction_operations':len(w['B']),'arbitrary_dirt_compensators':len(comp),'cleanup_operations':len(cleanup),'clean_source_columns':v,'arbitrary_columns_each_orientation':n,'orientations':2,'local_profile':dict(sorted(paid.items())),'local_rank_mass':sum(k*z for k,z in paid.items()),'negative_controls_rejected':2,'seconds':time.monotonic()-begin,'raw_word_sha256':hashlib.sha256(raw).hexdigest(),'complete_word_sha256':hashlib.sha256(out).hexdigest(),'remaining':['native phase/center-copy realization','changed-port all-size supplier interface','global controller and physical owners','finite invoice','two exact moment engines and outer assembly'],'scope':'No smaller-R improvement or kappa; explicit local scalar word only.'}
(O/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
