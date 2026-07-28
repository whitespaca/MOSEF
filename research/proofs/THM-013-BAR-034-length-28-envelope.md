# THM-013 and BAR-034: the length-28 finite envelope

## Claim status and scope

- `THM-013`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le28\).
- `BAR-034`: `PROVED` for the exact DEF-032 selector at \(m=28\).
- `REF-036`: `REFUTED`.

No claim below concerns \(m>28\), promise recognition, an asymptotic cap
rate, or general classical polynomial-time factoring.

## BAR-034: two failed schedules and the exact transition

At \(m=28\), the two M39 schedules give
\[
m+60=88,\qquad
\left\lceil\frac{16m}{5}\right\rceil=90.
\]
The complete balanced population has 507 primes. At cap 88, the six primes
\[
\{11867,12791,13633,13967,14051,15559\}
\]
share one signature and produce 15 failed pairs across all 58,464
descriptors. The 2,679 descriptors added through cap 90 do not separate
any of these pairs, so the multiplicative schedule fails on the same bucket.

The cap-88 complete profile has no other collision. Raw selector inclusion
therefore confines every later collision to this bucket. Incrementally
evaluating every newly added descriptor at caps 89 through 104 gives exact
collision-pair counts
\[
15,15,15,10,6,6,6,3,3,1,1,1,1,1,1,1,0.
\]
The pair \(\{11867,12791\}\) remains equal through all 95,778 cap-103
descriptors.

## The five-coordinate cap-104 repair

Across the descriptors added after cap 88 and through cap 104, 14
nonconstant raw coordinates induce exactly five distinct patterns on the
original six-prime bucket. Deterministic representatives are
\[
\begin{array}{c|rrrrrr}
\text{source}&11867&12791&13633&13967&14051&15559\\
\hline
\texttt{phi4:95:35:7:cofactor}&0&0&0&0&0&1\\
\texttt{phi6:59:75:92:cofactor}&0&0&0&0&1&0\\
\texttt{phi4:55:27:97:cofactor}&0&0&0&1&0&0\\
\texttt{phi4:31:43:91:cofactor}&0&0&1&0&0&0\\
\texttt{phi4:15:99:104:cofactor}&0&1&0&0&0&0
\end{array}
\]
Their five-bit signatures are \(0,16,8,4,2,1\). Appending these columns to
the complete 908-column cap-88 normalized signature gives a 913-coordinate
construction certificate separating all 128,271 population pairs.

All five new patterns are necessary for this incremental repair. The prime
\(11867\) has the all-zero new signature. Each of the other five primes is
nonzero on exactly one of the five available patterns, so omitting that
pattern makes it collide with \(11867\). The full 913-coordinate
certificate is not claimed minimum. The failed cap-103 pair and the
cap-104 certificate prove
\[
L_{28}^\star=104.
\]

## THM-013: repaired finite construction

M39 gives \(t_{27}^\star=60\). Since \(L_{28}^\star-28=76\), DEF-033 gives
\[
t_{28}^\star=76.
\]
Therefore the public factorization-independent selector \(L(m)=m+76\) is
injective on every complete balanced population for \(9\le m\le28\), and
offset 76 is minimal on this finite range.

For multiplicative caps, the new row gives
\[
\frac{L_{28}^\star-1}{28}=\frac{103}{28}>\frac{86}{27}.
\]
Hence the exact coefficients covering the complete range through 28 are
\(c>103/28\). The endpoint gives the failed cap 103, while \(26/7\) is one
fixed public succeeding witness because
\(\lceil(26/7)28\rceil=104\).

## Cost and recognition

Both repaired schedules remain linear, so DEF-032 gives
\(O(m^3\log m)\) compact modular work, \(O(m^3)\) GCDs and outputs, and
polynomial total bit complexity. Population enumeration, normalization,
dense expansion, and collision-bucket tracking are certificate operations
only. The balanced promise remains factor dependent and is not claimed
recognizable before factoring.

## Adversarial review

- The additive and multiplicative formulas are evaluated at their distinct
  exact public caps 88 and 90.
- Cap-88 completeness plus raw selector inclusion proves that tracking its
  sole collision bucket is sufficient at every later cap.
- Every new descriptor is evaluated exactly once in the cap-89--104
  transition; no sample or omitted intermediate cap is used.
- An independent repeated-multiplication evaluator checks every cap-88,
  cap-90, and cap-103 collision descriptor. Selected quotient coordinates
  additionally pass dense expansion and Rust/C# verification.
- Cap-104 injectivity follows from the complete cap-88 signature plus five
  explicit new raw coordinates.
- Only the five new repair coordinates are claimed minimum; the full
  913-coordinate construction certificate is not claimed minimum.
- The endpoint \(c=103/28\) is excluded by the exact ceiling condition.
- No finite envelope is described as an asymptotic rate.
- General factoring and promise recognition remain open.
