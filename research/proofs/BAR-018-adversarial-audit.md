# Adversarial audit of BAR-018

## Objective

Attempt to refute the stage Bezout identity, resultant, total prefix
trichotomy, unequal-difference factorization, endpoint polynomial GCDs,
prime-power valuations, boundary-factor claims, and formal-output counts.

## Algebraic reconstruction

Expanding \(S_B(Y)-B\) term by term gives
\[
S_B(Y)-B=(Y-1)\sum_{j=1}^{B-1}S_j(Y).
\]
Substitution \(Y=X^A\) produces the recorded multiple of \(S_A(X)\).
Therefore a common stage divisor divides \(B\), both formally and after
integer evaluation. At a root of \(S_A\), the second stage equals \(B\);
there are \(A-1\) roots with multiplicity one, giving
\(\operatorname{Res}(Q_1,Q_2)=B^{A-1}\).

For an endpoint root \(\zeta\ne1\), the audit independently reduces
\(D_{A,B}(\zeta)\) to \(\zeta S_{B-1}(\zeta)\). The simultaneous endpoint
condition is exactly \(\zeta^h=1\), excluding \(\zeta=1\) because
\(D_{A,B}(1)=B-A\ne0\). This proves both polynomial GCD equalities without
assuming that \(D_{A,B}\) is square-free.

## Total-branch reconstruction

When \(Q_1(g)\) is a unit, direct multiplication reconstructs the signed
aggregate from the rational residue. A proper prefix is already an output
factor. A full prefix forces \(g^A=1\), so the second stage becomes the
public integer \(B\). These cases are disjoint and exhaustive, including
mixed prime-power behavior.

Because the base is a unit, the \(X\) factor has valuation zero. Equation
\(D=gS_h(g)C(g)\) therefore gives the capped valuation sum at every prime
power. The unit/proper/full common-factor trichotomy follows without
cancelling a nonunit.

## Counterexample and boundaries

- \((N,g,A,B)=(25,3,3,2)\) has unit stages \(13,3\), unit common factor
  \(3\), difference \(15\), and cofactor/rational residue \(5\). This
  refutes the common-factor-only claim.
- \((9,2,5,7)\) has unit stages \(4,1\), difference \(6\), and proper
  common factor \(2S_2(2)=6\).
- \(A=2,B=3\) gives \(D=X(X^3+X-1)\), so the symmetric
  \(X^{A-1}-1\) endpoint does not persist.
- \((N,g,A,B,c_1,c_2)=(15,2,4,5,1,2)\) exercises the full-prefix public
  reduction \(F=2B=10\bmod15\).

Evaluation at zero and one verifies both boundary factors. If both vanished,
\(c_2=-c_1\) and \(c_1(A-B)=0\), contradicting the domain. The supports
intersect only at exponent zero, so the collected count has no hidden
cancellation.

## Independent evidence

- 42 ordered unequal factor pairs passed the stage coprimality, Bezout,
  common-step factor, and two endpoint-GCD checks.
- 672 signed boundary-factor checks and 802 exact cofactor coefficients
  agreed.
- 794,976 signed modular evaluations passed the total prefix reduction.
- 49,686 normalized differences and 78,792 prime-power components passed
  the factorization and valuation checks.
- All 11,256 proper differences followed the proper common-factor or
  unit-common-factor cofactor path.
- Python, Rust `u64`, and C# `BigInteger` agreed on 12 registered
  comparisons.

## Scope conclusion

The audit finds no defect in BAR-018 within DEF-023. The residual
unit-prefix rational/cofactor value remains a real extraction mechanism.
Nothing here classifies arbitrary rational residues, longer signed chains,
adaptive parameters, unrelated bases, other groups, or general circuits.
