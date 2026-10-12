# Leech106: exact copied-center cost obstruction

Date: 2026-10-12. Status: **both106-port natural-Gram witnesses fail the conventional copied-center cover, even after arbitrary gather-basis recombination**. No phase check, dirty-word construction or new kappa is claimed in this lane.

This batch uses the two frozen106-port witnesses with seeds55025 and55026 from `leech-full-minimal-screen`. Their scalar transfer is `T=W W^t/32`, with real rank24 and106distinct odd binary ports. It does not rerun a full-shell census or duplicate the phase lane.

## Direct accounting

Independent GF2 source-span calculations give rank24 for each of the24 coordinate gathers in both witnesses. Their direct copied-rank charge is therefore576. The conventional per-replica deficit is

`delta(L)=(L−1)*106−L*C`.

With C=576 this is `−470L−106`, negative for every positive stage count. This remains a failure if every other helper, idle, padding, phase and fallback cost is granted free.

## Arbitrary recombinations also fail

The direct cost alone does not rule out a better gather basis. We therefore established an exact bound for **every nonzero real functional on either retained port matrix**, not a sampled coefficient catalog.

For each106×24 port matrix W, the script found four disjoint24-row invertible bases, using96different ports. For each basis, it reconstructed the exact global response to basis-value coordinates. A functional that is nonzero at at most two positions of that basis lies in one of the276two-coordinate response families.

Within each such family, the zero ports can be classified exhaustively using exact projective ratios of the two response columns. This covers every real coefficient ratio, including directions with one zero coefficient. No rounding or finite coefficient grid is involved.

| Witness | Number of disjoint bases | Families checked | Minimum nonzero ports in each basis's two-coordinate families |
| --- | --- | --- | --- |
| seed55025 | 4 | 1,104 | 62,63,60,67 |
| seed55026 | 4 | 1,104 | 61,55,66,59 |

If a nonzero functional had at most11nonzero ports in total, one of the four disjoint bases would contain at most2of them. It would then belong to a tested two-coordinate family, each of which has more than11nonzero ports. Contradiction. Thus **every nonzero functional has at least12nonzero ports**. This is a certified lower bound, not a claim that support12 is attained.

A binary subspace of dimension r contains at most `2^(r−1)` odd vectors. Consequently a gather containing12distinct odd port labels must have rank at least5. This counting argument holds regardless of how those distinct odd labels are represented.

Any collection of gathers spanning the24-dimensional rowspace of T must contain at least24independent nonzero rows. Its copied-rank charge is therefore

`C>=24*5=120>106`.

Hence, even after arbitrary coefficient changes and overcomplete spanning collections **within this same transfer rowspace**,

`delta(L)<=−14L−106<0`

for every positive stage count. This is an all-rowspace proof, not a catalog-only result. The lower bound120 is not presented as an attainable factorization cost.

## Scope and the remaining escape routes

This rejects the conventional separately copied-center cover for these two106-port natural-Gram transfers. It also covers every minimal-rank24-center factorization of either transfer, since its gather rowspace must equal the transfer rowspace.

It does **not** reject another scalar transfer, gather directions outside this rowspace with cancelling auxiliary contributions, a new copied-center interface, or Leech geometry generally. In particular, it does not apply to the separately investigated full-shell cubic transfer that cancels inner-product-two corrections.

Because this cost obstruction is already decisive in the optimistic model, this lane does not expend work on recentering catalogs, a full paid profile or global admission. The independent phase lane may still provide useful compiler evidence; no phase conclusion is inferred here.

## Retained evidence

- `INPUT.json.gz`: the two exact frozen106-port witnesses.
- `SPARSE-FUNCTIONAL-CERTIFICATES.json.gz`: all eight basis index sets, exact rational coordinate maps, integer global response matrices and all2,208pair-family minima.
- `RESULT.json`: source-span charges, functional-support proof and cover obstruction.
- `verify_certificates.py`: independent checker using rational slopes instead of the constructor's gcd-normalized projective keys.
- `VERIFIED.json`: independent checks and rejection of a mutated response matrix and duplicated basis row.

Run `screen_cost.py`, then `verify_certificates.py` with SymPy Python and `PYTHONDONTWRITEBYTECODE=1`. Inputs and outputs are local to this folder. Source hashes are retained in `SOURCES.json`; `MANIFEST.json` covers every batch file except itself. Prior research folders remain unchanged.
