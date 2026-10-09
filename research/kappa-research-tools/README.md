# Research scripts behind PR #211 (not part of any certificate)

Exploration code. Hard-coded paths assume this layout (edit the constants at the top of each script):

- /home/claude/crocswap/w200 = CrocSwap/integer-mult-bounds @ a1175449f34d39ff933d9d8ab23ced1f32b290ec (PR200)
- /home/claude/crocswap/w193 = @ 187e1010ac8b259af8e9b5166f68b64bc27b4b47 (PR193)
- /home/claude/crocswap/w197 = PR197 head (packed-source-assisted-bit), w187 = PR187 head, w168 = PR168 @ 4a3c769

| Script | Purpose |
|---|---|
| fopt.py | Exact physical-chain model of PR200's bit word, frame join/meet algebra, chain cost sum t*ln(72/t) |
| desc1.py | single-op best-improvement frame descent (stalls at -0.02%) |
| casc.py / optall.py / optall2.py | cascading raise/lower moves + annealing; optall writes F_rows.json, runs PR200 terminal prove, prints packed kappa |
| lbound.py | global min (L) / max (U) feasible frames; dim-relaxed per-chain lower bound (4.6% below PR200, loose) |
| maxframe.py / minframe.py | all-max / all-min frames (both worse than PR200) |
| evalh.py | packed kappa from a per-vertex child histogram (bank packing + 3 leaf levels + assembly approx) |
| quick.py / sinkgain.py | model checks; marginal value of one extra terminal sink (~+2.6e-8 kappa) |
| sinkenum.py / cons.py / cons2.py | terminal-sink eligibility census (only 34 eligible; 518 blocked only by consumers) |
| gsel.py / p13.py | dead levers: packing-aware gauge reselection; p=13 bit word |

Frame IDs from word.register are process-local: never pickle ids across processes; store basis rows.
