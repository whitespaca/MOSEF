# THM-008 and BAR-029: the length-23 finite envelope

## Claim status and scope

- `THM-008`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le23\).
- `BAR-029`: `PROVED` for the exact DEF-032 selector at \(m=23\).
- `REF-031`: `REFUTED`.

No claim below concerns \(m>23\), promise recognition, an asymptotic cap
rate, or general classical polynomial-time factoring.

## BAR-029: recurrence and transition ladder

At \(m=23\), both M34 schedules give
\[
m+17=\left\lceil\frac{173m}{100}\right\rceil=40.
\]
The complete balanced population has 109 primes. The cap-40 selector has
5,148 descriptors, 41,184 raw primitive coordinates, and 160 normalized
nonconstant coordinates, but
\[
\{2411,2477,2741,2777,2837\}
\]
shares one signature. Thus all ten pair products fail every charged exit.

The complete profiles at caps 40 through 47 have collision-pair counts
\[
10,\ 10,\ 10,\ 6,\ 3,\ 3,\ 1,\ 0.
\]
At cap 46, \(\{2411,2777\}\) still collides across all 7,470 descriptors.
At cap 47, 9,016 descriptors yield 190 normalized coordinates and 109
distinct signatures. A deterministic 94-coordinate sublist separates all
5,886 population pairs.

The independent dense verifier checks every cap-40 descriptor on the full
five-prime bucket, every cap-46 descriptor on the predecessor pair, and every
pair in the cap-47 construction. Since cap 46 collides and every smaller
selector is its subset,
\[
L_{23}^\star=47.
\]

## THM-008: repaired finite construction

M34 gives \(t_{22}^\star=17\). Since \(L_{23}^\star-23=24\),
DEF-033 gives
\[
t_{23}^\star=24.
\]
Therefore the public factorization-independent selector \(L(m)=m+24\) is
injective on every complete balanced population for \(9\le m\le23\), and
offset 24 is minimal on this finite range.

For multiplicative caps, the new row gives
\[
\frac{L_{23}^\star-1}{23}=\frac{46}{23}=2>\frac{19}{11}.
\]
Hence the exact coefficients covering the complete range through 23 are
\(c>2\). The endpoint \(c=2\) gives the failed cap 46, while \(201/100\) is
one fixed public succeeding witness.

## Cost and recognition

Both repaired schedules remain linear, so DEF-032 gives
\(O(m^3\log m)\) compact modular work, \(O(m^3)\) GCDs and outputs, and
polynomial total bit complexity. Population enumeration, normalization, and
dense expansion are certificate operations only. The balanced promise
remains factor dependent and is not claimed recognizable before factoring.

## Adversarial review

- Both failed M34 formulas are evaluated at their exact common public cap 40.
- Every cap-40 and cap-46 collision member is checked densely.
- Cap-47 injectivity is a complete 109-prime certificate, not sampling.
- Exact threshold minimality follows from the cap-46 collision and raw
  selector inclusion.
- The 94-coordinate greedy certificate is not claimed minimum.
- The endpoint \(c=2\) is excluded by the exact ceiling condition.
- No finite envelope is described as an asymptotic rate.
- General factoring and promise recognition remain open.
