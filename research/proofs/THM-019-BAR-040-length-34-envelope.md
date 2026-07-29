# THM-019 and BAR-040: the length-34 finite envelope

## Claim status and scope

- `THM-019`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le34\).
- `BAR-040`: `PROVED` for the exact DEF-032 selector at \(m=34\).
- `REF-042`: `REFUTED`.

No claim below concerns \(m>34\), promise recognition, an asymptotic cap
rate, or general classical polynomial-time factoring.

## Both inherited public caps fail

At \(m=34\), the M45 schedules give
\[
m+162=196,\qquad
\left\lceil\frac{147m}{25}\right\rceil=200.
\]
The complete balanced population has 3,299 primes and 5,440,051 unordered
pairs. The exact partition-refinement audit appends each descriptor's
eight-bit primitive-exit mask to every still-live equality class. Its
retained buckets are exactly the non-singleton raw-signature equivalence
classes. Appending coordinates cannot merge discarded singletons, so this
is a lossless computation without hashing or sampling.

The cap-196 selector has 664,560 descriptors and leaves the three-prime
bucket
\[
\{97927,99527,127877\},
\]
which contributes three failed pairs. The cap-200 selector has 704,261
descriptors and leaves the pair
\[
\{97927,99527\}.
\]
Thus both inherited formulas fail, proving `REF-042`.

## Exact transition and threshold

Raw selector inclusion confines every post-cap-200 collision to the
displayed pair. Evaluation of every one of the 10,139 newly admitted
descriptors at cap 201 on both primes separates the pair. Hence cap 200 has
one collision while cap 201 has none, and
\[
L_{34}^{\star}=201.
\]

## One-coordinate minimum incremental repair

The split-recording construction contains 3,297 primitive coordinates
through cap 200 and separates every population pair except
\(\{97927,99527\}\). Cap 201 adds 10,139 descriptors and 81,112 primitive
coordinates. Exactly one is nonconstant on the final pair:
\[
\begin{array}{c|rr}
\text{source}&97927&99527\\
\hline
\texttt{phi6:149:201:45:cofactor}&1&0.
\end{array}
\]
Appending it gives a 3,298-coordinate certificate separating all
5,440,051 pairs. Cap 200 proves that zero new coordinates cannot suffice,
and the displayed coordinate suffices, so the minimum incremental repair
size is one. No minimum claim is made for the full construction.

## THM-019: repaired finite construction through length 34

M45 proved that the largest additive offset through length 33 is 162. The
new row gives
\[
L_{34}^{\star}-34=201-34=167.
\]
Therefore \(L(m)=m+167\) is injective on every complete balanced population
for \(9\le m\le34\), and 167 is the smallest common integer offset on this
finite range.

For multiplicative caps, the new endpoint is
\[
\frac{L_{34}^{\star}-1}{34}
 =\frac{200}{34}
 =\frac{100}{17}
 >\frac{194}{33}.
\]
Thus the exact coefficients through length 34 are \(c>100/17\). The
endpoint gives failed cap 200. The Farey-adjacent rational witness \(53/9\)
exceeds the endpoint by \(1/153\) and gives
\(\lceil53\cdot34/9\rceil=201\).

## Cost, recognition, and adversarial review

Both repaired schedules remain linear. DEF-032 therefore retains
\(O(m^3\log m)\) compact modular work, \(O(m^3)\) GCDs and outputs, and
polynomial total bit complexity. Population enumeration, partition
refinement, certificate extraction, dense expansion, and collision tracking
remain certificate operations only. The balanced promise is factor
dependent and is not claimed recognizable before factoring.

The two inherited schedules were evaluated at their distinct exact caps.
All later classes derive from the complete cap-200 bucket, and the adjacent
cap-200/cap-201 profiles prove threshold minimality. Every newly admitted
cap-201 coordinate was checked on the final pair, and the construction was
independently reconstructed and checked on all 5,440,051 pairs. Selected
coordinates also pass dense, Rust, and C# paths. These finite certificates
do not imply a recurrence, density theorem, asymptotic cap rate, promise
recognizer, or solution of general factoring.
