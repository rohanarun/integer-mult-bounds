# R480 native-fusion and observable-circuit followups

Baseline: [PR539](https://github.com/CrocSwap/integer-mult-bounds/pull/539), conditional kappa0.001584931113695072. All experiments use the unchanged PR510 R480 word at source head64edee18af02aab0c1696b677a0287dd0146381b. Input SHA256 is92e399e9a486b55229b5624632ac54f800dd9e022f2aee97f1e5f264bbc0ef5c. No higher kappa was found in these screens.

| Experiment | Exact outcome and limits |
|---|---|
| Native BIT fusion from PR521 | Original seven-file packet acquired with exact Git blob checks at a190fdb39f31647fc6f651625353710624627348. Independent Python3.14 replay passes344 dirty BIT columns and86 VALUE spectators. It remains a local primitive, not a complete multiplication supplier. |
| Direct transfer to R480 | Exact rational audit checks672 orthogonal frame projectors and2,220 consecutive positive jumps on the720 register chains. Zero pairs meet PR521's common-image rank-one criterion. All480 helpers are used in phase A, so PR535's untouched-before-B post-center template cannot transfer directly either. |
| Same-frame observational retargeting | 9,578 equal-response destination alternatives,629 frame-legal alternatives,227 target-zero gates. No strict floating moment-proxy improvement. |
| Simultaneous target-zero slicing | Remove all227 target-zero A gates and227 corresponding inverse cleanup gates. All720 scalar columns and nesting pass. Profile stays exactly {1:1200,2:1440,4:180,6:120,8:9}; all480 helpers remain used.46 subsequent same-frame retarget alternatives give no gain. |
| Retargeting plus frame changes | After slicing,555 equal-response alternatives tested across all672 existing catalogue frames;112 legal choices, no strict proxy improvement. This does not exhaust new rational frames or multi-gate redesigns. |
| Two-gate cancellations | Two pairs have identical nonzero rank-one target effects. Each passes fresh720-column replay after joint deletion, so cross terms do not invalidate these two deletions. Both retain the same histogram; no gain. |

## Why native fusion does not plug directly into these frame chains

For consecutive nested frames A subset B subset C, let P=Pi_B-Pi_A and Q=Pi_C-Pi_B. These orthogonal projectors satisfy PQ=QP=0. Thus (I-2P)(I-2Q)=I-2(P+Q), an involution with displacement rank rank(P)+rank(Q), at least2. PR521 instead uses distinct oblique rank-one projectors with the same image and PQ=Q, producing a nontrivial rank-one unipotent. The rational audit checks the relevant identities for every distinct observed triple and includes a positive oblique control. Intervening scalar interactions are ignored, so even this relaxed direct matching yields no instance. Center copies and cross-register rewrites are outside the screen.

This is a scoped compatibility obstruction. Redesigned nonorthogonal charts, altered scalar words, new geometry and a complete native BIT module remain open; it is not a universal impossibility result.

## Independent validation and reproduction

The sliced word separately passes the inherited PR370 checker with PR493's explicit mutable-source adaptation under Python3.11.15:720 columns, all120 sources restored, nested frames,671 nondegenerate used frames, unchanged five-stage price. PR425's interface-hypothesis checker also passes. Logs and the exact adaptation are retained under bit510-observable-slice/. These checks are not the full chronological physical-prefix, nine-stage owner, all-size, or emitted phase admission; no runtime speedup or new kappa is claimed from the454 removed scalar instructions.

The search and rational-projector screens ran under Python3.14.8 with SymPy. [reproduce.py](reproduce.py) copies the pinned input and recipes to a fresh caller-selected directory, reruns the native packet and all five screens, and compares mathematical JSON outputs while ignoring timing only. Run `python -B reproduce.py /absolute/new/output` in an environment with SymPy. It does not rerun the separately recorded Python3.11 supplier checker.

Do not repeat these exact neighborhoods without a changed input or search assumption. Most useful next directions are new first-use structure or multioperation changes that alter the paid frame histogram, rather than more fallback repricing or direct same-frame response substitutions.

Prepared for Rohan Arun with OpenAI Codex assistance. PR521: applecrusher with disclosed OpenAI assistance; PR510: DreamingOfClouds with disclosed Claude assistance; PR493: eumemic with disclosed Claude assistance; PR370 checker: Dylan Crow; PR425 interface: Zhihao Chen; inherited engines and credits remain with their authors. Original native-packet attribution and licenses are preserved in the source archive. All inherited theorem-scope assumptions remain conditional.

Fresh packaged replay passed all five screens and the native packet, reproducing every mathematical JSON field; [receipt](PACKAGED-REPLAY.json). Only measured runtime was excluded from equality.
