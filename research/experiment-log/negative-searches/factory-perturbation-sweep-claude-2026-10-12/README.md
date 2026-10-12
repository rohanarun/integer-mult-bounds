# Random-perturbation sweep of the PR522 factory (120 Daytona sandboxes)

**4,812 candidates, all evaluated, 0 beat the baseline.**

Each candidate perturbs PR522's pair-matching table: 1–4 random entries of the 14 blocks × 2 parities, each set to a matching in {0, 1, 2}. With probability 0.4 it also regenerates the Hamming packets with a new orientation seed.

Each candidate then goes through these steps:
- rebuild the factory with PR522's `construct_ranksector.py`;
- transfer PR514's retimed frames (falling back to raw frames);
- keep the frozen gauge/kernel selection, or rescan it exactly;
- read off the local profile and residual widths;
- price b with a fixed proxy: nine-stage one-owner hosting IP, banks allowed.

The rescan reproduces all 99 pivots on the baseline.

- Baseline proxy b = 0.0013733445.
- 171 distinct profile/width classes appeared.
- Best other matching table: 0.0013723655. Many tables reproduce the baseline word exactly.
- Every orientation-seed candidate loses the retimed frames. The best of them is 0.0013613, about 1.2e-5 lower. That comparison is therefore not fair to seeds; see `retry_when` in [results.json](results.json).

All candidates are in [ALL-CANDIDATES.json.gz](ALL-CANDIDATES.json.gz). Scripts are `sweep.py` (per sandbox) and `fleet_sweep.py` (launcher).

Prepared by Rohan Arun with Claude Opus 5.5 (Anthropic) assistance.
