# THM-012 and BAR-033: the length-27 finite envelope

## Claim status and scope

- `THM-012`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le27\).
- `BAR-033`: `PROVED` for the exact DEF-032 selector at \(m=27\).
- `REF-035`: `REFUTED`.

No claim below concerns \(m>27\), promise recognition, an asymptotic cap
rate, or general classical polynomial-time factoring.

## BAR-033: two failed schedules and the exact transition

At \(m=27\), the two M38 schedules give
\[
m+45=72,\qquad
\left\lceil\frac{27m}{10}\right\rceil=73.
\]
The complete balanced population has 365 primes. At cap 72, the six primes
\[
\{9463,9791,10607,10939,11087,11213\}
\]
share one signature and produce 15 failed pairs across all 31,950
descriptors. Cap 73 separates \(9791\), but the other five primes still
produce ten failed pairs across all 32,400 descriptors.

The cap-72 complete profile has no other collision. Raw selector inclusion
therefore confines every later collision to this bucket. Incrementally
evaluating every newly added descriptor at caps 73 through 87 gives exact
collision-pair counts
\[
15,10,10,3,3,3,3,3,3,1,1,1,1,1,1,0.
\]
The pair \(\{10607,10939\}\) remains equal through all 52,360 cap-86
descriptors.

## The five-coordinate cap-87 repair

Across the descriptors added after cap 72 and through cap 87, 235
nonconstant raw coordinates induce exactly five distinct patterns on the
original six-prime bucket. Deterministic representatives are
\[
\begin{array}{c|cccccc}
\text{source}&9463&9791&10607&10939&11087&11213\\
\hline
\texttt{phi4:11:15:73:second\_stage}&0&1&0&0&0&0\\
\texttt{phi4:15:87:83:cofactor}&0&0&0&1&0&0\\
\texttt{phi4:63:75:24:cofactor}&1&0&0&0&0&0\\
\texttt{phi6:35:75:46:cofactor}&0&0&0&0&1&0\\
\texttt{phi6:53:81:78:cofactor}&0&0&0&0&0&1
\end{array}
\]
Their five-bit signatures are \(4,1,0,2,8,16\). Appending these columns to
the complete 625-column cap-72 normalized signature gives a 630-coordinate
construction certificate separating all 66,430 population pairs.

All five new patterns are necessary for this incremental repair: omitting
the coordinate that isolates any one of the five nonzero-pattern primes
makes that prime share the all-zero new signature of \(10607\). The full
630-coordinate certificate is not claimed minimum. The failed cap-86 pair
and the cap-87 certificate prove
\[
L_{27}^\star=87.
\]

## THM-012: repaired finite construction

M38 gives \(t_{26}^\star=45\). Since \(L_{27}^\star-27=60\), DEF-033 gives
\[
t_{27}^\star=60.
\]
Therefore the public factorization-independent selector \(L(m)=m+60\) is
injective on every complete balanced population for \(9\le m\le27\), and
offset 60 is minimal on this finite range.

For multiplicative caps, the new row gives
\[
\frac{L_{27}^\star-1}{27}=\frac{86}{27}>\frac{35}{13}.
\]
Hence the exact coefficients covering the complete range through 27 are
\(c>86/27\). The endpoint gives the failed cap 86, while \(16/5\) is one
fixed public succeeding witness.

## Cost and recognition

Both repaired schedules remain linear, so DEF-032 gives
\(O(m^3\log m)\) compact modular work, \(O(m^3)\) GCDs and outputs, and
polynomial total bit complexity. Population enumeration, normalization,
dense expansion, and collision-bucket tracking are certificate operations
only. The balanced promise remains factor dependent and is not claimed
recognizable before factoring.

## Adversarial review

- The additive and multiplicative formulas are evaluated at their distinct
  exact public caps 72 and 73.
- Cap-72 completeness plus raw selector inclusion proves that tracking its
  sole collision bucket is sufficient at every later cap.
- Every new descriptor is evaluated exactly once in the cap-73--87
  transition; no sample or omitted intermediate cap is used.
- The cap-72, cap-73, and cap-86 collision buckets are checked by an
  independent dense evaluator.
- Cap-87 injectivity follows from the complete cap-72 signature plus five
  explicit new raw coordinates.
- Only the five new repair coordinates are claimed minimum; the full
  630-coordinate construction certificate is not claimed minimum.
- The endpoint \(c=86/27\) is excluded by the exact ceiling condition.
- No finite envelope is described as an asymptotic rate.
- General factoring and promise recognition remain open.
