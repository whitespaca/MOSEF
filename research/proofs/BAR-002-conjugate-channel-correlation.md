# BAR-002 - Conjugate Lucas pairing cannot add separation

Status: `DRAFT` pending bounded falsification and independent adversarial
review.

## Exact channel definitions

Fix an integer \(N\ge2\), a unit \(a\in(\mathbb Z/N\mathbb Z)^\times\),
and \(d>0\).

The multiplicative channel evaluates

\[
G_M(N,a,d)=\gcd(a^d-1,N).
\]

For an arbitrary parameter \(P\), define the Lucas sequence

\[
V_0(P,1)=2,\qquad V_1(P,1)=P,\qquad
V_{j+1}(P,1)=P V_j(P,1)-V_{j-1}(P,1).
\]

The Lucas channel first records

\[
G_\Delta(N,P)=\gcd(P^2-4,N)
\]

and then evaluates

\[
G_L(N,P,d)=\gcd(V_d(P,1)-2,N).
\]

A GCD succeeds exactly when it lies strictly between \(1\) and \(N\).
The implementation distinguishes a discriminant factor, a miss, a proper
factor, and a simultaneous collision. When \(G_\Delta=N\), it additionally
distinguishes whether the sequence GCD misses, factors, or collides. This is
more informative than Williams's algorithmic rule to reject a parameter with
\(G_\Delta\ne1\).

The **conjugate pairing** is the factorization-independent map

\[
P(a)=a+a^{-1}\pmod N.
\]

## Lemma 1 - exact conjugate identities

For every \(d\ge0\),

\[
V_d(P(a),1)=a^d+a^{-d}\pmod N.
\]

Consequently,

\[
V_d(P(a),1)-2
 =a^{-d}(a^d-1)^2\pmod N                                      \tag{1}
\]

and

\[
P(a)^2-4
 =a^{-2}(a^2-1)^2\pmod N.                                     \tag{2}
\]

### Proof

Put \(W_d=a^d+a^{-d}\) in \(\mathbb Z/N\mathbb Z\). Then \(W_0=2\),
\(W_1=a+a^{-1}=P(a)\), and direct multiplication gives

\[
W_{d+1}=P(a)W_d-W_{d-1}.
\]

The initial values and recurrence uniquely determine the sequence, so
\(W_d=V_d(P(a),1)\). Expanding
\(a^{-d}(a^d-1)^2\) gives \(a^d+a^{-d}-2\), proving (1).
Equation (2) is the special case obtained by expanding
\((a-a^{-1})^2\). \(\square\)

## Lemma 2 - prime support and valuations

Let \(p^e\Vert N\). Then

\[
\min\!\left(e,\nu_p(V_d(P(a),1)-2)\right)
=\min\!\left(e,2\nu_p(a^d-1)\right),                          \tag{3}
\]

where \(\nu_p(0)=+\infty\). In particular, the two differences have
identical prime support. If \(N\) is square-free, then

\[
G_L(N,P(a),d)=G_M(N,a,d).                                     \tag{4}
\]

### Proof

Because \(a\) is a unit modulo \(N\), it is also a \(p\)-adic unit for every
\(p\mid N\). The factor \(a^{-d}\) in (1) therefore has valuation zero.
Taking valuations in (1) and capping them at \(e\) gives (3). Positivity of
the capped valuation is unchanged by doubling, which proves equal prime
support. When every \(e=1\), the capped valuations themselves are equal,
which proves (4). \(\square\)

## BAR-002 statement

Let \(\Delta\) be a finite set of positive exponents containing \(2\).
For fixed \(N\) and unit \(a\), consider:

1. the multiplicative family \(G_M(N,a,d)\), \(d\in\Delta\); and
2. the conjugately derived Lucas family consisting of
   \(G_\Delta(N,P(a))\) and \(G_L(N,P(a),d)\), \(d\in\Delta\).

If any derived Lucas GCD is a proper factor, then some multiplicative GCD in
the same family is a proper factor. Therefore adding this Lucas family does
not enlarge the success domain of the multiplicative family.

### Proof

If \(G_L(N,P(a),d)\) is proper, its capped valuation profile is neither all
zero nor full. By (3), the profile of \(a^d-1\) is nonzero at exactly the
same primes. At any prime where the doubled valuation is not full, the
undoubled valuation is also not full. Thus \(G_M(N,a,d)\) is proper.

If \(G_\Delta(N,P(a))\) is proper, equation (2) applies the same argument to
\(a^2-1\), so \(G_M(N,a,2)\) is proper. The hypothesis \(2\in\Delta\)
places that multiplicative candidate in the family.

The combined family always retains every multiplicative candidate.
It therefore succeeds whenever the multiplicative family succeeds, while
the preceding implications show it cannot succeed on any additional input.
The success domains are equal. \(\square\)

## Strict degradation on prime powers

The derived Lucas channel can lose a split that the multiplicative channel
finds. For

\[
N=25,\qquad a=2,\qquad d=4,\qquad P(a)=15,
\]

the discriminant GCD is \(1\), but

\[
G_M(25,2,4)=5,\qquad G_L(25,15,4)=25.
\]

The valuation is doubled from one to two, turning a proper factor into a
simultaneous collision. This does not contradict BAR-002 because the combined
family retains the successful multiplicative candidate.

## Relation to Williams's \(p+1\) method

Williams's imported Lucas theorem distinguishes the Legendre-symbol branch
\((\Delta/p)=-1\), which gives the nonsplit \(p+1\) behavior, from
\((\Delta/p)=+1\), which gives the split \(p-1\) behavior. Under the conjugate
pairing,

\[
\Delta=P(a)^2-4=(a-a^{-1})^2.
\]

Away from the degenerate zero-discriminant case this is a square modulo every
prime divisor. The pairing therefore forces the split branch rather than
constructing Williams's nonsplit \(p+1\) channel. The primary source calls
the methods analogous and reports empirical use of both; it does not claim
independence of this pairing.

## Scope limitation: arbitrary Lucas parameters

BAR-002 applies only to \(P=a+a^{-1}\). It does not state that independently
selected Lucas parameters are redundant. For example,

\[
N=15,\qquad a=2,\qquad P=9,\qquad d=3
\]

gives

\[
G_M(15,2,3)=1,\qquad G_\Delta(15,9)=1,\qquad G_L(15,9,3)=5.
\]

Thus an independently selected nonsplit parameter can complement a
multiplicative miss at the same exponent. No theorem in this milestone turns
that finite example into an independence distribution, success probability,
or universal factoring guarantee.

## Complexity and theorem limits

- Computing \(P(a)\) uses an extended GCD and modular operations polynomial in
  \(\log N\); evaluating either sequence by binary Lucas composition is also
  polynomial in \(\log N+\log d\).
- The identity is algebraic and unconditional. It is not an asymptotic lower
  bound for every two-channel construction.
- BAR-002 does not cover independently sampled \(P\), other algebraic groups,
  adaptive parameter selection, or compact batch evaluation.
- No general classical factoring lower bound or polynomial-time factoring
  algorithm follows.

## Falsification plan

1. Exhaustively verify (1) and (2) for bounded composite \(N\), unit bases,
   and positive exponents.
2. Verify (4) on every square-free modulus in the registered box.
3. Search for a conjugately derived Lucas-only family success with
   \(2\in\Delta\).
4. Minimize prime-power valuation degradation and discriminant-degenerate
   sequence factors.
5. Search separately for independently parameterized Lucas factors after a
   multiplicative miss.
6. Differentially compare every exact failure branch in Python, Rust, and C#.
