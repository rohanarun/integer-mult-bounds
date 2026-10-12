# PR552 strict interior Steinberg trace search

Status: completed; no improved candidate. This extends the frozen endpoint-only search in `../trace552-search-alt` to genuine interior insertion gaps. It does not repeat endpoint evaluation except for the explicitly retained positive regression.

## Source and comparison

The input is PR552 head `33c33af0b7697155be1ea708e08cbd3f0707d94c`, reconstructed as `../source551-comparison/weighted/FULL-WORD.json.gz`. Its compressed SHA-256 is `a30810b755cf80e1128c0b932728bd51ca8e0bb31225fc415675afb42a766c8f`; it is byte-identical to the parent independent reconstruction at `../pr552-independent314/complex-local/weighted/FULL-WORD.json.gz`. The parent independently admitted that source; this search does not duplicate physical admission. The source reports conditional kappa 0.001591968902833346 and complex saving b = 0.001594507308884431019637.

The scripts import the frozen GK compiler from `../source550-review/local/vendor/gk`. Provider files are not modified. `CONTROLS-AND-SOURCE.json` records input equality and the positive regression binding.

## Search and result

For an original algebraic pair at positions p < q, gap a is immediately before original event a. The first operation must commute through events p+1 through a-1, and the second through a through q-1. Strict interior gaps are p+2 through q-1. The predecessor side uses positions less than a; the successor side uses positions greater than or equal to a. This preserves the untouched middle operations on their correct side of the replacement.

The signed rational Steinberg identity replaces two operations by three. Frame enumeration uses monotone nested replacement frames and every intermediate subspace through quotient dimension four. No larger quotient was encountered. Gaps are deduplicated by all three affected registers' predecessor/successor frame tuples, including signatures already covered by legal endpoint placements. Every positive local price nomination would receive a full GK profile check, including center constraints, with the complete candidate word and exact identity evidence retained. There were no positive nominations.

| Measure | Conservative scalar commutation | Identity-scale-aware commutation |
| --- | ---: | ---: |
| Algebraic pairs | 18,150 | 18,150 |
| Legal strict interior gaps | 384,587 | 384,587 |
| Duplicate or endpoint-equivalent signatures | 382,749 | 382,749 |
| New boundary signatures | 1,838 | 1,838 |
| Empty frame intervals | 1,672 | 1,672 |
| Nested frame assignments | 609 | 609 |
| Improved candidates | 0 | 0 |
| Runtime, seconds | 18.45 | 51.43 |

The initial predicate conservatively treats an overlapping scale operation as a barrier. The second script explicitly permits scale by one and commuting scale/scale pairs. This changes no search counts or outcome. Both processes exited successfully. Results and logs are retained separately; neither supersedes the other.

## Controls

`check_interior_identity.py` supplies an exact four-register example whose only legal gather gap is interior: e = (0 += 3/2 * 1), u = (3 += -5/4 * 1), v = (3 += 7/2 * 0), f = (1 += -1/2 * 2). The original e,u,v,f equals u,f,e,(0 += 3/4 * 2),v as a full rational 4 by 4 matrix. Both endpoint gathers and a wrong bridge sign are rejected. This is an algebraic/indexing test, not a physical supplier.

`regression548` reruns the frozen endpoint search on PR548 head `66dbc2bffc1bfa8d50b3f9a2ac7ccba8fd9f6f36`. It recovers the known B936/B1048 improvement in both endpoint placements. Candidate 000 decompresses exactly to the independently reconstructed PR550 word, content SHA-256 `6a02824c7484b9fd768a39d87b9c65dbe5221a877032ed1f74d11afb2acdd7d8`. These are regression artifacts, not new improvements over PR552.

## Reproduction and limits

From the frontier directory, with `PYTHONDONTWRITEBYTECODE=1`, run `./verify-sympy314/bin/python trace552-interior/search_interior.py`, then the corresponding `search_interior_identity_scale.py` or `check_interior_identity.py`. The scripts accept an alternate source and output directory as their first two arguments. The compiler and source dependency paths above must exist. The regression uses `trace552-search-alt/search_chain4.py` with the frozen PR548 raw word and `trace552-interior/regression548` as its output directory.

This is a finite local search over one fixed scalar word, one two-to-three identity family, and nested replacement frames. It does not prove global optimality, rule out collective retiming, test new geometries, or establish a new conditional kappa. Scalar identities, finite profile checks, phase admission, and global theorem assumptions remain distinct. No new physical verifier was run and no PR was edited or published by this worker.
