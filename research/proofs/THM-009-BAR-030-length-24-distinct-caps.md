# THM-009 and BAR-030: the length-24 distinct-cap envelope

## Claim status and scope

- `THM-009`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le24\).
- `BAR-030`: `PROVED` for the exact DEF-032 selector at \(m=24\).
- `REF-032`: `REFUTED`.

No claim below concerns \(m>24\), promise recognition, an asymptotic cap
rate, or general classical polynomial-time factoring.

## BAR-030: two failed schedules and the transition ladder

At \(m=24\), the two M35 schedules separate:
\[
m+24=48,\qquad
\left\lceil\frac{201m}{100}\right\rceil=49.
\]
The complete balanced population has 146 primes. The cap-48 selector has
9,212 descriptors, 73,696 raw primitive coordinates, and 214 normalized
nonconstant coordinates, but
\[
\{3049,3643,3769,3863,4057\}
\]
shares one signature. Thus all ten pair products fail every charged exit.

Cap 49 removes \(3769\) from the bucket but leaves
\[
\{3049,3643,3863,4057\},
\]
so six pair products still fail all 9,408 descriptors. Cap 50 preserves that
same four-prime bucket across all 9,604 descriptors. The complete profiles at
caps 48 through 51 have collision-pair counts
\[
10,\ 6,\ 6,\ 0.
\]

At cap 51, 11,400 descriptors yield 240 normalized coordinates and 146
distinct signatures. A deterministic 130-coordinate sublist separates all
10,585 population pairs. The independent dense verifier checks every cap-48
descriptor on the five-prime bucket, every cap-49 and cap-50 descriptor on
the four-prime bucket, and every pair in the cap-51 construction. Since cap
50 collides and every smaller selector is its subset,
\[
L_{24}^\star=51.
\]

## THM-009: repaired finite construction

M35 gives \(t_{23}^\star=24\). Since \(L_{24}^\star-24=27\), DEF-033 gives
\[
t_{24}^\star=27.
\]
Therefore the public factorization-independent selector \(L(m)=m+27\) is
injective on every complete balanced population for \(9\le m\le24\), and
offset 27 is minimal on this finite range.

For multiplicative caps, the new row gives
\[
\frac{L_{24}^\star-1}{24}=\frac{50}{24}=\frac{25}{12}>2.
\]
Hence the exact coefficients covering the complete range through 24 are
\(c>25/12\). The endpoint gives the failed cap 50, while \(209/100\) is one
fixed public succeeding witness.

## Cost and recognition

Both repaired schedules remain linear, so DEF-032 gives
\(O(m^3\log m)\) compact modular work, \(O(m^3)\) GCDs and outputs, and
polynomial total bit complexity. Population enumeration, normalization, and
dense expansion are certificate operations only. The balanced promise
remains factor dependent and is not claimed recognizable before factoring.

## Adversarial review

- The additive and multiplicative formulas are evaluated at their distinct
  exact public caps 48 and 49.
- Every cap-48, cap-49, and cap-50 collision member is checked densely.
- Cap-51 injectivity is a complete 146-prime certificate, not sampling.
- Exact threshold minimality follows from the cap-50 collision and raw
  selector inclusion.
- The 130-coordinate greedy certificate is not claimed minimum.
- The endpoint \(c=25/12\) is excluded by the exact ceiling condition.
- No finite envelope is described as an asymptotic rate.
- General factoring and promise recognition remain open.
