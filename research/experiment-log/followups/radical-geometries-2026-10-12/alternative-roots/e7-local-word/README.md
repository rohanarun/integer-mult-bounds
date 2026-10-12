# E7: a concrete local word, and an exact cost obstruction

This followup goes beyond the root-geometry screen. It builds an explicit scalar circuit with actual monotone binary frames from the saved E7 decoder. It is a **failed improvement**, retained to avoid repeating the same generic factory design.

## Construction and search

- 63 source/target ports in F2^9.
- 7 retained centers, each rank7, copied once (49 total copied ranks).
- 189 source clones feed the exact center collection matrix. Center scatter has264 scalar additions.
- The2016 nonzero off-diagonal Gram corrections are delivered under their actual target caps. A greedy schedule reuses an existing source carrier if its current frame can legally rise to the next target frame; otherwise it creates another clone at that source's initial rank1 frame.
- All clones are created before any source advances. The construction therefore does not retrospectively copy a source from a frame it has already left.
- 32 complete schedules: one deterministic order and31 seeded permutations. Every schedule has a complete frame recount. The best retained witness uses **R1505 helpers**, comprising7 centers,189 center-delivery clones and1309 additional correction clones. This is much larger than current112's R504.

The complete word has14,818 scalar operations:1,687 factory/gather,264 center scatter,2,016 side corrections,9,164 initial arbitrary-dirt compensators, and1,687 inverse cleanup operations. Paid local profile:

```
{1:1972, 2:1238, 3:298, 4:121, 5:282, 6:1204, 7:18, 8:2}
```

Its rank mass is14,602, agreeing with `2*63*8 +9*1505 +49`.

## Independent checks

`audit.py` imports no constructor. It verifies:

-  all63 clean source columns;
-  all1,631 source/target/arbitrary-helper-dirt columns in both orientations;
-  exact identity restoration of every source and helper;
-  all literal frame inclusions using explicit binary spans;
-  every side correction is inside its target perpendicular cap;
-  the copied center frames and complete paid profile;
-  rejection of a missing dirty compensator and an illegal zero-frame source access.

`COMPLETE-WORD.json.gz` contains the initial compensator, main stages, special center scatter, and final cleanup. This is a scalar/frame witness. Native phases, physical center-copy implementation, changed-port supplier interface, global controller, hosting and finite invoice were not admitted.

## Exact rejection before expensive global admission

For the same uniform odd-stage cover accounting, per-replica deficit is `(L-1)*63 - L*49`. At L9 this is63. A necessary condition at exponent b is

```
L * sum_r H[r]*r*((m/r)^b-1) < deficit,  m=1+8L.
```

This retains only the local word fee and grants zero extra idle/padding/fallback cost, so it is optimistic. `price_obstruction.py` uses rational positive partial sums for logarithms and `exp(x)-1 > x` to prove:

-  fixed nine-stage word: **b <0.000159859335581136**;
-  every uniform odd stage count L>=5 in this accounting: **b <0.000395874003913413**. Here `deficit/L <14` and `m>=41`; smaller positive odd L gives nonpositive deficit.

These ceilings are far below the current complex component's b≈0.0015935194. They are ceilings for this exact factory word and cover family, not for E7 geometry or new decoders. There is no new kappa or useful global candidate to publish.

The first attempt to serialize the exact rational price certificate hit Python's4300-digit conversion limit. The original error is retained as `price-first-failure.log`; rerunning with `PYTHONINTMAXSTRDIGITS=0` wrote the unchanged exact certificate. No mathematical check was weakened.

## Next direction

The clean E7 decoder works, but a generic per-source factory spends too much. A worthwhile replacement must share packet transforms or change the decoder, shrinking both residual inventory and actual frame fee; merely rearranging this word's global hosting or stage count cannot catch the leader.

Reproduce from the frontier390 root with `PYTHONDONTWRITEBYTECODE=1`, the existing `verify-sympy314/bin/python`, then `build.py`, `audit.py`, and `price_obstruction.py` in this directory. Use `PYTHONINTMAXSTRDIGITS=0` for the last command. Earlier geometry witnesses remain unchanged.
