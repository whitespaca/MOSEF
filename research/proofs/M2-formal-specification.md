# M2 formal multiplicative-channel specification

Status: adversarially reviewed; LEM-001 and LEM-002 are `PROVED`.

## Domain and notation

Let

\[
N=\prod_{p\in P(N)}p^{e_p}\ge 2,\qquad \gcd(g,N)=1,\qquad d\in\mathbb Z_{>0}.
\]

Here \(P(N)\) is the set of distinct prime divisors of \(N\), \(e_p\ge 1\),
and \(\nu_p(0)=+\infty\). Define

\[
D_N(g,d)=\{p\in P(N):\operatorname{ord}_p(g)\mid d\}
\]

and the capped valuation profile

\[
a_p(N,g,d)=\min\{e_p,\nu_p(g^d-1)\}.
\]

The support condition is an **order separator** when
\(\varnothing\ne D_N(g,d)\ne P(N)\). The valuation condition is a
**prime-power separator** when at least one \(a_p>0\) and at least one
\(a_q<e_q\); \(p=q\) is allowed. These are analysis definitions. A POSF
constructor may not use the unknown factorization to compute them.

A **support-POSF** in this milestone consists of two explicitly materialized
sets \(G_m(N)\) and \(\Delta_m(N)\), and it evaluates their Cartesian product.
Every base is materialized as its canonical residue in \([0,N-1]\). The
support-POSF success domain excludes inputs already discharged by exact
primality and perfect-power preprocessing. A **valuation-separating family**
uses the same representation but replaces the support success condition by
the exact valuation condition. Neither type of universal family is constructed
here.

## LEM-001: support-separator sufficiency

**Status:** `PROVED`.

**Statement.** Under the domain conditions above, if
\(\varnothing\ne D_N(g,d)\ne P(N)\), then

\[
1<\gcd(g^d-1,N)<N.
\]

**Proof.** Choose \(p\in D_N(g,d)\). By the definition of multiplicative
order, \(g^d\equiv1\pmod p\), so \(p\mid\gcd(g^d-1,N)\) and the GCD exceeds
one. Since the support is proper, choose \(q\in P(N)\setminus D_N(g,d)\).
Then \(g^d\not\equiv1\pmod q\), so \(q\nmid\gcd(g^d-1,N)\). Because \(q\mid
N\), the GCD is strictly smaller than \(N\). Repeated prime factors do not
affect either strict inequality. \(\square\)

## LEM-002: exact valuation criterion

**Status:** `PROVED`.

**Statement.** Under the same domain conditions,

\[
\gcd(g^d-1,N)=\prod_{p\in P(N)}p^{a_p(N,g,d)}.
\]

Consequently, the GCD is nontrivial exactly when the capped valuation profile
is neither the all-zero profile nor the full profile \((e_p)_{p\in P(N)}\).

**Proof.** For each prime \(p\), the exponent of \(p\) in a GCD is the minimum
of its exponents in the two arguments. The exponent in \(N\) is \(e_p\), while
the exponent in \(g^d-1\) is \(\nu_p(g^d-1)\), including the convention for
zero. Unique factorization gives the product formula. The product equals one
exactly when every \(a_p=0\), and equals \(N\) exactly when every
\(a_p=e_p\). These are the only trivial GCDs. \(\square\)

### Square-free corollary

If \(N\) is square-free, every \(e_p=1\) and

\[
a_p=1\quad\Longleftrightarrow\quad p\mid g^d-1
\quad\Longleftrightarrow\quad \operatorname{ord}_p(g)\mid d.
\]

Thus the support condition is necessary and sufficient for a nontrivial GCD
on square-free inputs.

### Prime-power corollary

If \(N=p^e\) with \(e\ge2\), the support condition can never be proper. The
candidate GCD is nevertheless nontrivial exactly when

\[
0<\nu_p(g^d-1)<e.
\]

The smallest counterexample to the proposed all-input equivalence is
\((N,g,d)=(4,3,1)\): \(D_4(3,1)=\{2\}=P(4)\), but
\(\gcd(3^1-1,4)=2\). The smallest odd example is \((9,2,2)\).

## Candidate evaluation pseudocode

```text
EVALUATE-CANDIDATE(N, g, d):
    require N >= 2 and d > 0
    g <- g mod N
    u <- gcd(g, N)
    if 1 < u < N:
        return DIRECT-FACTOR(u)
    if u = N:
        return INVALID-BASE

    r <- modular_power(g, d, N)
    h <- gcd((r - 1) mod N, N)
    if h = 1:
        return MISS
    if h = N:
        return SIMULTANEOUS-COLLISION
    return FACTOR(h)
```

```text
TRY-SUPPORT-POSF(N, constructor):
    require N >= 2
    if VALIDATION-PRIME(N):
        return PRIME
    if N = a^k is a perfect power with k >= 2:
        return PERFECT-POWER(a, k)

    (G, Delta) <- constructor(N, ceil(log2 N))
    if construction is invalid, exceeds a declared bound,
       uses factor-dependent information, or fails:
        return CONSTRUCTION-FAILURE

    require every g in G to be materialized as its canonical residue modulo N
    require every d in Delta to be a materialized positive integer
    for every (g, d) in the Cartesian product G x Delta:
        outcome <- EVALUATE-CANDIDATE(N, g, d)
        if outcome is DIRECT-FACTOR or FACTOR:
            return outcome
        record INVALID-BASE, MISS, and SIMULTANEOUS-COLLISION
    return UNRESOLVED
```

