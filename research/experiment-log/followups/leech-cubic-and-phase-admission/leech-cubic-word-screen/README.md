# Leech cubic word-cost screen

The new full-shell cubic decoder passes the algebraic and label-cap screens, but its simplest pure-source-copy factory cannot beat the current complex supplier. An exact rational necessary-condition check gives **b < 0.00137** for every positive integer stage count in the same uniform-stage accounting. This is a bound on that factory and cover model, not on Leech geometry or all circuits for the cubic decoder. No new kappa is claimed.

## What is being priced

The pinned decoder has 98,280 ports, 2,600 designated centers, ambient dimension 26, and one common 25-dimensional gather space U. Its copied-center charge is C=65,000. All source labels lie in U and are odd. Therefore U is not contained in any target's orthogonality cap: each target's own odd label is a witness.

The concrete E7 factory in `references/build.py` makes source copies at the source's native one-dimensional frame, uses copies in gathers and side corrections, compensates arbitrary initial helper dirt, and restores helpers. For this new cubic factorization all gathers share U, so one source copy can feed every center. It is unnecessary to make a separate copy for every nonzero coefficient.

But a pure-source carrier that has reached U cannot serve any later side correction. In this factory class, retaining both a gather delivery and a native correction delivery for each port needs at least one extra carrier per port, in addition to the 2,600 designated centers. This includes exchanging the roles of the original input and its copy. The class does not permit replacing individual-source corrections by mixed or coded carriers, repurposing designated centers as a different decoder, or changing the frame interface. The result does not lower-bound those other constructions.

Even granting every B correction for free, helper stock is at least R=100,880. For zero-start helpers, the actual local profiler's telescoping rank identity gives

```
M = 2*v*(h-1) + h*R + C
  = 7,601,880.
```

This counts source climbs from their native line to the full frame, target climbs from zero to their native cap, every helper's zero-to-full traversal, and copied-center rank. Extra carrier copies only increase M. The E7 constructor/audit and result are retained as the concrete interface reference. We have not emitted or admitted a full Leech dirty-register word.

## Normalization and exact exclusion

For the prospective uniform-stage extension, m=1+(h-1)L=25L+1. Let T denote the number of invocation replicas after canceling the common group multiplicity. The existing cover accounting has

```
global_profile = T*L*local_profile + nonnegative_idle_profile
global_deficit = T*((L-1)*v - L*C).
```

These identities are not inferred from the E7 approximation. `verify.py` checks the corresponding admitted PR558 receipt: T=8, L=9, exactly 72 copies of its local profile, and deficit 8*(8*112-9*64)=2,560. The remaining owner calls have nonnegative counts and include rank 48. `references/prepare_supplier_base.py` and `emit_supplier_hosted.py` show literal local-call accumulation and owner remainder accounting. The original three-stage complex note records the same copied-center deficit at L=3. A general h26 controller has not been emitted or physically admitted; our statement is conditional on using this unchanged accounting extension.

Only **local paid ranks** are bounded by h=26. Global idle/padding ranks can be larger. We drop their nonnegative moment excess, not their baseline mass. Dividing the necessary global moment condition by T gives

```
L * sum_r H[r]*r*((m/r)^b - 1) < (L-1)*v - L*C.
```

Since r<=26 for the local transitions and exp(x)-1>x, the left side exceeds L*b*M*log(m/26). Thus a necessary condition is

```
b < (33,280 - 98,280/L) / (M*log((25L+1)/26)).
```

`screen.py` and independently implemented `verify.py` prove rejection at b=137/100000 using 128 positive rational terms of the logarithm's atanh series. They check L=3 through 63 individually and use monotonicity of the logarithm plus deficit/L<33,280 for every L>=64. L=1,2 already have nonpositive deficit. This also covers all potentially relevant odd L; checking even L only strengthens the relaxation. A floating diagnostic gives a maximum upper-bound expression of about 0.001360627 at L=10 and is not the certificate.

The negative control omitting all carrier-copy rank fails this rejection, while positive optimistic delta at L=3 remains 1,560. This isolates why counting only copied-center deficit was misleading.

## Original-source excursions

An alternative is to move each original input p -> U, feed every center, and return U -> p instead of retaining a copy. Scalar algebra permits this: side corrections modify target registers, not x, so inverse gather still restores arbitrarily dirty centers. `excursion_control.py` checks a six-register, two-center dyadic example on every scalar basis column. Omitting a dirt compensator or cleanup gate is rejected.

The current monotone profiler rejects U -> p. Even a generalized phase/frame implementation must pay it. A single round trip adds 2*(25-1)=48 ranks per port beyond the unchanged endpoint traversal, or 4,717,440 ranks per local invocation. Because no additional live helper bank balances these new transitions, the same-cover deficit becomes

```
(33,280 - 4,717,440)*L - 98,280
= -4,684,160*L - 98,280 < 0.
```

Thus it fails even at b=0. Repeating the excursion during inverse gather would add another 48 per port; the rejection already grants that inverse extra for free. The toy is a scalar/frame-distance control, not a full 26-dimensional Clifford replay.

## Next useful direction

Do not generate the billions of individual side-correction operations for this factory. The next useful construction must change the inventory argument: exploit mixed/coded carriers or response kernels with a new dirty-word schedule, or change the decoder/label/cover combination. Merely sharing the 2,600 gathers on one frame is already included in the losing bound. The cubic decoder remains a valid finite construction worth retaining; it has not produced a competitive paid supplier.

`RESULT.json`, `VERIFIED.json`, and `EXCURSION.json` separate the exact arithmetic exclusion, reference normalization, and successful scalar/failed cost controls. `SOURCES.json` pins research inputs; `MANIFEST.json` pins this package. Existing frozen research and provider sources were not modified.
