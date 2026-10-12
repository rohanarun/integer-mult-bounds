# Independent controls for PR552 common-subspace graph cuts

Completed: the pairwise energy and residual cut machinery pass exhaustive small-DAG controls. The audit found one supplier-context defect: scatter boundaries require equality, while the initial graph encoded only inclusion. The root worker was notified and is correcting that model separately. This directory retains the original source snapshot; it does not modify the running parent search.

## Audited source and defect

`ROOT-SOURCE.py.txt` snapshots root `search552_global_wave_cuts.py` after its capacity fix and before the equality fix, SHA-256 `cef3c20d40f32f59def690ec8711fce6b9ae2e71cb3ff79f7ee95b6f388f524a`. It uses capacity scale 10^7 and a hard capacity greater than the entire all-unselected cut, with signed-int32 bounds. Its input is the independently reconstructed PR552 word at head `33c33af0b7697155be1ea708e08cbd3f0707d94c`.

The GK profiler requires the current center frame to equal its declared frame, and each current target frame to equal its scatter level, at the A/B boundary. These boundaries do not perform a climb. Inserting a normal inclusion edge to a fixed anchor permits a preceding A event to contract below that anchor and pays for a nonexistent climb. Freezing the immediately preceding event for each center/target register, after checking its frame equals the anchor, removes these invalid assignments.

`ANCHOR-GAP.json` gives an exact example: empty initial frame → free line event → fixed line scatter anchor → fixed plane. The relaxed graph's minimal cut selects nothing; its maximal cut contracts the free event and has zero fee difference. That maximal selection violates the equality boundary. Freezing the event removes it. `SUPPLIER-ANCHOR-CONTROLS.json` also calls the pinned real GK profiler on tiny fixtures: both the center and target mutations are rejected with the expected exact error. These fixtures test the profiler only, not physical supplier admission.

The parent reported no gain and no selected events in the original PR552 cut sweep, so this defect does not invalidate an accepted improvement. Its no-gain result was over a relaxed domain, subject to rounding, rather than an exact supplier model. Maximal neutral-cut searches require the equality fix or full-profile rejection. The parent reported its earlier accepted neutral words had already passed the full profile.

## Energy controls

`check.py` independently enumerates every selected subset on 500 sampled binary frame DAGs in dimensions three and four, plus explicit controls. It uses direct binary spans for inclusion, checks the floating fee difference against the pairwise/unary energy, compares the rounded cut minimum with exhaustive enumeration, and checks minimal and maximal residual source sets against the intersection and union of every rounded optimum.

Results: 8,610 direction/kind cases, 42,184 legal subsets, and 161,480 rejected invalid subsets, including 143,423 selections violating fixed nodes. 6,506 cases include repeated operand edges; 1,881 have distinct minimal/maximal optimal selections. The maximum observed rounding discrepancy is approximately 4.48e-7. Positive contraction and extension gains, all-fixed no-gain cases, inactive directions, repeated frames, and neutral alternatives are included. Runtime was about two seconds.

For a monotone edge F ⊆ G with d = dim(G)-dim(F):

- If both endpoints contract, selecting only the successor is illegal. Selecting only the predecessor costs cost(d+1)-cost(d).
- If both endpoints extend, selecting only the predecessor is illegal. Selecting only the successor has the same positive cost.
- If only one endpoint changes, its selected unary term is cost(d-1)-cost(d). This includes an active endpoint adjacent to a fixed inactive endpoint.
- Repeated edges are separate register-chain charges and must be accumulated separately.

All legal subset energies matched to floating tolerance. The hard capacity exceeded the known feasible all-unselected cut, so no optimum crossed a hard constraint. The suite checks the actual rounded objective, not exact real-number optimality. Unrounded unary constants can make the printed rounded lower bound slightly negative even when the selected word's actual fee difference is zero.

## Scope and reproduction

Use the SSD Python environment with `PYTHONDONTWRITEBYTECODE=1`: run `./verify-sympy314/bin/python trace552-cut-controls/check.py` and `./verify-sympy314/bin/python trace552-cut-controls/check_supplier_anchors.py` from the frontier directory. NumPy/SciPy are required; the second script uses the frozen GK module in `source550-review/local/vendor/gk`.

The suite independently validates finite graph energy and residual selection, while explicitly exhibiting the original boundary model gap. It does not prove global optimality, certify a new conditional kappa, rerun the full PR552 physical verifier, or modify/publish any PR. The source has no target-register start_extra entries and no same-register add operations, so those context corner cases are absent. The profiler's additional served-level descent conditions depend only on fixed center/target data here.
