# Leech106: degenerate frames do admit exact native phases

**Result: the isotropic-normal concern is resolved.** The current pinned binary Clifford interface accepts arbitrary independent linear frames, including degenerate subspaces. The original Leech106 gather and the alternative label lane's repaired23-dimensional witness both pass exact, global-phase-sensitive finite tests. No new kappa is claimed.

## What the actual interface requires

The constructor `canonical_frame(n,U)` in the pinned compiler completes a basis of U to an arbitrary invertible binary matrix G. It conjugates a coordinate Fourier block by a binary address permutation and quadratic phase. G need not be orthogonal, and U need not have a nondegenerate restricted dot product.

The retained [general-frame argument](general-clifford-frames.tex) makes this explicit. In binary symplectic coordinates, the relevant preimage frame is

`L_U = {(u,u+v): u in U, v in U-perp}`.

It is Lagrangian even when U is degenerate. Actual tests independently construct this subspace, compare it with the inverse Clifford tableau's Z-space preimage, check its rank, and verify the transition Fourier ranks. This is a statement about general Clifford frames, not a claim that a degenerate hyperplane has an orthonormal basis.

Therefore no label repair is necessary merely because the original gather normal is isotropic. Lower-dimensional labels can still improve rank costs; the separate repaired witness is tested for that reason.

## Executed phase tests

| Witness | Binary dimension | Gather dimensions | Phase-bearing recipes checked |
| --- | ---: | --- | ---: |
| Original seed55026 |25 | Common rank24 frame, isotropic normal |322 |
| Repaired seed55025 |23 |24 coordinate gathers, ranks16–20, sum453 |1,126 |

The original322 recipes comprise:

- 212 rank-zero source/target endpoint adapters;
- 106 rank23 source-line-to-gather transitions;
- two rank24 gather/return transitions;
- two rank1 gather/full-frame transitions.

The shared rank1 residual was also decoded into explicit left/right monomial wrappers. Applying their inverses produces exactly one coordinate Fourier child, including its scalar global phase. Negative controls reject an incorrect global phase, an extra translation, and the wrong residual width. The global-phase control has the *same tableau*, so tableau equality alone would miss it.

The repaired1,126 recipes comprise212 endpoints,842 actual nonzero source-to-coordinate-gather incidences, and72 gather/return/tail transitions. Gather ranks are16 once,17 twice,18 three times,19 eleven times, and20 seven times. These ranks agree with the frozen alternative-label witness.

[An independent serialized-recipe audit](SERIALIZED-AUDIT.json) decodes every saved monomial recipe without calling the recipe constructor or `lower_child`, reconstructs the intended operator from the frozen source labels/frames, and compares both tableaus and a nonzero exact amplitude. All 1,448 original/repaired saved recipes pass; the separate cubic audit adds 103.

## Full-shell cubic decoder: the 26-dimensional interface also passes

The root lane's retained [scalar result](CUBIC26-SCALAR-SOURCE.json) describes a 2,600-center dyadic cubic factorization on 98,280 ports. Its copied-rank screen has C = 65,000 and optimistic deficit `33280*L - 98280`; this is a necessary screen, not a paid circuit. This phase lane does not independently reconstruct that scalar factorization.

For the native frame interface, zero-embed each original 25-bit label into 26 dimensions and use the common gather `U = F2^25 × {0}`. All 98,280 labels were individually checked to remain distinct, odd and contained in U. Zero embedding preserves every binary pairing by the identity `(p,0)·(q,0) = p·q`, so it preserves the old cap conditions without enumerating all quadratic pairs.

The normal of U is the last coordinate vector, of norm one; U is nondegenerate and has dimension 25. For every source line, the general-frame distance identity therefore gives source-to-gather rank 24, zero-to-gather rank 25 and gather-to-full rank 1. This is an all-label containment census plus a structural family argument, not an enumeration of 98,280 phase recipes.

The [bounded exact phase test](CUBIC26-RESULT.json) selects 33 distinct deterministic port indices spanning the label list and including minimum/maximum label-weight cases. It verifies 67 frame preimages and constructs 103 phase-bearing recipes: 66 source/target endpoint adapters, 33 rank-24 source transitions, two rank-25 gather transitions and two rank-1 tails. [Independent decoding](CUBIC26-SERIALIZED-AUDIT.json) passes for all 103, including scalar global phases. No exponential Hilbert-space vector is allocated.

The pinned `cgate`, `fourier`, and `canonical_frame` functions have no odd-ambient-dimension precondition. The actual 26-dimensional endpoint recipes pass. This settles the finite Clifford interface question; it does not settle any separate parity, covering, coefficient or precision requirement imposed by a future global supplier assembly.

