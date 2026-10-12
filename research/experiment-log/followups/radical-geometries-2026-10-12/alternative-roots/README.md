# Alternative root geometries: exact clean decoder and cap screens

New finite experiment for Rohan Arun, with OpenAI Codex assistance. Source anchor: PR548 `66dbc2bffc1bfa8d50b3f9a2ac7ccba8fd9f6f36`; the actual current112 raw word is SHA256-bound in `RESULT.json`. No supplier or kappa is claimed.

The old Leech census only counted lines and inner products. These tests instead check two actual local-word conditions: each nonzero side correction must have its source label inside the target's perpendicular cap, and each retained center must collect at a proper binary frame. The current raw word and its gk frame accountant were read first, along with the archived Leech screen and latest PR548 negative searches.

## Exact construction

`screen.py` constructs A4/A6/A8, D4/D5/D6/D8, E6/E7/E8 root lines with integral coordinates scaled by2. Every root has squared norm8. E6/E7 are spans of the first six/seven specified E8 simple roots. It constructs **injective odd binary labels** with `p_i dot p_j = 1 + (r_i dot r_j)/4 (mod2)`. Thus every nonzero off-diagonal entry of the Gram decoder `r_i dot r_j /8` has orthogonal source/target labels. A symplectic decomposition embeds the lattice's possibly degenerate binary Gram form; no guessed labels or floating ranks are used.

`center_screen.py` enumerates **every nonzero normal** in each constructed binary ambient space. For normal a, it computes the exact rational nullspace of roots with `p_i dot a = 1`. A vector u in that nullspace defines a collection direction supported wholly inside `a-perp`. This is a necessary local condition, not a full circuit.

`decoder_basis_screen.py` and `optimize_centers.py` find independent legal collection directions and solve exact scatter coefficients. The latter minimizes the sum of frame ranks among the enumerated nullspace basis directions using the linear matroid greedy rule. When a nullspace is multidimensional this is **not** an exhaustive search over all its linear combinations. All reported selected decoders are dyadic and factor the exact Gram matrix. Subtracting its off-diagonal entries leaves the identity.

`independent_check.py` imports no constructor and uses standard-library Fractions plus a separate binary elimination. It verifies every scalar matrix entry, odd/injective ports, all correction caps, center frame ranks, and two negative controls for each of ten decoded geometries, including the real current112 baseline.

## Outcome

| Geometry | Ports | Binary label dimension | Chosen center ranks | Copy charge | Nine-stage deficit model |
|---|---:|---:|---|---:|---:|
| A4 | 10 | 5 | 4,4,4,4 | 16 | -64 |
| A6 | 21 | 7 | six rank6 | 36 | -156 |
| A8 | 36 | 9 | eight rank8 | 64 | -288 |
| D4 | 12 | 7 | four rank4 | 16 | -48 |
| D5 | 20 | 7 | five rank5 | 25 | -65 |
| D6 | 30 | 9 | six rank6 | 36 | -84 |
| D8 | 56 | 11 | eight rank8 | 64 | -128 |
| E6 | 36 | 7 | six rank6 | 36 | -36 |
| E7 | 63 | 9 | seven rank7 | 49 | 63 |
| Current punctured E8 | 112 | 9 | eight rank8 | 64 | 320 |

Here the deficit model is `(L-1)*ports - L*sum(center ranks)` per replica, for the same odd-stage cover accounting ansatz. At L9 it reproduces the actual current112 deficit320 (eight replicas give2560). This is a structural screen of potential rank savings, **not an emitted controller or an exact moment price**. The initial local calculation mistakenly used the bit-side `4*ports` term for the nine-stage complex model; that was corrected to `8*ports` before these recorded conclusions. Smaller helper count alone cannot remedy a nonpositive rank deficit in this ansatz.

- **E6:** all27 possible nontrivial center directions are one-dimensional, and every one collects at rank6. Six independent centers cost36, exactly the port count; the modeled deficit is -36 for every stage count. It needs a genuinely different decoder/cover, not the tested Gram decoder.
- **E7:** survives this test. Seven rank7 centers and an exact dyadic decoder exist; full witnesses are saved. Its nine-stage modeled surplus is63 versus320 for current112, and it has2016 directed raw side corrections (32 per port), versus a denser E8 ancestry. Fewer corrections might permit cheaper helpers, but no such scheduled word was built and there is no winning kappa.
- **Full E8/120:** under the tested Gram-based label lift, all511 normal nullspaces are zero. Its naive coordinate decoder cannot collect a center at a proper hyperplane. The actual112-port word instead has exactly8 nontrivial center normals, all one-dimensional, reproducing its eight rank8 centers. This gives a concrete algebraic reason why puncturing changes feasibility; it is not an impossibility theorem for other decoders or label assignments.
- The A/D variants have negative modeled rank margins for the selected legal decoders, even before helper cost. They are poor direct replacements in this cover family.

## Missing admission

These are clean scalar factorizations, not smaller-R local suppliers. To become a candidate they need a scheduled monotone-frame gather/correction circuit; arbitrary dirty-helper compensation and restoration; exact phases and center transfers; source/target interfaces; a new controller and physical owners for changed ports/h; finite prefix/invoice; and both exact moment/outer engines. Legal individual collections do not make repeated uses of one source compatible with a single monotone frame chain.

Most useful continuation: use the E7 witness as a compact new decoder testbed, designing a genuinely new helper circuit; or seek a code geometry whose collection directions retain more ports per copied rank. Do not rerun the same root counts or claim that smaller dimension alone beats E8.

## Reproduction

From the frontier390 root with its existing Python environment and pinned current112 source, run, in order:

```
PYTHONDONTWRITEBYTECODE=1 ./verify-sympy314/bin/python -B radical-geometry-alternatives/screen.py
PYTHONDONTWRITEBYTECODE=1 ./verify-sympy314/bin/python -B radical-geometry-alternatives/center_screen.py
PYTHONDONTWRITEBYTECODE=1 ./verify-sympy314/bin/python -B radical-geometry-alternatives/decoder_basis_screen.py
PYTHONDONTWRITEBYTECODE=1 ./verify-sympy314/bin/python -B radical-geometry-alternatives/optimize_centers.py
PYTHONDONTWRITEBYTECODE=1 ./verify-sympy314/bin/python -B radical-geometry-alternatives/independent_check.py
```

Primary mathematical references consulted: [IAS/PCMI root-system notes, Dn coordinate roots](https://static.ias.edu/pcmi/2004/program/rsga12.pdf); [MIT E8 root-system description](https://www-math.mit.edu/~dav/e8plane.html); [Harvard E6 roots lecture notes](https://people.math.harvard.edu/~elkies/M263.21/index.html). The finite identities and counts above were computed from the saved explicit vectors, not inferred from those sources.

## Subsequent concrete E7 construction

The [E7 local-word followup](e7-local-word/README.md) now builds and independently replays an actual monotone scalar word with dirty-helper restoration. Best of32 schedules uses R1505 and loses: the fixed-word nine-stage complex saving is rigorously below0.000159859335581136 even with optimistic free hosting. This supersedes the earlier statement that no E7 scheduled word had been built; full physical/global admission remains absent.
