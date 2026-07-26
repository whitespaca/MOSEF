# Adversarial audit of BAR-017

## Objective

Attempt to refute the exact polynomial factorization, the prime-power
valuation formula, the endpoint trichotomy, the compact cofactor algorithm,
and the stated output costs. This audit does not review unequal factors or
general signed circuits.

## Algebraic reconstruction

For each \(j\ge1\),
\[
X^{Aj}-X^j=X^j\left((X^{A-1})^j-1\right)
=X^j(X^{A-1}-1)S_j(X^{A-1}).
\]
Summing \(j=1,\ldots,A-1\) gives exactly
\[
S_A(X^A)-S_A(X)=X(X^{A-1}-1)H_A(X).
\]
The \(j=0\) terms cancel. No division or nonzero-denominator assumption is
used.

The exponent \(j-1+(A-1)k\) has residue \(j-1\) modulo \(A-1\), so distinct
pairs \((j,k)\) cannot collide. The count is \(A(A-1)/2\), and the largest
exponent occurs at \(j=A-1,k=A-2\), giving \(A(A-2)\).

## Valuation and branch reconstruction

For every \(p^e\mid N\), the base precheck gives \(\nu_p(g)=0\). The
valuation of the product is therefore
\[
\nu_p(D_A(g))=\nu_p(E_A(g))+\nu_p(H_A(g)),
\]
including infinity for a zero factor. Capping at \(e\) gives BAR-017 exactly.
A global unit endpoint preserves the GCD, a proper endpoint is already an
extraction, and a full endpoint forces a full difference. Mixed local
unit/full behavior is a proper global endpoint and is therefore not omitted.

## Compact recurrence reconstruction

With \(n=A-1\), \(y=x^n\), and
\(t_j=x^{j-1}S_j(y)\),
\[
t_{j+1}=xt_j+(xy)^j.
\]
Together with \(z_{j+1}=xyz_j\) and
\(h_{j+1}=h_j+t_{j+1}\), this is exactly the matrix recurrence recorded in
the proof. Raising one fixed \(3\times3\) matrix to \(n-1\) uses
\(O(\log A)\) modular matrix products. The \(A=2\) boundary uses the identity
matrix and returns \(H_2=1\).

## Independent evidence

- Exact integer polynomial reconstruction passed for every \(2\le A\le24\).
- Compact and expanded cofactor evaluation agreed in 27,209 modular cases.
- All 43,148 prime-power component valuations satisfied the capped sum.
- Every proper difference followed the endpoint or unit-endpoint cofactor
  branch; no full endpoint produced a proper difference.
- Python, Rust `u64`, and C# `BigInteger` implementations agreed on 12
  registered comparisons.
- The M21 witness reduces through the proper endpoint, while
  \((N,g,A)=(55,2,3)\) exercises the distinct unit-endpoint cofactor branch.

## Scope conclusion

The audit finds no defect in BAR-017 within DEF-022. The result must not be
extended to unequal factors, arbitrary coefficient vectors, longer chains,
adaptive factor-dependent choices, other groups, or general arithmetic
circuits.
