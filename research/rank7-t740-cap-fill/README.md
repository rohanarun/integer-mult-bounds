# PR #2979's words attain their packing cap at T740: conditional κ = 0.001729035764875516181444 − 10⁻⁴⁶ − 10⁻⁷⁰

```text
Status / UTC update / priority revision: DONE (moment nomination; see "Complete replay") · 2026-10-16 · priority revision 6 · base main d8e0f83f
Concrete question and changed premise: PR2979's open question 3. Can an integral allocation of its unchanged words reach
    the fixed-capacity packing cap? At T74 the optimal basis is fractional, and the best integral mix found there is
    still 1.55e-9 below the cap.
Established result and evidence status: yes, at T740. Ten lockstep copies of PR2979's literal T74 fill, plus 332
    whole-role relocations, give an allocation that lies exactly on the optimal face. Its idle histogram is 740 x the
    optimal basic idle profile, so the exact root equals the cap. Gain over PR2979: exactly 1782229002663727/10^24
    (about 1.78e-9). Packing only; author-checked (AI-assisted); not maintainer-reviewed.
Public artifact URL + exact commit: this package (see the PR).
Next useful task: none on packing for these words, since the cap is attained. Further gains must change the words
    (PR2979's open questions 1 and 2).
Active claim / expiry: released.
```

## Result

| | κ (headline; each − 10⁻⁴⁶ − 10⁻⁷⁰) | T | literal root vs the fixed-capacity cap |
|---|---|---:|---|
| PR #2969 (Dugongue; PR2942 + PR2957 words) | 0.001724035224748104878550 | 370 | attains that word's cap |
| PR #2979 (Marius-Paul Dumitrean; these words) | 0.001729033982646513517717 | 74 | 1.782e-9 below |
| **this package (same words)** | **0.001729035764875516181444** | **740** | **attains the cap** |

- **Words.** PR2979's two provider words are used unchanged: no gate, frame, scalar, entrance, cleanup or buffer change.
  - Local profile per call: {1:2445, 2:706, 3:232, 4:108, 5:18, 8:8}.
  - Width inventory: {4:26, 5:2, 6:16, 7:52, 8:99, 9:213}.
  - 91 private buffers.
- **Allocation.** 740 replicas, 6,660 calls and 2,717,280 helper roles.
- **Complete paid profile.** {1:16456860, 2:4701960, 3:1594737, 4:719280, 5:137085, 8:53280, 48:281903}.
- **Physical stock.** 663,040 live + 408 helpers + 8 centres + 91 buffers + 2 guards = **663,549**.
- **Exact root.** [0.001729035764875516181444, 0.0017290357648755161814441]. This is exactly PR2979's certified
  fixed-capacity relaxation cap (its `certificates/RELAX-CAP.json`).
- **Trusted ceiling.** `research/complex-local-word-ceiling/ceiling.py` gives 0.001756233636808 for this local profile.
  That model sends all idle mass to rank-51 children and ignores the 8/16/32/48 capacities. The root realizes
  **98.45%** of it.

## Why T740

The optimal face of PR2979's fixed-capacity relaxation is spanned by 12 tight patterns.

- **Three counts are fixed on that face, per replica:**
  - [9,9,9]@32: 93/4
  - [9,9,9,9,9]@48: 1341/20
  - []@48: 7619/20
- **Consequence.** An integral optimum exists exactly when 20 | T.
  - `verify.py` derives the three fixed counts exactly, from row multipliers over the 12 tight columns.
  - 1341 = 3² · 149 is prime to 20, so the [9,9,9,9,9]@48 count 1341T/20 is an integer only when 20 | T.
  - An integer-programming check over T = 1..80 finds integral optimal-face points exactly at 20, 40, 60 and 80.
  - PR2979's chronology is PR2917's T74 order, which interleaves two copies of the T37 chronology. The smallest
    multiple of it with 20 | T is T740.
- **Why T74 cannot reach the cap.** At T74 even the best integral pattern mix, ignoring chronology, is 1.552e-9 below
  the cap. PR2979's shipped fill is 1.782e-9 below.

## Construction

`lift.py` defines the allocation completely.

### The lift

