"""Run PR #51's independent compiler (check_compiled_witness.check) on the pinned optimal matchings.
Env: REBUILD_WORK (dir holding h23/ and h25/ from rebuild_alternative_selected.py).
"""
import sys,json,struct
import os
G=os.environ.get('PR51_GRAPH_CODE','research/enlarged-positive-frame-networks/agents/graph/code'); sys.path.insert(0,G)
from check_compiled_witness import check, read_dag, read_labels
W=os.environ['REBUILD_WORK']; OUT=os.environ.get('LINKS_DIR','research/optimal-matching-51')
for h,res,uses in ((23,f'{W}/h23/rebuild-result.json',f'{OUT}/links-23.uses'),(25,f'{W}/h25/rebuild-result.json',f'{OUT}/links-25.uses')):
    row=dict(json.load(open(res))['producer'])
    raw=open(uses,'rb').read(); n,k=struct.unpack_from('<2I',raw); links=[list(struct.unpack_from('<2I',raw,8+8*i)) for i in range(k)]
    hh,v,nn,q,args,core,cover,roots,kinds,active=read_dag(row['dag_path']); ranks,frames=read_labels(row['dag_path']+'.positive',h,nn)
    deg=[0]*nn
    for x in range(1,nn):
        if active[x] and args[2*x]: deg[args[2*x]]+=1; deg[args[2*x+1]]+=1
    for r in roots: deg[r]+=1
    hist=[0]*(h+1)
    for x in range(1,nn):
        if not active[x]: continue
        r=ranks[x]
        if args[2*x]:
            hist[r]+=deg[x]-1; hist[h-r]+=1
            for y in (args[2*x],args[2*x+1]): hist[r-ranks[y]]+=1
        else: hist[1]+=deg[x]
    for j in range(q):
        r=ranks[roots[j]]
        if kinds[j]: hist[r]+=1; hist[h]+=1
        else: hist[h-1-r]+=1; hist[1]+=1
    for d,u in links:
        t=roots[u&0x7fffffff] if u>>31 else u//2; val=t if u>>31 else args[2*t+(u&1)]
        ru,rv,rt=ranks[d],ranks[val],ranks[t]; hist[h-ru]-=1; hist[rv]-=1; hist[rt-rv]-=1; hist[rt-ru]+=1
    row['histogram']=hist; row['matched']=k
    out=check({"producer":row,"selected_links":{"links":links}},False)
    print(h,'PASS' if out else 'FAIL',{x:out[x] for x in out if x in ('status','roles','complete_dirty_basis')})
