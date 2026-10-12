from evalsel import *
from cand import used_g,used_k
import json
b0,_=evaluate(SEL)
free=[h for h in range(R) if h not in used_g and h not in used_k]
res=[]
for h in free:
    s=copy.deepcopy(SEL);s['gauge'][str(h)]=list(first[h])
    b,info=evaluate(s)
    res.append((h,None if b is None else (b-b0)/b0*100,info if b is None else ''))
from collections import Counter
print(Counter(r[2] for r in res if r[1] is None))
ok=sorted([r for r in res if r[1] is not None],key=lambda r:-r[1])
print(len(ok),ok[:10])
json.dump(res,open('tryg.json','w'))
