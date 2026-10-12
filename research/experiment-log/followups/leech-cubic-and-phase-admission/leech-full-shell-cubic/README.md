# Full Leech shell: a cubic dyadic decoder

Status: **new exact finite scalar and label construction; no admitted supplier or kappa**. This changes the scalar decoder on all 98,280 antipodal lines, rather than puncturing the natural rank-24 Gram decoder down to 106 ports.

## Why change the decoder?

For lattice inner product t, the natural transfer t/4 is nonzero at t=2, but those port labels have the wrong binary pairing for a correction. Use instead

    f(t) = t(t^2 - 4)/48.

It has f(4)=1, vanishes at t=0 and t=±2, and equals ∓1/16 at t=±1. The earlier sampled full-shell row censuses have only these off-diagonal classes. The construction deliberately cancels the incompatible classes instead of deleting their ports.

In the retained integer coordinates, s=8t and every vector has squared norm 32:

    T(v,w) = s(s^2 - 256)/24576.

The apparent factor 3 in the denominator does not require thirds in the implementation. An explicit factorization uses only integer gathers and a common scatter denominator 8192.

## A dyadic factorization with 2,600 centers

Start with 2,624 source features:

- 24 divided cubes D_i=(w_i^3-w_i)/3, always integers;
- 24 linear coordinates w_i;
- 552 square-linear monomials w_i^2 w_j for i != j;
- 2,024 distinct-coordinate cubic monomials w_i w_j w_k.

Their target numerators are respectively v_i^3, (v_i^3-256v_i)/3, v_i^2 v_j, and 2v_i v_j v_k. Both divided expressions are integral for every integer coordinate. The common denominator is 8192.

Because sum_k w_k^2=32, for any j != i,

    w_i*w_j^2 = 31*w_i - 3*D_i - sum_{k != i,j} w_i*w_k^2.

For each i choose j=(i+1) mod 24. These 24 eliminated features are distinct, and their replacements contain no other eliminated feature. All substitutions are integral, leaving exactly **2,600 dyadic centers**. No division by 3 or 31 is added to a scalar operation.

[Exact polynomial certificate](POLYNOMIAL-CERTIFICATE.json) checks all 3,176 nonzero bivariate monomial coefficients in the resulting identity. The residual before imposing the sphere equation is explicitly (32-||w||^2) times a polynomial, so it vanishes on every retained source vector. [Compression](COMPRESSED-RESULT.json) also checks all 2,358,720 source norm identities and 16,384 factor pairs.

## All-pairs correction compatibility

This proof does not require enumerating a 98,280-square matrix or assuming a sampled neighbor census holds everywhere.

All vectors have norm 32 and integral coordinates in the retained lattice basis, whose Gram divided by 8 is integral. Hence t=(v dot w)/8 is an integer. Cauchy gives |t|<=4; distinct canonical antipodal representatives exclude equality off the diagonal. The retained binary congruence gives p(v) dot p(w)=1+t mod 2 for every pair. At every off-diagonal even t, f(t)=0. At odd t, the binary pairing is zero. Thus every nonzero correction has the required target-cap relation. Values at t=±3, even if present, would also be dyadic and compatible.

The independent witness audit reconstructs all 98,280 labels from actual lattice coordinates and checks the full bilinear congruence. It also independently verifies all compressed gather-rank bases and sampled factor matrices. A separate bounded regression checked **6,289,920 pairs in 64 full rows**, eliminating all 294,400 incompatible natural-Gram edges encountered. Sampled row counts are not advertised as an exhaustive matrix census.

## Gathering frames and the limited cost screen

Append one zero coordinate to the original 25-bit labels. In dimension 26, all labels lie in the same proper, nondegenerate 25-dimensional hyperplane with odd normal e25. Distinctness, oddness and all pairings are unchanged. Each of the 2,600 source feature supports spans exactly that hyperplane; retained independent 25-element bases prove the ranks.

The sum of center-gather ranks is therefore **65,000**, below the **98,280 ports**. The old optimistic center-copy screen becomes

    delta(L) = (L-1)*98280 - L*65000 = 33280*L - 98280.

It is positive at L=3, where it equals 1,560. This is only a necessary optimistic screen. It does not pay for all factory copies, side-correction helpers, chronological transitions, controller roles, precision or tape costs. It must not be converted into kappa. The companion word-cost review examines those missing costs.

Generic Clifford geometry can accept dimension 26, but the currently published global supplier wrappers are specialized to their original geometry. This package has not generalized or admitted those wrappers. Even successful finite admission would retain the inherited all-size and analytic assumptions.

## Evidence and reproduction

Run with Python 3.14, NumPy and SymPy, assertions enabled, and bytecode disabled:

    python -B screen.py
    python -B compress_sphere.py
    python -B verify.py
    python -B verify_polynomial.py

Scripts write beside themselves. No source search script is imported by the independent verifier. The shared minimal-vector generator is retained and credited; no exponentially large Clifford matrix or all-pairs shell matrix is formed. Inputs are included under `inputs/`.

[Result](RESULT.json), [compressed result](COMPRESSED-RESULT.json), [independent audit](VERIFIED.json), [row checks](ROW-CHECKS.json), source files, exact factor samples, gather bases and all logs are retained. Negative controls reject a changed factor coefficient, an even port label and the original incompatible Gram correction. Subsequent phase and chronological word-cost reviews have separate packages and must be read before interpreting this as a usable construction.

Credit: the retained Golay/minimal-vector generator originates in the earlier Claude-assisted archive. The actual lattice quotient and binary congruence are reused from the prior full-shell experiment. The cubic decoder, integral center elimination and new audits were prepared for Rohan Arun with OpenAI Codex assistance; source pins preserve the inherited provenance. This is a finite research candidate, not a priority claim for polynomial kernels.
