# R480 bit-side followups after PR535

Prepared for rohanarun with OpenAI Codex assistance. These are scoped negative searches, not a new kappa claim.

PR535 moved the bottleneck to the PR510 R480 bit supplier: bit c = 0.001587447106092548137108; conditional global kappa = 0.001584931111785787. The source here is pinned to DreamingOfClouds commit `64edee18af02aab0c1696b677a0287dd0146381b`; its 36 package files match Git blob hashes in `SOURCE-ACQUISITION.json`. Original notices credit the R480/R489 authors, E8 geometry, hosting pipeline, and disclosed Claude assistance.

## What was tested

| Search | Coverage | Outcome |
|---|---|---|
| Single-operation monotone frame reassignment | Exact rational closure of all 672 supplied frames; 99 legal alternatives | No improvement |
| Forward-propagated frame lifts | 93,117 attempted seeds, 103 legal closures | No improvement |
| Odd stage counts | 5 through 31, 14 cases; all width-8 helpers hosted whole, fixed per-replica schedule | 5/7 infeasible in this no-bank model; 9 reproduces the baseline; all tested larger candidates lose |
| Non-root entrance directions, excluding retained totals | 14,706 plane pairs, 118 non-root line classes | Every response class independent |
| Non-root entrance directions, including retained totals | 16,110 plane pairs, 120 non-root line classes, plus 120 root classes | Every response class independent; both F2 elimination algorithms agree |

The scalar program separately passes all 720 arbitrary input columns, restoring sources and helpers and adding each source to its corresponding target. No helper has a zero response column. This does not replace address, physical hosting, or all-size realization proofs.

## Why the expanded kernel screen matters

PR510 checked root-line classes. This screen also checks every non-root rational line shared by distinct first-touch planes. R480 helpers first appear in a root line or a two-dimensional plane. Distinct planes can share at most one line; every plane pair was inspected. Full modular rank four certifies zero intersection over Q, and every remaining pair is resolved by exact rational nullspace computation. All shared non-root lines are collected, with the complete helper class at that direction.

For a line present in just one first-touch plane, its eligible helpers form a subset of that plane's root-line class, already independent. Root lines themselves are checked directly. Therefore there is no nonzero common entrance subspace with dependent response columns among this fixed word's helpers, including its retained-total carriers: any positive-dimensional entrance subspace contains a line covered by the preceding cases. This excludes the shared-response-kernel mechanism on the unchanged first-touch map. It does not exclude a new scalar word, delayed first use, source/helper mixing beyond the model, post-center redesign, or new geometry.

## Limits and retry criteria

The frame screens only use the supplied root-closed frame catalogue, fixed scalar order, and fixed center barriers. The propagated screen chooses minimum-rank catalogue upper frames; it is not a search of all rational subspaces or all simultaneous assignments. Frame costs use floating discovery scores.

The stage screen checks integer pattern/stage constraints and exact rational moment endpoints, but does not emit a physical certificate for each candidate. Its optimizer is floating point; this is not a formally certified global optimum. The five/seven-stage failures concern the no-bank whole-hosting model only. Pooled or asynchronous schedules, banked layouts and changed local words remain outside that screen.

The strongest useful next change is to the scalar circuit or first-touch structure. Repeating the same direction search or supplied-catalogue lifting with unchanged inputs is unlikely to help.

## Reproduction and artifacts

Raw results, complete failed/no-gain profiles, logs and source scripts are retained in the named subdirectories. Scripts resolve paths relative to the original frontier390 workspace; source files are preserved byte-for-byte in `source.tar.gz`; extract it to recover `source/` with the original two-package layout. To reproduce elsewhere, restore those source paths or change only the path configuration, preserving the pinned data and mathematical search parameters. The independent response control accepts paths explicitly:

```sh
python verify_bit510_response_classes.py source/research/e8-r480-dead-totals/data/bitE8mut-r480.json.gz bit510-nonroot-including-totals/ROOTS-AND-SCALAR.json bit510-nonroot-including-totals/RESULT.json /absolute/new/control.json
```

Python 3.11+ is required; SymPy for the rational intersection search and SciPy for stage optimization. The source includes all attribution and license notices. This archive does not assert a new unconditional multiplication theorem or practical runtime gain.
