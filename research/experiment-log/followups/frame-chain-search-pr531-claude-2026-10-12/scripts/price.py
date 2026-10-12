import importlib.util,sys,json
from fractions import Fraction as Q
E='/tmp/v531/base/work/pr361/code/engines/'
def load(n):
    s=importlib.util.spec_from_file_location(n,E+n+'.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=load('moment')
def price(P,m=73,W=7168):
    P={int(k):v for k,v in P.items() if v}
    return float(Q(M.certify(P,m,W,True)['lower']))
if __name__=='__main__':
    import time;t=time.time()
    P=json.load(open('/tmp/v531/hosted/HOSTED.json'))['global_profile']
    print(price(P),time.time()-t)
