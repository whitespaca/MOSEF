# BAR-003 - Combined-signature and balanced-semiprime density barrier

Status: proved after bounded falsification, cross-language differential
checks, and independent adversarial and source-scope review.

## Computation model and scope

Let \(\Delta\subset\mathbb Z_{>0}\) be a finite nonempty exponent set. In the
M3/M7 schedule at input bit length \(k\),

\[
\Delta(k)=
\{tM_B(k):1\le t\le R(k)\},\qquad
M_B(k)=\operatorname{lcm}(1,\ldots,B(k)),
\]

after duplicate exponents are removed. The schedule is constructed without
the factorization. The prime signatures below are analytical objects evaluated
at the unknown factors; they are not claimed to be computable from \(N\)
without factoring.

For an odd prime \(p\), define the combined divisibility signature

\[
\sigma_\Delta(p)=
\left(
\mathbf 1_{p-1\mid d},
\mathbf 1_{p+1\mid d}
\right)_{d\in\Delta}
\in\{0,1\}^{2|\Delta|}.                            \tag{1}
\]

For distinct odd primes \(p,q\), call \(N=pq\) locally combined-promised for
\(\Delta\) when at least one of the following holds, with either orientation
of \(p,q\):

\[
p-1\mid d,\ q-1\nmid d
\quad\text{or}\quad
p+1\mid d,\ q+1\nmid d                             \tag{2}
\]

for some \(d\in\Delta\). Because a square-free semiprime has no other
composite non-perfect-power divisors, this local condition is also the
hereditary union of DEF-004 and DEF-007 for that input.

## DEF-008 - combined schedule signature

Equation (1) is the combined \(p-1/p+1\) schedule signature. For a finite set
\(S\) of odd primes, define its hit set

\[
H_\Delta(S)=\{p\in S:\sigma_\Delta(p)\ne0\}.
\]

Write \(s=|S|\), \(h=|H_\Delta(S)|\), \(D=\max\Delta\), and let
\(\tau(d)\) be the number of positive divisors of \(d\).

## BAR-003 statement

The following assertions hold.

1. **Exact semiprime characterization.** For distinct odd primes \(p,q\),
   \(pq\) satisfies (2) if and only if
   \(\sigma_\Delta(p)\ne\sigma_\Delta(q)\).
2. **Finite-distribution upper bound.** Suppose \(s=|S|\ge2\) and every
   product of two distinct primes in \(S\) is evaluated with the same exponent
   set \(\Delta\).
   Under the uniform distribution on the \(\binom{s}{2}\) unordered pairs,
   the promised fraction \(\rho_\Delta(S)\) satisfies

   \[
   \rho_\Delta(S)
   \le
   \frac{\binom{s}{2}-\binom{s-h}{2}}{\binom{s}{2}}
   =
   \frac{h(2s-h-1)}{s(s-1)}.                       \tag{3}
   \]

   Here \(\binom{r}{2}=0\) for \(r<2\).
3. **Hit-set divisor bound.**

   \[
   h\le 2\sum_{d\in\Delta}\tau(d)
   \le4|\Delta|\sqrt D.                            \tag{4}
   \]

   Consequently, for \(s\ge2\),

   \[
   \rho_\Delta(S)
   \le
   \min\left\{1,\frac{8|\Delta|\sqrt D}{s-1}\right\}. \tag{5}
   \]
4. **Magnitude barrier.** Every prime \(p>D+1\) has
   \(\sigma_\Delta(p)=0\). Thus if \(\min S>D+1\), then
   \(\rho_\Delta(S)=0\).
5. **Balanced-semiprime corollary.** For \(n\ge2\), put

   \[
   S_n=\{p\text{ odd prime}:2^n<p<2^{n+1/2}\}.
   \]

   Every product of distinct primes in \(S_n\) has input length \(k=2n+1\).
   If \(|S_n|\ge2\) and

   \[
   \max\Delta(2n+1)+1<2^n,                         \tag{6}
   \]

   then the hereditary union of the M3 and M7 promise classes has exact
   density zero on these balanced semiprimes. More generally, if

   \[
   |\Delta(2n+1)|\sqrt{\max\Delta(2n+1)}
   =o(|S_n|),
   \]

   then the upper bound (5) tends to zero along those \(n\) for which
   \(|S_n|\ge2\).

