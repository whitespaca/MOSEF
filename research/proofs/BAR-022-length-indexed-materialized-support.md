# BAR-022 - Length-indexed materialized-support barrier

## Status

`PROVED` for the exact M28 materialized-lift submodel. The theorem gives an
exact pair-coverage upper bound and a necessary bit budget for any public
schedule indexed only by the eventual input length. It does not extend that
budget bound to the M26 compact modular evaluator.

## Length-indexed schedule grammar

For every input length \(m\), a constructor that does not receive \(N\) or
any factor of \(N\) selects a finite exceptional-cofactor schedule
\(\mathcal T_m\). Each tuple contains a public family, valid public factors
\((A,B)\), and a public base \(g\). All tuple encodings, construction work,
compact modular operations, outputs, GCDs, and extraction work are charged.
The M27 base, stage, public-bound, direct-cyclotomic, cofactor, and resultant
prechecks remain present.

There are two different cost ledgers.

1. The **compact ledger** charges binary parameter encodings and the modular
   operations used to evaluate the M26 formulas modulo the received \(N\).
2. The **materialized-lift ledger** additionally emits every nonzero exact
   integer \(z_{m,j}\) whose reduction is sent to a GCD, and charges

   \[
   W_m=\sum_j \operatorname{bitlength}(|z_{m,j}|).
   \]

An exact lift equal to zero may be deleted: its GCD with every \(N\) is the
full collision \(N\), never a proper factor. The theorem below concerns the
second ledger. The schedule is fixed after \(m\) is known but before the
particular \(N\) is chosen.

## Balanced analytical population

Put

\[
 \mathcal P_m=
 \{p\text{ prime}:2^{m-1}\le p^2<2^m\},
 \qquad s_m=|\mathcal P_m|,
\]

and suppose \(s_m\ge2\). Every two distinct \(p,q\in\mathcal P_m\) satisfy

\[
 2^{m-1}\le pq<2^m.
\]

Their odd product therefore has standard input length
\(\operatorname{bitlength}(pq)=m\). The legacy ceiling-log index agrees
because the product is not a power of two. Define

\[
 b_m=\left\lfloor\frac{m-1}{2}\right\rfloor.
\]

Every \(p\in\mathcal P_m\) obeys \(p\ge2^{b_m}\).
This population is an adversarial analysis device, not a claimed
factorization-independent promise recognizer.

## Theorem

Let

\[
 H_m=\{p\in\mathcal P_m:p\mid z_{m,j}\text{ for some }j\},
 \qquad h_m=|H_m|.
\]

Then:

1. exactly
   \[
   \binom{s_m-h_m}{2}
   \]
   distinct square-free inputs \(pq\), with \(p,q\in\mathcal P_m\), have
   every materialized GCD equal to one;
2. at most
   \[
   \binom{s_m}{2}-\binom{s_m-h_m}{2}
   \]
   population pairs can even be touched by the support, before accounting
   for full collisions;
3. the materialized bit budget satisfies
   \[
   b_mh_m\le W_m;
   \]
4. consequently, a schedule that factors every population pair must satisfy
   \[
   h_m\ge s_m-1
   \quad\text{and}\quad
   W_m\ge b_m(s_m-1).
   \]

More generally, along any sequence of lengths for which
\(W_m/b_m\le s_m-2\), the schedule has a square-free balanced miss at every
such length.

## Proof

If \(p,q\notin H_m\), neither prime divides any \(z_{m,j}\). Hence
\(\gcd(z_{m,j},pq)=1\) for every charged exact value. Conversely, the pairs
with both endpoints outside \(H_m\) are exactly the
\(\binom{s_m-h_m}{2}\) pairs counted in the first item. Every remaining pair
has at least one endpoint in \(H_m\), so their count gives the second item
as an upper bound. It need not be attained: if one value is divisible by
both endpoints, that value produces a full collision rather than a proper
factor.

Let

\[
 D_m=\prod_j |z_{m,j}|.
\]

