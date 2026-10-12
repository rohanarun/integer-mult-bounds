# Changed stages and ternary reflection geometry: exact discovery screens

This category finishes two previously skipped branches with bounded executable tests. It does not produce a new kappa or an admitted multiplication supplier.

Source anchor: PR548 head `66dbc2bffc1bfa8d50b3f9a2ac7ccba8fd9f6f36`, using the fresh local word and native data-phase recipe already independently replayed by the parent worker.

## Executed results

| Test | Result | Interpretation |
| --- | --- | --- |
| Non-uniform dimensions with the current nine-stage word | Exact binary span rank of all112 ports is9. All nine full-word calls require dimension at least9; the existing common-axis/disjoint-complement layout has only72 private axes, so `sum(h_j-1)=72` forces all nine dimensions to9. | No free variable within this particular layout. New overlapping stage geometry, different numbers of stages, or new local words remain open. This is not a universal no-go theorem for non-uniform scheduling. |
| Literal F3 lift | Tested the first nine axes in each port's first native idle-cover child:77 of112 prefixes fail orthonormality;231 rows become norm zero modulo3. | The existing binary chart cannot simply be relabeled ternary. These are real native chart prefixes, not all2972 complete owner maps. |
| Literal Z4 lift | All112 tested chart prefixes fail orthonormality. | Changing the address algebra to Z4 requires a new construction. Existing Z4-valued *phase exponents* are distinct from using Z4 addresses. |
| New F3 norm-one reflection ports | Dimensions3–8 all pass exhaustive pairwise reflection closure and involution,1,307,655 vector pairs total. Exact normalized real tight-frame identities also pass. | A concrete different-label geometry exists. It is a candidate starting point, not a costed supplier. |
| Six-dimensional126-port scalar transform | All126 input basis vectors pass, totaling15,876 exact output entries. Graph degree45, common neighbors12 for adjacent ports and18 otherwise; `A^2=27I-6A+18J`. | Supplies an exact reference transform and decoder target for further circuit design. No dirty-helper or monotone-frame admission yet. |

## Positive ternary construction

Take projective norm-one vectors in `F3^d`, represented by vectors in `{-1,0,1}^d` whose first nonzero coordinate is1 and whose squared norm is1 modulo3. Reflection is

`r_v(w) = w + (v dot w) v  (mod3)`.

For norm-one `v`, this is an orthogonal involution. The enumerator checks that it preserves the complete chosen port set, for every ordered pair of ports, and returns to `w` after two applications.

| Dimension | Projective ports | Orthogonal neighbors per port | Exact normalized real tight-frame coefficient |
| --- | ---: | ---: | ---: |
| 3 | 3 | 2 | 1 |
| 4 | 12 | 3 | 3 |
| 5 | 45 | 12 | 9 |
| 6 | 126 | 45 | 21 |
| 7 | 351 | 126 | 351/7 |
| 8 | 1080 | 351 | 135 |

The six-dimensional case is relatively close to the current112-port word. Its126 ports consist of6 coordinate lines and120 four-coordinate sign lines. However,729 ternary addresses exceed512 binary addresses in the current9-dimensional binary local space. Fewer coordinates alone are not a saving.

For a clean scalar reference, extend each input evenly to both signs of its line, put zero on other addresses, and apply a radix3 Fourier transform on729 addresses. If `S` is the sum of original inputs, each target output is `(F(q)+S)/3`. The code represents the cubic root of unity by exact integer pairs in `Z[omega]`, with `omega^2+omega+1=0`; no floating Fourier arithmetic is used. This computes the norm-one orthogonality adjacency matrix exactly. The reference uses1458 radix3 butterflies,8748 pair additions and8748 calls to multiplication by omega, plus extension/output costs. These operations are not a supplier rank invoice and the dense reference does not establish a smaller helper count.

## Remaining obligations

1. Synthesize a compact scalar word for the126-port adjacency transform, including arbitrary dirty helpers and cleanup.
2. Construct monotone ternary frames and exact phase/residual-wrapper identities for every used transition.
3. Derive an odd-characteristic global cover and compiler, including the correct recursive child-cost model. Binary moment prices cannot be reused merely by substituting a dimension.
4. Provide physical owner allocation, paid rank profile, deficit, coefficient/tape invoices, and all bootstrap/outer constraints.

The current result supports pursuing step1. It does not establish that the ternary route will beat the current binary design.

## Infrastructure and reproducibility

The main enumerations ran in a fresh Daytona `python:3.12` sandbox created exclusively for this task. The sandbox was deleted after result download; a direct API lookup then returned404. A post-deletion SDK lookup hit a `TypeError`; that diagnostic is retained separately in the receipt, and the HTTP404 is the cleanup evidence. No other sandbox was inspected, changed, or deleted. The scalar reference ran locally on the mounted SSD with Python3.14.8.

- [Exact discovery script](experiments.py), [frozen input](INPUT.json), [results](RESULT.json), [remote output](REMOTE-STDOUT.log).
- [126-port scalar reference](ternary126_transform.py), [exact results](TERNARY126-TRANSFORM.json), [execution log](TERNARY126-TRANSFORM.log).
- [Daytona driver](run_daytona.py), [receipt](DAYTONA-RECEIPT.json), [driver log](DAYTONA-RUN.log). The driver refers to an already-authorized local credential path; it contains no credential and is environment-specific.

