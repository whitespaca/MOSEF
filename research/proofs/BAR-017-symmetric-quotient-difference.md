# BAR-017: Exact reduction of the symmetric quotient-stage difference

## Claim status

- `DEF-022`: `DEFINITION`.
- `BAR-017`: `PROVED`; exact adversarial audit passed.
- `REF-018`: `REFUTED`.

No external theorem is imported. The proof uses polynomial identities,
prime-adic valuations, and binary matrix powering.

## DEF-022: symmetric depth-two cancellation

Fix a public integer \(A\ge2\). In the DEF-021 chain with factors
\((A,A)\) and coefficients \((-1,1)\), define
\[
D_A(X)=S_A(X^A)-S_A(X).
\]
Also define the endpoint and cofactor
\[
E_A(X)=X^{A-1}-1,
\]
\[
H_A(X)=\sum_{j=1}^{A-1}X^{j-1}S_j(X^{A-1})
      =\sum_{j=1}^{A-1}\sum_{k=0}^{j-1}
        X^{j-1+(A-1)k}.                                      \tag{1}
\]
For a unit base \(g\bmod N\), the evaluator retains the two stage quotients,
\(D_A(g)\), \(E_A(g)\), and \(H_A(g)\), together with every GCD. The
endpoint receives total unit, proper-factor, or full-collision semantics.
The public base, modulus, and exponent encodings, two geometric-sum
evaluators, endpoint exponentiation, compact cofactor evaluator, outputs,
GCDs, any unit-branch inversion, extraction, and requested formal output are
charged.

This is one symmetric depth-two family only. Unequal factors, arbitrary
coefficients, longer chains, adaptive construction, unrelated bases, other
groups, and general arithmetic circuits are outside scope.

## BAR-017

The exact factorization is
\[
D_A(X)=X E_A(X) H_A(X).                                      \tag{2}
\]
Consequently, if \(p^e\mid N\), \(p\nmid g\), and
\[
\alpha_p=\min(e,\nu_p(E_A(g))),\qquad
\beta_p=\min(e,\nu_p(H_A(g))),
\]
then
\[
\min(e,\nu_p(D_A(g)))=\min(e,\alpha_p+\beta_p).              \tag{3}
\]

Globally, the endpoint trichotomy is total:

1. If \(\gcd(E_A(g),N)=1\), then
   \(\gcd(D_A(g),N)=\gcd(H_A(g),N)\), and unit division recovers the cofactor
   residue.
2. If \(1<\gcd(E_A(g),N)<N\), the endpoint already factors \(N\).
3. If \(\gcd(E_A(g),N)=N\), then \(\gcd(D_A(g),N)=N\).

Thus every proper symmetric-difference GCD is accompanied either by a proper
endpoint GCD or, in the unit-endpoint branch, by the same proper cofactor GCD.
The M21 witness is in the first case:
\[
N=9,\quad g=2,\quad A=5,\quad
E_5(2)=2^4-1=15,\quad \gcd(E_5(2),9)=3.
\]

The cofactor branch is genuine rather than vacuous. At
\[
N=55,\quad g=2,\quad A=3,
\]
the stage quotients are \(7\) and \(18\), the endpoint is \(3\), and
\[
H_3(X)=1+X+X^3,\qquad H_3(2)=11.
\]
Both stages and the endpoint are units modulo \(55\), while
\(D_3(2)=11\) has proper GCD \(11\). BAR-017 characterizes this success as
the explicit cofactor branch; it does not eliminate it.

## Proof

Starting from the two geometric sums,
\[
\begin{aligned}
D_A(X)
 &=\sum_{j=0}^{A-1}(X^{Aj}-X^j)\\
 &=\sum_{j=1}^{A-1}X^j\left(X^{(A-1)j}-1\right)\\
 &=X(X^{A-1}-1)
   \sum_{j=1}^{A-1}X^{j-1}S_j(X^{A-1}),
\end{aligned}
\]
which proves (2) and (1). Because \(p\nmid g\), \(\nu_p(g)=0\).
Taking valuations of (2), then capping at \(e\), proves (3).

Multiplication by a unit preserves every prime-power capped valuation, which
proves the unit branch. A proper endpoint GCD is already an extraction. A
full endpoint divides \(D_A(g)\) by (2), so the difference is also full.
These cases are disjoint and exhaustive.

## Compact cofactor evaluation and output cost

Put \(n=A-1\), \(x=g\bmod N\), and \(y=x^n\bmod N\). For
\[
t_j=x^{j-1}S_j(y),\qquad z_j=(xy)^j,\qquad
h_j=\sum_{i=1}^{j}t_i,
\]
the initial state is \((t_1,z_1,h_1)=(1,xy,1)\), and
\[
\begin{pmatrix}t_{j+1}\\z_{j+1}\\h_{j+1}\end{pmatrix}
=
\begin{pmatrix}
x&1&0\\
0&xy&0\\
x&1&1
\end{pmatrix}
\begin{pmatrix}t_j\\z_j\\h_j\end{pmatrix}.                  \tag{4}
\]
Therefore \(H_A(g)=h_n\) is obtained by one exponentiation for \(y\) and
binary powering of the fixed \(3\times3\) matrix in (4), using
\(O(\log A)\) modular operations. The two geometric sums and endpoint use
the same asymptotic bound. Construction, GCDs, the optional inversion, and
extraction are polynomial in the charged input lengths.

The pairs in (1) have distinct exponents: the residue modulo \(A-1\) fixes
\(j-1\), then the quotient fixes \(k\). Hence \(H_A\) has exactly
\[
\sum_{j=1}^{A-1}j=\frac{A(A-1)}2
\]
nonzero monomials and degree \(A(A-2)\). A dense output has
\(A(A-2)+1\) slots. Compact evaluation does not materialize these outputs;
any requested sparse or dense list is charged by its actual size.

## Refuted statement

`REF-018` states that the symmetric repeated-factor difference yields an
unclassified extraction mechanism beyond any compact endpoint/cofactor
factorization. Equations (2) and (3) refute that statement. This scoped
reduction supplies neither a universal exponent schedule nor a recognition,
density, probability, or general factoring theorem.
