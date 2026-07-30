# THM-002 - Random nonsplit Lucas parameters on a hereditary promise class

Status: `PROVED` after bounded falsification and independent adversarial and
source-scope review.

## Computation model and schedule

Let \(B(k)\) and \(R(k)\) be fixed nondecreasing positive integer functions
that are polynomially bounded and computable in time polynomial in \(k\). Put

\[
M_B(k)=\operatorname{lcm}(1,2,\ldots,B(k)).
\]

All complexity is measured in the binary input length. A fresh parameter
\(P\) is sampled exactly uniformly from \(\{0,\ldots,K-1\}\) by rejection
sampling unbiased bits. The Lucas sequence is

\[
V_0(P,1)=2,\qquad V_1(P,1)=P,\qquad
V_{j+1}(P,1)=PV_j(P,1)-V_{j-1}(P,1).
\]

For \(d>0\), one exact candidate first computes

\[
h_\Delta=\gcd(P^2-4,K).
\]

If \(h_\Delta\) is proper it is returned. In every other branch, including
\(h_\Delta=K\), the candidate computes

\[
h_L=\gcd(V_d(P,1)-2,K)
\]

and returns it only when it is proper. A miss or full collision is retried;
neither is interpreted as primality or as nonmembership.

## LEM-003 - exact Lucas root count

Let \(q\) be an odd prime and \(d>0\). Then

\[
\#\{P\in\mathbb F_q:V_d(P,1)=2\}
=\frac{\gcd(d,q-1)+\gcd(d,q+1)}2.                 \tag{1}
\]

Among these roots, exactly

\[
1+\mathbf 1_{2\mid d}                              \tag{2}
\]

are discriminant-degenerate parameters \(P=\pm2\). Also,

\[
\#\left\{P\in\mathbb F_q:
\left(\frac{P^2-4}{q}\right)=-1\right\}=\frac{q-1}{2}, \tag{3}
\]

where the notation in (3) is the Legendre symbol.

### Proof

We first discharge the finite-field structure used below. Every finite
multiplicative subgroup \(H\) of a field is cyclic. Indeed, if \(e\) is its
exponent, then every element of \(H\) is a root of \(X^e-1\), so
\(|H|\le e\); finite abelian group structure supplies an element whose order
is \(e\) by combining elements of maximal prime-power order, while
\(e\le|H|\). Thus \(e=|H|\) and that element generates \(H\).
Consequently \(\mathbb F_q^\times\) and
\(\mathbb F_{q^2}^\times\) are cyclic of orders \(q-1\) and \(q^2-1\).
The norm map \(x\mapsto x^{q+1}\) sends a generator of the latter group to
an element of order \(q-1\), so its kernel is cyclic of order \(q+1\).

Let \(\alpha\) be a root of

\[
X^2-PX+1.
\]

Then the other root is \(\alpha^{-1}\), and the recurrence gives

\[
V_d(P,1)=\alpha^d+\alpha^{-d}.
\]

If \(P^2-4\) is a nonzero square, \(\alpha\) lies in
\(\mathbb F_q^\times\), a cyclic group of order \(q-1\). If the discriminant
is a nonsquare, \(\alpha\) lies in the norm-one subgroup of
\(\mathbb F_{q^2}^\times\), which is cyclic of order \(q+1\). In either group,

\[
\alpha^d+\alpha^{-d}=2
\quad\Longleftrightarrow\quad
(\alpha^d-1)^2=0
\quad\Longleftrightarrow\quad
\alpha^d=1.
\]

A cyclic group of order \(r\) has exactly \(\gcd(d,r)\) roots of
\(X^d=1\). Away from \(\alpha=\pm1\), the map
\(\alpha\mapsto P=\alpha+\alpha^{-1}\) has fibers
\(\{\alpha,\alpha^{-1}\}\). The element \(1\) always contributes the
degenerate parameter \(P=2\), and \(-1\) contributes \(P=-2\) exactly when
\(d\) is even. Splitting the roots between the two cyclic groups, pairing the
nondegenerate roots, and counting the degenerate parameters only once gives
(1) and (2).

