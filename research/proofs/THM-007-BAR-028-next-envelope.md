# THM-007 and BAR-028: the next finite-envelope jump

## Claim status and scope

- `THM-007`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le22\).
- `BAR-028`: `PROVED` for the exact DEF-032 selector at \(m=22\).
- `REF-030`: `REFUTED`.

No claim below concerns \(m>22\), promise recognition, an asymptotic cap
rate, or general classical polynomial-time factoring.

## BAR-028: recurrence of both repaired formulas

At \(m=22\), both M33 schedules give
\[
m+12=\left\lceil\frac{153m}{100}\right\rceil=34.
\]
The complete balanced population has 80 primes. The cap-34 selector has
2,838 descriptors, 22,704 raw primitive coordinates, and 83 normalized
nonconstant coordinates, but it leaves two collision buckets:
\[
\{1481,1511,1571,1663,1721,1747,1867,1931,2029\},
\qquad
\{1907,1999\}.
\]
Thus 37 distinct semiprime pairs fail every charged exit.

The independent dense verifier evaluates every cap-34 descriptor on both
complete buckets. The same verifier also checks every cap-38 descriptor on
the final predecessor collision \(\{1481,1571\}\). These are exact
descriptor-by-descriptor failures, not sampled collisions.

## Exact repair threshold

The complete profiles at caps 34 through 39 have respectively
\[
71,\ 75,\ 76,\ 77,\ 79,\ 80
\]
distinct signatures. Their collision-pair counts are
\[
37,\ 15,\ 10,\ 6,\ 1,\ 0.
\]
At cap 39, 5,016 descriptors yield 115 normalized coordinates and 80
distinct signatures. A deterministic 73-coordinate sublist has pairwise
distinct packed signatures; the dense verifier checks all 3,160 population
pairs.

Because cap 38 still collides and every smaller selector is its subset, cap
39 is the exact first injective cap:
\[
L_{22}^\star=39.
\]

## THM-007: repaired finite construction

M33 gives \(t_{21}^\star=12\). Since \(L_{22}^\star-22=17\),
DEF-033 gives
\[
t_{22}^\star=17.
\]
Therefore the public factorization-independent selector with
\[
L(m)=m+17
\]
is injective on every complete balanced population for \(9\le m\le22\) and
exposes a proper factor of every distinct-prime balanced semiprime in this
finite range. Offset 17 is minimal because offset 16 gives cap 38 and retains
the registered predecessor collision.

For multiplicative caps, the new row gives
\[
\frac{L_{22}^\star-1}{22}=\frac{38}{22}=\frac{19}{11}>
\frac{32}{21}.
\]
Hence the exact coefficients covering the complete range through 22 are
\(c>19/11\). The old witness \(153/100\) fails; \(173/100\) is one fixed
public succeeding witness.

## Cost and recognition

Both repaired schedules remain linear, so DEF-032 gives
\(O(m^3\log m)\) compact modular work, \(O(m^3)\) GCDs and outputs, and
polynomial total bit complexity. Population enumeration, normalization, and
dense expansion are certificate operations only. The balanced promise
remains factor dependent and is not claimed recognizable before factoring.

## Adversarial review

- Both failed M33 formulas are evaluated at their exact common public cap 34.
- Every member of both cap-34 buckets is checked by an independent dense
  evaluator.
- Cap 38 retains an independently checked collision, proving failure of all
  smaller caps by raw selector inclusion.
- Cap-39 injectivity is a complete 80-prime certificate, not sampling.
- The 73-coordinate greedy certificate is not claimed minimum.
- \(c=19/11\) is excluded because the ceiling condition is strict.
- No finite envelope is described as an asymptotic rate.
- General factoring and promise recognition remain open.