This is a barrier for bounded exponent magnitude or sparse divisor structure.
It is not a lower bound for every polynomial-bit-length schedule: an exponent
with \(\Theta(k)\) bits may exceed a balanced prime factor and is not excluded
by (6).

## Proof

### Signature characterization

Condition (2) holds exactly when one coordinate of (1) is \(1\) for one prime
and \(0\) for the other. That is equivalent to the two bit vectors being
different. Swapping the two primes supplies the opposite orientation. This
proves assertion 1.

### Pair and hit-set counts

If two primes both lie outside \(H_\Delta(S)\), both signatures are the zero
vector and assertion 1 shows that their pair is not promised. Hence every
promised pair intersects \(H_\Delta(S)\). There are

\[
\binom{s}{2}-\binom{s-h}{2}
\]

such pairs, proving (3). Some pairs inside this count may still have equal
nonzero signatures, so (3) is an upper bound rather than an equality in
general.

If \(p\in H_\Delta(S)\), then for some \(d\in\Delta\), either \(p-1\mid d\)
or \(p+1\mid d\). For a fixed \(d\), every first type is \(p=r+1\) and every
second type is \(p=r-1\) for a positive divisor \(r\mid d\). There are at most
\(2\tau(d)\) candidates, before imposing primality or membership in \(S\).
A union bound over \(d\) proves the first inequality in (4).

Divisors below \(\sqrt d\) pair with divisors above \(\sqrt d\), with at most
one unpaired square root, so \(\tau(d)\le2\sqrt d\). Since \(d\le D\), the
second inequality in (4) follows. Equation (3) is at most
\(2h/(s-1)\); substituting (4) and the trivial probability bound \(1\) gives
(5).

### Magnitude and balanced intervals

If \(p>D+1\), then \(p-1>D\ge d\) and \(p+1>D\ge d\) for every
\(d\in\Delta\). Neither positive integer can divide \(d\), so the signature
is zero. If every prime in \(S\) has this property, all pair signatures are
equal and assertion 1 gives density zero.

For distinct \(p,q\in S_n\),

\[
2^{2n}<pq<2^{2n+1}.
\]

Therefore \(\lceil\log_2(pq)\rceil=2n+1\), so all pairs use the same schedule.
Condition (6) puts every prime in \(S_n\) above \(D+1\), proving the exact
zero-density statement. The asymptotic conditional statement follows
directly from (5). \(\square\)

## REF-004 - refuted small-magnitude coverage claim

The following claim is refuted:

> A combined \(p-1/p+1\) schedule can cover every balanced semiprime even when
> its largest exponent is smaller than both prime factors minus one.

If \(p,q>D+1\), both signatures are zero, so no scheduled exponent produces a
divisibility asymmetry in either channel. The smallest unrestricted witness is
\(\Delta=\{1\}\), \(N=15=3\cdot5\): neither \(p-1,p+1,q-1,\) nor \(q+1\)
divides \(1\).

## Recognition and density limitations

- BAR-003 chooses the density/barrier branch of M8. It does not give a
  factorization-independent exact recognizer for DEF-004, DEF-007, or their
  hereditary union.
- Computing \(\sigma_\Delta(p)\) from a known prime is polynomial in the input
  and exponent representation, but obtaining the unknown \(p\) from \(N\) is
  not discharged.
- The finite density is over an explicitly stated uniform pair distribution.
  No random-integer smoothness model or average-to-worst-case transfer is used.
- The zero-density corollary applies only under the magnitude inequality (6).
  It does not exclude schedules whose exponents have sufficiently large value
  while retaining polynomial bit length.
- No general classical factoring algorithm or lower bound is claimed.

## Falsification plan

1. Exhaust finite positive exponent families and odd-prime pairs.
2. Compare direct search for (2) with signature inequality.
3. Verify that every promised pair intersects the hit set and that (3) holds.
4. Verify \(h\le2\sum\tau(d)\) and the elementary square-root relaxation.
5. Exhaust primes above \(D+1\) to confirm zero signatures and zero pair
   success.
6. Differentially check selected signatures, witness outcomes, and hit counts
   in Python, Rust, and C#.
