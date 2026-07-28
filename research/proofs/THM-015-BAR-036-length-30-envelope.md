# THM-015 and BAR-036: the length-30 finite envelope

## Claim status and scope

- `THM-015`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le30\).
- `BAR-036`: `PROVED` for the exact DEF-032 selector at \(m=30\).
- `REF-038`: `REFUTED`.

No claim below concerns \(m>30\), promise recognition, an asymptotic cap
rate, or general classical polynomial-time factoring.

## Both inherited public caps fail

At \(m=30\), the two M41 schedules give
\[
m+76=106,\qquad
\left\lceil\frac{26m}{7}\right\rceil=112.
\]
The complete balanced population has 927 primes and 429,201 unordered
pairs. A lossless raw-prefix audit packs the eight primitive charged exits
of each descriptor into one byte. Equality of byte prefixes is exactly
equality of every raw support coordinate; no hash or sampling is used.

The cap-106 selector has 100,380 descriptors and leaves the 14-prime bucket
\[
\begin{split}
\{&26297,27701,28447,28591,29131,29209,29387,\\
  &30817,31177,31327,31723,31849,32027,32633\},
\end{split}
\]
which contributes 91 failed pairs. The cap-112 selector has 121,878
descriptors and leaves the nine-prime bucket
\[
\{26297,27701,28591,29209,29387,30817,31177,31849,32027\},
\]
which contributes 36 failed pairs. Therefore both inherited formulas fail
on the new complete population, proving `REF-038`.

## Exact transition and threshold

Raw selector inclusion implies that every collision after cap 112 lies in
the displayed nine-prime bucket. Evaluating only newly admitted descriptors
on that complete bucket gives the exact collision-pair ladder
\[
\begin{array}{c|rrrrrrrrrrrr}
L&112&113&114&115&116&117&118&119&120&121&122&123\\
\hline
\#\text{ pairs}&36&36&36&21&21&21&15&10&10&3&3&0.
\end{array}
\]
At caps 121 and 122 the only collision bucket is
\[
\{28591,29209,29387\}.
\]
Cap 123 is injective. Hence
\[
L_{30}^{\star}=123.
\]

## Two-coordinate minimum incremental repair

The complete cap-123 normalization starts from 1,317,600 raw coordinates,
removes 1,264,248 constant coordinates and 50,849 duplicate coordinates,
and leaves 2,503 normalized columns. Selecting one cap-122 source for each
old support mask gives 2,401 old representative columns.

Cap 123 adds 11,030 descriptors and 88,240 primitive coordinates. Exactly
two coordinates are nonconstant on the final triple:
\[
\begin{array}{c|rrr}
\text{source}&28591&29209&29387\\
\hline
\texttt{phi4:123:59:87:cofactor}&0&0&1\\
\texttt{phi4:79:123:54:cofactor}&1&0&0.
\end{array}
\]
Appending both to the 2,401 old representatives gives a 2,403-coordinate
construction certificate separating all 429,201 pairs. One binary
coordinate can assign at most two signatures to three primes, so at least
two new coordinates are necessary. The displayed pair suffices. Therefore
the minimum incremental repair size is exactly two. No minimum claim is
made for the full 2,403-coordinate construction.

## THM-015: repaired finite construction through length 30

M41 proved that the largest additive offset through length 29 is 76. The
new row gives
\[
L_{30}^{\star}-30=123-30=93.
\]
Therefore the public factorization-independent selector \(L(m)=m+93\) is
injective on every complete balanced population for \(9\le m\le30\), and
93 is the smallest common integer offset on this finite range.

For multiplicative caps, the new endpoint is
\[
\frac{L_{30}^{\star}-1}{30}
 =\frac{122}{30}
 =\frac{61}{15}
 >\frac{103}{28}.
\]
Consequently the exact coefficients covering the complete range through 30
are
\[
c>\frac{61}{15}.
\]
The endpoint gives failed cap 122. The fixed rational witness \(49/12\) is
larger by \(1/60\) and gives
\(\lceil(49/12)30\rceil=123\), so it succeeds.

## Cost and recognition

Both repaired schedules remain linear, so DEF-032 gives
\(O(m^3\log m)\) compact modular work, \(O(m^3)\) GCDs and outputs, and
polynomial total bit complexity. Population enumeration, raw-prefix
comparison, normalization, dense expansion, and collision tracking are
certificate operations only. The balanced promise remains factor dependent
and is not claimed recognizable before factoring.

## Adversarial review

- The inherited additive and multiplicative formulas are evaluated
  separately at their exact public caps 106 and 112.
- One lossless byte stores all eight primitive exits for each descriptor;
  no probabilistic digest decides a collision.
- Raw selector inclusion confines every cap-113--123 collision to the
  complete cap-112 bucket.
- The cap-122 collision and cap-123 injectivity are adjacent exact profiles,
  proving threshold minimality.
- The full cap-123 normalized profile independently has 927 distinct
  signatures on the same ordered population.
- A repeated-multiplication evaluator checks all 222,258 public-cap
  descriptors, 385,398 transition local exits, and 88,240 new primitive
  repair coordinates.
- Four selected coordinates additionally pass dense expansion and Rust/C#
  verification.
- The 2,403-coordinate certificate is independently reconstructed and all
  429,201 unordered pairs are checked.
- Only the two-coordinate incremental repair is claimed minimum; the full
  construction is not claimed minimum.
- The new endpoint \(61/15\) is compared against every earlier finite row;
  it is not inferred from a regression or trend.
- General factoring and promise recognition remain open.
