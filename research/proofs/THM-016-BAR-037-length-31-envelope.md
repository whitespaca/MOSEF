# THM-016 and BAR-037: the length-31 finite envelope

## Claim status and scope

- `THM-016`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le31\).
- `BAR-037`: `PROVED` for the exact DEF-032 selector at \(m=31\).
- `REF-039`: `REFUTED`.

No claim below concerns \(m>31\), promise recognition, an asymptotic cap
rate, or general classical polynomial-time factoring.

## Both inherited public caps fail

At \(m=31\), the two M42 schedules give
\[
m+93=124,\qquad
\left\lceil\frac{49m}{12}\right\rceil=127.
\]
The complete balanced population has 1,280 primes and 818,560 unordered
pairs. A lossless raw-prefix audit packs the eight primitive charged exits
of each descriptor into one byte. Equality of byte prefixes is exactly
equality of every raw support coordinate; no hash or sampling is used.

The cap-124 selector has 166,050 descriptors and leaves the 18-prime bucket
\[
\begin{split}
\{&33619,34819,35543,36929,37097,37483,37897,38189,38239,\\
  &38933,39863,41627,42323,42473,44621,44963,45259,45329\},
\end{split}
\]
which contributes 153 failed pairs. The cap-127 selector has 180,558
descriptors and leaves the 12-prime bucket
\[
\{33619,34819,36929,37483,37897,38189,38239,38933,
44621,44963,45259,45329\},
\]
which contributes 66 failed pairs. Therefore both inherited formulas fail
on the new complete population, proving `REF-039`.

## Exact transition and threshold

Raw selector inclusion implies that every collision after cap 127 lies in
the displayed 12-prime bucket. Evaluating only newly admitted descriptors
on that complete bucket gives the exact collision-pair ladder
\[
\begin{array}{c|rrrrrrrrrrrrrrrrrr}
L&127&128&129&130&131&132&133&134&135&136&137&138&139&140&141&142&143&144\\
\hline
\#\text{ pairs}&66&66&66&66&21&21&21&21&10&10&6&6&1&1&1&1&1&0.
\end{array}
\]
At caps 139 through 143 the only collision bucket is
\[
\{37483,44963\}.
\]
Cap 144 is injective. Hence
\[
L_{31}^{\star}=144.
\]

## One-coordinate minimum incremental repair

The complete cap-144 normalization starts from 2,100,384 raw coordinates,
removes 2,017,361 constant coordinates and 79,549 duplicate coordinates,
and leaves 3,474 normalized columns. Selecting one cap-143 source for each
old support mask gives 3,361 old representative columns.

Cap 144 adds 1,836 descriptors and 14,688 primitive coordinates. Exactly
one coordinate is nonconstant on the final pair:
\[
\begin{array}{c|rr}
\text{source}&37483&44963\\
\hline
\texttt{phi6:11:105:144:cofactor}&1&0.
\end{array}
\]
Appending it to the 3,361 old representatives gives a 3,362-coordinate
construction certificate separating all 818,560 pairs. Cap 143 still
collides, so a zero-coordinate incremental repair is impossible; the
displayed coordinate suffices. Therefore the minimum incremental repair
size is exactly one. No minimum claim is made for the full
3,362-coordinate construction.

## THM-016: repaired finite construction through length 31

M42 proved that the largest additive offset through length 30 is 93. The
new row gives
\[
L_{31}^{\star}-31=144-31=113.
\]
Therefore the public factorization-independent selector \(L(m)=m+113\) is
injective on every complete balanced population for \(9\le m\le31\), and
113 is the smallest common integer offset on this finite range.

For multiplicative caps, the new endpoint is
\[
\frac{L_{31}^{\star}-1}{31}
 =\frac{143}{31}
 >\frac{61}{15}.
\]
Consequently the exact coefficients covering the complete range through 31
are
\[
c>\frac{143}{31}.
\]
The endpoint gives failed cap 143. The fixed rational witness \(60/13\) is
larger by \(1/403\) and gives
\(\lceil(60/13)31\rceil=144\), so it succeeds.

## Cost and recognition

Both repaired schedules remain linear, so DEF-032 gives
\(O(m^3\log m)\) compact modular work, \(O(m^3)\) GCDs and outputs, and
polynomial total bit complexity. Population enumeration, raw-prefix
comparison, normalization, dense expansion, and collision tracking are
certificate operations only. The balanced promise remains factor dependent
and is not claimed recognizable before factoring.

## Adversarial review

- The inherited additive and multiplicative formulas are evaluated
  separately at their exact public caps 124 and 127.
- One lossless byte stores all eight primitive exits for each descriptor;
  no probabilistic digest decides a collision.
- Raw selector inclusion confines every cap-128--144 collision to the
  complete cap-127 bucket.
- The cap-143 collision and cap-144 injectivity are adjacent exact profiles,
  proving threshold minimality.
- The full cap-144 normalized profile independently has 1,280 distinct
  signatures on the same ordered population.
- A repeated-multiplication evaluator checks all 346,608 public-cap
  descriptors, 983,880 transition local exits, and 14,688 new primitive
  repair coordinates.
- Four selected coordinates additionally pass dense expansion and Rust/C#
  verification.
- The 3,362-coordinate certificate is independently reconstructed and all
  818,560 unordered pairs are checked.
- Only the one-coordinate incremental repair is claimed minimum; the full
  construction is not claimed minimum.
- The new endpoint \(143/31\) is compared against every earlier finite row;
  it is not inferred from a regression or trend.
- General factoring and promise recognition remain open.
