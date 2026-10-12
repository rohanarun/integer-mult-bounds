# Leech labels: actual compression, recentering, and a sharper boundary

Date: 2026-10-12. This new batch preserves prior frozen results and changes only the33-port Leech label representation and center factorization. **No admitted supplier or kappa is claimed.**

## Allowable changes were established first

Under the existing binary-label contract, every port is odd (`p_i dot p_i=1`), distinct ports have distinct labels, and a nonzero off-diagonal scalar transfer `T[t,i]` requires `p_i dot p_t=0` so the source lies under the target's orthogonal cap. The same ordinary binary dot product determines source and target geometry.

A quotient preserving the old entire Gram matrix cannot reduce the ambient dimension below its exact rank26. Changing to a different nondegenerate bilinear coordinate form does not evade this rank bound. Independently choosing source/target pairings would change the supplier interface and was not done.

However, inner products at pairs with zero corrections are unconstrained by this step. We changed those free Gram entries while preserving every required condition. Native phase/compiler admission for the resulting geometry remains separate.

## Constructive compression:26 dimensions to16

The forced-orthogonality graph has264edges. We found a12-coloring and a12-clique, proving its chromatic number is12. For a port of color c and within-color tag z, assign

`p = e_c direct_sum z direct_sum z`.

The duplicated tag is isotropic: it contributes zero to every pairwise dot product. Thus equal-color ports have inner product1, different-color ports have inner product0, all ports remain odd, and the tags distinguish all33ports. Two tag bits in each copy suffice, yielding16dimensions.

This is an explicit valid completion, not just a smaller clique lower bound. Its Gram rank is12 and label-span rank14. For this particular Gram matrix and distinct-port requirement,16 ambient dimensions is optimal: a color class of size at least3 needs at least2 radical dimensions; nondegeneracy then forces ambient dimension at least `12+2*2=16`.

The original six unsplit centers now all gather in proper hyperplanes. Their ranks are `14,7,4,4,12,6`, with total copied rank47, improving the previous split-center charge62.

## Recenter the scalar factorization:47 copied ranks to33

The six gather rows are dependent: the global row is exactly minus the sum of the five other rows. We enumerated all364 projective coefficient directions in `{-1,0,1}^6`, evaluated their exact source-label span ranks, and selected a minimum-cost independent basis from this catalog.

The selected change-of-basis matrix has determinant−1 and integral inverse. Applying the inverse to the scatter preserves the entire scalar transfer exactly. One gathered row becomes zero and is removed. Five centers remain, with ranks

`4,4,6,7,12`, totaling **33**.

All frames remain proper in the16-dimensional binary ambient space. Required correction caps and distinct odd ports remain unchanged. `RECENTER-WITNESS.json.gz` retains the new gather/scatter factors and exact basis change; `RECENTER-CATALOG.json.gz` retains every tested direction.

## Why further basis changes cannot rescue this transfer

The five independent gather rows have disjoint source supports of sizes `7,4,4,12,6`, partitioning all33ports. Each support is a clique of required orthogonal pairs. Any linear combination involving one of these rows contains that whole support because the supports are disjoint, so its gathered rank is at least that group's size.

For any five independent recombinations, the invertible5×5 coefficient matrix has a nonzero determinant term. This assigns a distinct group to each gathered row through a nonzero coefficient. Summing the five rank lower bounds gives at least `7+4+4+12+6=33`. Any spanning overcomplete collection drawn from the same gather-rowspace contains five independent rows and cannot cost less.

Thus **33 is a global minimum copied rank for gather-rowspace recombinations**, not merely the best among364 directions. The unchanged scalar transfer has rank5, so this includes every minimal-rank five-center factorization of it. The earlier45rank lower bound applies only to the original six individual gather supports; it is explicitly superseded when the centers are recombined.

In the existing copied-center cover,

`delta(L) = (L−1)*33 − L*C <= −33`

for every positive stage count. Consequently this successful compression and recentering still cannot produce positive saving in that cover, even if all other costs are free.

This is **not** a no-go for other Leech transfers. New scalar transfers, auxiliary gathers outside the present transfer rowspace with cancellations, or eliminating the paid center-copy interface remain outside the proof. Merely changing labels or recombining these centers is now a certified dead end for positive saving.

## Evidence and reproduction

- `COLOR-WITNESS.json.gz`:33distinct odd labels in16dimensions, same dyadic scalar transfer, coloring.
- `CENTER-CLIQUE-BOUND.json`: exact clique witnesses for the original six centers; scoped to those original supports.
- `RECENTER-RESULT.json`: new five-center result and all-coefficient lower-bound argument.
- `RECENTER-WITNESS.json.gz`: exact new factors and integral basis change.
- `VERIFIED.json`: independent saved-witness audit, including old Gram rank, new labels, correction caps, proper gathering, preserved recentered transfer, integral basis inverse, partition-clique witnesses and negative controls.

Run with NumPy/SymPy Python and `PYTHONDONTWRITEBYTECODE=1`, in order: `color_labels.py`, `check_center_clique_bound.py`, `recenter_exact.py`, `verify_and_certify.py`. Inputs are retained locally. No phase compilation, chronological dirty-helper word, full paid profile, owner maps, global invoice or kappa calculation was claimed.

The scripts,64 constructive-color trials,364 center directions, witnesses and source pins are retained. `MANIFEST.json` covers every batch file except itself. Prior batches are unchanged.