The lift is Dugongue's PR2969 convention with ten copies.

| | T74 (PR2979) | T740 (this package) |
|---|---|---|
| call | (s, r) at time t | (s, r + 74j) at time 10t + j |
| role | (t, h, o, c, p, z) | (10t + j, h, o + 74j, c, p, z) |

Here j = 0, …, 9.

### The relocations

`allocation/RELOCATIONS.json` lists 332 roles. Each line is [time, helper, owner, child, port]: one role and its new bin.

- Each bin a relocated role leaves or enters (263 bins) is repacked as a compact prefix, in (time, helper) order.
- Nothing else changes.

### What the relocations change

The ten copies carry 60 bins of the non-tight pattern [4,8,9,9,9,9]@48. The relocations change the mix by:

    60 x [4,8,9,9,9,9]@48  ->  57 x [9,9,9,9,9]@48 + 3 x []@48
    75 x [9,9,9]@32        ->  60 x [4,9,9,9]@32 + 15 x [8,8,8,8]@32

- Both sides are balanced by capacity and width, and every resulting pattern is tight.
- The literal histogram {1:173160, 3:49617, 5:17205, 48:281903} equals 740 × the basic optimum
  {1:234, 3:1341/20, 5:93/4, 48:7619/20}.

### The chains

The change cannot be made directly. The 4s and 8s of the [4,8,9,9,9,9] bins come from late calls, and all but 20 of
the [9,9,9]@32 bins close early. So each displaced role moves along a short chain of **same-width exchanges**:

1. It enters an unlocked bin whose window contains its call.
2. It evicts a same-width role of an earlier call, which moves on in turn.
3. The chain ends when a target bin can take the last role.

Every intermediate bin keeps its pattern.

| step | what moves | relocations |
|---|---|---:|
| A | 60 fours into [9,9,9]@32 bins (→ [4,9,9,9]) | 150 |
| B | the 45 nines of the 15 latest-closing [9,9,9]@32 bins into 9 early empty @48 bins (→ [9,9,9,9,9]) | 45 |
| C | 60 eights into those 15 bins (→ [8,8,8,8]) | 80 |
| D | 12 nines of three emptied [4,8,9,9,9,9] bins, one each into 12 of the others (→ [9,9,9,9,9]) | 12 |
| E | 45 nines of nine late [9,9,9,9,9]@48 bins (→ []), one each into the other 45 | 45 |

- `construction/plan_t740.py` is the seeded greedy search, kept as provenance.
- It regenerates RELOCATIONS.json exactly in about 20 seconds plus a 48-second engine check.
- `construction/CHAINS.json` records every exchange: 664 out/in events.

## Verification

**Registered, bounded** (standard library only, Python 3.12):

`verify.py` runs in about 65 seconds and checks:

- **Inputs.** Every PR2979 input file matches its SOURCES.json pin.
- **Providers.** PR2979's provider registry is re-derived from its two words with its frame accounting.
- **Allocation.** The T740 ORDER/DISPATCH/FILL is rebuilt, and its canonical payload SHA-256 values match
  `allocation/EXPECTED.json`.
- **Owner engine.** PR2979's vendored engine (PR2839/PR2751 lineage) checks all 2,717,280 roles:
  - windows, same-call families, capacities, masks and compact prefixes;
  - the claimed complete profile and the rank-mass identity.
- **Physical stock.** 663,549.
- **Cap certificate.** PR2979's Fractions-only cap certificate is re-verified, and:
  - the idle histogram equals 740 × the basic idle profile;
  - every literal bin pattern has an identically zero reduced cost;
  - the exact root bracket equals the cap bracket.
- **Moment.** PR2917/PR2979's dyadic moment auditor is re-pinned only to PR2979's headline
  (`tools/audit_allocation_moment.py`), and shows a strict gain.
- **Claim.** CLAIM.json agrees with all of the above.

`controls.py` runs in about five minutes. Seven failure controls are rejected or lose the gain:

