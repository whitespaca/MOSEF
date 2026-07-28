# THM-011 and BAR-032: the length-26 finite envelope

## Claim status and scope

- `THM-011`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le26\).
- `BAR-032`: `PROVED` for the exact DEF-032 selector at \(m=26\).
- `REF-034`: `REFUTED`.

No claim below concerns \(m>26\), promise recognition, an asymptotic cap
rate, or general classical polynomial-time factoring.

## BAR-032: two failed schedules and an incremental repair

At \(m=26\), the two M37 schedules give
\[
m+40=66,\qquad
\left\lceil\frac{257m}{100}\right\rceil=67.
\]
The complete balanced population has 268 primes. At cap 66, the seven primes
\[
\{6229,6703,6793,6947,7187,7229,7649\}
\]
share one signature and produce 21 failed pairs across all 23,465
descriptors. Cap 67 reduces the complete collision set to
\[
\{7187,7229,7649\},
\]
which produces three failed pairs across all 25,938 descriptors.

Raw selector inclusion confines every later collision to the cap-66 bucket.
Exact transition checks at caps 66 through 71 give collision-pair counts
\[
21,3,3,3,3,0.
\]
The final triple remains equal across every one of the 27,876 cap-70
descriptors.

Cap 71 supplies new primitive columns on the final triple. Two public
cofactor columns suffice:
\[
\begin{array}{c|ccc}
\text{source} & 7187 & 7229 & 7649\\
\hline
\texttt{phi4:7:71:65:cofactor} & 0&0&1\\
\texttt{phi4:19:71:50:cofactor} & 0&1&0
\end{array}
\]
Appending these two columns to the complete 561-column cap-67 normalized
signature gives a 563-coordinate construction certificate that separates
all 35,778 population pairs. One binary coordinate cannot separate a
three-member bucket, so two is the minimum number of new coordinates for
this incremental repair. Therefore
\[
L_{26}^\star=71.
\]

## THM-011: repaired finite construction

M37 gives \(t_{25}^\star=40\). Since \(L_{26}^\star-26=45\), DEF-033 gives
\[
t_{26}^\star=45.
\]
Therefore the public factorization-independent selector \(L(m)=m+45\) is
injective on every complete balanced population for \(9\le m\le26\), and
offset 45 is minimal on this finite range.

For multiplicative caps, the new row gives
\[
\frac{L_{26}^\star-1}{26}=\frac{70}{26}=\frac{35}{13}>
\frac{64}{25}.
\]
Hence the exact coefficients covering the complete range through 26 are
\(c>35/13\). The endpoint gives the failed cap 70, while \(27/10\) is one
fixed public succeeding witness.

## Cost and recognition

Both repaired schedules remain linear, so DEF-032 gives
\(O(m^3\log m)\) compact modular work, \(O(m^3)\) GCDs and outputs, and
polynomial total bit complexity. Population enumeration, normalization, and
dense expansion are certificate operations only. The balanced promise
remains factor dependent and is not claimed recognizable before factoring.

## Adversarial review

- The additive and multiplicative formulas are evaluated at their distinct
  exact public caps 66 and 67.
- Cap-66 completeness plus raw selector inclusion proves that tracking its
  sole collision bucket is sufficient at every later cap.
- Every cap-66, cap-67, and cap-70 collision member is checked densely.
- Cap-71 injectivity follows from the complete cap-67 signature plus two
  explicit new raw coordinates, not from sampling or a full-profile
  assumption.
- Exact threshold minimality follows from the cap-70 collision and raw
  selector inclusion.
- Only the two new repair coordinates are claimed minimum; the full
  563-coordinate construction certificate is not claimed minimum.
- The endpoint \(c=35/13\) is excluded by the exact ceiling condition.
- No finite envelope is described as an asymptotic rate.
- General factoring and promise recognition remain open.