The distinct primes in \(H_m\) all divide \(D_m\), so their square-free
product divides \(D_m\). Therefore

\[
 2^{b_mh_m}
 \le\prod_{p\in H_m}p
 \le D_m.
\]

Taking base-two logarithms and using
\(\log_2|z_{m,j}|\le\operatorname{bitlength}(|z_{m,j}|)\) gives
\(b_mh_m\le W_m\).

If \(h_m\le s_m-2\), two distinct population primes remain outside the
support and their product is a miss. Universal population coverage thus
requires \(h_m\ge s_m-1\), and substitution into the preceding inequality
gives \(W_m\ge b_m(s_m-1)\). This proves every item.

## Compact-evaluation separation

The materialized budget is not implied by the compact ledger. For every
integer \(t\ge2\), take the valid order-four exceptional tuple

\[
 A=3,\qquad B=2^t+3,\qquad g=2.
\]

Both factors are \(3\bmod4\), and the M26 identity gives

\[
 5C_4(2)
 =S_3(2)+S_B(2^3)
 =7+\frac{8^B-1}{7}.
\]

The public integer encodings have \(O(t)\) bits. The M26 binary geometric-sum
formula evaluates \(C_4(2)\bmod N\) with a constant number of recurrences
whose count encodings have \(O(t)\) bits, hence in time polynomial in
\(t+\operatorname{bitlength}(N)\).

However,

\[
 C_4(2)>\frac{8^{B-1}}5>2^{3B-6},
\]

so

\[
 \operatorname{bitlength}(C_4(2))
 \ge3B-5=3\cdot2^t+4.
\]

Thus polynomial compact evaluation does not imply a polynomial
materialized-lift bit budget. This is the exact obstruction recorded as
`REF-024`. It does not assert that this large cofactor has enough distinct
balanced prime divisors to cover the population.

## Recognition and scope

Family congruences, parameter encodings, and the input length are public.
Membership of an unknown factor in \(H_m\), or in the analytical population
\(\mathcal P_m\), is not supplied to the constructor. BAR-022 is therefore a
support-counting theorem, not a recognizer or an algorithm.

The result rules out cheap universal coverage only when the exact integers
or equivalent explicit prime-support certificates are charged. It does not
rule out compact values with exponentially long exact lifts, schedules that
depend on \(N\), adaptive schedules, other arithmetic circuits, or general
classical polynomial-time factoring. No asymptotic lower bound for
\(s_m\) is imported or claimed.

## Adversarial review

- **Input length:** the population inequalities make every distinct
  semiprime product have exactly the declared length; no prime is chosen
  after changing the schedule index.
- **One unhit prime:** leaving one population prime unhit does not itself
  force a missed pair, so the theorem uses the necessary threshold
  \(h_m\ge s_m-1\), not \(h_m=s_m\).
- **Full collisions:** touched-pair coverage is explicitly an upper bound.
  A value divisible by both factors may reduce success.
- **Zero values:** they yield only full collisions and are removed before
  forming \(D_m\).
- **Repeated factors:** the obstruction uses distinct-prime semiprimes;
  failure on that subclass is enough to refute universality.
- **Support versus magnitude:** the compact-gap example proves exponential
  exact magnitude only. It is not converted into a prime-support lower
  bound.
- **Prime population:** no density or asymptotic size for
  \(\mathcal P_m\) is assumed. The theorem is exact for every finite
  population with \(s_m\ge2\).
- **Hidden factor access:** prime divisors are used only by the adversarial
  proof and audit, never by the schedule constructor.
- **Quantifier boundary:** \(\mathcal T_m\) may vary with \(m\) but not with
  the particular \(N\). \(N\)-dependent and adaptive schedules remain open.

EXP-0027 exhaustively checks the support formula, every pairwise GCD, the
materialized bit inequality, and bounded exact versions of the compact-gap
family. Independent Rust and C# implementations reproduce the registered
support profiles. Those finite checks validate the implementation but are
not used as the proof.
