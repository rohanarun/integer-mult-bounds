import sys,copy,json,gzip,subprocess,os
sys.path.insert(0,'/tmp/k531')
from evalsel import *
from cand import used_g
def build_word(sel,out):
    w=g.build(word,sel)
    for k in ('global_profile','live','complex_coarse_float','gain_percent_float'): w['report'].pop(k,None)
    w['report'].update(v=112,h=9,R=504,cst=64)
    open(out,'wb').write(g.dump(w));return w
if __name__=='__main__':
    which=sys.argv[1];secs=sys.argv[2]
    sel=copy.deepcopy(SEL)
    drop=[int(x) for x in which.split(',')] if which!='none' else []
    sel['kernel']=[c for c in sel['kernel'] if c['E'][0] not in drop]
    tag='ret_'+which.replace(',','_')
    build_word(sel,f'/tmp/k531/{tag}_sel.gz')
    subprocess.run([sys.executable,'-B','/tmp/w531/research/direct-delivery504-global/code/coalesce_frames.py','--word',f'/tmp/k531/{tag}_sel.gz','--out',f'/tmp/k531/{tag}_co'],check=True,capture_output=True)
    subprocess.run([sys.executable,'/tmp/sapkg/sa.py',f'/tmp/k531/{tag}_co/FULL-WORD.json.gz','5',secs,f'/tmp/k531/{tag}_sa','0.00152','0',f'/tmp/k531/{tag}_sel.gz'],check=True,capture_output=True)
    w=json.load(gzip.open(f'/tmp/k531/{tag}_sa.gz'))
    prof=g.profile(w);wc=Counter(widths_of(w))
    Pp=hostlp.full(dict(prof),wc[8],wc[9],wc[7]);b=price(Pp)
    print(tag,dict(wc),dict(sorted(prof.items())),b,'%+.4f%%'%((b/0.0015200680778324964-1)*100),flush=True)
