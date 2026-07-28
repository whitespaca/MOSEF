# THM-017 and BAR-038: the length-32 finite envelope

## Claim status and scope

- `THM-017`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le32\).
- `BAR-038`: `PROVED` for the exact DEF-032 selector at \(m=32\).
- `REF-040`: `REFUTED`.

No claim below concerns \(m>32\), promise recognition, an asymptotic cap
rate, or general classical polynomial-time factoring.

## Both inherited public caps fail

At \(m=32\), the two M43 schedules give
\[
m+113=145,\qquad
\left\lceil\frac{60m}{13}\right\rceil=148.
\]
The complete balanced population has 1,750 primes and 1,530,375 unordered
pairs. The audit appends the exact eight-bit primitive-exit mask of each
descriptor to every still-live equality class. After any prefix, the
retained buckets are exactly the non-singleton raw-signature equivalence
classes. A discarded singleton cannot merge with another signature after
more coordinates are appended. Thus this partition refinement is lossless;
it uses neither a hash nor sampling.

The cap-145 selector has 264,384 descriptors and leaves the 14-prime bucket
\[
\begin{split}
\{&46549,51599,53887,54049,57859,58031,59651,59699,\\
  &61673,61861,62201,62743,63463,64037\},
\end{split}
\]
which contributes 91 failed pairs. The cap-148 selector has 284,004
descriptors and leaves the six-prime bucket
\[
\{46549,53887,59651,59699,61673,63463\},
\]
which contributes 15 failed pairs. Therefore both inherited formulas fail
on the new complete population, proving `REF-040`.

## Exact transition and threshold

Raw selector inclusion implies that every collision after cap 148 lies in
the displayed six-prime bucket. Evaluating every newly admitted descriptor
on each still-live class gives the exact collision-pair ladder
\[
\begin{array}{c|rrrrrrrrrr}
L&148&149&150&151&152&153&154&155&156&157\\
\hline
\#\text{ pairs}&15&10&10&10&10&6&6&6&3&3\\[2pt]
L&158&159&160&161&162&163&164&165&166&167\\
\hline
\#\text{ pairs}&3&1&1&1&1&1&1&1&1&0.
\end{array}
\]
At caps 159 through 166 the only collision bucket is
\[
\{59699,63463\}.
\]
Cap 167 is injective. Hence
\[
L_{32}^{\star}=167.
\]

## One-coordinate minimum incremental repair

Whenever an exact descriptor mask splits a live class, the audit records
every primitive bit that varies on that class. Appending those bits
reproduces the same refinement. Through cap 166 this gives 1,748 explicit
primitive coordinates whose signatures separate every population pair
except \(\{59699,63463\}\).

Cap 167 adds 20,656 descriptors and 165,248 primitive coordinates. Exactly
one is nonconstant on the final pair:
\[
\begin{array}{c|rr}
\text{source}&59699&63463\\
\hline
\texttt{phi4:167:119:93:cofactor}&1&0.
\end{array}
\]
Appending it gives a 1,749-coordinate construction certificate separating
all 1,530,375 pairs. Cap 166 still collides, so a zero-coordinate
incremental repair is impossible; the displayed coordinate suffices.
Therefore the minimum incremental repair size is exactly one. No minimum
claim is made for the full 1,749-coordinate construction.

## THM-017: repaired finite construction through length 32

M43 proved that the largest additive offset through length 31 is 113. The
new row gives
\[
L_{32}^{\star}-32=167-32=135.
\]
Therefore the public factorization-independent selector \(L(m)=m+135\) is
injective on every complete balanced population for \(9\le m\le32\), and
135 is the smallest common integer offset on this finite range.

For multiplicative caps, the new endpoint is
\[
\frac{L_{32}^{\star}-1}{32}
 =\frac{166}{32}
 =\frac{83}{16}
 >\frac{143}{31}.
\]
Consequently the exact coefficients covering the complete range through 32
are
\[
c>\frac{83}{16}.
\]
The endpoint gives failed cap 166. The Farey-adjacent rational witness
\(26/5\) is larger by \(1/80\) and gives
\(\lceil(26/5)32\rceil=167\), so it succeeds.

## Cost and recognition

Both repaired schedules remain linear, so DEF-032 gives
\(O(m^3\log m)\) compact modular work, \(O(m^3)\) GCDs and outputs, and
polynomial total bit complexity. Population enumeration, equivalence-class
refinement, certificate extraction, dense expansion, and collision tracking
are certificate operations only. The balanced promise remains factor
dependent and is not claimed recognizable before factoring.

## Adversarial review

- The inherited additive and multiplicative formulas are evaluated
  separately at their exact public caps 145 and 148.
- The retained classes are the exact equality partition under all processed
  raw coordinates; singleton removal is lossless under coordinate appending.
- Raw selector inclusion confines every cap-149--167 collision to the
  complete cap-148 bucket.
- The cap-166 collision and cap-167 injectivity are adjacent exact profiles,
  proving threshold minimality.
- The selected primitive coordinate at each split reproduces the exact
  partition and yields an explicit 1,749-coordinate construction.
- An independent closed-form geometric-sum evaluator checks all 548,388
  public-cap descriptors, 791,952 transition local exits, and 165,248 new
  primitive repair coordinates.
- Four selected coordinates additionally pass dense expansion and Rust/C#
  verification.
- The construction certificate is independently reconstructed and all
  1,530,375 unordered pairs are checked.
- Only the one-coordinate incremental repair is claimed minimum; the full
  construction is not claimed minimum.
- The new endpoint \(83/16\) is compared against every earlier finite row;
  it is not inferred from a regression or trend.
- General factoring and promise recognition remain open.
