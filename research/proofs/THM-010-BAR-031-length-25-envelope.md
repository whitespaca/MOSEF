# THM-010 and BAR-031: the length-25 finite envelope

## Claim status and scope

- `THM-010`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le25\).
- `BAR-031`: `PROVED` for the exact DEF-032 selector at \(m=25\).
- `REF-033`: `REFUTED`.

No claim below concerns \(m>25\), promise recognition, an asymptotic cap
rate, or general classical polynomial-time factoring.

## BAR-031: two failed schedules and the transition ladder

At \(m=25\), the two M36 schedules give
\[
m+27=52,\qquad
\left\lceil\frac{209m}{100}\right\rceil=53.
\]
The complete balanced population has 196 primes. At cap 52, the nine primes
\[
\{4133,4297,4337,4423,4663,5011,5179,5233,5297\}
\]
share one signature and produce 36 failed pairs across all 11,628
descriptors. Cap 53 removes \(4133\), but the remaining eight-prime bucket
still produces 28 failed pairs across all 12,324 descriptors.

Raw selector inclusion confines every later collision to the cap-52 bucket.
Exact transition checks at caps 52 through 65 give collision-pair counts
\[
36,28,28,15,10,10,10,3,3,3,3,1,1,0.
\]
The last collision is \(\{5011,5179\}\), preserved by every one of the
22,050 cap-64 descriptors.

At cap 65, 23,104 descriptors yield 437 normalized coordinates and 196
distinct signatures. A deterministic 169-coordinate
sublist separates all 19,110 population pairs. The independent dense
verifier checks every cap-52 descriptor on the nine-prime bucket, every
cap-53 descriptor on the eight-prime bucket, every cap-64 descriptor on the
predecessor pair, and every pair in the cap-65 construction. Therefore
\[
L_{25}^\star=65.
\]

## THM-010: repaired finite construction

M36 gives \(t_{24}^\star=27\). Since \(L_{25}^\star-25=40\), DEF-033 gives
\[
t_{25}^\star=40.
\]
Therefore the public factorization-independent selector \(L(m)=m+40\) is
injective on every complete balanced population for \(9\le m\le25\), and
offset 40 is minimal on this finite range.

For multiplicative caps, the new row gives
\[
\frac{L_{25}^\star-1}{25}=\frac{64}{25}>
\frac{25}{12}.
\]
Hence the exact coefficients covering the complete range through 25 are
\(c>64/25\). The endpoint gives the failed cap 64, while \(257/100\) is one
fixed public succeeding witness.

## Cost and recognition

Both repaired schedules remain linear, so DEF-032 gives
\(O(m^3\log m)\) compact modular work, \(O(m^3)\) GCDs and outputs, and
polynomial total bit complexity. Population enumeration, normalization, and
dense expansion are certificate operations only. The balanced promise
remains factor dependent and is not claimed recognizable before factoring.

## Adversarial review

- The additive and multiplicative formulas are evaluated at their distinct
  exact public caps 52 and 53.
- Cap-52 completeness plus raw selector inclusion proves that tracking its
  sole collision bucket is sufficient at every later cap.
- Every cap-52, cap-53, and cap-64 collision member is checked densely.
- Cap-65 injectivity is a complete 196-prime certificate, not sampling.
- Exact threshold minimality follows from the cap-64 collision and raw
  selector inclusion.
- The greedy construction certificate is not claimed minimum.
- The endpoint \(c=64/25\) is excluded by the exact ceiling condition.
- No finite envelope is described as an asymptotic rate.
- General factoring and promise recognition remain open.
