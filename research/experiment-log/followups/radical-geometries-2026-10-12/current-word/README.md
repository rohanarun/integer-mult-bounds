# Current-word retests and research baseline

Source: PR548 head66dbc2bffc1bfa8d50b3f9a2ac7ccba8fd9f6f36, the exact canonical word already independently replayed. Current submitted composition is PR547, conditional kappa0.001590984155135328. The user-supplied PR523-era table is historical.

## Two executed retests on the changed word

[Connectivity and proportional quotient screen](current-word-screens.json), [full linear-combination quotient screen](current-word-span-screens.json).

- The current word has728 registers, all in one connected component. Thus there is no additional direct-summand deletion in this literal word. This does not exclude a different decoder or a nontrivial restriction of the port set.
- Of842 helper-source climbs,180 have nonempty already-at-frame substitute pools, with260 pool registers counted over all probes. Exact rational tests find zero proportional substitutes and zero linear-combination substitutes after preserving436 protected initial columns. The source, target and already-entered helper columns are protected; only initial cold-helper dirt is ignored. Target registers are excluded from the alternative source pool. No candidate was applied.
- All16,890 scalar elementary operations are invertible: every add has distinct operands and every scale is nonzero. Consequently the older full-register-row substitution test cannot succeed when arbitrary initial register rows are independent. Testing an observable quotient is meaningful; demanding equality of complete independent rows is structurally impossible. Our new quotient test still finds no gain in its specified pool.

These are finite frozen-word screens, not a claim that every frame rewrite or helper reduction fails. A constructed candidate would still need regenerated dirt compensation/cleanup, phase maps, mutable-source checks, complete hosting, invoices and exact prices.

## Stronger reason to change the design

The separately published PR549-dual extension bounds every fractional whole-helper packing of the current fixed PR548 word at complex b<0.001593525797874 and kappa<0.0015909905134466499622: less than0.000399647% improvement over our current submission. Both exact engines and Python3.11/3.14 agree. This explains why the active search now targets changed words, geometry, stage structure or label algebra.

The geometry campaign is split into Leech slices, alternative root systems, and ternary/stage tests. A finite decoder or attractive point set is not a multiplication supplier; report native-frame/dirty-helper/global obligations separately.

Scripts write results beside themselves, load the pinned source through the frontier workspace, and should be run with PYTHONDONTWRITEBYTECODE=1. A one-line exploratory inspection initially had a missing space after the Python keyword `and`; it failed before reading inputs or executing any test, and the corrected inspection succeeded. No experiment result comes from that syntax error.

Prepared for Rohan Arun with OpenAI Codex assistance. Original canonical source and prior experiment authors retain credit.
