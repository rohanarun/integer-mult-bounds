# PR550 Steinberg trace searches: no further gain

Prepared for Rohan Arun with OpenAI Codex assistance. Read-only source: PR550 head `c7337040822978f1611ce9d9d44e7bb96d887e23`, downloaded `source550-review`; candidate reconstructed independently by the parent into `pr550-independent314/local/candidate/FULL-WORD.json.gz`. Vendor files and published packages were not changed.

PR550 uses one exact Steinberg expansion on PR548: two additions become three, permitting lower frames and a better paid profile. Its archived discovery window was256. These followups remove the distance window and test both possible end placements after exact scalar commuting exchanges.

## Results

| Search | Algebraic matches | Exact commuting placement directions | Frame assignments | New gains |
|---|---:|---:|---:|---:|
| 2to3, common replacement frame | 18,105 pairs | 4,203 | 1,782 | 0 |
| 2to3, nested three frames, quotient through3 | 18,105 pairs | 4,203 | 9,130 | 0 |
| 2to3, nested three frames, quotient through4 | 18,105 pairs | 4,203 | 13,290 | 0 |
| 3to2 contraction, nested two frames | 5,741 triples | 380 | 384 | 0 |

The quotient-through4 expansion run encountered no larger frame interval: its candidate intervals were fully enumerated. This does not mean all rewrites of a word were exhausted. The search covers the specified two/three-addition identities, gathering events to the earliest or latest participating position using pairwise commuting scalar events; it does not insert at every interior position or combine multiple neutral moves.

All gates retain their actual rational coefficients. A2to3 pair uses the coefficient product with the correct sign; inverse3to2 requires an existing exact matching bridge coefficient. Frame charges are calculated from the entire affected-register frame chains, then every positive float nomination is subjected to the full unchanged `gk.profile` verifier. Four apparent A-side gains fail that full center/interface check and are excluded. There were no surviving new candidate words or kappa nominations on PR550.

The source-gate arrays, input frames, target caps, centers and boundary data are retained. A winning rewrite would regenerate cleanup exactly and retain its full word plus move evidence; the new results contain none because no gain survived.

## Regression: recovers PR550 exactly

Running the same common-frame all-distance search on the pinned PR548 word finds precisely the known pair at B positions936/1048, in both end placements. It returns the correct delta `+rank1 -rank2 -rank3 +rank4`. The earliest-placement candidate is **byte-identical after decompression** to the independently reconstructed PR550 candidate. See `REGRESSION.json` and the retained `regression548` outputs. These two nominations are an old known improvement, not new winners.

## Files and scope

- `search.py`, `RESULT.json`, `run.log`: common-frame expansion.
- `search_chain.py`, `CHAIN-RESULT.json`, `chain-run.log`: three-frame extension through quotient dimension3.
- `search_chain4.py`, `CHAIN4-RESULT.json`, `chain4-run.log`: completed interval enumeration through dimension4.
- `search_contract.py`, `CONTRACT-RESULT.json`, `contract-run.log`: inverse contraction.
- `regression548`: known-gain control with both exact candidate words.

Run scripts with `PYTHONDONTWRITEBYTECODE=1` and the existing frontier390 Python environment. The default input is the independently rebuilt PR550 word. Optional positional arguments select another source word and an existing output directory; the regression's input provenance is explicitly recorded as PR548. This is a research search, not physical/global admission. No local word change was published and no source package was modified.

Retry conditions: broader identities, an interior insertion placement, a changed scalar word, or a coordinated sequence of neutral moves. Repeating this same all-distance neighborhood on the same head is unlikely to help.