An initial harness assertion compared a tuple against a list although both represented the same nullspace. The original script and [error note](CUBIC26-INITIAL-TOOL-ERROR.txt) are retained; correcting the container comparison changed no mathematical construction. Negative controls reject a vector outside U and an incorrect global phase with unchanged tableau.

## Avoiding exponential Hilbert-space vectors

The original compiler's literal phase interpreter allocates2^n amplitudes, which is unsuitable for these dimensions. This batch preserves the original tableau compiler and adds an exact phase evaluator based on quadratic path sums:

1. Each C gate introduces one binary path variable and a Gaussian-dyadic coefficient.
2. Address permutations/translations update affine binary output expressions.
3. Diagonal phases accumulate a Z4 quadratic polynomial.
4. Output constraints are solved by binary elimination.
5. The remaining quadratic Gauss sum is evaluated by exact Gaussian-integer elimination.

All operations are exact integers, binary bitsets, Z4 phases and powers-of-two denominators. The evaluator stores no 2^25, 2^23 or 2^26 state vector. Equality of exact Clifford tableaus plus one nonzero amplitude fixes the otherwise missing global scalar phase.

Before using this backend at larger dimensions, tests compared180 Gauss sums with complete enumeration,744 amplitudes with the pinned literal state interpreter, and60 lowered recipes with the pinned compiler's literal implementation. All agree. This is a new local phase backend with explicit regression evidence; it is not a Lean formalization.

## Scope: what passed and what remains

Passed:

- actual general-frame preimages, including the degenerate original gather;
- source/target endpoint compatibility;
- the listed nested gather transitions and cleanup tails;
- exact serialized monomial/Fourier recipes, including global phase;
- the original rank1 residual-wrapper identity and negative controls.

Not built or established:

- a complete chronological scalar program with arbitrary dirty-helper restoration;
- phase coverage for all transitions of that unbuilt program;
- helper inventory, whole-call physical owners, paid-child histogram, coefficient/precision/tape invoice;
- moment roots, bootstrap/outer assembly, or a new kappa;
- any unconditional all-size multiplication theorem.

In particular, summing these standalone edge ranks is not a valid supplier invoice: a real schedule must account for shared register chains, scalar ordering and cleanup.

## Files and reproduction

- [Pinned compiler](clifford_exact.py), [source pins](SOURCE-PINS.json), [general-frame derivation](general-clifford-frames.tex).
- [Exact symbolic phase backend](symbolic_phase.py), [literal crosscheck code](test_symbolic_phase.py), [crosscheck results](SYMBOLIC-CROSSCHECK.json), [log](SYMBOLIC-CROSSCHECK.log).
- [Original witness](PUNCTURED-WITNESSES.json.gz), [original tests](admit_original_frames.py), [result](ORIGINAL25-RESULT.json), [phase recipes](ORIGINAL25-PHASE-RECIPES.json.gz), [log](ORIGINAL25.log).
- [Frozen repaired witness](REPAIRED23-WITNESS.json.gz), [repaired tests](admit_repaired_frames.py), [result](REPAIRED23-RESULT.json), [phase recipes](REPAIRED23-PHASE-RECIPES.json.gz), [log](REPAIRED23.log).
- [Independent recipe decoder](audit_serialized_recipes.py), [audit result](SERIALIZED-AUDIT.json), [audit log](SERIALIZED-AUDIT.log).

Run the crosscheck, original test, repaired test and serialized audit in that order using Python3.14 with `PYTHONDONTWRITEBYTECODE=1`. All scripts write beside themselves; mathematical execution needs only the Python standard library. The retained repaired witness is frozen and independent of later changes in the alternative-label lane. No Daytona sandbox was used.

Cubic files: [test script](admit_cubic26_frames.py), [original harness](admit_cubic26_frames.initial.py), [frozen labels](CUBIC26-ALL-QUOTIENT-LABELS.json.gz), [phase recipes](CUBIC26-PHASE-RECIPES.json.gz), [run log](CUBIC26.log), [independent audit code](audit_cubic26_recipes.py), [audit log](CUBIC26-SERIALIZED-AUDIT.log). Run the cubic test and independent audit after the shared phase backend crosscheck. [MANIFEST.json](MANIFEST.json) hashes every retained file except itself.

## Provenance

The compiler is pinned to the PR548 vendor copy; exact SHA256 is retained. It is the inherited Gaussian-dyadic compiler credited to icekylinx with Codex assistance. The general-subspace construction/exposition retains its credit to icekylinx with GPT-6 Astra assistance and subsequent Codex integration. The Leech source vectors and scalar witnesses retain their prior provenance, while the repaired labels come from the separate `leech106-label-repair` lane. This batch's quadratic phase evaluator, tests and certificates were prepared with OpenAI Codex assistance. No upstream compiler or other lane's files were changed.
