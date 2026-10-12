from pathlib import Path
import json,shutil,hashlib,os
R=Path(__file__).resolve().parent;assert os.path.ismount('/Volumes/SP AI 01_16') and os.access(R,os.W_OK)
P=R/'trace550-retiming-publication';D=P/'research/complex-trace-joint-retiming';D.mkdir(parents=True,exist_ok=False)
shutil.copytree(R/'source550-review',D/'upstream550')
for f in ['WORD.json.gz','PRICE.json','PLAN.json','CONSTRUCTION.json']:shutil.copy2(R/'trace550-retimed-candidate'/f,D/f)
shutil.copy2(R/'source550-acquisition.json',D/'UPSTREAM-ACQUISITION.json')
shutil.copy2(R/'source550-review/LICENSE',D/'LICENSE')
(D/'README.md').write_text('''# Joint frame retiming of the rank-five trace word

Draft candidate: conditional kappa **0.001591209947088545**, complex b **0.001593745931467828731002**. This is about0.01033% above PR550's0.001591045666134196, with the unchanged PR543 R420 bit supplier.

This applies120 jointly chosen frame changes to PR550's exact scalar word, preserving all scalar instructions, entrances, ports, centers, cut and target levels. The local paid profile changes from `{1:2285,2:455,3:487,4:169,5:56,6:56,8:8}` to `{1:2276,2:514,3:404,4:204,5:56,6:56,8:8}`. Rank mass and helper widths remain fixed. The frozen literal owner plan changes only its paid profile. No extra bit-side gain is claimed.

Two independent rational engines certify the candidate full-profile b and reject its next10^-24 tick. The numerical outer nomination passes47 strict constraints. **At draft publication full independent phases, owner replay and fresh invoice/assembly admission are pending.** The current artifact is a priced candidate, not an admitted new winner. Verification updates will retain this initial status.

`CONSTRUCTION.json` lists all120 frame changes. `WORD.json.gz`, `PLAN.json` and `PRICE.json` are frozen inputs and exact pricing evidence. `upstream550/` is the complete83-file dependency-closed package from PR550 head c7337040822978f1611ce9d9d44e7bb96d887e23, acquired with exact Git blob binding. It retains its own manifests and sources. Its root verifier replays the unchanged upstream witness; it is not the verifier of this candidate. A candidate verifier and fresh receipts will accompany the admission update.

The discovered schedule came from the credited PR534 frame-chain search, with seed55001,60seconds, temperature0.002 and exponent0.001593581126479114854212, using the causal minimum frames as lower bounds. Its floating objective only nominated this witness; exact engines and physical checkers decide admission. Seed55002 at temperature0.03 found no gain. All single-event changes were separately excluded at the baseline exponent, so this gain requires coordinated frame changes rather than one greedy edit.

Conditional scope remains inherited: all-size compiler, common-label/mutable-source realization, whole-call hosting, precision/tape and analytic-transfer contracts. This is not an unconditional multiplication theorem, practical speedup or complete Lean proof.

Prepared for Rohan Arun with OpenAI Codex assistance. Credits: eumemic/Codex PR550 trace expansion and admission, rohanarun/Claude PR534 frame-chain method, Dugongue PR548/PR541, icekylinx PR535/PR531, chafreaky PR544, eumemic/Claude PR543 bit supplier, DreamingOfClouds PR484 and the inherited gauge/kernel/phase/moment ancestry. Original notices and licenses remain in upstream550.
''')
(D/'STATUS.json').write_text(json.dumps(dict(status='DRAFT_EXACT_PROFILE_NOMINATION_PHYSICAL_PENDING',kappa='0.001591209947088545',complex_b='0.001593745931467828731002',baseline_pr=550,baseline_head='c7337040822978f1611ce9d9d44e7bb96d887e23'),indent=2)+'\n')
(D/'MANIFEST.json').write_text(json.dumps({f.relative_to(D).as_posix():hashlib.sha256(f.read_bytes()).hexdigest()for f in sorted(D.rglob('*'))if f.is_file()and f!=D/'MANIFEST.json'},indent=2)+'\n')
(R/'TRACE550-RETIMING-PR-BODY.md').write_text('''Draft priced candidate: conditional **κ =0.001591209947088545**, about **0.01033% above #550** at c7337040822978f1611ce9d9d44e7bb96d887e23. Complex b=0.001593745931467828731002; cited unchanged #543 bit c=0.001653826988146798944268.

Jointly retime120 frames in #550's scalar word. All scalar instructions and interfaces are preserved; local profile becomes `{1:2276,2:514,3:404,4:204,5:56,6:56,8:8}`. Both rational price engines agree and reject the next b tick. The outer nomination passes47 strict constraints.

**Submitted before full verification as requested: native phase replay, whole-owner admission, fresh invoice and final assembled receipt are running/pending. This is a candidate, not yet an independently admitted new winner.** Complete frozen source, candidate word, exact prices and change list are included; verifier and admission receipts will follow.

Conditional on inherited all-size compiler, common-label/mutable-source, whole-call hosting, precision/tape and analytic-transfer assumptions. No unconditional theorem or practical-speedup claim. Unchanged #543 bit supplier is cited, not rebuilt in this package.

Prepared for Rohan Arun with OpenAI Codex assistance. Credits: eumemic/Codex #550; rohanarun/Claude #534 frame-chain search; Dugongue #548/#541; icekylinx #535/#531; chafreaky #544; eumemic/Claude #543; DreamingOfClouds #484 and inherited ancestry. Notices/licenses retained.
''')
print(sum(f.is_file()for f in P.rglob('*')))