For (3), count pairs \((P,y)\in\mathbb F_q^2\) satisfying

\[
y^2=P^2-4.
\]

The invertible change \(u=P-y\), \(v=P+y\) identifies these pairs with
\(uv=4\), of which there are \(q-1\). Therefore

\[
\sum_{P\in\mathbb F_q}
\left(1+\left(\frac{P^2-4}{q}\right)\right)=q-1,
\]

so the character sum is \(-1\). There are two zero-discriminant parameters.
If \(n_+\) and \(n_-\) are the nonzero square and nonsquare counts, then

\[
n_++n_-=q-2,\qquad n_+-n_-=-1,
\]

which gives \(n_-=(q-1)/2\). \(\square\)

## DEF-007 - hereditary nonsplit Lucas asymmetry

An odd composite non-perfect-power integer \(K\), with
\(k=\operatorname{bitlength}(K)\), has a \((B,R)\)-nonsplit Lucas asymmetry witness if
there are distinct odd primes \(p,q\mid K\) and
\(1\le t\le R(k)\) such that, for

\[
d=tM_B(k),
\]

we have

\[
p+1\mid d,\qquad q+1\nmid d.                       \tag{4}
\]

An input is in the hereditary promise class when every odd divisor of the
input that is composite and not a perfect power has such a witness at its
local bit length. Membership is promised and may depend on the unknown
factorization; the algorithm does not recognize it.

The class is nonempty. For the constant schedule \(B(k)=2,\ R(k)=2\), the
input \(K=15\) has the witness \(p=3,\ q=5,\ t=2\), because
\(d=2\operatorname{lcm}(1,2)=4\), so \(p+1=4\mid d\) and
\(q+1=6\nmid d\).

## THM-002 statement

For every fixed schedule pair \(B,R\) above, there is a classical Las Vegas
algorithm that completely factors every input in the hereditary nonsplit
Lucas-asymmetric promise class, is always correct, terminates almost surely,
and runs in expected time polynomial in the binary input length.

At each witness trial, its probability of returning a proper factor is at
least \(1/12\).

M84 makes the finite-budget form executable and total on every positive
input. With \(s\) complete cycles at each randomized node, the local
on-promise unresolved probability is at most \((11/12)^s\), and the complete
factorization unresolved probability is at most
\(\min\{1,4m(11/12)^s\}\). The all-branch proof is in
`research/proofs/M84-bounded-total-promise-wrappers.md`.

## Algorithm

On a residual integer \(K\):

1. run deterministic polynomial-time primality testing;
2. perform exact maximal-perfect-power preprocessing and recurse on the base;
3. if \(K\) is even, return the factor \(2\);
4. repeatedly execute complete cycles over \(1\le t\le R(k)\);
5. at every \(t\), put \(d=tM_B(k)\), sample a fresh exact uniform
   \(P\bmod K\), and evaluate the discriminant and sequence GCD branches above;
6. validate every returned split and recurse on both children.

## One-trial success probability

Fix a residual odd composite \(K\) and a witness \((p,q,t)\). Projection of a
uniform \(P\bmod K\) to \((P\bmod p,P\bmod q)\) is uniform on
\(\mathbb F_p\times\mathbb F_q\).

At \(p\), restrict to parameters with nonsquare discriminant. There are
\((p-1)/2\) such parameters by LEM-003. If \(\alpha\) is a root of
\(X^2-PX+1\), then \(\alpha\) is in the norm-one group of order \(p+1\).
Since \(p+1\mid d\), we have \(\alpha^d=1\), hence

\[
V_d(P,1)=2\pmod p.                                  \tag{5}
\]

At \(q\), call a parameter bad when it is a nondegenerate root of
\(V_d(P,1)-2\). Since \(p+1\mid d\), the exponent \(d\) is even. LEM-003
therefore gives

