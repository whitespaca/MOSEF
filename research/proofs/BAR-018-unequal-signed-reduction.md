# BAR-018: Exact unequal signed reduction and its residual boundary

## Claim status

- `DEF-023`: `DEFINITION`.
- `BAR-018`: `PROVED`; exact adversarial audit passed.
- `REF-019`: `REFUTED`.

No external theorem is imported. The proof uses polynomial identities,
root evaluation, Euclid's lemma, and prime-adic valuations.

## DEF-023: unequal depth-two signed form

Fix public unequal integers \(A,B\ge2\), nonzero public integers \(c_1,c_2\),
and
\[
Q_1(X)=S_A(X),\qquad Q_2(X)=S_B(X^A),\qquad
F(X)=c_1Q_1(X)+c_2Q_2(X).
\]
For a public unit \(g\bmod N\), the evaluator retains both quotient residues,
their GCDs, \(F(g)\), the total first-prefix branch, and every reduction
below. The normalized difference is
\[
D_{A,B}(X)=Q_2(X)-Q_1(X).
\]
Put \(h=\gcd(A-1,B-1)\).

The public base, modulus, factors, signed coefficients and their encodings,
two binary geometric-sum evaluations, coefficient reductions,
multiplications, addition, every GCD, any unit-branch inversion, extraction,
and any requested formal output are charged. This is one depth-two chain.
Longer chains, factor-dependent parameters, unrelated bases, other groups,
and general arithmetic circuits remain outside scope.

## Stage coprimality and total prefix reduction

Define
\[
T_B(Y)=\sum_{j=1}^{B-1}S_j(Y).
\]
Then
\[
Q_2(X)-B=(X-1)Q_1(X)T_B(X^A).                    \tag{1}
\]
Consequently
\[
\gcd_{\mathbb Q[X]}(Q_1,Q_2)=1,\qquad
\operatorname{Res}(Q_1,Q_2)=B^{A-1}.             \tag{2}
\]
For integers \(g,N\),
\[
\gcd(Q_1(g),Q_2(g),N)\mid\gcd(B,N).              \tag{3}
\]

Let \(L=Q_1(g)\) and \(Q=Q_2(g)\). The following trichotomy is total.

1. If \(\gcd(L,N)=1\), set
   \[
   R=c_1+c_2QL^{-1}\pmod N.
   \]
   Then \(F(g)=LR\pmod N\), hence
   \(\gcd(F(g),N)=\gcd(R,N)\).
2. If \(1<\gcd(L,N)<N\), the first prefix already factors \(N\).
3. If \(\gcd(L,N)=N\), then \(g^A=1\pmod N\), \(Q=B\pmod N\), and
   \[
   F(g)=c_2B\pmod N.                              \tag{4}
   \]

Thus a general coefficient pair reduces completely to a proper prefix,
the public full-prefix value, or one rational residue under a unit prefix.
The unit-prefix residue can still expose a new factor; this theorem
classifies that remaining location rather than eliminating it.

## Exact normalized-difference factorization

There is an integer polynomial \(C_{A,B}\) such that
\[
D_{A,B}(X)=X S_h(X)C_{A,B}(X).                   \tag{5}
\]
Moreover,
\[
\gcd_{\mathbb Q[X]}(D_{A,B},X^{A-1}-1)
=\gcd_{\mathbb Q[X]}(D_{A,B},X^{B-1}-1)
=S_h(X).                                         \tag{6}
\]
For every \(p^e\mid N\), because \(p\nmid g\),
\[
\min(e,\nu_p(D_{A,B}(g)))
=\min\!\left(e,\nu_p(S_h(g))+\nu_p(C_{A,B}(g))\right).       \tag{7}
\]

Globally, the common factor \(gS_h(g)\) gives another total trichotomy.

1. If \(\gcd(gS_h(g),N)=1\), unit division recovers \(C_{A,B}(g)\), and its
   GCD equals the difference GCD.
2. If \(1<\gcd(gS_h(g),N)<N\), the common factor already extracts a factor.
3. If \(\gcd(gS_h(g),N)=N\), the difference is a full collision.

The residual cofactor path is genuine. At
\[
(N,g,A,B)=(25,3,3,2)
\]
the stages are \(13\) and \(3\), both units, while the difference is \(15\)
and has GCD \(5\). Here \(h=1\), so the common factor is the unit \(g=3\);
unit division and the rational-prefix reduction both return \(5\bmod25\).

The common-factor path is also genuine. At
\[
(N,g,A,B)=(9,2,5,7)
\]
the stages are \(4\) and \(1\), both units, while the difference is \(6\).
Here \(h=2\) and \(gS_2(g)=6\), whose GCD is \(3\).

## Boundary factors and formal output

Only the constant monomial is shared by the supports of \(Q_1\) and \(Q_2\).
Therefore
\[
X\mid F \iff c_1+c_2=0,\qquad
(X-1)\mid F \iff c_1A+c_2B=0.                   \tag{8}
\]
For unequal \(A,B\) and nonzero \(c_1,c_2\), both conditions cannot hold.
The formal degree is \(A(B-1)\), and the collected nonzero-monomial count is
\[
A+B-2\quad\text{if }c_1+c_2=0,\qquad
A+B-1\quad\text{otherwise}.                     \tag{9}
\]
The cofactor in (5) has degree \(A(B-1)-h-1\). Compact residue evaluation
does not materialize any expanded polynomial. A requested sparse or dense
coefficient list is charged by its actual output size.

## Proof

For (1), use
\[
S_B(Y)-B=(Y-1)\sum_{j=1}^{B-1}S_j(Y)
\]
with \(Y=X^A\), and \(X^A-1=(X-1)S_A(X)\). Any common polynomial divisor of
\(Q_1\) and \(Q_2\) divides the nonzero constant \(B\), proving coprimality.
At every nontrivial \(A\)-th root \(\zeta\), \(Q_2(\zeta)=B\); since \(Q_1\)
is monic of degree \(A-1\), the root product definition gives the resultant.
Evaluating (1) at \(g\) proves (3). The three prefix branches follow from
ordinary modular inversion and from
\((g-1)S_A(g)=g^A-1\), proving (4).

The constant terms of \(Q_1\) and \(Q_2\) cancel in \(D_{A,B}\), so \(X\)
divides the difference. Let \(\zeta\ne1\) satisfy
\(\zeta^{A-1}=1\). Then \(\zeta^A=\zeta\), \(S_A(\zeta)=1\), and
\[
D_{A,B}(\zeta)=S_B(\zeta)-1=\zeta S_{B-1}(\zeta).
\]
This vanishes exactly when \(\zeta^{B-1}=1\). The common roots are precisely
the nontrivial \(h\)-th roots of unity. Since \(X^{A-1}-1\) is square-free,
the first equality in (6) follows; interchanging \(A,B\) proves the second.
In particular \(S_h\mid D_{A,B}\). It is coprime to \(X\), proving (5) in
\(\mathbb Z[X]\) by monic polynomial division. Taking valuations of (5)
proves (7) and the trichotomy.

Finally, evaluation at zero and one proves (8). The two support sets meet
only at exponent zero, proving (9) and the degree claims.

## Refuted statement

`REF-019` states that every proper unequal normalized-difference GCD is
already exposed by the natural common factor \(gS_h(g)\). The
\((25,3,3,2)\) witness refutes it: the common factor is a unit and the
residual cofactor has GCD \(5\). BAR-018 supplies no universal schedule,
recognizer, density, probability, or general classical factoring theorem.
