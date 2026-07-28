# THM-014 and BAR-035: the length-29 finite envelope

## Claim status and scope

- `THM-014`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le29\).
- `BAR-035`: `PROVED` for the exact DEF-032 selector at \(m=29\).
- `REF-037`: `REFUTED`.

No claim below concerns \(m>29\), promise recognition, an asymptotic cap
rate, or general classical polynomial-time factoring.

## Exact raw profiles at the two public caps

At \(m=29\), the two M40 schedules give
\[
m+76=105,\qquad
\left\lceil\frac{26m}{7}\right\rceil=108.
\]
The complete balanced population has 685 primes and 234,270 unordered
pairs. A lossless raw-prefix audit packs the eight primitive charged exits
of each descriptor into one byte. Equality of two byte prefixes is exactly
equality of every raw support coordinate at that cap; no hash or sampling is
used.

The cap-105 selector has 99,424 descriptors and 795,392 raw coordinates.
Its 685 raw signatures are distinct. The cap-108 selector has 109,782
descriptors and 878,256 raw coordinates, and its 685 raw signatures are
also distinct. Thus both public schedules survive the new complete
population.

## Exact threshold and single-coordinate repair

The same complete raw audit gives the adjacent profiles
\[
\begin{array}{c|r|r|r}
L&\text{descriptors}&\text{distinct signatures}&\text{collision pairs}\\
\hline
102&89{,}789&684&1\\
103&95{,}778&685&0.
\end{array}
\]
At cap 102, the only collision is
\[
\{18979,21031\}.
\]
Raw selector inclusion implies that every cap below 102 also fails. The
cap-103 injective profile therefore proves
\[
L_{29}^{\star}=103.
\]

The complete cap-103 normalization starts from 766,224 raw coordinates,
removes 733,526 constant coordinates and 31,143 duplicate coordinates, and
leaves 1,555 normalized columns. Independently selecting one cap-102 source
for each old support mask gives 1,527 old representative columns. Among all
5,989 descriptors added at cap 103 and all 47,912 primitive coordinates,
exactly one coordinate distinguishes the predecessor pair:
\[
\begin{array}{c|rr}
\text{source}&18979&21031\\
\hline
\texttt{phi4:87:95:103:cofactor}&0&1.
\end{array}
\]
Appending this coordinate to the 1,527 old representatives gives a
1,528-coordinate construction certificate separating all 234,270 pairs.
At least one new coordinate is necessary because the predecessor pair
collides; the displayed coordinate suffices. Hence the minimum incremental
repair size is exactly one. No minimum claim is made for the full
1,528-coordinate construction.

## THM-014: finite construction through length 29

M40 proved that the largest additive offset through length 28 is attained at
\(m=28\):
\[
L_{28}^{\star}-28=104-28=76.
\]
The new row gives
\[
L_{29}^{\star}-29=103-29=74<76.
\]
Therefore the same public factorization-independent selector
\(L(m)=m+76\) is injective on every complete balanced population for
\(9\le m\le29\), and 76 remains the smallest common integer offset on this
finite range.

For multiplicative caps, the new local endpoint is
\[
\frac{L_{29}^{\star}-1}{29}=\frac{102}{29}
 < \frac{103}{28}.
\]
Consequently the exact coefficients covering the complete range through 29
remain \(c>103/28\), with the controlling failed endpoint still supplied by
the length-28 cap-103 pair. The fixed witness \(26/7\) remains sufficient;
at length 29 it gives cap 108, five above the exact threshold.

## REF-037: threshold monotonicity is false on these populations

The exact finite values satisfy
\[
L_{28}^{\star}=104>103=L_{29}^{\star}.
\]
Thus the hypothesis that \(L_m^\star\) must be nondecreasing between
successive complete balanced populations is false already from 28 to 29.
These populations occupy different prime intervals, so raw selector
inclusion in the cap variable does not imply monotonicity in the input-length
variable. This counterexample does not imply a decreasing trend or any
asymptotic law.

## Cost and recognition

Both surviving schedules remain linear, so DEF-032 gives
\(O(m^3\log m)\) compact modular work, \(O(m^3)\) GCDs and outputs, and
polynomial total bit complexity. Population enumeration, raw-prefix
comparison, normalization, dense expansion, and collision tracking are
certificate operations only. The balanced promise remains factor dependent
and is not claimed recognizable before factoring.

## Adversarial review

- The additive and multiplicative formulas are evaluated separately at
  their exact public caps 105 and 108.
- One lossless byte stores all eight primitive exits for each descriptor;
  no probabilistic digest is used to decide a collision.
- The cap-102 collision and cap-103 injectivity are adjacent exact profiles,
  so raw selector inclusion proves threshold minimality without untested
  intermediate caps.
- The complete cap-103 normalized profile independently has 685 distinct
  signatures on the same ordered population.
- A repeated-multiplication evaluator checks every cap-102 descriptor on the
  final pair and every new cap-103 primitive coordinate. Selected quotient
  coordinates additionally pass dense expansion and Rust/C# verification.
- The 1,528-coordinate certificate is independently reconstructed and all
  234,270 unordered pairs are checked.
- Only the one-coordinate incremental repair is claimed minimum; the full
  construction is not claimed minimum.
- The length-29 local endpoint \(102/29\) does not replace the larger
  length-28 endpoint \(103/28\).
- A decrease from \(L_{28}^{\star}\) to \(L_{29}^{\star}\) is not described
  as an asymptotic trend.
- General factoring and promise recognition remain open.
