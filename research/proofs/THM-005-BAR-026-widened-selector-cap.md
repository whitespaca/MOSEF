# THM-005 and BAR-026: widened public selector caps

## Claim status and scope

- `DEF-032`: `DEFINITION`.
- `THM-005`: `PROVED` on the complete finite balanced-semiprime promise
  \(9\le m\le20\).
- `BAR-026`: `PROVED` for the exact M32 cap grammar and finite range.
- `REF-028`: `REFUTED`.

None of these claims is an asymptotic injectivity theorem, a recognizer for
the balanced promise, or a classical polynomial-time factoring algorithm for
arbitrary integers.

## DEF-032: public widened-cap selector

For an input length \(m\ge9\) and a public integer \(L\ge m\), let
\(\mathcal T_{m,L}\) contain every valid exceptional descriptor
\[
(\mathit{family},A,B,g),\qquad 2\le A,B,g\le L,
\]
from the \(\Phi_4\) and \(\Phi_6\) families fixed in DEF-031. The function
\(L=L(m)\) is fixed before the input \(N\); it cannot inspect \(N\), either
unknown factor, a root set, or a support signature.

Every descriptor charges the eight primitive exits from DEF-031: base, both
stages, both public bounds, direct cyclotomic, public overlap resultant, and
independent compact cofactor. Aggregate and retained overlap outputs remain
charged but are Boolean functions of these primitive exits. Constant-column
deletion and duplicate-column merging are analytical normalization only and
do not remove work from the public algorithm.

The base branch is total even when \(L\) reaches a population prime. If
\(\gcd(g,N)\) is proper, it is already a factor. If it is \(N\), the
unit-only continuation is skipped. On one prime, the branch-total primitive
mask is therefore the base bit alone when \(p\mid g\), and otherwise the
seven continuation bits follow the base bit.

## Monotonicity lemma

