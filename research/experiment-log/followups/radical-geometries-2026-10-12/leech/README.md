# Leech slices, exact decoders, and native-cap obstructions

Date: 2026-10-12. Status: executed finite geometry and decoder screens; **no new supplier or kappa**.

This continues, rather than repeats, the earlier Claude Leech census in `negative-searches/leech-lattice-screen-claude-2026-10-12`. Its Golay generator is reused in `leech_vectors.py`; the full-shell census is not presented as a new result. The new questions are whether smaller Leech slices have useful exact decoders and whether their correction supports fit the existing native binary-label contract.

## Findings

| Construction / test | Executed result | Meaning |
| --- | --- | --- |
| Norm-6 Leech slice | 552 vectors form 276 lines in dimension 23. Exact integer Gram identity `G^2 = 960 G`, diagonal 80, all off-diagonal entries ±16. | Coherence is 1/5, better than the whole Leech-shell 1/2. This is a genuinely different object from the prior census. |
| Natural orthogonal decoder | Projector `G/960` has entries ±1/60 off the diagonal. | Fails the current dyadic scalar gate contract, but does not reject other decoders. |
| Smith decoder in a 23-coordinate chart | Exact `B A = I_23`, with `8 B` integral. Smith factors: one 1, eleven 4s, eleven 8s. B has 488 nonzeros, uses 26 line coordinates, and all 23 omitted-term controls fail. | Odd-denominator difficulty can be avoided for coordinate reconstruction. |
| Smith decoder as port transfer | `A B` has only 18 diagonal entries equal to 1; 250 are zero. | It is not the required 276-port diagonal-one transfer. Its sparse correction graph alone does not fix this. |
| Coordinate-pivot diagonal-one transfer | Integer B with one nonzero per port yields diagonal-one `A B`, but all 75,900 off-diagonal entries are nonzero. | The native orthogonal-cap rule forces 276 pairwise orthogonal odd labels, hence binary ambient dimension at least 276. |
| All two-coordinate cancellation directions | 253 coordinate pairs, 1,243 directions and 226,534 dyadically legal target normalizations. Every target gets 100 nonzeros including its diagonal; denominator at most 4. | This is a concrete nonuniform diagonal-one dyadic transfer, with 27,324 directed off-diagonal corrections. Lexicographic tie choice contains a certified 100-label orthogonal clique. |
| Universal scalar-support bound | Every nonzero functional on the 23-dimensional span has at least 100 nonzero ports. All 276 two-coordinate columns attain the bound. | No decoder using this fixed encoding can improve scalar support below 100; 27,324 directed off-diagonal corrections is the exact minimum for diagonal-one transfer. |
| 32 equal-cost randomized tie assignments | Best observed clique certificate falls from 100 to 46, seed 54812; all 32 assignments have a clique of at least 46. | All tested assignments still require at least 46 binary label dimensions. This is a lower bound for the concrete witnesses, not a theorem about every Leech decoder or every tie assignment. |
| Five Golay-octad subsets | 64 lines / dimension 8; 128 / 16, 14, 12; 192 / 24. All have explicit dyadic coordinate decoders, exact diagonal frame operators and coherence 1/2. | These are valid sparse algebraic alternatives, but a single octad and disjoint copies preserve the old sign-pattern structure; no radical saving is established. Native port/frame admission remains unbuilt. |

A further exact filter obstruction: within the two-dimensional algebra `a I + b G`, a diagonal-one rank-23 matrix needs `b=1/80`, while a diagonal-one rank-253 matrix needs `a=12/11`, `b=-1/880`. Neither is dyadic. This rules out those symmetric filters, **not** arbitrary nonuniform encoders/decoders.

## Why the binary labels matter

The existing complex word cannot simply use an attractive Euclidean point set. Its native correction step must put each source under the target's orthogonal cap. If transfer entry `T[t,i]` is nonzero off the diagonal, this requires `p_i dot p_t = 0` over F2; each port also satisfies `p_i dot p_i = 1`. A clique of q such constraints gives an identity Gram submatrix, forcing ambient label dimension at least q. The witness checker validates each reported clique directly.