```text
COMPLETE-FACTOR(N, constructor):
    require N >= 1
    if N = 1:
        return FACTORS(empty multiset)
    if VALIDATION-PRIME(N):
        return FACTORS({N})

    if PERFECT-POWER(N) returns (a, k) with a >= 2 and k >= 2:
        base_result <- COMPLETE-FACTOR(a, constructor)
        if base_result is CONSTRUCTION-FAILURE or UNRESOLVED:
            return base_result
        return FACTORS(each multiplicity in base_result multiplied by k)

    outcome <- TRY-SUPPORT-POSF(N, constructor)
    if outcome is CONSTRUCTION-FAILURE or UNRESOLVED:
        return outcome
    if outcome is not DIRECT-FACTOR(h) or FACTOR(h):
        return INTERNAL-ERROR
    if h <= 1 or h >= N or N mod h != 0:
        return INTERNAL-ERROR

    left <- COMPLETE-FACTOR(h, constructor)
    if left is CONSTRUCTION-FAILURE or UNRESOLVED:
        return left
    right <- COMPLETE-FACTOR(N / h, constructor)
    if right is CONSTRUCTION-FAILURE or UNRESOLVED:
        return right
    return FACTORS(multiset union of left and right)
```

`UNRESOLVED` never means prime. `PERFECT-POWER` must return an exact identity,
and each reported split is validated before recursion. The support constructor
is invoked only after prime and perfect-power branches fail.

## Bit-complexity ledger

Let \(m=\lceil\log_2 N\rceil\), let \(C(m)\) bound construction and explicit
materialization, let \(|G_m(N)|\le B(m)\), let
\(|\Delta_m(N)|\le E(m)\), and let \(T(m)=B(m)E(m)\) bound the Cartesian
product. Every base is stored as a canonical \(m\)-bit residue; let \(L(m)\)
bound every exponent bit length. Let \(M(m)\) be the bit cost of multiplying
\(m\)-bit integers and \(G(m)\) the bit cost of an \(m\)-bit GCD. Binary
modular exponentiation evaluates one pair in

\[
O(M(m)L(m)+G(m))
\]

bit operations and \(O(m+L(m))\) working bits, apart from the explicitly
charged family representation. One complete family pass therefore costs

\[
O\!\left(C(m)+T(m)\bigl(M(m)L(m)+G(m)\bigr)\right).
\]

This is polynomial only if \(C,B,E,L\), representation conversion, and any
channel-specific preprocessing are polynomial in \(m\). The explicit base
materialization contributes \(O(B(m)m)\) bits and is charged to \(C(m)\).
A compact rule whose expansion or evaluation is superpolynomial does not meet
the condition.

For recursion, each successful split increases the number of nontrivial
leaves by one. Since the total number of prime factors with multiplicity is at
most \(m\), a complete factor tree has fewer than \(2m\) nodes. If the same
monotone polynomial bound applies at every node and primality/perfect-power
handling is polynomial, multiplying the per-node bound by \(O(m)\) preserves
polynomial time. This ledger is conditional: no universal constructor or
separator guarantee is proved here.

## Refuted and unresolved universal obligations

The original all-composite support-POSF target, formerly `OPEN-001`, is
`REFUTED`: no prime power \(p^e\), \(e\ge2\), admits a nonempty proper support.
Two repaired universal targets remain open.

1. `OPEN-002`: preprocess prime powers exactly in polynomial time, then
   construct a support-POSF for every remaining composite recursive cofactor.
2. `OPEN-003`: construct a valuation-separating family for every composite,
   including prime powers.

Either target must construct \(G_m(N)\) and \(\Delta_m(N)\) without access to
the factorization; bound family cardinalities, explicit base representation,
exponent generation, and exponent bit lengths by polynomials in \(m\);
guarantee a successful direct-factor or separator branch on its exact domain;
cover every recursive cofactor; prove channel operations and failed inversions
have polynomial bit cost; and supply polynomial primality and perfect-power
handling. None of these obligations is assumed by LEM-001 or LEM-002.

## Falsification plan

The deterministic harness checks every composite \(4\le N\le500\), every unit
base \(2\le g\le20\), and \(1\le d\le20\). It compares the support and
valuation predictions with the directly computed GCD, checks square-free
equivalence, and searches for support-only false negatives on nonsquarefree
inputs. There is no random seed.

## Adversarial review record

An independent reviewer attempted to refute both lemmas and reran the
registered 78,860-case search plus a clean-room enumeration of 193,200 cases
using every normalized unit residue for composite \(N\le200\) and
\(1\le d\le24\). No counterexample to either lemma was found. The review
identified and this revision repairs: the impossible all-composite
support-POSF scope, missing recursive pseudocode, ambiguous Cartesian-product
semantics, omitted base-representation cost, overbroad finite-search labels,
and missing named boundary regressions. The lemmas use no factor-dependent
constructor, average-case assumption, or unproved imported result.
