# PR552 four-gate commutator routes

Completed bounded search: no improved paid profile. All3,629 add gates and every distinct existing third register were screened for contiguous replacement, across three receipts. Incompatible register-frame intervals were rejected. The first two passes prioritized expensive gates and warm helpers; the coverage pass added the omitted helpers and input/target intermediates without repeating previously priced routes. Combined: 41,801 compatible register routes, 83,602 orientations and 167,480 enumerated nested-frame assignments.

Source PR552 head33c33af0b7697155be1ea708e08cbd3f0707d94c, compressed word SHA-256 a30810b755cf80e1128c0b932728bd51ca8e0bb31225fc415675afb42a766c8f, from the parent independent reconstruction. The unchanged GK profiler is imported from source550-review/local/vendor/gk. No provider source or PR was edited.

## Distinct route and algebra

Consulted pinned PR556 head24321d9347828751adabd86de4a4a7807207afac: retained trace evidence lists two/three-gate expansions, reversals and commutation screens, but no explicit single-add four-gate commutator screen. Three inspected source files and their Git-blob receipts are retained under pr556/.

For original a += k*c and any distinct existing register b, the sequence

    a += u*b; b -= (k/u)*c; a -= u*b; b += (k/u)*c

has exactly the original action on every input column, including arbitrary initial dirt in b. The reverse orientation is also tested. Exact rational 3 by 3 controls cover24 signed dyadic coefficient/orientation cases and reject the wrong final sign. The search uses u=1; other nonzero u do not change this finite frame-price model, though physical scalar invoice costs may change.

The shared intermediate b makes all four frames nested. Every transition on a,b,c, including predecessor/successor transitions, is charged. Scatter-center and target equality anchors are enforced, not modeled as extra climbs. Frame intervals are completely enumerated only through quotient dimension3; larger intervals use existing source frame catalog plus interval endpoints. Their counts are retained explicitly. Thus this is not an exhaustive exclusion of all possible four-gate frame assignments.

## Validation and outcomes

RESULT.json records the top384 gates:13,028 assignments, no gain,7.40seconds. REMAINDER-RESULT.json records the remaining3,245 gates:68,632 assignments, no gain,51.46seconds. COVERAGE-RESULT.json closes register-choice caps for both groups and includes input/target intermediates; it also finds no gain. Separate logs and scripts reproduce all passes.

check_profiles.py independently reconstructs24 losing replacements and runs the complete GK profile. Every analytically computed price delta matches the full profile; their increase is0.005713669981716407. These are control cases, not winning nominations, and no candidate word files are asserted for them. The exact local commutator identity handles arbitrary scalar dirt; no full physical phase/owner/invoice replay was needed because there was no improving nomination.

Noncontiguous placements, compensating interactions with surrounding gates, new register geometries, and exhaustive larger frame intervals remain outside this batch. No conditional kappa improvement or global optimality is claimed. All processes completed successfully. Use PYTHONDONTWRITEBYTECODE=1 with the frontier verify-sympy314/bin/python environment to rerun the scripts; source paths are relative to the frontier directory.
