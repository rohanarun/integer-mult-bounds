# Frame-chain search and follow-up screens on the PR531 504-helper word (Claude, 2026-10-12)

**Result:** conditional κ = **0.001526158885117467**. That is +0.553% over #531 (0.001517760977820331), published as draft [#534](https://github.com/CrocSwap/integer-mult-bounds/pull/534).

**What changed:** only the operation frames. Each frame is lifted to contain its constructor frame, and every register chain stays monotone. Scalar operations, helpers, widths, the owner map and the idle remainders are all unchanged. Every #531 checker passes on the new word.

| Screen | Status | Finding |
|---|---|---|
| Frame-chain search | gain | Fee 33.0977 → 32.9013, local profile {1:2220,2:368,3:460,4:168,5:168,6:56,7:8}. 23 of 40 fleet seeds reached the same optimum (`FLEET-40.json`). |
| Commuting-op reorder plus frames | no gain | Same optimum 32.90125. |
| Freeing the 8 slack constructor frames | no gain | Same optimum. |
| Hosting LP ceiling | no gain | The #531 owner map already equals the pattern-LP ceiling. |
| Gauge/pivot additions on 224 free helpers | infeasible | Blocked by target nesting or the centre chain; no dependent pairs. |
| Two-dimensional gauge raises | infeasible | Break target final hyperplanes. |
| Kernel-class retirement (#532 style) | loss | +0.339% against the +0.554% frame-optimised baseline. |
| Dead-op slicing (238 ops) | neutral | No profile change. |

**Lower bound:** with no coupling between registers, the floor for frame-only changes is fee 20.46. The remaining gap to 32.90 comes from frames shared across register interactions. Closing it needs a new scalar decomposition, not a better frame or order choice.
