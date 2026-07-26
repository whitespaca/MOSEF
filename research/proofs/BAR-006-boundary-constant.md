# BAR-006 - Constant-sensitive straight-line boundary barrier

Status: `PROVED` inside DEF-008--DEF-011 and DEF-010's restricted
multiplication-only model; independent adversarial and source-scope review
pending.

## DEF-011 - optimized exact divisor budget

For an exponent bit length \(\ell\ge1\), define

\[
b_\ell=\lceil\log_2(\ell+1)\rceil,\qquad
c_\ell=\lceil\log_2(b_\ell+1)\rceil,
\]

\[
T_\ell=\max\left\{1,
\left\lfloor\frac{\ell}{b_\ell^2c_\ell}\right\rfloor\right\}.
\]

Let \(A_\ell\) be the largest integer \(a\ge0\) satisfying

\[
(T_\ell+1)^a<2^\ell.
\]

Define

\[
C(\ell)=(\ell+1)^{T_\ell}2^{A_\ell},\qquad
R(L)=\max_{1\le\ell\le L}C(\ell).
\]

All quantities are exact integers. No floating-point logarithm is used by the
reference implementation.

## BAR-006 statement

Every positive integer \(d\), with ordinary unsigned bit length
\(\ell(d)\), satisfies

\[
\tau(d)\le C(\ell(d))\le R(\ell(d)).
\tag{1}
\]

Moreover,

\[
\log_2 R(L)
\le (1+o(1))\frac{L}{\log_2L}.
\tag{2}
\]

Let a common factorization-independent explicit schedule at input length
\(k\) contain \(E(k)=k^{O(1)}\) positive exponents, each of bit length at most

\[
L(k)\le(c+o(1))k\log_2k
\tag{3}
\]

for a fixed \(c\ge0\). Its global combined \(p-1/p+1\) hit set then satisfies

\[
|H(k)|\le 2^{ck+o(k)}.
\tag{4}
\]

If \(S_k\) is a stipulated finite odd-prime population such that every
distinct product from \(S_k\) has common input length \(k\) and

\[
|S_k|\ge2^{\alpha k}
\]

for fixed \(\alpha>c\), then the uniform unordered-pair fraction satisfying
the combined local divisibility-asymmetry promise is at most

\[
2^{-(\alpha-c)k+o(k)}
\tag{5}
\]

and tends to zero.

For a fixed number of initial bases, a common DEF-010 multiplication
straight-line schedule with total charged node count

\[
T(k)\le(c+o(1))k\log_2k
\]

has \(E(k)\le T(k)+O(1)\) and \(L(k)\le T(k)+1\), so (4)--(5) apply with the
same coefficient \(c\).

## Proof of the divisor estimate

Write

\[
d=\prod_i p_i^{a_i}
\]

and put \(\ell=\ell(d)\), \(T=T_\ell\). Split the prime factors at \(T\).
There are at most \(T\) small primes \(p_i\le T\). Since
\(2^{a_i}\le d<2^\ell\), each contributes at most \(\ell+1\) to
\(\tau(d)=\prod_i(a_i+1)\). Their total contribution is at most

\[
(\ell+1)^T.
\]

Let \(A=\sum_{p_i>T}a_i\) be the total multiplicity of the large primes.
Every such prime is at least \(T+1\), so

\[
(T+1)^A\le d<2^\ell.
\]

Thus \(A\le A_\ell\). For every positive integer \(a\),
\(a+1\le2^a\), and hence the large-prime contribution is at most
\(2^A\le2^{A_\ell}\). Multiplying the two contributions proves (1).

As \(\ell\to\infty\),

\[
b_\ell=\log_2\ell+O(1),\qquad
c_\ell=\log_2\log_2\ell+O(1),
\]

and

\[
T_\ell
=\frac{\ell}{b_\ell^2c_\ell}(1+o(1)).
\]

Therefore

\[
T_\ell\log_2(\ell+1)
=o\left(\frac{\ell}{\log_2\ell}\right).
\tag{6}
\]

The definition of \(A_\ell\) gives

\[
A_\ell<\frac{\ell}{\log_2(T_\ell+1)}.
\]

Also

\[
\log_2(T_\ell+1)
=\log_2\ell-O(\log_2\log_2\ell),
\]

so

\[
A_\ell
\le(1+o(1))\frac{\ell}{\log_2\ell}.
\tag{7}
\]

Equations (6)--(7) prove the one-length version of (2).
To pass to the monotone envelope, first note the exact crude bound

\[
\log_2C(\ell)\le2\ell:
\]

\(T_\ell b_\ell\le\ell\), and \(A_\ell<\ell\). For
\(\ell\le L/(\log_2L)^2\), this is \(o(L/\log_2L)\). For the remaining
\(\ell\), one has
\(\log_2\ell=\log_2L-O(\log_2\log_2L)\), the one-length estimate is uniform,
and \(\ell/\log_2\ell\le L/\log_2L\) for all sufficiently large \(L\).
Taking the maximum proves (2).

