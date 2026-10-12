# PR552 changed-scalar-word trace followup

Prepared for Rohan Arun with OpenAI Codex assistance. **No further improvement found.** This is a new input-word experiment, not a repeat of the previous PR550 screen.

Source: [PR552](https://github.com/CrocSwap/integer-mult-bounds/pull/552), exact head `33c33af0b7697155be1ea708e08cbd3f0707d94c`. The input is the reconstructed wave-plus-weighted word from `source551-comparison/weighted/FULL-WORD.json.gz`. It is **byte-identical** to the parent's separate reconstruction at `pr552-independent314/complex-local/weighted/FULL-WORD.json.gz`; `SOURCE-BINDING.json` retains both hashes. PR552's twelve weighted source changes make its scalar word different from PR550. No native or global verification was duplicated here.

## Searches and outcomes

| Search | Algebraic matches | Exact commuting placements | Nested-frame assignments | Surviving gains |
|---|---:|---:|---:|---:|
| 2to3 expansions | 18,150 pairs | 4,225 | 10,444 | 0 |
| 3to2 contractions | 5,848 triples | 378 | 378 | 0 |

Both searches cover all event distances within each A/B phase. Participating additions use their actual rational coefficients; contractions require an exact matching coefficient-product bridge. The search gathers selected operations to the earliest or latest participating position only when every required scalar interchange commutes exactly.

The two-to-three search permits three distinct nested frames. It enumerates every subspace in candidate intervals through quotient dimension4, and no larger interval occurred in this run. The inverse search permits two nested frames and encountered no interval larger than its exhaustive quotient dimension3. This is exhaustion of those generated frame intervals, not all possible word rewrites or all interior insertion placements.

The fee uses b0.001594507308884431. Whole affected-register chains calculate proposed deltas, then the complete unchanged `gk.profile` checks every positive nomination. Four apparent A-side gains fail the required center-frame boundary. Their positions, proposed frames, deltas and exact error messages are retained in `CHAIN4-RESULT.json`. No positive candidate survives and no new kappa is claimed.

## Regression and scope

The same expansion search was run on the earlier PR548 input. It rediscovers the known PR550 move at B positions936/1048, in both end placements, with delta `+rank1 -rank2 -rank3 +rank4`. The recovered earliest-placement candidate is **byte-identical after decompression** to the independently reconstructed PR550 word. `REGRESSION.json` and `regression548/` retain that control. These are known old gains, not PR552 improvements.

Scripts preserve exact scalar coefficients and regenerate inverse cleanup for any surviving nomination. They import the existing pinned gk primitives; reproduction requires the frontier390 provider inputs and Python environment. They do not mutate those providers. Optional positional arguments select an alternate word/output directory. All writes and retained logs are inside this directory.

The claimed PR552 global bound remains conditional on inherited all-size contracts. This worker only searches exact local trace identities and frames; it does not independently admit its global κ. Next useful directions are different identities, interior insertions or coordinated neutral rewrites, rather than rerunning this same neighborhood on the same head.
