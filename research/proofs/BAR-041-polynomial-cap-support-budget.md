# BAR-041: polynomial numeric caps have insufficient prime support

## Claim status and exact scope

- `DEF-034`: `DEFINITION`.
- `BAR-041`: `PROVED`.
- `REF-043`: `REFUTED`.

The result applies to the exact branch-total DEF-032 selector with one public
numeric cap \(L(m)\) bounding every \(A,B,g\). It does not apply to
polynomial-bit encodings of exponentially large parameters, input-dependent
or adaptive schedules, other compact recurrence grammars, arbitrary
arithmetic circuits, or general classical factoring algorithms.

## DEF-034: exact-output support budget

Fix \(m\ge9\) and a DEF-032 cap \(L\ge m\). For each valid descriptor
\((i,A,B,g)\), let its eight positive public integers be

\[
\begin{array}{llll}
g,&S_A(g),&S_B(g^A),&B,\\
B\text{ or }2B,&\Phi_i(g),&R_i(A,B),&C_i(g).
\end{array}
\]

Here \(R_i\) is the exact cyclotomic/cofactor resultant and
\[
\Phi_i(g)C_i(g)=
\alpha_iS_A(g)+S_B(g^A),\qquad
\alpha_4=1,\quad\alpha_6=2.
\]
Define \(W(m,L)\) as the sum of the base-two bit lengths of all eight
integers over every descriptor. This is an analytical upper ledger. It
charges continuation integers even when the nonunit-base branch would skip
them, so it can only overestimate the branch-total prime support.

Let \(H_{m,L}\subseteq\mathcal P_m\) contain every balanced population prime
dividing at least one of these exact integers, and put
\[
b_m=\left\lfloor\frac{m-1}{2}\right\rfloor.
\]

## Uniform exact-output bound

Put \(b=\operatorname{bitlength}(L)\). For every valid descriptor,

\[
\begin{array}{c|c}
\text{integer}&\text{bit-length upper bound}\\
\hline
g&b\\
S_A(g)&Lb\\
S_B(g^A)&L^2b\\
B&b\\
B\text{ or }2B&b+1\\
\Phi_i(g)&2b+1\\
R_i(A,B)&4b+2\\
C_i(g)&L^2b+1.
\end{array}
\]

The two geometric-sum bounds follow from
\[
S_A(g)<g^A,\qquad S_B(g^A)<g^{AB}.
\]
For both exceptional families, the two linear-remainder coefficients whose
quadratic norm is \(R_i\) have absolute value at most \(L^2\). Hence
\[
0<R_i\le3L^4<2^{4b+2}.
\]
Finally the exceptional numerator is positive and
\[
0<C_i(g)\le\alpha_iS_A(g)+S_B(g^A)<2g^{AB},
\]
which gives the cofactor row without expanding the dense quotient.

Summing the rows gives the per-descriptor bound
\[
V(L)=2L^2b+Lb+9b+5.
\]
There are at most \(2(L-1)^3\) DEF-032 descriptors, so
\[
W(m,L)\le
2(L-1)^3\bigl(2L^2b+Lb+9b+5\bigr)
=O(L^5\log L).
\tag{1}
\]

## Exact support consequence

Every \(p\in\mathcal P_m\) is at least \(2^{b_m}\). The square-free product
of the distinct primes in \(H_{m,L}\) divides the product of all charged
exact integers. Therefore
\[
b_m|H_{m,L}|\le W(m,L).
\tag{2}
\]
Every population prime outside \(H_{m,L}\) has zero in all eight primitive
coordinates of every descriptor. The base is a unit for it, every
continuation value is a unit, and all derived aggregate or overlap
coordinates are Boolean functions of these zero primitive bits. Thus all
outside primes share the all-zero raw signature. In particular the selector
has at least
\[
\binom{
  |\mathcal P_m|-\left\lfloor W(m,L)/b_m\right\rfloor
}{2}
\tag{3}
\]
forced failed pairs whenever the upper entry is at least two.

## Balanced-population lower bound

SRC-006 inspects Rosser--Schoenfeld Corollary 1, equations (3.5) and (3.6):
\[
\frac{x}{\log x}<\pi(x)\quad(x\ge17),\qquad
\pi(x)<1.25506\frac{x}{\log x}\quad(x>1).
\]
Neither endpoint of the balanced interval is prime, so, with
\(x=2^{m/2}\),
\[
|\mathcal P_m|=\pi(x)-\pi(x/\sqrt2).
\]
Exact integer arithmetic gives
\[
\frac{1.25506}{\sqrt2}<\frac89.
\]
For \(m\ge10\), the source hypotheses hold and \(m/(m-1)\le10/9\). Hence
\[
|\mathcal P_m|
>
\frac{2^{m/2}}{81\log(2^{m/2})}
=\Omega\left(\frac{2^{m/2}}m\right).
\tag{4}
\]

## BAR-041 and REF-043

Let \(L(m)\) be any factorization-independent polynomially bounded numeric
cap allowed by DEF-032. Then \(L(m)\le Cm^d\) eventually for fixed
\(C,d\), so (1) makes \(W(m,L(m))\) polynomial in \(m\). Equations (2) and
(4) imply
\[
|\mathcal P_m|-\left\lfloor
\frac{W(m,L(m))}{b_m}
\right\rfloor\longrightarrow\infty.
\]
Therefore, for every sufficiently large \(m\), at least two balanced primes
share the all-zero DEF-032 signature. Their square-free \(m\)-bit product
receives no proper GCD from the complete selector.

Thus no polynomially bounded public numeric cap can make the exact DEF-032
selector injective on all sufficiently large complete balanced
populations. This proves `BAR-041` and refutes `REF-043`.

## Falsification and scope audit

- **Zero and negative values:** none occur. All geometric sums, public
  bounds, cyclotomics, resultants, and exact cofactors are positive.
- **Nonunit bases:** continuation values are overcharged in \(W\); a prime
  dividing the base already belongs to \(H_{m,L}\).
- **Full collisions:** equation (3) uses primes outside the union support,
  so every primitive GCD is one rather than a full collision.
- **Derived outputs:** aggregate support is cyclotomic OR cofactor support;
  retained overlaps are Boolean functions of primitive bits and cannot split
  two all-zero signatures.
- **Exact division:** the cofactor bound uses the proved exceptional identity
  and positivity, not modular division or a dense-output assumption.
- **Endpoint counting:** powers of two are composite and half-integer powers
  of two are nonintegral, so the displayed \(\pi\)-difference matches the
  strict balanced interval.
- **Source hypotheses:** \(m\ge10\) gives \(x\ge32\) and
  \(x/\sqrt2>1\), satisfying both inspected inequalities.
- **Compact-gap escape:** BAR-022's \(B=2^m+3\) family has polynomial
  parameter bit length but exponentially large numeric \(B\). It is outside
  every polynomial numeric cap and is not ruled out by BAR-041.
- **Quantifier order:** the cap may be any fixed polynomial function and the
  threshold may depend on it. The proof does not choose the input primes
  before the public schedule is fixed.
- **General factoring:** this is a grammar-specific obstruction. It is not a
  lower bound for adaptive schedules, other compact formulas, or arbitrary
  classical algorithms.
