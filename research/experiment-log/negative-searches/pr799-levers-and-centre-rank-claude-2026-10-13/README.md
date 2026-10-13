# PR799 levers and the centre-rank lever (Claude, 2026-10-13)

PR799's X4 word was rebuilt with the package's own chain and κ = 0.001661634653669567 reproduced exactly. All runs below price with a frame model that reproduces the word's local profile {1:2548, 2:338, 3:430, 4:194, 5:56} plus centres {8:8}, including `helper_final` low ends and the early-cleanup tail.

| Screen | Result |
|---|---|
| Commuting target-gate reorder plus frame lifts (`sa3.py`) | about 15M moves; no gain (fee 34.11302, same as PR799) |
| The same, frames free down to predecessor joins (`sa3free.py`), and annealed | no gain |
| Further low terminal frames (`lowend.py`): move a helper's full-cleanup gates into the early tail, then end at its row/column cone | 0 of 378 helpers end below dimension 9 |
| Start-frame promotion of the 72 zero-response cold helpers (`sa3z.py`, `zcost.py`) | all 72 blocked: their zero-frame premix gates feed targets pinned at level 0 by the centre barrier |
| More bootstrap levels in the outer witness | no effect: s − a shrinks by a factor s per level and is already below 1e-20 |

## Centre-rank lever (`centres.py`)

The complex deficit is T(2Kv − L·cst) = 8(896 − 9·64) = 2560, where cst = 64 is the summed rank of the 8 centre frames. Pricing PR799's profile with lower centre ranks (deficit adjusted by T·L·Δcst):

- one centre at rank 7: **+2.8% b**;
- all 8 centres at rank 7: **+22% b**.

Each PR799 centre holds one E8 coordinate total over 56 sources, and the binary labels of those sources span rank 8. A scan of 664 decoding directions (8 coordinates, the 112 roots, 112 ±e_i±e_j and 256 half-vectors) finds support label-span rank 8 only for the coordinate directions; every other direction gives rank 9. Splitting a total over several centres only increases cst. **With these ports, no linear decoding total has a centre below rank 8.**

A geometry or port labelling in which the decoder totals' sources span at most 7 binary label dimensions, keeping dyadic decoding, is worth about 2.8% per centre. That is the sharpest open target for new-geometry proposals.
