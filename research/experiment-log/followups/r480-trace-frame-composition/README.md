# R480 trace and frame composition: success and failed approaches

Published [PR542](https://github.com/CrocSwap/integer-mult-bounds/pull/542) at `fceff375b8308e793afbc684690341fab5affc39`: conditional kappa **0.001587467473762886**, 0.0160671% above PR541. Python 3.14 physical replay and Python 3.11 packaged physical replay pass. All 58 remote package/workflow blobs match local bytes. GitHub CI was queued at publication.

## Experiments and results

| Approach | Outcome |
|---|---|
| Single catalogue frame changes after the 227-gate slice | 98 legal alternatives, no gain |
| Coupled forward catalogue closure | 86,248 seeds, 99 legal closures, no gain |
| Causal minimum operand spans on the sliced original R480 word | 19 reduced frames and three new rank-three closures; conditional kappa 0.001586980532763499 after physical admission |
| Re-minimize the whole sliced PR541 preload word | Loser: prospective kappa 0.001585401901749835; no physical admission claimed for this loser |
| Transfer only the original 19 reductions to the sliced PR541 word | Winner: conditional kappa 0.001587467473762886; independently recounted and physically verified |

PR541 is pinned at `6fd04b2e266b7915b69f96f27758cfce520aa40a`. Its unmodified constructor supplies 60 commuting source preloads. PR510 source is pinned at `64edee18af02aab0c1696b677a0287dd0146381b`. Our slice removes 227 target-zero A gates and their 227 inverse cleanup gates; it alone preserves the paid histogram. The winning transfer changes frames only where the exact gate identities match. All 480 width-eight helpers and the original owner schedule remain.

Do not infer cost optimality from minimum subspace inclusion. Do not add separate profile deltas: the changes interact. A guessed additive profile `{1:1277,2:1301,3:60,4:169,5:1,6:130}` failed an assertion; the actual chain profile is `{1:1286,2:1319,3:45,4:169,5:1,6:130}`. Nine rank-eight center copies are also paid. The failed assertion was observed in command output; no standalone raw log for that assertion was retained.

## Failures and repairs

- First final-price run failed because PROFILE.json had not yet been generated. The subsequent retry also encountered its already-created output directory. The incomplete directory was preserved separately, the actual profile was reconstructed, and a fresh run passed. [Initial failure](initial-missing-profile.log).
- First packaged Python 3.11 run rejected a floating discovery diagnostic: fee_delta -0.044958264775633694 versus -0.04495826477563014. All other non-timing metadata matched. Only fee_delta and elapsed time are omitted from this diagnostic receipt comparison; full words, frames, profiles and rational arithmetic remain exact. [Initial failure](initial311-diagnostic.log), [successful retry](packaged-full311.json).

## Verification and next bottleneck

Fresh replay checks 720 local columns, 960/1440 native formal columns, all 675 frame Grams, both local orientations, 138,240 whole-owner occurrences and 10,500,480 global events. All 18 bridge, 17 parent and 16 hosting mutation controls reject. Invoice: native payload 101 bits below 104; global prefix 191 bits charged 192; two-level coefficient 421 bits charged 512; row coefficient 18355 below 20161. Both Python versions agree on raw records, profile, invoice and kappa.

Two independent rational engines certify bit c=0.001590005077309865651707. The cited unchanged PR535 complex b=0.001589991533606044174031 now binds. Six explicit bootstrap cutoffs, 47 outer inequalities and four invalid-parameter/grid controls pass. Further bit-only improvements cannot raise the headline until the complex supplier or outer transfer improves.

The [complete package](verified-package.tar.gz) includes scripts, byte-preserved dependencies, input words, exact receipts, source notices and a dedicated 3.11/3.14 workflow. This archive is byte-checked against the published package. It includes historical BASE receipts separately from the final composition. No historical campaign trial counts have been changed.

All inherited all-size compiler, common-label/mutable-source, hosting, precision/tape and analytic-transfer assumptions remain conditional. PR535's complex operator is cited, not rebuilt in this composition. These are finite conditional certificates, not a practical runtime gain or full Lean proof.

Credits: Dugongue PR541; DreamingOfClouds PR510; eumemic PR493; icekylinx PR535; Dylan Crow PR370; Zhihao Chen PR425; literal-charge ancestry PR461/464/465/539 and other inherited authors. Our discovery, composition and archive prepared for Rohan Arun with OpenAI Codex assistance. Original notices are retained in the package.
