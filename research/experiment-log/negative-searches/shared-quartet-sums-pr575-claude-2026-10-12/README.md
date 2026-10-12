# Two-call joint geometry and shared quartet sums on the PR575 word (Claude, 2026-10-12)

## 1. Two-call joint label space (BW₁₆ ⊇ E8 ⊥ E8): blocked by the interface

The complex window is tied to the label dimension: m = 8h + 1, with h = 9 and m = 73 (PR531 `GLOBAL-HOSTING.md`; `coalesce_frames.py` default). A joint label space for two calls means h = 18 and m = 145, which changes the outer recursion, the controller and all 47 assembly constraints; a factory word cannot make that change. Local calls are also independent subproblems with no shared data, so there are no cross-call sums to deliver as blocks.

## 2. Where the single-dimension climbs come from (`where1.py`)

On the PR575 joint-prefix word (P575, used in 24 of PR579's 72 calls), the local profile is {1:2352, 2:580, 3:336, 4:192, 5:56, 6:56}. Rank-1 climbs come from:

- helpers: 1,616 (A 694, B 656, final 266);
- targets: 392 (in B);
- sources: 344.

Typical helper chains are 1,1,1,1,4,1 and 1,1,1,1,2,1,1,1: a helper accumulates its quartet one source at a time.

## 3. Are the same sums rebuilt? (`reuse.py`, `reuse2.py`, `share*.py`) No.

Exact rational replay of all A, cut and B operations tracks each register's data combination. Of 1,812 distinct data sums with at least 2 sources, 1,532 are formed by one register only. All other repeats are deliveries: a value copied from a register that already holds it.

Only 70 events rebuild a sum from sources that another helper already holds. All 70 are pair or quartet sums inside kernel or mutable-source chains, where the rebuilding register already holds other data and has non-source operations, and in 42 of them the provider register has already moved on. No clean single-gate replacement exists.

**Conclusion:** the current factory already shares nearly every partial sum. The single-dimension cost is the price of building each distinct sum once, not of duplicated work. Reducing it needs a different set of required sums (a new decomposition), for example a minimum-fee "frame-weighted addition chain" over the sums the decoder needs. That is the open problem to pose to geometry and coding-theory experts.

Status: `bounded_no_gain`.