If \(m\le L\le L'\), then
\[
\mathcal T_{m,L}\subseteq\mathcal T_{m,L'}.
\]
Consequently, the raw signature at \(L\) is a projection of the raw
signature at \(L'\). Any pair separated at \(L\) remains separated at
\(L'\), and every collision class at \(L'\) is contained in a collision
class at \(L\).

The normalized column count need not be monotone because a column can become
constant or duplicate after the population is fixed. This does not affect
the conclusion: DEF-031's exact normalization lemma preserves pair
separation at each cap, while raw-coordinate inclusion gives monotonicity
between caps.

## Complete finite threshold certificate

For each \(16\le m\le20\), exhaustive cap search began at \(L=m\) and stopped
at the first injective signature. The registered exact thresholds are:

| \(m\) | \(|\mathcal P_m|\) | minimal \(L\) | \(L-m\) | descriptors at \(L\) | normalized columns | certificate columns | collision at \(L-1\) |
|---:|---:|---:|---:|---:|---:|---:|---|
| 16 | 12 | 19 | 3 | 522 | 16 | 10 | \(\{191,227,233\}\) |
| 17 | 18 | 19 | 2 | 522 | 24 | 16 | \(\{277,317\},\{263,349\}\) |
| 18 | 25 | 27 | 9 | 1,612 | 42 | 20 | \(\{503,509\}\) |
| 19 | 31 | 27 | 8 | 1,612 | 47 | 26 | \(\{569,719\}\) |
| 20 | 44 | 31 | 11 | 2,430 | 59 | 40 | \(\{809,827\}\) |

For every row, the compact implementation evaluated every cap from \(m\)
through the displayed threshold. At the predecessor cap, the independent
dense implementation evaluated all eight branch-total exit bits for every
descriptor on every prime in the displayed collision bucket. At the
threshold, a deterministic greedy sublist of normalized columns gives
distinct packed signatures for the entire listed population. Greediness is
not used as a minimality claim; only the checked injectivity of the resulting
certificate matters.

All smaller caps fail because the displayed predecessor collision exists and
the smaller selector is a subset of the predecessor selector. Thus the table
gives exact minimal thresholds, not merely the first values seen by an
unchecked heuristic search.

## THM-005: finite widened construction

Let
\[
L_+(m)=m+11.
\]
For every \(9\le m\le20\), the public selector
\(\mathcal T_{m,L_+(m)}\) exposes a proper factor of every
\[
N=pq,\qquad p\ne q,\quad p,q\in\mathcal P_m.
\]

For \(9\le m\le15\), THM-004 proves injectivity already at \(L=m\), so the
monotonicity lemma applies. For \(16\le m\le20\), \(m+11\) is at least the
registered threshold in the table. The threshold certificate and
monotonicity therefore give injectivity. BAR-024 converts signature
inequality exactly into a proper charged GCD.

The integer offset 11 is minimal for this complete finite range: offset 10
gives \(L(20)=30\), where \(809\) and \(827\) still collide.

## BAR-026: exact multiplicative endpoint and finite boundary

For a fixed real or rational coefficient \(c\), the cap
\[
L_c(m)=\lceil cm\rceil
\]
meets a registered threshold \(L_m^\star\) exactly when
\[
c>\frac{L_m^\star-1}{m}.
\]
Across \(16\le m\le20\), the maximum right-hand side is
\[
\max\left\{\frac{18}{16},\frac{18}{17},\frac{26}{18},
\frac{26}{19},\frac{30}{20}\right\}=\frac32.
\]
Hence the coefficients that cover all five threshold rows are exactly
\(c>3/2\). There is an infimum but no smallest real or rational coefficient.
The endpoint \(c=3/2\) fails at \(m=20\) because it gives \(L=30\) and retains
the collision \(\{809,827\}\). The public rational witness
\(c=151/100\) succeeds on the registered range.

This proves a sharp finite cap boundary for DEF-032. It does not show that
any fixed \(c>3/2\), \(m+11\), or another polynomial cap stays injective at
unbounded lengths. REF-028, the claim that \(m+10\) suffices throughout the
complete range \(9\le m\le20\), is refuted by the same \(m=20\) collision.

## Polynomial cost

There are at most \(2(L-1)^3\) descriptors. Each descriptor uses
\(O(\log L)\) public bits per entry and, by BAR-020 and BAR-021, requires
\(O(\log L)\) modular composition steps plus a constant number of GCDs and
charged outputs. Thus a polynomially bounded, polynomial-time computable
\(L(m)\) gives
\[
O(L(m)^3\log L(m))
\]
compact modular steps, \(O(L(m)^3)\) GCDs and outputs, and polynomial total
bit complexity in the \(m\)-bit modulus. For \(L=m+11\) or
\(\lceil151m/100\rceil\), this is \(O(m^3\log m)\) compact work.

The analytical certificate enumerates population primes and is not a promise
recognizer. The public algorithm constructs the selector from \(m\) alone
and verifies any proper GCD directly.

## Adversarial review

- **Hidden factor access:** rejected; only \(m\) and the fixed public cap
  formula construct the selector.
- **False normalized monotonicity:** avoided; monotonicity is proved on raw
  selector inclusion and transferred through exact normalization.
- **Nonunit bases:** retained with a total base-GCD branch and skipped
  unit-only continuation.
- **Threshold minimality:** certified by a complete predecessor collision and
  selector inclusion, not by an optimizer's stopping condition alone.
- **Certificate minimality:** not claimed; greedy certificates are only
  checked separating sublists.
- **Multiplier endpoint:** \(c=3/2\) is excluded explicitly; the result has
  no nonexistent “smallest” rational coefficient.
- **Cost leakage:** descriptor construction, compact evaluation, every GCD,
  output, and extraction are charged.
- **Finite-to-asymptotic leakage:** rejected; the theorem stops at \(m=20\).
- **General factoring:** unchanged and open within this project.