Run `python -B experiments.py` and `python -B ternary126_transform.py` in this category directory. No third-party packages are needed for the mathematical tests. The `seconds` fields are nondeterministic timing diagnostics; other mathematical fields are deterministic. `experiments.py` retains some unused chart-construction scratch statements; the tested axes are exactly `INPUT.json.native_axes`, extracted as the first nine axes of the first idle child in the pinned data-phase recipes.

## Primary references

- [Daytona Python SDK](https://www.daytona.io/docs/en/python-sdk/) and [authentication](https://www.daytona.io/docs/api-keys). The installed SDK, rather than presumed latest API compatibility, was inspected before use.
- [MIT notes on quadratic forms over finite fields](https://math.mit.edu/~dav/Fqquadforms.pdf), for odd-characteristic quadratic-space context.
- [Appleby, Properties of the extended Clifford group](https://arxiv.org/abs/0909.5233), for odd-prime-power Clifford representation context. The script does not claim to implement this full theory.

Prepared with OpenAI Codex assistance. Source-derived input remains attributed to the pinned PR548 package and its inherited suppliers.

## Followup: native ternary charts and cap-supported decoders

The failed literal binary-to-ternary lift does **not** prevent constructing native ternary charts. For every126 norm-one port, the followup explicitly constructs a6×6 orthogonal matrix sending the first coordinate axis to that port, and an orientation-corrected determinant-one matrix. Independent row and column Gram checks, first-column comparison and modular Gaussian determinant checks pass for all126 O maps and126 SO maps. Full matrices are retained in [TERNARY126-CHARTS.json](TERNARY126-CHARTS.json).

The adjacency spectrum was computed by exact rational ranks, independently of assuming the strongly regular graph multiplicities:

| Eigenvalue | Multiplicity | Exact rank of A minus eigenvalue times I |
| --- | ---: | ---: |
| 45 | 1 | 125 |
| 3 | 90 | 36 |
| −9 | 35 | 91 |

Two scalar decoders have diagonal one and off-diagonal support only on orthogonal port pairs:

| Decoder | Exact rational rank | Entry alphabet | Scalar rank-one factors required |
| --- | ---: | --- | ---: |
| I−A/3 | 36 | −1/3,0,1 | at least36 |
| I+A/9 | 91 | 0,1/9,1 | at least91 |

Both ranks were computed directly and checked against the verified spectrum. Explicit exact rank factorizations are retained, with multiplication checked against the scaled decoder matrix. The low-rank decoder has eigenvalues−14 once,0 ninety times and4 thirty-five times. Its126/36=3.5 ports per scalar rank compares unfavorably with the current112-port/eight-center construction on this simple burden metric. Scalar rank is not an admitted physical center count or a cost invoice.

### Necessary proper-frame support test

For the rank36 decoder, we enumerated **all364 projective F3 hyperplane normals**. We asked whether its rational column space contains a nonzero direction supported entirely on the ports perpendicular to that normal.

- **252 hyperplanes have no direction.** Full-column-rank modular restrictions were independently certified using252 exact nonzero36×36 integer determinants.
- **112 hyperplanes have five-dimensional direction spaces.** Exact rational nullspaces and all resulting126-coordinate directions are retained. These112 normals are precisely the isotropic normals.
- The resulting **560 directions collectively span only35 dimensions**, and every direction has coordinate sum zero. The rank36 decoder's remaining nonzero-sum component cannot be expressed using these proper-frame directions.

Consequently, an exact **minimum-rank36 scalar factorization entirely through proper ternary support frames is obstructed** for this particular decoder. All proper linear subspaces are contained in an enumerated hyperplane. This does not rule out an overcomplete factorization with cancellation outside the decoder column space, a different decoder, or a changed phase representation.

There is also a geometric caveat: each surviving isotropic normal lies inside its own perpendicular hyperplane, so that hyperplane is degenerate for the standard dot product. It cannot itself have a basis of five mutually orthonormal axes. Survivors therefore are not automatically valid native frame centers.

- [Followup code](ternary_charts_decoders.py), [chart/decoder result](TERNARY126-CHARTS-DECODERS-RESULT.json), [log](TERNARY126-CHARTS-DECODERS.log).
- [Rank36 exact factorization](I_minus_A_over3-FACTORIZATION.json), [rank91 exact factorization](I_plus_A_over9-FACTORIZATION.json).
- [Hyperplane screen](ternary_hyperplane_screen.py), [result](TERNARY126-HYPERPLANE-RESULT.json), [all exclusion/survival witnesses](TERNARY126-HYPERPLANE-WITNESSES.json), [log](TERNARY126-HYPERPLANE.log).
- [Collective-span script](ternary_hyperplane_span.py), [span result](TERNARY126-HYPERPLANE-SPAN.json).

These followups ran locally on the SSD in the existing Python3.14 environment with SymPy/NumPy. The initial generic SymPy dense-rank run was intentionally interrupted after the native charts passed, then resumed with exact DomainMatrix arithmetic using the saved charts. The [initial script](ternary_charts_decoders-before-domainmatrix.py) and [interrupted log](TERNARY126-CHARTS-DECODERS-interrupted.log) preserve that implementation issue. To regenerate everything from scratch, run the initial script only through its chart-generation section, then the current followup, hyperplane, and span scripts in that order. The initial run was stopped for a slower elimination backend, not for a mathematical failure. No additional sandbox was created.
