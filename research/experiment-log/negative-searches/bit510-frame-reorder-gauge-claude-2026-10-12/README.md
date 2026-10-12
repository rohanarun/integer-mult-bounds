# R480 bit word after PR535: wider frame, reorder and entrance screens (Claude, 2026-10-12)

In PR535/PR539 the bit side binds: c = 0.001587447106 against complex 0.001589992, so there is +0.16% of headroom. This entry widens the PR510-followups frame screen and adds two new screens.

| Screen | Status | Finding |
|---|---|---|
| Frame lifts over **all** root-closed subspaces | no gain | 97.5% of gate frames already equal the meet of their successors. Every legal lift raises the fee. |
| Commuting XOR-gate reorder plus frames | no gain | 462k fee-neutral swaps; the optimum is unchanged. |
| Bit gauges (helper starts at its first line, width 7) | infeasible here | Only 5 of 240 line-first helpers are compatible with target caps, and their lines conflict. |

**Why the gauge route still matters.** If 80 helpers per call could enter at width 7, their residuals would exactly fill the 23,040 rank-7 idle children, which currently host nothing. By the m64 moment alone, that substitution is worth about **+1.1% on c**; 10 such helpers would already exceed the 0.16% headroom. Getting there needs a bit word with short helper dirt responses, plus a bit-side target-level / Lemma A interface. That is a design change, not a search over the existing word.