- **No relocations.** The bare ten-copy lift is valid, but its root is PR2979's, below the cap.
- **A missing link.** One chain link is omitted.
- **A window violation.** One role is sent to a bin whose window excludes its call.
- **A family collision.** One role is sent to a family its call already uses.
- **A stale profile.** The claimed profile is wrong.
- **Tampered relocations.** The relocations are altered, so the payload pin fails.
- **A wrong baseline.** The moment auditor is given the wrong baseline.

```sh
python3 scripts/research_package.py --package research/rank7-t740-cap-fill --check-only
python3.12 scripts/research_package.py --package research/rank7-t740-cap-fill
python3 -B research/rank7-t740-cap-fill/construction/plan_t740.py --out /tmp/t740-plan   # provenance: regenerates RELOCATIONS.json
```

### Complete replay

`reproduce.py` is PR2979's own `reproduce.py` with four explicit changes:

1. PR2979's package is exported from its exact commit `be191346`.
2. The adapters are derived with `tools/derive_adapters.py`, which only adds the pinned comparator pr2979.
3. The admission takes this package's T740 ORDER/DISPATCH/FILL and compares it with PR2979's headline.
4. The final assertions bind this CLAIM.json.

It runs PR2979's whole chain at T740:

- exact Git exports;
- a fresh retained bootstrap;
- PR2917's source stages and PR2979's rank7 overlay;
- fresh native chains for both providers;
- complete admission, which covers owners, parent lift, rebind, discovery, block norm, physical/prefix invoice,
  independent outer checks and the release.

It needs Python 3.12 with numpy, scipy, sympy, mpmath, gmpy2 and psutil (PR2979's pins).

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python3.12 -B research/rank7-t740-cap-fill/reproduce.py --repo . --work /tmp/t740-complete --jobs 1
```

Status of the complete replay: see the PR description. Until a complete replay receipt is attached, this package is a
**moment nomination with literal T740 owners**. That is the same status as PR2969's T370 nomination, which PR2979 used
as its comparator.

## Scope

- **Packing only.** All of PR2979's claims about its words are inherited unchanged, and none is re-proved here:
  - finite identities, native chains and frame accounting;
  - inherited all-size, compiler, hosting, precision and analytic hypotheses.
- **PR2979's status.** The repository archived PR2979 as a source package. It is not scientifically admitted, and
  current priorities ask for an independent audit of it. This package depends on that audit exactly as PR2979 does.
- **What is not claimed.** No selected-frontier change, no new mechanism, and no independent human review.
- **Optimality.** The cap is the optimum of PR2979's fixed-capacity relaxation, so no allocation of these words in that
  model can do better. Other templates, capacities or words are outside this statement.

## Open next questions

1. **Can a smaller T reach the cap?**
   - Why it matters: T740 makes the allocation ten times larger than T74.
   - First step: build a T20, T40 or T60 chronology compatible with the outer contract.
   - Blocked by: PR2917's T37-based order and the admission chain assume that chronology. A new order needs its own
     window and admission work, and gives no κ gain beyond the cap.
2. **Can the words improve?** With the cap attained, any further gain must change them. See PR2979's open questions 1
   (B-phase re-pairing around the normal-7 pivots) and 2 (input changes placed later in A).
   - First step: price one candidate rewrite with PR2979's certified frame accounting.
   - Blocked by: a certified frame solver harness that PR2979 did not ship.

These are recorded as structured `open_questions` in TASK.json.

## Credit

- **Marius-Paul Dumitrean (PR #2979):** the words, the literal T74 fill lifted here, the cap certificate, the admission
  adapters and `reproduce.py`.
- **Dugongue (PR #2969):** the lockstep T-lift convention and whole-role cross-copy moves.
- **themilkman216:** the observation about the T at which these caps become integral.
- **Mason Hale (PR #2917):** the T74 chronology, owner/moment checks and admission chain.
- **Tekalign:** the independent owner checker.
- **Jeremy Diviney (PR #2908):** the moment auditor arithmetic and paired-extraction lineage.
- **Jeremy Kothe (PR #2957):** the rewrites inside these words.
- **Yiyang Lu:** the flow model behind PR2979's fill.
- **icekylinx:** the exact auditor.

New work by Rohan Arun, prepared with substantial AI assistance (Anthropic Claude). Apache-2.0. Retained notices apply.
