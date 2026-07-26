# THM-001 - Las Vegas factoring on a hereditary semismooth-order class

Status: `PROVED` after bounded falsification and independent adversarial
review.

## Definition

Let \(B(k),R(k)\) be nondecreasing, polynomially bounded integer functions
computable in time polynomial in \(k\), with \(B(k),R(k)\ge1\), and put

\[
M_B(k)=\operatorname{lcm}(1,2,\ldots,B(k)).
\]

For a composite integer \(K\) that is not a perfect power, let
\(k=\lceil\log_2 K\rceil\). A **\((B,R)\)-semismooth asymmetry witness** is a
tuple \((p,q,t)\) such that

1. \(p\ne q\) are distinct prime divisors of \(K\);
2. \(1\le t\le R(k)\);
3. \(p-1\mid d=tM_B(k)\);
4. \(q-1\nmid d\).

An integer \(N\ge2\) is in the **hereditary
\((B,R)\)-semismooth-asymmetric promise class** when every divisor \(K\mid N\)
that is composite and not a perfect power has such a witness at its local bit
length.

This condition does not mention a selected base. It is therefore stronger than
merely naming a successful candidate after seeing the factorization. It still
depends on unknown prime divisors, so membership is promised rather than
recognized.

## THM-001 statement

**Status:** `PROVED`.

For every fixed schedule pair above, there is a classical Las Vegas algorithm
which, on every \(N\) in the hereditary promise class, returns the complete
prime factorization of \(N\), is always correct, terminates with probability
one, and has expected running time polynomial in
\(m=\lceil\log_2 N\rceil\).

No termination or polynomial-time claim is made outside the promise. A bounded
implementation may return `UNRESOLVED` after an explicitly declared trial
budget without treating that result as a primality or nonmembership decision.

## Algorithm

```text
RANDOM-SEMISMOOTH-SPLIT(K):
    k <- ceil(log2 K)
    M <- lcm(1, ..., B(k))
    repeat:
        for t = 1, ..., R(k):
            sample a uniformly from {0, ..., K - 1}
            u <- gcd(a, K)
            if 1 < u < K:
                return FACTOR(u)
            if u = K:
                continue
            h <- gcd(modular_power(a, t M, K) - 1, K)
            if 1 < h < K:
                return FACTOR(h)
```

`COMPLETE-RANDOM-SEMISMOOTH-FACTOR` first uses deterministic polynomial-time
primality and exact maximal-exponent perfect-power detection. It recursively
factors a perfect-power base and multiplies its prime multiplicities. At every
other composite it calls `RANDOM-SEMISMOOTH-SPLIT`, validates the returned
proper divisor, and recursively factors both children.

Uniform sampling is exact: draw \(k\) independent unbiased bits, interpret them
as \(x\in[0,2^k-1]\), and reject \(x\ge K\). Since
\(2^{k-1}<K\le2^k\), the expected number of bit draws per residue is less than
two.

## One-trial success lemma

Fix a reached composite non-perfect-power \(K\) and a promise witness
\((p,q,t)\). Put \(d=tM_B(k)\), and sample \(a\) uniformly modulo \(K\).
Then the trial at this \(t\) returns a nontrivial factor with probability at
least \(5/12\).

If \(1<\gcd(a,K)<K\), the first GCD succeeds directly. The only residue with
\(\gcd(a,K)=K\) is \(a=0\). It remains to analyze the
\(\varphi(K)\) units.

For every unit \(a\), the condition \(p-1\mid d\) and Fermat's theorem imply
\(a^d\equiv1\pmod p\). The projection of a uniform unit modulo \(K\) to
\((\mathbb Z/q\mathbb Z)^\times\) is uniform. That group is cyclic of order
\(q-1\), so the equation \(x^d=1\) has exactly
\(\gcd(d,q-1)\) solutions. Because \(q-1\nmid d\), this proper divisor is at
most \((q-1)/2\). Hence at least half the units satisfy
\(a^d\not\equiv1\pmod q\); each such unit is an order separator and succeeds
by LEM-001.

There are \(K-\varphi(K)-1\) proper nonunit residues and at least
\(\varphi(K)/2\) successful units. Therefore

\[
\Pr[\mathrm{success}]
\ge \frac{K-1-\varphi(K)/2}{K}
\ge \frac{K-1}{2K}.
\]

A composite non-perfect-power has at least two distinct prime divisors, so
\(K\ge6\), and the last expression is at least \(5/12\).

## Correctness and termination

Every returned divisor is checked to lie strictly between \(1\) and \(K\), so
the algorithm never returns a false split. Prime leaves are recognized
deterministically. Exact perfect-power preprocessing preserves all
multiplicities.

At a non-perfect-power recursive node, one value of \(t\) in each cycle is a
witness. Each trial uses a fresh independent exact sample. Regardless of the
outcomes at other values, the conditional probability that the cycle succeeds
is at least \(5/12\). Thus the probability of surviving \(s\) complete cycles
is at most \((7/12)^s\), which tends to zero, and the expected number of cycles
is at most \(12/5\). Every child
divides \(N\), so the hereditary promise applies recursively. Induction on the
input value proves complete correctness, and the geometric tail proves
almost-sure termination.

## Expected bit complexity

The stage exponent satisfies \(M_B\mid B!\), hence

\[
\log_2 M_B\le\log_2(B!)\le B\log_2 B.
\]

It is built by \(B-1\) iterative LCM computations, and every intermediate
divides \(B!\). Each exponent \(d=tM_B\) has bit length

\[
O(B(k)\log B(k)+\log R(k)).
\]

Evaluating the two schedules is polynomial by hypothesis. One cycle makes
\(R(k)\) exact residue samples, modular exponentiations, and
GCD computations, all polynomial in \(k\). Its expected random-bit and
arithmetic cost is polynomial because exact sampling takes fewer than two
\(k\)-bit draws in expectation and the expected cycle count is at most
\(12/5\).

Exact maximal-exponent perfect-power detection is polynomial: enumerate
\(2\le e\le k\), compute the integer \(e\)-th root by binary search with
products capped above \(K\), and verify equality. The maximal exponent leaves
a non-perfect-power base, so perfect-power preprocessing nodes cannot be
consecutive. Charge each unary perfect-power node to its unique following
binary-tree node, which is either a split node or a prime leaf. The binary
split tree has fewer than \(2m\) nodes, so the complete recursion has fewer
than \(4m\) invocations. By monotonicity, each node's schedules are bounded by
those at \(m\); linearity of expectation therefore gives polynomial expected
total time and polynomial space.

## Recognition status and limitations

- The theorem is unconditional on the explicitly defined promise class.
- Membership is **promised, not recognized**. The bounded oracle factors small
  inputs only to test the definition; it is not part of the algorithm.
- The theorem neither bounds the density of the class nor proves that typical
  semiprimes satisfy it.
- The result is randomized. The condition \(q-1\nmid d\) does not ensure that a
  fixed base separates \(q\): that base may lie in a proper subgroup.
- No implication to general polynomial-time factoring or OPEN-002 is claimed.

## Falsification and reproducibility plan

1. Exhaust every small hereditary promised input with a finite residue oracle.
2. Count successful residues exactly at every bounded witness and check the
   \(5/12\) lower bound.
3. Minimize a fixed-base counterexample to the invalid deterministic
   replacement of the randomized step.
4. Differentially check registered candidate outcomes in Python, Rust, and C#.