\[
C_q(d)
=\frac{\gcd(d,q-1)+\gcd(d,q+1)}2-2                 \tag{6}
\]

bad parameters. The first GCD in (6) is at most \(q-1\). Because
\(q+1\nmid d\), the second GCD is a proper divisor of \(q+1\), hence is at
most \((q+1)/2\). Consequently,

\[
C_q(d)\le\frac{3q-9}{4}<\frac{3q}{4},               \tag{7}
\]

so more than \(q/4\) parameters modulo \(q\) are safe.

If a safe parameter is discriminant-degenerate modulo \(q\), then the
discriminant GCD contains \(q\) but not \(p\), by the nonsplit choice at
\(p\), and is a proper factor. Otherwise (5) holds at \(p\) while the sequence
value is not \(2\) modulo \(q\). Any earlier discriminant factor is proper
because it omits \(p\); if there is no such factor, the sequence GCD contains
\(p\) and omits \(q\), so it is proper.

The probability of this event is therefore

\[
\frac{p-1}{2p}\cdot\frac{q-C_q(d)}q
\ge\frac13\cdot\frac{q-C_q(d)}q
>\frac13\cdot\frac14=\frac1{12}.                    \tag{8}
\]

The theorem states the conservative lower bound \(1/12\).

## Correctness and termination

Every returned divisor is checked to lie strictly between \(1\) and the
current input, so every recursive split is correct. Prime recognition and
exact perfect-power expansion preserve multiplicities.

One value of \(t\) in every complete cycle is a witness. Conditional on any
history, its fresh parameter succeeds with probability at least \(1/12\).
Thus the probability of surviving \(s\) cycles is at most
\((11/12)^s\). The expected number of cycles is at most \(12\), and
termination is almost sure. The hereditary promise applies at every recursive
odd composite non-perfect-power child.

## Bit complexity

The standard LCM construction gives

\[
\log_2M_B(k)=O(B(k)\log B(k)),
\]

so every \(d=tM_B(k)\) has

\[
O(B(k)\log B(k)+\log R(k))
\]

bits. Exact uniform rejection sampling needs fewer than two \(k\)-bit draws
in expectation. Binary Lucas evaluation uses \(O(\log d)\) modular matrix
multiplications, followed by polynomial-time GCDs.

Each complete cycle evaluates \(R(k)\) candidates, the expected cycle count
is constant, and the fixed schedule functions are polynomially bounded.
After maximal-perfect-power preprocessing, the recursion has \(O(m)\) nodes
by the same multiplicity accounting as THM-001. Expected total time and space
are polynomial in the original bit length \(m\).

## Scope and falsification plan

- The promise is factor dependent and is not recognized by the algorithm.
- The theorem is not a density statement and gives no outside-promise
  termination guarantee.
- It does not assert statistical independence from Pollard \(p-1\).
- It uses a fresh uniform parameter at every attempt; a fixed parameter is
  not covered.
- It does not give a general classical polynomial-time factoring algorithm.

The bounded falsification checks are:

1. enumerate (1) over small odd primes and exponents;
2. enumerate (3) over the same primes;
3. enumerate the CRT success event for every ordered witness in a registered
   box and compare it with the product formula;
4. verify that every parameter in the proved event exposes an exact factor;
5. include repeated-prime, multiprime, even, degenerate, miss, and collision
   boundaries;
6. differentially verify selected counts and candidate branches in Python,
   Rust, and C#.

The registered search completed all six checks over odd primes through 43
and exponents through 80, with 714 ordered witnesses and 75,934 proved-event
splits. Its canonical summary SHA-256 is
`23ed0067d2ccb642c3676ff4ea3f5c34e1e622f6372626aa84377eac74b7d905`.
Independent review additionally checked 2,481,900 root parameters through
odd primes below 300 and exponents through 300, plus 1,080 repeated-factor
and multiprime event splits, without finding a counterexample.
