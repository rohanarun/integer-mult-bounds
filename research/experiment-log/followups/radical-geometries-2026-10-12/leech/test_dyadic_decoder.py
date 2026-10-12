"""Construct and verify a nonorthogonal dyadic decoder for the 276 Leech slice lines.
The Smith witness is exact. This is a scalar encoding identity, not a complex word.
"""
import gzip,json,time
from pathlib import Path
from collections import Counter
import sympy as S
from sympy.matrices.normalforms import smith_normal_decomp
ROOT=Path(__file__).resolve().parent
w=json.load(gzip.open(ROOT/'WITNESSES.json.gz'))
Y=S.Matrix(w['equiangular_lines_scaled']);c=S.Matrix(w['norm6_slice_c'])
assert c[-1]==-1 and Y*c==S.zeros(276,1)
# Drop final coordinate: a dyadically invertible chart of this integral hyperplane.
A=Y[:,:23];t0=time.monotonic();D,U,V=smith_normal_decomp(A,domain=S.ZZ)
assert D==U*A*V
inv=S.diag(*[1/D[i,i] for i in range(23)])
B=V*inv*U[:23,:]
assert B*A==S.eye(23)
B8=8*B;assert all(x.q==1 for x in B8)
# Omission controls use the unmodified encoding, not a repaired decoder.
controls=0
for i in range(B.rows):
 j=next(j for j in range(B.cols) if B[i,j]);mut=B.copy();mut[i,j]=0
 assert mut*A!=S.eye(23);controls+=1
nz=[x for x in B if x]
res={'status':'PASS_EXACT_DYADIC_NONORTHOGONAL_DECODER_NOT_SUPPLIER_ADMISSION',
 'shape_encoder':[276,23],'shape_decoder':[23,276],
 'identity':'B A = I_23; all entries of 8 B are integers',
 'smith_invariant_factors':[str(D[i,i]) for i in range(23)],
 'decoder_nonzeros':len(nz),'encoder_nonzeros':sum(x!=0 for x in A),
 'decoder_denominators':dict(Counter(str(x.q) for x in nz)),
 'decoder_max_abs_numerator':max(abs(int(x.p)) for x in nz),
 'decoder_used_line_indices':[j for j in range(276) if any(B[:,j])],
 'omitted_decoder_term_controls_rejected':controls,'seconds':time.monotonic()-t0,
 'interpretation':'The natural orthogonal projector has odd denominators, but this explicit nonorthogonal coordinate decoder avoids them. Lower coherence does not yet imply a saving.',
 'missing':['A useful local scalar endpoint word with arbitrary dirty helper restoration','Binary frame/port labeling and compatible scalar-event frame chains','Exact phases and adjoints for every emitted frame edge','Paid child histogram, helpers and geometric adapters','Whole-call global owner maps, invoice, two moment roots and outer assembly','All-size compiler and analytic-transfer contracts']}
(ROOT/'DYADIC-DECODER.json').write_text(json.dumps(res,indent=2)+'\n')
wit={'A':[[int(x) for x in row] for row in A.tolist()], 'eight_B':[[int(x) for x in row] for row in B8.tolist()]}
(ROOT/'DYADIC-DECODER-WITNESS.json.gz').write_bytes(gzip.compress(json.dumps(wit,separators=(',',':')).encode(),mtime=0))
print(json.dumps(res,indent=2))
