# BAR-005 - Multiplication straight-line compression barrier

Status: `PROVED` inside DEF-010's restricted model; bounded falsification and
independent adversarial and source-scope review are required before milestone
completion.

## DEF-010 - exact representation and evaluation semantics

Fix an integer modulus \(N\ge2\) and a residue \(g\in\mathbb Z/N\mathbb Z\).
A factor-oblivious multiplication straight-line program (MSLP) has nodes

\[
x_0=g,\qquad x_i=x_{a_i}x_{b_i}\pmod N
\quad(1\le i\le t),
\]

where \(0\le a_i,b_i<i\). Any subset of the existing nodes may be declared as
outputs. Associate a formal positive exponent to every node by

\[
e_0=1,\qquad e_i=e_{a_i}+e_{b_i}.
\]

The representation cost and generic modular evaluation cost both charge every
multiplication node. Parent indices and output indices are explicit. The
program is independent of the unknown factors of \(N\).

This model includes repeated squaring, ordinary addition chains, shared
addition chains, and same-base multiplication DAGs. It excludes inversion,
division, nonmultiplicative group operations, factor-dependent or adaptive
branches, special field endomorphisms, and implicit output expansion that is
not charged node by node. Consequently, BAR-005 is not a lower bound for a
general algebraic computation model.

## BAR-005 statement

For every DEF-010 program with \(t\) multiplication nodes:

1. \(x_i=g^{e_i}\pmod N\) for every node \(0\le i\le t\);
2. \(1\le e_i\le2^i\), so every exposed exponent has bit length at most
   \(t+1\);
3. computing a node equal as a formal power to \(g^d\) requires at least
   \[
   \lceil\log_2d\rceil=\ell(d)-1
   \]
   multiplication nodes when \(d\) is a power of two, and at least
   \(\lceil\log_2d\rceil\) nodes for every positive \(d\);
4. the bounds are tight for \(d=2^t\), by repeated squaring;
5. the program exposes at most \(t+1\) distinct node outputs.

Let a common factorization-independent schedule at input length \(k\) expose
nodes from one or more such programs with total charged multiplication-node
count \(T(k)\), including every output-producing program. Then its explicit
realized exponent family has

\[
E(k)\le T(k)+c,\qquad L(k)\le T(k)+1
\]

for the fixed number \(c\) of initial bases. In the one-base model \(c=1\).
Therefore, if \(T(k)=o(k\log k)\), BAR-004 applies and gives the same
subexponential hit-set and stipulated-population vanishing-fraction
conclusions.

If \(T(k)=k^{O(1)}\), every realized exponent has polynomial bit length.
Thus a short symbolic descriptor cannot hide a superpolynomial-bit exponent
while retaining polynomial generic multiplication cost in this model.
BAR-005 makes no conclusion at the boundary
\(T(k)\not=o(k\log k)\), and it does not show that a schedule at that boundary
has useful divisor structure.

## Proof

The residue identity follows by induction. It is true at node zero. If it is
true for all earlier nodes, then

\[
x_i
=x_{a_i}x_{b_i}
=g^{e_{a_i}}g^{e_{b_i}}
=g^{e_{a_i}+e_{b_i}}
=g^{e_i}\pmod N.
\]

For exponent growth, \(e_0=1=2^0\). Inductively, both parents of node \(i\)
have indices at most \(i-1\), so

\[
e_i=e_{a_i}+e_{b_i}
\le2^{a_i}+2^{b_i}
\le2^{i-1}+2^{i-1}
=2^i.
\]

Hence no program of \(t\) multiplications can realize an exponent exceeding
\(2^t\). If it realizes \(d\), then \(d\le2^t\) and
\(t\ge\lceil\log_2d\rceil\). For a positive integer \(d\),
\(\lceil\log_2d\rceil=\ell(d)-1\) exactly when \(d\) is a power of two; in
general \(\lceil\log_2d\rceil\ge\ell(d)-1\). Repeated squaring chooses
\((a_i,b_i)=(i-1,i-1)\) and attains \(e_i=2^i\), proving tightness on powers
of two.

A program has only its \(t+1\) existing nodes available as outputs. Summing
node charges across a fixed number of initial-base programs gives the schedule
bounds. Substitution into BAR-004 proves the \(o(k\log k)\) consequence.
The polynomial-cost statement follows directly from \(L(k)\le T(k)+1\).
\(\square\)

## REF-006 - compact tower descriptor does not imply compact evaluation

Refute the following claim inside DEF-010:

> The symbolic descriptor
> \(\operatorname{tower}(s)=2^{2^s}\) makes
> \(g^{\operatorname{tower}(s)}\bmod N\) evaluable using a number of generic
> modular multiplications polynomial in \(s\).

BAR-005 requires at least

\[
\log_2(2^{2^s})=2^s
\]

multiplications. Repeated squaring attains exactly \(2^s\), so the generic
cost is exponential in \(s\), despite the short syntax.

## Limitations

- Formal exponents are tracked before using modulus-specific identities such
  as an unknown group order. Coincidental residue equality is not treated as
  a factor-oblivious way to certify a smaller program for the target exponent.
- The result does not cover addition, subtraction, inversion, Frobenius maps,
  elliptic-curve operations, noncommutative programs, adaptive GCD branches,
  or algorithms that exploit known algebraic structure other than generic
  modular multiplication.
- The result does not exclude polynomial-cost schedules with
  \(\Theta(k\log k)\) or more multiplication nodes.
- It is not a promise recognizer, a natural-density theorem, a factoring lower
  bound, or a general classical factoring result.

## Falsification plan

1. Enumerate every commutative parent choice through a registered step bound.
2. Stop at the first node with formal exponent above \(2^i\).
3. Compare every enumerated residue with direct modular exponentiation.
4. Confirm that repeated squaring attains every registered maximum.
5. Evaluate the tower family through a registered descriptor level and compare
   its exact lower bound with repeated squaring.
6. Differentially compare selected programs and lower bounds in Python, Rust,
   and C#.
