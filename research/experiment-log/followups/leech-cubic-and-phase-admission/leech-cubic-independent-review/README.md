# Independent review of the compressed full-shell Leech cubic decoder

Status: exact finite scalar/label/gather review passes. This is not a chronological dirty-register word, compiler admission, paid-cost certificate, global kappa, or practical speedup.

Run from the parent SSD directory with `PYTHONDONTWRITEBYTECODE=1 ./verify-sympy314/bin/python -B leech-cubic-independent-review/verify.py`. The checker reads the source files named and SHA256-pinned in `SOURCE-HASHES.json`; it never imports the parent factor-construction implementation. `RESULT.json` and `RUN.log` retain the result. The shared vector enumeration is reused as input, not advertised as a new Leech census.

## Exact factorization

For scaled integer vectors v,w of norm32, let s=v dot w. The transfer is T=s(s²−256)/24576. Its diagonal is one. The original2624-center integer feature construction has numerator (s³−256s)/3 and common denominator8192. Its divided-cube feature is D_i(w)=(w_i³−w_i)/3, integral for every integer w_i. The linear target (v_i³−256v_i)/3 is also integral since256≡1 mod3.

Set j=i+1 modulo24. The sphere identity

    w_i w_j² =31w_i−3D_i(w)−Σ_{k≠i,j}w_i w_k²

eliminates24 ordered-pair features with coefficient one. Therefore it preserves dyadic coefficients and leaves2600 centers. The new target coefficients are v_i³−3v_i v_j² for D_i, (v_i³−256v_i)/3+31v_i v_j² for w_i, and v_i(v_k²−v_j²) for retained w_i w_k²; triple coefficients remain2v_i v_j v_k.

Our independently written reconstruction agrees with all source and target entries in the128-vector retained sample and all16384 products. We additionally checked100 integer off-shell pairs against the stronger identity

    compressed numerator = (s³−256s)/3
      −(||w||²−32) Σ_i v_i v_{i+1}² w_i.

This shows precisely why the norm32 condition is needed; the compressed factorization is not claimed on arbitrary source vectors. The multinomial expansion and displayed elimination identity establish the general algebra, rather than treating the finite sample as an exhaustive factor proof.

## Universal cap compatibility without a quadratic pair census

The checker reconstructs all98280 labels from integer lattice coordinates in the retained24-row basis B and verifies B B^T/8 is integral. It checks the entire25×25 embedding Gram identity. Thus for every pair, with t=v dot w/8,

    p(v) dot p(w) = 1+t modulo2.

All retained vectors have norm32 and distinct canonical antipodal representatives. Cauchy gives |t|≤4; equality would require equal or opposite vectors, excluded off the diagonal. Hence every off-diagonal t is an integer in[-3,3]. For even t∈{-2,0,2}, t(t²−4)/48=0. For odd t, labels are orthogonal. This proves the correction-cap implication for all pairs, including hypothetical t=±3; it does not rely on sampled rows establishing a complete inner-product census. Diagonal t=4 gives one.

## Gather ranks and zero extension

Each of2600 supplied gather witnesses contains25 binary-independent labels on ports where that exact source feature is nonzero. We checked65000 such witness memberships. All labels lie in F2^25, so the gather rank is exactly25. Extending labels by a zero26th coordinate preserves oddness, distinctness and every pairing. Every gather then spans the proper nondegenerate hyperplane U=F2^25×{0}; its orthogonal complement has odd unit normal e25. No extra ambient bit was counted as free paid work.

The generic Clifford implementation inspected has dimension-parameterized `cgate(n,q)` and `canonical_frame(n,U)` functions and no odd-dimension or full-live-port-span precondition. This source inspection supports the elementary zero-extension screen; it is not a phase replay or proof that the entire supplier contract admits the construction. The current global wrapper explicitly asserts h=9,v=112, and its invoice asserts m=73. Those programs do not certify h=26 merely because the finite embedding passes. A literal26-bit `zero_state` allocates2^26 states; no such unbounded replay was launched in this lane.

## Optimistic arithmetic and remaining work

Exact copied rank C=2600×25=65000 and N=98280 give

    δ(L)=(L−1)N−LC =33280L−98280.

At L=3, this optimistic deficit is1560. The uncompressed2624-center construction has C=65600, δ(3)=−240 and first positive odd L=5. This compression therefore changes the necessary copied-rank screen meaningfully. It does not charge a real word's gathering, scatter, correction, phase, helper lifetime, or hosting costs.

Remaining: chronological scalar word with restored dirty helpers; legal frame transitions and exact native phases; complete paid-rank profile; all-size hosting/admission and final conditional optimization. The106-port rowspace no-go applies to its old linear Gram transfer and does not reject this cubic transfer.

Negative controls: changing a target coefficient breaks the product identity; deleting a gather-basis element lowers rank; changing the affine embedding breaks its Gram identity. One initial read-only `rg` used an incorrect nested Clifford path and returned file-not-found; the corrected inspected source is `source548-review/complex-global/vendor531/vendor/clifford/clifford_exact.py`. No mathematical experiment was discarded after that path typo.