## Proof of the hit-set and population bounds

By DEF-008 and BAR-003, every hit prime is one more or one less than a
positive divisor of a scheduled exponent. Therefore

\[
|H(k)|
\le2E(k)R(L(k)).
\]

Taking binary logarithms, using (2)--(3), and observing that
\(\log_2E(k)=O(\log k)=o(k)\) gives (4). BAR-003 bounds the promised-pair
fraction on \(S_k\) by the fraction of pairs meeting the hit set. Since
\(|H(k)|/|S_k|\le2^{-(\alpha-c)k+o(k)}\), its exact pair bound gives (5).
BAR-005 supplies the stated DEF-010 node and bit-length inequalities.
\(\square\)

## Explicit divisor-rich boundary family

Let

\[
P_r=\prod_{j=1}^{r}p_j
\]

be the product of the first \(r\) primes. Rosser--Schoenfeld equation (3.13),
inspected in SRC-006, gives

\[
p_r<r(\log r+\log\log r)\qquad(r\ge6).
\]

Thus \(\ell(P_r)=O(r\log r)\). Conversely, \(p_j\ge j+1\), so the last half
of the product gives \(\ell(P_r)=\Omega(r\log r)\). Hence

\[
\ell(P_r)=\Theta(r\log r).
\tag{8}
\]

The exponent is square-free and has exactly

\[
\tau(P_r)=2^r
\tag{9}
\]

divisors. Trial enumeration of primes only through
\(p_r=O(r\log r)\), followed by exact multiplication, constructs \(P_r\) in
time polynomial in \(r\). Left-to-right binary exponentiation realizes
\(g^{P_r}\) with exactly

\[
\ell(P_r)-1+\operatorname{popcount}(P_r)-1
\le2\ell(P_r)-2
\tag{10}
\]

multiplication nodes. BAR-005 supplies the matching
\(\ell(P_r)-1\) lower bound, so this is an explicit
\(\Theta(r\log r)\)-node factor-oblivious family with exponential divisor
capacity.

Capacity is not prime yield. Equations (8)--(10) do not lower-bound the number
of divisors \(d\mid P_r\) for which \(d-1\) or \(d+1\) is prime. In addition,
\(P_r\) contains exactly one factor of two. For every odd prime \(q\), one of
\(q-1,q+1\) is divisible by four, so they cannot both divide \(P_r\).
Every nonzero one-exponent signature is therefore either \((1,0)\) or
\((0,1)\), never \((1,1)\).

The family establishes that the exact boundary and exponential divisor
capacity are nonvacuous. It does not establish a nonvanishing guarantee on a
stipulated external population.

## REF-007 - boundary node count alone is insufficient

Refute the following claim:

> Every common factor-oblivious DEF-010 schedule using
> \(\Theta(k\log k)\) multiplication nodes has a nonvanishing combined-promise
> fraction on each stipulated exponentially large common-input-length prime
> population.

Take \(t(k)=\lfloor k\log_2k\rfloor\), repeatedly square, and expose every
node exponent

\[
1,2,4,\ldots,2^{t(k)}.
\]

The union of all their positive divisors is just
\(\{2^j:0\le j\le t(k)\}\). Consequently at most
\(2(t(k)+1)\) odd primes can occur as one more or one less than a divisor.
The schedule uses \(\Theta(k\log k)\) charged nodes but has only a polynomial
global hit set. BAR-003 therefore makes its promised-pair fraction vanish on
every stipulated population of size \(2^{\Omega(k)}\). Node count at the
boundary is not sufficient; divisor shape and prime yield remain necessary.

## Limitations

- The leading constant in (2) is an upper-bound coefficient. No matching
  divisor-function lower bound or novelty claim is made.
- The population theorem is conditional on explicitly stipulated finite sets
  \(S_k\). It does not prove that such common-input-length prime populations
  exist with a chosen \(\alpha\), nor does it transfer to natural density.
- BAR-006 is silent when \(c\ge\alpha\), including the critical equality
  \(c=\alpha\).
- The primorial family has exponential divisor capacity but no proved
  asymptotic lower bound for prime hits \(d\pm1\).
- The DEF-010 consequence remains restricted to exact formal exponents in a
  factor-oblivious multiplication-only same-base DAG.
- No promise recognizer, general factoring algorithm, or general classical
  lower bound is claimed.

## Falsification plan

1. Exhaust all positive exponents below a registered power of two and stop at
   the first violation of the exact DEF-011 budget.
2. Construct first-primes primorials through a registered count, enumerate
   all \(2^r\) divisors, and verify exact binary node accounting.
3. Generate every candidate \(d\pm1\), decide primality by exact trial
   division against a complete sieve through the square root of the largest
   candidate, and compare direct signatures.
4. Stop at the first prime in both channels; the proof predicts none.
5. Differentially check selected primorial divisor counts, signatures,
   asymmetries, and hit counts in Python, Rust, and C#.
