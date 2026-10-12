# Barnes–Wall / Reed–Muller geometry screen and block-climb prize (Claude, 2026-10-12)

**Question:** is BW₁₆ / RM(·,4) a better port geometry than E8 / [8,4,4], and how much is "climbing in blocks" worth on the current leader?

## Prize: what block climbs are worth on #579

#579's histogram is {1:171840, 2:37152, 3:27686, 4:13824, 5:4032, 6:4032, 8:576, 30:1, 48:1817}, with b = 0.0016038. Rank mass, m = 73 and W = 7168 are held fixed, and part of the rank-1 children are merged into blocks:

| Merge rank-1 children into | 10% | 25% | 50% | 100% |
|---|---:|---:|---:|---:|
| rank-2 blocks | +0.75% | +1.91% | +3.89% | +8.10% |
| rank-4 blocks | +1.52% | +3.89% | +8.09% | +17.6% |
| rank-8 blocks | +2.30% | +5.94% | +12.6% | +29.0% |

For comparison, all of last night's progress was about +1%. A geometry whose circuit turns even 10% of single-dimension climbs into rank-4 blocks beats that.

## Geometry statistics (`bw16.py`, `BW16-STATS.json`)

BW₁₆ was built by Construction D from RM(1,4) and RM(3,4): 4,320 minimal vectors, all of norm 8, giving 2,160 lines.

| | E8 | BW₁₆ |
|---|---:|---:|
| Lines | 120 | 2,160 |
| Lines per dimension | 15 | 135 |
| Coherence (max \|cos\|) | 1/2 | 1/2 |
| Welch bound | 0.343 | 0.249 |
| Share of other lines with nonzero inner product | 0.471 | 0.604 |
| Flats of AG(m,2) by size | 8 / 28 / 14 / 1 for sizes 1 / 2 / 4 / 8 | 16 / 120 / 140 / 30 / 1 for sizes 1 / 2 / 4 / 8 / 16 |

## Reading

- **Used directly as ports, BW₁₆ is worse than E8.** Coherence is the same, the correlated-neighbour share is higher (0.60 vs 0.47), and the data block grows 18× (2,160 lines). It fails the same way Leech did.
- **Its useful feature is the extra nesting level.** AG(4,2) has a full doubling flag of flats, 1 ⊂ 2 ⊂ 4 ⊂ 8 ⊂ 16, including 30 hyperplane blocks of size 8. [8,4,4] stops at 14 quartets inside 8 coordinates.
- **Hypothesis for the next experiment:** keep the 120 E8 ports and use BW₁₆ ⊇ E8 ⊥ E8 only as a *joint label space for pairs of calls*. Cross-call terms could then enter as whole 8-dimensional blocks (rank-8 climbs), extending the joint-prefix idea of #571. Building this needs a new factory word; nothing here certifies it.

Status: `analysis_only`. Retry when a factory is specified that uses the RM(1,4) hyperplane blocks for joint delivery.
