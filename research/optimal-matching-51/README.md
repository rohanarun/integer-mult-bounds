# Exact optimal carrier matching on PR #51's enlarged positive-frame networks

Under PR #51's inherited analytic and fixed finite-alphabet multitape
hypotheses, keeping its graphs, labels, geometry and data profile,

$$T(n)=O(n(\log n)^{1-\kappa}),\qquad
\kappa=\frac{4171627317}{10^{14}}=4.171627317\times10^{-5}>2^{-15}.$$

This is **0.00996% above PR #51** (`4171211781/10^14`). The bit saving is
`83436027/(2·10^12) = 4.17180135e-5`, against PR #51's
`4171385779/10^14`, and W = 175,503,731 is unchanged.

## Idea

PR #51 matches carriers with `moment_match_rank_node`: Hopcroft–Karp followed
by local exchanges scored by a **rank-only proxy** for the moment. With the
matching size fixed, the role count, W and the rank deficit are fixed, and the
bit moment is **linear in the chosen edges**. Each admissible edge (donor u →
use w, carrying value y into target t) replaces the frame transitions
`(u→sink), (0→y), (y→t)` with `(u→t)`. Each transition's actual fixed-basis
block profile depends only on its frame pair.

We therefore dump every admissible edge with its exact signed block change
under PR #51's actual signed positive frames and negative basis
`L=I−4J/[3(h+3)]`. The admissible set uses PR #51's own adjacency rule:
rank/node chronology plus signed positive-label inclusion. We then solve the
**max-weight maximum-cardinality matching** for the first-order gain
`Σ c_t·t·ln t` (PR #44's method).

| | PR #51 | This |
|---|---:|---:|
| h=23 matched / roles | 6,681 / 36,219 | 6,681 / 36,219 (same cardinality) |
| h=25 matched / roles | 9,601 / 47,461 | 9,601 / 47,461 |
| admissible edges | 11,526 (h23), 15,794 (h25) | same |
| κ | 4.171211781e-5 | **4.171627317e-5** |

Everything else is PR #51, unchanged:
- graphs, clones and alternative partitions
- positive labels and geometry
- the both-negative data profile with its 169 exact classes
- the phase, copied centers, paid corrections and the balanced assembly

## Files

- `links-{23,25}.uses`: pinned matchings, binary `<2I n,count>` + `<2I donor,use>`.
- `selected-links-{23,25}.json`: the same matchings in PR #51's witness format.
- `axes-optimal-matching.json`: PR #51's axis fixture with the new blocks.
- `composition-summary.json`: output of PR #51's
  `explicit_profile_composition.py` on that fixture.
- `tools/cprof.cpp`: PR #51's `positive_frame_profiles.cpp` frame and
  transition logic with a closed-form projector for any basis `L=I+cJ`. It
  builds matrices mod three fixed primes and uses PR #51's max-corner pivot
  rule. It has a `DUMP_EDGES` mode. With PR #51's own matching at
  `c=-4/[3(h+3)]` it **reproduces PR #51's certified blocks exactly at both
  h**, with zero rank defects.
- `tools/solve51.py` (scipy), `tools/legal51.py`, `edges/`, `reproduce.sh`.

## Checks

- PR #51's own exact arithmetic reproduced (κ = 4171211781/10^14).
- PR #51's h23 and h25 producers rebuilt from its published evidence with
  `rebuild_alternative_selected.py` (R = 36,219 and 47,461, all recorded
  digests matching).
- New matchings: PR #51's independent compiler `check_compiled_witness.check`
  passes at both h, covering:
  - the scalar identity
  - rational frame containment
  - the physical role compiler
  - the rank timeline
- Exact composition with PR #51's script: 47 strict constraints and
  7 margins.

**Required before marking ready:** recompute both axis profiles with PR #51's
exact Boost-based `agents/geometry/code/positive_frame_profiles.cpp`
(negative basis, on the rebuilt DAGs and `links-{h}.uses`). Confirm the blocks
equal `axes-optimal-matching.json`. This is discovery-profiler output, so it
needs the same exact integer-minor certification PR #51 used. Then run the
full repository verification.

A finite optimum over matchings for these graphs is not a claim of global
optimality.

## Attribution

hipotures / RaD (PR #51: enlarged positive frames, producers, geometry, data
classes, composition and checker). Exact optimal matching method from PR #44.
icekylinx, James Chang, Dominik Scholz, Zhihao Chen, Aurel Prosz / Paureel,
Chafik Boukhalfa, eumemic, Douglas Colkitt, OpenAI, Harvey–van der Hoeven,
and all retained predecessors. Prepared by Rohan Arun with Anthropic Claude
assistance.
