# Native complex moment and new Leech experiments

This batch records a small conditional gain and all completed geometry searches, including failed constructions. It does not claim the original 100 proposals are all complete.

## Published conditional gain

[PR559](https://github.com/CrocSwap/integer-mult-bounds/pull/559) composes the native complex moment with eumemic's [PR558](https://github.com/CrocSwap/integer-mult-bounds/pull/558): **kappa = 0.001592517892053334**, up **2.738320e-12** (about **0.00000017194909%**) from PR558. This is a tiny recurrence accounting correction, not a new geometry or a practical speedup.

The complex cover uses exact binary Clifford transitions and a complete child histogram; it does not use the bit supplier's GL local-ring bad-residue selector. Only the extra complex surcharge is removed. The bit surcharge, finite charges and inherited all-size compiler, common-label/mutable-source, hosting, precision/tape and analytic assumptions remain. See the [independent source review](complex552-fallback-independent/README.md). The [discovery audit](complex552-fallback-audit/) preserves earlier provisional screens as historical evidence; the later review and packaged verification supersede pending statuses.

The complete PR558 verifier passed independently at head `060b137c8a6f9d73fd7864c7f8cf2736d6441774`. The new packaged calculation passed on Python 3.11 and 3.14 with identical mathematical outputs. It checks both exact moment engines, endpoint and next tick, unchanged bit contamination, seven bootstrap levels, 47 strict outer inequalities and invalid parameter controls. PR552 regression also passed. [Verification receipts](verification/) separate local verification from observed GitHub CI.

The [PR package archive](native-complex552-publication.tar.gz) preserves the verifier, original notes, inputs, manifest and workflow. The [independent PR558 source/replay archive](pr558-review.tar.gz) preserves all 158 acquired source blobs and fresh physical/admission receipts. [Archive hashes and inventory counts](ARCHIVES.json) were checked against every source file before upload.

## New geometry and word results

| Experiment | Executed result | Interpretation |
| --- | --- | --- |
| [Leech label compression and recentering](leech-label-compression/README.md) | 33 ports: labels reduced from 26 dimensions to 16; copied rank reduced from 62 to 47, then 33. Exact all-coefficient rowspace lower bound proves 33 optimal within that class. | No positive saving in the existing copied-center cover. New transfers or auxiliary gathers outside this rowspace remain open. |
| [Full Leech minimal shell](leech-full-minimal-screen/README.md) | Built actual lattice quotient labels for 98,280 lines. Natural full-shell decoder has 4,600 incompatible cap neighbors per port. A 116-port puncture lacks proper coordinate gathers; two 106-port rank-24 dyadic witnesses pass scalar, cap and proper-gather checks. | Finite candidates only. Native phase admission, chronological dirty-helper word, paid profile and full invoice are missing. |
| [One-to-four commutator routes](trace552-commutator-routes/README.md) | 41,801 compatible routes, 83,602 orientations and 167,480 frame assignments; no gain. Exact dirty-matrix and full-profile controls retained. | Finite tested neighborhood, not a universal impossibility. |

## Failures and next experiments

The native-moment preflight initially paired an invoice with an owner receipt from a different replay. The hash guard rejected it; consistent paired receipts fixed it before any mathematical claim was accepted. The package keeps the original invoice and failure record.

For the 106-port Leech witnesses, proper linear containment is not enough: the common normal is isotropic, and the required native phase/chart completion has not been established. Next work must resolve that interface and cost actual helpers before pricing an outer kappa. For the 33-port transfer, repeating label changes or gather-rowspace basis changes cannot beat the proved copied-rank floor. A different scalar transfer, gathers outside that rowspace with cancellations, or avoiding paid center copies would be a genuinely new experiment.

All jobs in this batch terminated. Scripts, witnesses, rejected cases, exact scope and dependencies are retained. Source authorship and upstream notices remain in each package; new experiments and source audit prepared for Rohan Arun with OpenAI Codex assistance.
