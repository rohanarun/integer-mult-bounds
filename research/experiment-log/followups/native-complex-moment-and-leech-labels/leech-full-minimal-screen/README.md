# Full Leech minimal shell: actual lattice labels and punctured rank24 decoders

Status: **new finite scalar, lattice-label, correction-cap and proper-gather witnesses; no admitted supplier or new kappa**.

This branch studies the complete196,560-vector Leech minimal shell, not the earlier276-line projected equiangular configuration or its33-port subsets. The old Golay minimal-vector generator and known shell census are reused as regressions and explicitly credited. The new work constructs actual `Lambda/2Lambda` labels, diagnoses the natural full-shell decoder, and finds punctured subsets with exact finite witnesses.

## New exact results

| Test | Executed result |
| --- | --- |
| Actual scaled Leech lattice basis |24×24 integer basis, determinant2^36; after division of the Gram by8, integral even unimodular Gram of determinant1. Every retained minimal-vector coordinate is integral in this basis. |
| Quotient classes |98,280 distinct minimal-line classes in `Lambda/2Lambda`. Naive parity of the displayed24 integer coordinates gives only2 classes and is unusable. |
| Native binary labels |Explicit congruence produces98,280 distinct odd25-bit labels with `p(v) dot p(w)=1+<v,w>_Lambda mod2`. |
| Natural full-shell decoder |Rank24, dyadic, diagonal-one Gram transfer. It fails correction-cap compatibility on4,600 neighbors per port in each of three complete representative neighbor censuses. All24 natural coordinate gathers span the full25-dimensional label space. |
| Full-shell greedy puncture |116 ports, exact real rank24, all correction caps pass. Coordinate gathers remain dimension25, so this construction has no proper coordinate-center frames. |
| Even-coordinate-pool puncture, seed55025 |106 ports, exact real rank24, all correction caps pass. Every coordinate gather has rank24 in a proper hyperplane of the25-dimensional label space. |
| Even-coordinate-pool puncture, seed55026 |Another106-port/rank24 witness with the same cap/gather properties and30 fewer directed correction incidences. |

The independent witness audit passes, including recomputation of every retained label from the lattice basis, all dyadic entries and correction caps, proper-gather normals, and negative controls for an even label and incorrect diagonal. No constructor or search script is imported by that audit.

## Why the natural full-shell construction fails

Let `W` be the98,280×24 matrix containing one integer representative per antipodal minimal line, scaled so each squared norm is32. The natural transfer

`T = W W^t /32`

has rank24 and diagonal one. Its coefficients are dyadic. The complete local neighbor census around one representative of each of the three coordinate shapes gives:

| Absolute lattice inner product | Lines |
| --- | ---: |
| 4 |1, the diagonal |
| 2 |4,600 |
| 1 |47,104 |
| 0 |46,575 |

The associated25-bit labels have dot product zero for odd lattice inner products. Therefore the47,104 inner-product-one corrections fit the target cap, but the4,600 inner-product-two corrections do not. Scalar low rank alone is insufficient.

For this **specific** natural Gram decoder, extending the local counts over the symmetric full shell gives5,081,469,120 directed off-diagonal correction incidences, including452,088,000 incompatible cap incidences. These are coefficient-incidence calculations, not physical register or runtime estimates and not lower bounds on other Leech-derived decoders. No98,280² pair matrix was formed. The script checked full neighbor lists for three representative shapes and the24×24 frame operator; the prior shell symmetry/census is used as a regression, not claimed as a newly exhaustive all-pairs computation.

## The actual quotient construction

The displayed integer coordinates are scaled by `sqrt(8)`. A lattice basis is derived by exact Hermite normal form from4D24, twice the retained extended-Golay generators, and the odd vector`(-3,1,...,1)`. Its inverse denominators are only1,2,4,8. All98,280 minimal-line representatives are converted into integral lattice coordinates before reducing modulo2.

The lattice Gram modulo2 is alternating and nondegenerate. Adding one odd coordinate yields a25-dimensional nonalternating bilinear form. An explicit basis congruence turns that form into the ordinary binary dot product. Appending1 to each true quotient class and applying this congruence gives the odd port labels. The full congruence and lattice basis are retained, so this construction does not confuse `Lambda/2Lambda` with parity of ambient coordinates.