The current supplier uses nine binary label dimensions. Even the natural extension suggested by a 23- or 24-dimensional Euclidean geometry would use roughly 24 or 25. Our best constructed two-coordinate Leech transfer already forces at least 46. It is not thereby disproved at larger dimension, but all frame, helper and global costs must be rebuilt and priced; lower Euclidean coherence alone does not predict a better bound.

## Exact support lower bound

Take any real linear functional nonzero on the 23-dimensional span of these 276 lines. Its zero lines lie in a subspace of dimension at most 22. If there are m such lines, their normalized Gram matrix H has `trace(H)=m` and `trace(H^2)=m(m+24)/25`, because every off-diagonal inner product has absolute value 1/5. Eigenvalue Cauchy-Schwarz and `rank(H)<=22` give

`m^2 <= 22*m*(m+24)/25`.

For m>0, this reduces to `3m<=528`, hence m<=176. (For m=0 the conclusion is immediate.) Thus every such functional has at least `276-176=100` nonzero ports. A decoder column normalized to one at its target is necessarily nonzero on the span, so it has at least 99 nonzero off-diagonal entries. Our explicit two-coordinate columns attain this simultaneously for all 276 targets.

`verify_support_bound.py` rechecks the exact retained Gram identities, the rank23 configuration, the rational inequality and all276 attaining columns. It also checks an explicit equality-case zero set: its176-line raw Gram satisfies `H^2=640H`, certifying rank22 exactly. `SUPPORT-BOUND.json` retains that zero set. This bound is independent of coefficient denominators and the number of coordinates used; it applies to all real functionals for this fixed encoding.

## What remains worth testing

A jointly optimized decoder using three or more coordinates per target could create a different correction graph, but **cannot reduce scalar support below100** for this fixed 276-line encoding. The remaining objective is changing where the unavoidable nonzero corrections occur to improve the binary-label realization, followed by center-gathering hyperplane tests. Different slices, subsets or encodings require their own bounds. Optimizing Euclidean coherence or scalar sparsity alone is insufficient.

The 32 random assignments are reproducible probes, not an exhaustive search over the 6–22 equal-cost choices at every target. Center gathering, dirty-helper restoration, local paid frame profile, exact phases, owner maps, global invoice, moment roots and outer assembly have not been completed for any new geometry here. No full all-size compiler or analytic theorem follows from these finite identities.

## Reproduce and inspect

Run each script from any directory using Python with NumPy and SymPy; it writes only beside itself. Set `PYTHONDONTWRITEBYTECODE=1`. Order:

1. `test_slices.py`
2. `test_dyadic_decoder.py`
3. `test_decoder_caps.py`
4. `test_diagonal_transfer.py`
5. `test_sparse_functionals.py`
6. `test_sparse_ties.py`
7. `verify_witnesses.py`
8. `verify_support_bound.py`

`verify_witnesses.py` does not import the constructors. It independently checks the retained integer matrices, both negative controls, octad encoder/decoder identities, dyadic left inverse, diagonal-one transfers, correction-cap labels and sparse-transfer clique certificates. Its result is `VERIFIED.json`.

`test_sparse_ties-initial-error.log` preserves a tooling failure: a NumPy integer was used as a Python arbitrary-width bitset. Explicit conversion of the bit index to Python int fixed the implementation; the failed attempt produced no valid search result. The successful rerun and its output are retained separately.

## Sources and credit

- Earlier generator and census: Claude-assisted repository experiment, reused with attribution above; exact source hash retained in `SOURCES.json`.
- [Neil I. Gillespie, Equiangular lines, Incoherent sets and Quasi-symmetric designs](https://arxiv.org/abs/1809.05739), especially the Leech/276-line/E8 relationship. The identities claimed here were computed directly.
- [Cohn and Kumar, Universally optimal distribution of points on spheres](https://www.ams.org/journals/jams/2007-20-01/S0894-0347-06-00546-7/S0894-0347-06-00546-7.pdf): primary reference for the 552-point configuration. The publisher PDF fetch returned 403 in this run; it was not treated as execution evidence.
- Current source548 `audit_and_transport.py` supplies the explicit dyadic-addition and signed-binary-scale contract. Its hash and the source head are retained in `SOURCES.json`.
