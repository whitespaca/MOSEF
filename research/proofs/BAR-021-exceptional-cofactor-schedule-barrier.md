# BAR-021 - Local exceptional-cofactor profiles and fixed-schedule barrier

## Status

`PROVED` for the exact M27 public exceptional-cofactor schedule model. The
result isolates every stage and direct-cyclotomic overlap and proves that no
fixed finite joint base/parameter schedule covers all composite inputs. It
does not rule out an input-length-dependent or input-adaptive schedule.

## Model and local criterion

Write \(Q_1=S_A(X)\), \(Q_2=S_B(X^A)\), and use the M26 factorizations

\[
 F_4=Q_1+Q_2=\Phi_4C_4,\qquad
 F_6=2Q_1+Q_2=\Phi_6C_6
\]

under their respective congruence conditions. For
\(N=\prod_j p_j^{e_j}\), a public unit base \(g\), and \(i\in\{4,6\}\), put

\[
 a_{i,j}(g)=\min(v_{p_j}(C_i(g)),e_j).
\]

Then

\[
 \gcd(C_i(g),N)=\prod_j p_j^{a_{i,j}(g)}.
\]

Consequently the cofactor GCD is proper exactly when at least one
\(a_{i,j}(g)>0\) and at least one \(a_{i,k}(g)<e_k\), where \(j=k\) is
allowed. For square-free \(N\), this says that \(g\bmod p_j\) is a root of
\(C_i\) for a nonempty proper subset of the prime factors. For a prime power,
success requires a strictly intermediate valuation.

Both cofactors are monic of degree

\[
 d=A(B-1)-2.
\]

Thus their reduction modulo every prime is nonzero and has at most \(d\)
roots in the field, hence at most \(\min(d,p-1)\) unit roots modulo \(p\).
This is an upper bound, not a lower bound or a public root constructor.

## Exact stage overlap

The M24 resultants and multiplicativity of the resultant give

\[
\begin{aligned}
 |\operatorname{Res}(Q_1,C_4)|&=B^{A-1},&
 |\operatorname{Res}(Q_2,C_4)|&=B^{A-1},\\
 |\operatorname{Res}(Q_1,C_6)|&=B^{A-1},&
 |\operatorname{Res}(Q_2,C_6)|
 &=2^{A(B-1)-2}B^{A-1}.
\end{aligned}
\]

Indeed, at a root of \(Q_1\), the second stage equals \(B\), so
\(|\operatorname{Res}(Q_1,F_i)|=B^{A-1}\). The first coefficient contributes
\(2^{A(B-1)}\) to the second order-six stage resultant. On the removed
cyclotomic factor,

\[
 |\operatorname{Res}(Q_1,\Phi_4)|
 =|\operatorname{Res}(Q_2,\Phi_4)|
 =|\operatorname{Res}(Q_1,\Phi_6)|=1,
\]

while

\[
 |\operatorname{Res}(Q_2,\Phi_6)|=4.
\]

The last identity follows from
\(S_B(\zeta_6^A)=2\zeta_6^{-1}\), whose norm is four. Therefore a prime can
divide a stage and its cofactor value at the same base only if it divides
\(B\) in the order-four family, or \(2B\) in the order-six family. The
resultants remain compact base/exponent descriptors; their generally large
integer expansions are not required.

## Exact direct-cyclotomic overlap

Reduction of the dense quotient modulo the removed quadratic gives

\[
 C_4(X)\equiv u_4+v_4X\pmod{\Phi_4},
\]

where

\[
 u_4=\frac{A(B+2)+1}{4},\qquad
 v_4=\frac{A(B-2)+1}{4},
\]

and

\[
 C_6(X)\equiv u_6+v_6X\pmod{\Phi_6},
\]

where

\[
 u_6=-\frac{2(A(B-2)+1)}{3},\qquad
 v_6=\frac{A(B+4)+4}{3}.
\]

The congruence hypotheses make every displayed quotient integral. Taking
quadratic norms yields

\[
 R_4=|\operatorname{Res}(\Phi_4,C_4)|=u_4^2+v_4^2
\]

and

\[
 R_6=|\operatorname{Res}(\Phi_6,C_6)|
 =u_6^2+u_6v_6+v_6^2.
\]

Both are positive. Hence neither exceptional cyclotomic factor repeats over
\(\mathbb Q[X]\). If a prime \(p\) divides both \(\Phi_i(g)\) and \(C_i(g)\),
then \(p\mid R_i\). The factorization-independent precheck
\(\gcd(R_i,N)\) therefore isolates every possible direct/cofactor overlap.
Computing \(u_i,v_i,R_i\) uses integers with
\(O(\log A+\log B)\) bits.

## Fixed finite joint-schedule barrier

Let \(\mathcal T\) be any nonempty finite set of public tuples
\((i,A,B,g)\), where the family congruences hold and \(g\ge2\). Include the
base GCD, both stages, the public stage bounds, the direct cyclotomic, the
cofactor, and the public \(R_i\) precheck.

For each tuple, the positive integer values

\[
 g,\quad Q_1(g),\quad Q_2(g),\quad \Phi_i(g),\quad C_i(g)
\]

are nonzero. The constants \(B\), \(2B\) where applicable, and \(R_i\) are
also positive. Let \(P\) be their finite product across \(\mathcal T\).
Only finitely many primes divide \(P\), so infinitely many primes do not.
Choose distinct such primes \(p,q\) and set \(N=pq\). Every charged value is
coprime to \(N\), every computed GCD is one, and the entire fixed schedule
misses \(N\). Infinitely many choices of \(p,q\) remain.

Thus no fixed finite public joint base/parameter schedule succeeds on every
composite input, even after adding the exact overlap prechecks.

## Complexity and recognition boundary

For one public tuple, the M26 compact evaluator, the two small overlap
descriptors, the direct quadratic, and all GCDs cost polynomially many bit
operations in
\(\log N+\log A+\log B+\log g\). Enumerating all roots modulo \(p\) instead
costs \(p-1\) explicit trials and is not polynomial in \(\log p\).

Family membership is publicly recognized from congruences of \(A,B\).
Whether an unknown prime factor sees a cofactor root or an intermediate
valuation is factor-dependent. No factorization-independent recognizer or
density theorem is supplied.

The barrier fixes \(\mathcal T\) before choosing \(N\). It does not apply to
a sequence \(\mathcal T_m\) indexed by the eventual input length, to a
schedule constructed from \(N\), or to adaptive schedules. Applying the
finite-product argument to any of those models without resolving the
resulting circular dependence would be invalid.

## Adversarial review

- **Repeated factors:** the capped valuation criterion covers prime powers;
  the fixed-schedule obstruction already holds on square-free semiprimes.
- **Hidden common factors:** exact stage resultants restrict their prime
  support, and \(R_i\) isolates direct/cofactor overlap.
- **Repeated cyclotomic factor:** impossible over \(\mathbb Q[X]\) because
  \(R_i>0\).
- **Root-count misuse:** the degree bound is only an upper bound and is not
  converted into a success probability.
- **Recognition:** local roots and valuations use unknown factors only for
  analysis, never for schedule construction.
- **Output size:** dense cofactors and expanded stage resultants remain
  charged; the algorithm uses compact formulas and descriptors.
- **Overclaim:** the Euclidean avoidance proof concerns a fixed finite
  schedule only and is not a lower bound for length-dependent or adaptive
  algorithms.

EXP-0026 checked the remainder and resultant formulas, every stated overlap
implication in its finite box, prime-power local profiles, fixed-prefix
obstructions, and selected independent Rust/C# descriptors. Those checks
support the implementation but are not used as the proof.
