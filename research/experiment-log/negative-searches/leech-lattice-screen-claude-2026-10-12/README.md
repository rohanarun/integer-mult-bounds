# Leech lattice port-geometry screen (Claude, 2026-10-12)

**Question:** could the Leech lattice replace the E8 / F₂⁹ frame geometry behind the complex supplier (PR433 lineage) and give a cheaper complex word?

**Method:** `leech.py` builds Λ₂₄ from the extended Golay code [24,12,8]. Its weight enumerator was checked as 1, 759, 2576, 759, 1. The script then lists all 196,560 minimal vectors in three shapes: (±2⁸,0¹⁶), (∓3,±1²³) and (±4²,0²²). It also runs an inner-product census over the 98,280 lines and checks that the frame is tight. `compare.py` runs the same census on the 240 E8 roots.

| | E8 (current) | Leech |
|---|---|---|
| Dimension (with parity label) | 8 (9) | 24 (25) |
| Lines | 120 | 98,280 |
| Coherence (max \|cos\|) | 1/2 | 1/2 |
| Welch bound | 0.343 | 0.204 |
| Share of other lines with nonzero inner product | 56/119 = 0.471 | 51,704/98,279 = 0.526 |
| Binary code / relative distance | [8,4,4] / 1/2 | [24,12,8] / 1/3 |
| Tight frame | yes | yes |
| Minimal-vector classes mod 2 | 120 in E8/2E8 | 98,280 in Λ/2Λ |

**Reading:**

- **Coherence:** the same as E8, 1/2.
- **Correlated neighbours:** each line has more of them. In the moment-root price this is the side-correction load per port.
- **Label dimension:** almost 3× larger, so m grows as 1+24L instead of 1+8L.
- **Binary code:** the Golay code has a worse relative distance than extended Hamming.
- **Where Leech wins:** only on raw line count (4,095 lines per dimension versus 15). The current pricing does not reward line count.

**Verdict:** no structural advantage per port, so no κ candidate was built. Status: `analysis_only`. Leech is worth revisiting only under a pricing model that rewards line count or kissing number. The full retry condition is in `results.json`.
