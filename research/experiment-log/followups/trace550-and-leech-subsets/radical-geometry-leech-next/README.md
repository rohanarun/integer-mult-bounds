# Smaller Leech slices with explicit binary labels

Date: 2026-10-12. Status: **positive finite scalar, correction-cap and center-cap witnesses; no admitted supplier or new kappa**. This batch is isolated from the frozen prior `radical-geometry-leech` results. It reuses the retained276-line Leech slice, never reruns the full lattice census.

The prior exact100-support bound applies to the full276-line encoding. This experiment changes the port set itself and searches actual binary Gram completions, rather than repeating random clique tests.

## Executed constructions

Deterministic maximal two-coordinate hyperplane slicing produced:

| Ports | Exact real rank | Tight frame? | Best tested dyadic transfer support per column |
| --- | --- | --- | --- |
| 276 | 23 | yes | 100, prior batch |
| 176 | 22 | yes | 56 |
| 120 | 21 | no | 40 |
| 80 | 20 | no | 28 |
| 52 | 19 | no | 19 |
| 33 | 18 | no | 12–13 |

All subsets retain equiangular coherence1/5. Smaller support here does not contradict the prior bound because the port set has changed. `NESTED-SLICES.json` includes exact ranks, all enumerated zero-set sizes and the selected nested indices. The176-port slice has a general zero-set upper bound126; the tested two-coordinate normals attain only120, so that step is not claimed globally optimal.

For33,52 and80ports, the decoder gives an explicit dyadic matrix `T=A B` with diagonal1. Each nonzero off-diagonal transfer imposes a required F2 orthogonality constraint. We searched free entries of a symmetric Gram matrix with diagonal1 and fixed zeros at those constraints, minimizing its **exact GF2 rank** for12seconds per instance. This is a bounded local search, not a minimum-rank proof.

| Ports | Initial completion rank | Best retained rank / label dimension | Centers initially | Centers after repair |
| --- | --- | --- | --- | --- |
| 33 | 33 | 26 | 6 | 7 |
| 52 | 51 | 44 | 9 | 10 |
| 80 | 80 | 59 | 9 | 10 |

Each retained Gram matrix was factored exactly into ordinary binary dot-product labels. All port labels are distinct and odd. Every required off-diagonal correction lies in the appropriate target orthogonal cap.

## A failure and its explicit repair

The initial factorization failed one genuine additional condition: coordinate0 gathered source labels spanning the entire binary ambient space, leaving no proper gathering hyperplane. This failure is retained in `LABEL-CHECKS.json`.

Splitting that center's scalar gather into two additive pieces preserves `T` exactly while making both source spans proper. One extra center suffices in each retained case. `SPLIT-CENTERS-WITNESSES.json.gz` contains the complete new A/B matrices, binary port labels and a nonzero orthogonal normal for every center. This is a concrete repair of the center-gathering obstruction, not a claim that arbitrary dirty helper data or frame schedules have been solved.

## Verification and interpretation

`verify_final_witnesses.py` imports none of the search or constructor scripts. It independently checks:

- exact diagonal-one dyadic transfer;
- distinct odd port labels and every required correction-cap relation;
- every center's nonzero proper-hyperplane normal;
- equality with the original unsplit transfer;
- rejection of an even-label mutant and an incorrect center normal.

Result: `VERIFIED.json`, **PASS_INDEPENDENT_SCALAR_LABEL_AND_CENTER_CAP_WITNESSES**.

This improves the evidence from a coherence proxy to actual finite algebra and labels. The dimensions26/44/59 are still large relative to port count and current nine-dimensional native labels. No favorable paid profile or global price is established. The current reported frontier reference was PR550; none of these tests is a kappa comparison with it.

Remaining obligations: a chronological scalar/frame word with arbitrary dirty helper restoration, full phase and adjoint checks, local paid-child histogram, geometric adapters, whole-call owner maps, invoice, moment roots and outer assembly. All-size compiler and analytic-transfer contracts remain separate. A potentially useful next objective is jointly changing decoder support and Gram completion to reduce binary dimensions; the present completion search held each selected decoder fixed.

## Reproduction

Python3.14 with NumPy and SymPy was used. Set `PYTHONDONTWRITEBYTECODE=1`. Scripts write beside themselves. Run in order:

1. `search_nested_slices.py`
2. `test_slice_gram_rank.py`
3. `search_gram_completions.py`
4. `factor_and_check_labels.py`
5. `split_dense_centers.py`
6. `verify_final_witnesses.py`

The first script locates the prior frozen batch as sibling `radical-geometry-leech`; its exact input is also preserved as `SOURCE-LINES.json.gz` for inspection. Wall-time-bounded search iteration counts can vary across machines; the retained witnesses and independent audit are the authoritative result.

The prior published batch remains unchanged. Source hashes and local provenance are retained in `SOURCES.json`; all batch files are covered by `MANIFEST.json`.
