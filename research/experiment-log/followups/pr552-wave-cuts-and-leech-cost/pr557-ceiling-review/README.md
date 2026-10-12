# Independent replay and scope review of PR557

Status: **independent PR557 replay PASS; transfer to the final PR552 word UNPROVED**. This is a ceiling certificate review, not a new kappa record.

## Exact sources and replay

PR557: https://github.com/CrocSwap/integer-mult-bounds/pull/557 at head `a1e805c528884818ddf7d730024c1d8de9660f81`.

`ACQUISITION.json` records 42 individually verified Git blobs: the complete `research/frame-domain-ceiling` package, its vendored dependencies, supplied cross-platform validation receipts, and dedicated workflow. `PR557.json` and `TREE.json` retain the fetched metadata. Source files and notices remain unchanged.

Executed with the SSD Python3.14 environment and standard-library verification code:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONINTMAXSTRDIGITS=0 ./verify-sympy314/bin/python -B pr557-ceiling-review/source/research/frame-domain-ceiling/verify.py --work /Volumes/SP\ AI\ 01_16/CodexWorkspaces/imb-retime2/frontier390/pr557-ceiling-review/replay314
```

The process exited0. Reconstruction, all exact dual checks, and all four expected mutation rejections passed. `replay314/RESULT.json` SHA-256 is `cf8a5b239b947e0a5cac2a3a76cde1e6d7e444a5874e4874fcdbd4b5ffa63f80`, byte-identical to both supplied author platform results. Logs and receipts are retained. No optimizer, NumPy or SciPy is imported by the supplied verifier.

## What it closes

The certificate fixes PR551 head `e7faafc4fec401d24080e5b2df12f964f1cfe123`: scalar operations and order, starts, center cut, endpoints, helper widths, owner schedule, and conservative bad-class charge. It covers simultaneous reassignment of all3,657 A/B event frames to legal binary subspaces, including prefix frames.

All finite frame intervals have quotient dimension at most3. The2,375 variable events split into71 components. Rational LP duals check26,470 constraints and34,685 columns using two independent outward rational moment engines. The verified exclusion is complex b ≥0.001594507308884431019638. With the retained outer engine it excludes the next kappa grid value0.001591968902833347.

The graph allows charged center climbs that the physical word does not perform. The proof explicitly treats this as a relaxation containing all literal assignments, so a lower bound on it remains valid. This differs from interpreting such a relaxed graph as an admission certificate for a proposed word.

This review independently reran the exact certificate and inspected its stated finite-domain/dual construction. It did not rerun the full physical PR551 supplier, prove the inherited all-size interfaces, or independently formalize the mathematical theorem. Mutation rejection logs are expected negative controls, not unexplained failures.

## Why it does not directly cover PR552

PR552 head `33c33af0b7697155be1ea708e08cbd3f0707d94c` has a different A scalar word. Exact comparisons are retained in `COMPARISON.json` and `SUBSEQUENCE.json`.

| Property | PR551 | PR552 |
| --- | ---: | ---: |
| A operations | 1,769 | 2,007 |
| B operations | 1,888 | 1,888 |
| Helper count R | 504 | 504 |

B scalar operations and order are identical, with18 frame differences. Ports, center frames, starts, target levels, and cut agree. The reconstructed PR551 bytes exactly match our previous reconstruction (SHA-256 `dac4d6d6ad99208d3d50c640acb2f82e81ddaa1dc97a29da758353fd3bd49fa9`). Final PR552 bytes have SHA-256 `a30810b755cf80e1128c0b932728bd51ca8e0bb31225fc415675afb42a766c8f`.

Neither the exact scalar sequence nor the operand-support sequence of PR551 A embeds as a subsequence of final PR552 A. More strongly, both corresponding multisets lack12 required PR551 operations in PR552. For example, `add241←24` appears once in PR551 and zero times in final PR552, which instead reads helper240. Thus independent reordering cannot repair this simple shared-event mapping. These12 substitutions change register dependencies; they are not merely coefficient or frame differences.

There is a narrower useful relation: PR551 A is an exact scalar subsequence of the **pre-weighted wave** intermediate, deleting238 operations. None of the removed operations is the last A event of a center/target anchor. Event deletion plus a rigorously established rank-charge inequality may support a domination argument for that intermediate. This package has not certified that argument, and it does not bridge the12 later source substitutions. Equal prices/profiles alone do not transfer PR557's proof to PR552.

## Remaining routes

A direct ceiling for final PR552 would need newly reconstructed domains and an exact dual certificate for its changed register dependency graph, or a proved domination map addressing the12 substitutions. Research routes outside PR557 include scalar rewrites/reordering, changed cuts/helpers/widths, owner repacking, nonbinary frames, different bad-class charges, and new outer arguments. Their exclusion from this theorem is not evidence that they yield an improvement.

No PR, provider source, or other worker's files were edited; no publication was performed. All work and logs are on the mounted SSD. The parent handles archival and publication.
