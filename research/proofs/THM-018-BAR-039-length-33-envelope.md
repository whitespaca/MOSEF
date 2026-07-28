# THM-018 and BAR-039: the length-33 finite envelope

## Claim status and scope

- `THM-018`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le33\).
- `BAR-039`: `PROVED` for the exact DEF-032 selector at \(m=33\).
- `REF-041`: `REFUTED`.

No claim below concerns \(m>33\), promise recognition, an asymptotic cap
rate, or general classical polynomial-time factoring.

## Both inherited public caps fail

At \(m=33\), the M44 schedules give
\[
m+135=168,\qquad
\left\lceil\frac{26m}{5}\right\rceil=172.
\]
The complete balanced population has 2,410 primes and 2,902,845 unordered
pairs. The exact partition-refinement audit appends each descriptor's
eight-bit primitive-exit mask to every still-live equality class. Its
retained buckets are exactly the non-singleton raw-signature equivalence
classes. Appending coordinates cannot merge discarded singletons, so this
is a lossless computation without hashing or sampling.

The cap-168 selector has 418,502 descriptors and leaves the 12-prime bucket
\[
\begin{split}
\{&66089,71039,75161,75629,78791,80309,81043,91387,\\
  &91411,92173,92641,92671\},
\end{split}
\]
which contributes 66 failed pairs. The cap-172 selector has 447,678
descriptors and leaves the eight-prime bucket
\[
\{71039,75161,75629,80309,91387,91411,92173,92671\},
\]
which contributes 28 failed pairs. Thus both inherited formulas fail,
proving `REF-041`.

## Exact transition and threshold

Raw selector inclusion confines every post-cap-172 collision to the
displayed eight-prime bucket. Evaluation of every newly admitted descriptor
on each still-live class gives
\[
\begin{array}{c|rrrrrrrr}
L&172&173&174&175&176&177&178&179\\
\hline
\#\text{ pairs}&28&28&28&15&15&10&10&6\\[2pt]
L&180&181&182&183&184&185&186&187\\
\hline
\#\text{ pairs}&6&6&6&6&3&3&3&3\\[2pt]
L&188&189&190&191&192&193&194&195\\
\hline
\#\text{ pairs}&1&1&1&1&1&1&1&0.
\end{array}
\]
At caps 188 through 194 the only collision is
\(\{80309,92671\}\). Cap 195 is injective. Therefore
\[
L_{33}^{\star}=195.
\]

## One-coordinate minimum incremental repair

The split-recording construction contains 2,409 primitive coordinates
through cap 194 and separates every population pair except
\(\{80309,92671\}\). Cap 195 adds 28,112 descriptors and 224,896 primitive
coordinates. Exactly one is nonconstant on the final pair:
\[
\begin{array}{c|rr}
\text{source}&80309&92671\\
\hline
\texttt{phi4:195:91:20:cofactor}&1&0.
\end{array}
\]
Appending it gives a 2,410-coordinate certificate separating all
2,902,845 pairs. Cap 194 proves that zero new coordinates cannot suffice,
and the displayed coordinate suffices, so the minimum incremental repair
size is one. No minimum claim is made for the full construction.

## THM-018: repaired finite construction through length 33

M44 proved that the largest additive offset through length 32 is 135. The
new row gives
\[
L_{33}^{\star}-33=195-33=162.
\]
Therefore \(L(m)=m+162\) is injective on every complete balanced population
for \(9\le m\le33\), and 162 is the smallest common integer offset on this
finite range.

For multiplicative caps, the new endpoint is
\[
\frac{L_{33}^{\star}-1}{33}=\frac{194}{33}>\frac{83}{16}.
\]
Thus the exact coefficients through length 33 are \(c>194/33\). The
endpoint gives failed cap 194. The Farey-adjacent rational witness
\(147/25\) exceeds the endpoint by \(1/825\) and gives
\(\lceil147\cdot33/25\rceil=195\).

## Cost, recognition, and adversarial review

Both repaired schedules remain linear. DEF-032 therefore retains
\(O(m^3\log m)\) compact modular work, \(O(m^3)\) GCDs and outputs, and
polynomial total bit complexity. Population enumeration, partition
refinement, certificate extraction, dense expansion, and collision tracking
remain certificate operations only. The balanced promise is factor
dependent and is not claimed recognizable before factoring.

The two inherited schedules were evaluated at their distinct exact caps.
All later classes derive from the complete cap-172 bucket, and the adjacent
cap-194/cap-195 profiles prove threshold minimality. Every newly admitted
cap-195 coordinate was checked on the final pair, and the construction was
independently reconstructed and checked on all 2,902,845 pairs. Selected
coordinates also pass dense, Rust, and C# paths. These finite certificates
do not imply a recurrence, density theorem, asymptotic cap rate, promise
recognizer, or solution of general factoring.
