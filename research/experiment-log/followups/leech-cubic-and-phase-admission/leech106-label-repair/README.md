# Leech106: smaller valid binary label completions

Completed finite improvement: **106 distinct odd ports in23 binary dimensions instead of25**, with the same rank24 scalar Gram transfer and all forced correction caps preserved. The best coordinate-gather copied-rank total falls from576 to453. This is useful compiler evidence, not an admitted supplier or a new kappa.

## Exact outcomes

Both inputs are frozen106-port subsets of the full Leech minimal shell. Only unconstrained binary inner products are changed; real vectors, scalar transfer `T=W W^t/32`, diagonal-one identity and dyadic coefficients are retained.

| Witness seed | Original dimension | New dimension | Label span | New gather-rank total | Original total |
| --- | ---: | ---: | ---: | ---: | ---: |
| 55025 | 25 | 23 | 20 | 453 | 576 |
| 55026 | 25 | 23 | 20 | 457 | 576 |

The better witness has24 gather ranks `19,18,16,19,17,20,20,19,19,19,20,20,19,18,19,19,17,19,19,18,20,20,20,19`. Every one is a proper subspace of the23-dimensional ambient space. Its scalar transfer still has24 real center dimensions; reducing label dimension does not reduce this scalar rank.

## Construction and bounded search

Join ports by an edge whenever their off-diagonal scalar transfer is nonzero. Such edges require orthogonal binary labels. The graphs contain3,081 and3,066 undirected edges, respectively.

For a proper q-coloring, assign each port of color c a label

    p_i = e_c direct_sum z_i direct_sum z_i.

The duplicated tags contribute zero to every binary inner product. Different colors are orthogonal; equal colors have dot product one. Unique tags within each color make the labels distinct, while every label is odd. This construction was previously used for the33-port witness; the new work applies and optimizes it for these106-port graphs.

First,512 DSATUR-style trials across the two graphs found20-colorings and26-dimensional labels. Those valid but larger-ambient results remain in COLOR-RESULT.json. Bounded tabu repair then found19-,18- and17-colorings for both graphs. The17-colorings have at most8 ports per color, so three duplicated tag bits suffice, giving17+6=23dimensions. Sixty-four within-color tag permutations were tested for each retained coloring; exact witness records include the selected assignment.

Sixteen- and fifteen-color attempts ran for22seconds each per input. The best remaining edge conflicts were3/9 for seed55025 and4/10 for seed55026. These are saved failures, not chromatic lower bounds. Greedy cliques of sizes10 and9 are verified lower bounds only; no exact chromatic number is claimed.

## Independent checks and scoped lower bound

verify_labels.py imports neither constructor nor search code. It checks the unchanged source vectors, exact real rank24, scalar Gram matrix and dyadic alphabet; every label's oddness and distinctness; all forced correction orthogonalities; and exact equality of each saved gather span with its required source span. Even, duplicate and deliberately nonorthogonal labels are rejected for every saved witness.

For each17-color completion, the binary Gram rank is17, label-span rank20, and ambient dimension23. The23-dimensional realization is minimal **for that selected color-block Gram with distinct ports**: a color class of7 or8 ports requires at least three radical tag dimensions, and a nondegenerate ambient bilinear space requires at least17+2*3 dimensions. This is not a lower bound for other Gram completions or new scalar transfers.

## Isotropic normals and phase work

The phase lane checked the actual compiler contract and confirmed that canonical frames accept arbitrary independent subspaces, including degenerate ones. An isotropic hyperplane normal is therefore not itself a feasibility obstruction. This lane did not add a gratuitous coordinate to manufacture an odd normal.

The exact23-dimensional witness was supplied to the separate phase lane for actual phase-sensitive frame and adapter checks. This folder claims label/gather validity only; consult that lane's completed receipts for phase results. It does not claim all chronological transitions, dirty-helper scheduling, local paid profile, global owner maps or a finite invoice.

## Why this does not rescue the fixed transfer

The separately frozen leech106-cost-screen certificate proves that every nonzero real gather functional in either fixed transfer rowspace touches at least12 ports. Any rank-r binary subspace contains at most2^(r-1) distinct odd vectors, so each such gather has rank at least5. At least24 independent gathers are needed, giving copied rank at least120>106, independent of this relabeling.

Thus the conventional separately copied-center cover still has negative optimistic deficit for every stage count. Our453/457 totals improve the finite representation but do not evade that stronger cost obstruction. New scalar transfers, auxiliary directions outside the fixed rowspace, or a different center interface remain outside this conclusion.

## Artifacts and reproduction

- COLOR-RESULT.json and COLOR-WITNESSES.json.gz retain the initial larger-ambient completions.
- TABU-RESULT.json and TABU-LOWER-RESULT.json retain successes and failed lower-color searches.
- REPAIRED-WITNESSES.json.gz contains all six final constructive witnesses; select source_seed55025 and dimension23 for the best one.
- REPAIRED-RESULT.json retains all64 tag-order trials per coloring.
- VERIFIED.json is the independent exact audit.

Each repaired witness has vectors (106 by24), labels (106 integer masks), dimension, coloring, gather_frames (24 binary bases), transfer_scaled (106 by106), transfer_denominator32, and tag_seed. Gather j uses the nonzero entries of vectors[:,j]; scatter is vectors/32 and gather is vectors transposed.

Use the frontier verify-sympy314/bin/python with PYTHONDONTWRITEBYTECODE=1. Run color_search.py, tabu_colors.py, tabu_lower.py, build_labels.py, then verify_labels.py. Every process is complete; source pins and all losses are retained. No source-provider or external PR was modified or published.