The natural scalar transfer is supported at off-diagonal absolute inner products1 and2. Puncturing searches therefore avoid exactly the inner-product-two graph. Each selected port removes forbidden surviving candidates using one vector-dot batch. Three seeded greedy maximal subsets were constructed; maximal means no extra port from that run's pool can be added, not maximum-cardinality or optimal.

## Proper gathers by puncturing the label space first

The even-coordinate half contains49,128 lines. All of their labels lie in one explicit proper hyperplane, obtained from the lattice vector8e0. Restricting the search to that half preserves24-dimensional real rank while making every natural coordinate-center gather proper in25-dimensional binary space.

The common normal is an even-weight, isotropic binary vector. Its hyperplane is degenerate for the restricted dot product; the current result proves proper linear-frame containment, **not** an orthonormal-axis completion or a phase-lowering theorem. Fresh native frame/Clifford admission remains required.

For the better106-port witness, the transfer alphabet is exactly`{-1/4,0,1/4,1}`. It has6,132 directed off-diagonal correction incidences and1,684 nonzero gather/scatter coefficients. These counts show a concrete potential workload. They do not measure a completed circuit, helper count or paid child profile.

Compared with the current112-port construction, this witness has24 scalar center dimensions instead of8 and25 binary label dimensions instead of9, with slightly fewer ports. That is a clear burden in these particular metrics, but no kappa or universal impossibility follows. The result is useful chiefly because it establishes actual finite label/decoder/gather compatibility for a full-shell-derived Leech subset, while pinpointing what still needs improvement.

## What remains missing

1. A chronological scalar/frame program and arbitrary dirty-helper cleanup for the retained106-port witness.
2. Native phase/adjoint recipes and residual adapters for its actual, partly degenerate frames.
3. Local paid-child accounting and a helper inventory; the rank24 scalar factorization does not fix these costs.
4. Global owner placement, coefficient/precision/tape invoice, moment roots, bootstrap and outer assembly.
5. Any all-size compiler and analytic-transfer obligations remain conditional even after finite admission.

Possible next changes include different decoder support on the full shell or larger cap-compatible subsets. Repeating the known full-shell kissing-number/coherence census alone would not address these obstructions.

## Files and reproduction

- [Search and exact construction](screen_full_shell.py), [result](RESULT.json), [run log](RUN.log).
- [Lattice basis and binary congruence](LATTICE-BASIS-AND-LABELS.json), [all quotient labels](ALL-QUOTIENT-LABELS.json.gz), [three punctured witnesses](PUNCTURED-WITNESSES.json.gz).
- [Independent checker](verify_punctured_witnesses.py), [verified result](VERIFIED.json), [verification log](VERIFY.log).
- [Reused generator](leech_vectors.py), [source pins](SOURCE-PINS.json).

Run both scripts with Python3.14, NumPy and SymPy, setting`PYTHONDONTWRITEBYTECODE=1`. Scripts write beside themselves. The three greedy subsets use fixed seeds; this is a bounded search, not an optimality certificate. No Daytona sandbox was needed.

## Primary sources and credit

- [Nebe–Sloane lattice catalogue: Leech](https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/Leech.html), for lattice dimension, determinant, minimum norm and shell size; a byte-pinned local copy is retained.
- [Gabriele Nebe, An even unimodular72-dimensional lattice of minimum8](https://www.math.rwth-aachen.de/~Gabriele.Nebe/papers/Ext72.pdf), section2.2, for the quadratic-space interpretation of an even unimodular lattice modulo2; a byte-pinned PDF is retained.
- [Cohn–Kumar, Optimality and uniqueness of the Leech lattice among lattices](https://arxiv.org/abs/math/0403263), as primary background rather than execution evidence.

The Golay generator and shell enumeration are reused from the earlier Claude-assisted research archive. The actual lattice-coordinate quotient,25-bit congruence, puncturing, dyadic decoder/cap tests and independent witness audit were prepared with OpenAI Codex assistance. Source hashes distinguish reused and newly executed work.
