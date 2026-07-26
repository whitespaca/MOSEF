# BAR-009 - Addition-subtraction chains do not evade factor-scale scarcity

## Status and scope

Status: `PROVED`.

This result concerns factor-oblivious same-base straight-line programs that
charge every product or ratio node, every modular inversion, and every
parent, sign, and output index. It extends the DEF-010 analysis only to this
addition-subtraction model. It does not cover implicit exponential batches,
modulus-specific exponent reduction, adaptive factor-dependent schedules,
special endomorphisms, unrelated multi-base expressions, other algebraic
channels, or general factoring.

The factor-scale hit-set conclusion concerns the exponent-mediated combined
\(p-1/p+1\) promise after the unit branch. A proper factor found by the
initial base GCD precheck is a separate algorithmic exit and is not silently
counted as a common prime-signature hit.

## DEF-014

Fix \(N\ge2\). A base precheck computes \(u=\gcd(g,N)\). A proper \(u\)
is returned as a factor, \(u=N\) is an invalid base, and otherwise
\(x_0=g\bmod N\) is a unit.

A factor-oblivious same-base addition-subtraction program has, for
\(1\le i\le t\),
\[
x_i=x_{a_i}x_{b_i}^{s_i}\pmod N,\qquad
0\le a_i,b_i<i,\qquad s_i\in\{-1,+1\}.
\]
Its signed formal exponents are
\[
z_0=1,\qquad z_i=z_{a_i}+s_i z_{b_i}.
\]
The constructor explicitly emits every parent pair, sign, and output index.
A product node uses one modular multiplication. A ratio node uses one
extended-GCD modular inversion and one modular multiplication. The
constructor, descriptor, evaluation, and retained output set are all charged.

## BAR-009 statement

Every DEF-014 node satisfies
\[
x_i=g^{z_i}\pmod N,\qquad |z_i|\le2^i.
\]
Consequently, exact formal realization of a nonzero signed exponent \(d\)
requires at least
\[
\lceil\log_2|d|\rceil
\]
charged nodes. Positive powers of two attain this bound by repeated
squaring.

For every unit \(g\bmod N\) and \(d>0\),
\[
\gcd(g^{-d}-1,N)=\gcd(g^d-1,N),
\]
where the negative power is evaluated using the modular inverse. An exponent
zero gives \(g^0-1=0\) and therefore the full collision \(N\). Thus the
candidate family exposed by a program is completely represented, without
loss, by the distinct positive integers
\[
\{|z_i|:z_i\ne0\}.
\]

For a fixed number of initial bases, let a common factorization-independent
schedule have total charged node count \(T(k)=O(k\log k)\). It exposes only
\(T(k)+O(1)\) distinct nonzero absolute exponents, each of bit length at most
\(T(k)+1=O(k\log k)\). BAR-008 therefore applies: at every fixed target
factor cap \(2^{\beta k}\), the global combined \(p-1/p+1\) hit set has size
\[
2^{O(k\log\log k/\log k)}=2^{o(k)}.
\]
On every stipulated common-input-length prime population \(S_k\), with
\(|S_k|\ge2^{\alpha k}\) and members at most \(2^{\beta k}\), the
promised-pair fraction is at most
\[
2^{-\alpha k+o(k)}
\]
and tends to zero.

## Proof

### 1. Unit and evaluation semantics

After the base precheck, \(x_0=g\) is a unit. Products and inverses of units
remain units, so every requested inverse exists. The extended Euclidean
algorithm computes it in polynomial bit complexity.

The residue identity is inductive. It holds at node zero. If it holds for
earlier nodes, then
\[
x_i
=x_{a_i}x_{b_i}^{s_i}
=g^{z_{a_i}}g^{s_i z_{b_i}}
=g^{z_{a_i}+s_i z_{b_i}}
=g^{z_i}\pmod N.
\]

### 2. Signed exponent growth

The base case is \(|z_0|=1=2^0\). Both parents of node \(i\) have index at
most \(i-1\), hence
\[
|z_i|
\le |z_{a_i}|+|z_{b_i}|
\le2^{a_i}+2^{b_i}
\le2^{i-1}+2^{i-1}
=2^i.
\]
If \(z_i=d\ne0\), this gives
\[
i\ge\lceil\log_2|d|\rceil.
\]
Choosing \(a_i=b_i=i-1\) and \(s_i=+1\) is repeated squaring and attains
\(z_i=2^i\).

### 3. Negative and zero outputs add no candidates

For \(d>0\),
\[
g^{-d}-1=-g^{-d}(g^d-1)\pmod N.
\]
The multiplier \(-g^{-d}\) is a unit modulo \(N\). Multiplication by a unit
does not change any capped prime-power valuation and therefore does not
change the GCD with \(N\). The negative and positive candidates are exactly
the same. If \(d=0\), the residue difference is zero and the GCD is all of
\(N\), not a proper factor.

It follows that signs and cancellations can be removed from the output
family by retaining only distinct nonzero absolute formal exponents.

### 4. Cost and factor-scale transfer

A \(t\)-node table has \(t\) signs and \(2t\) parent indices, hence
\(O(t\log(t+1))\) descriptor bits. It performs \(t\) modular
multiplications and at most \(t\) extended-GCD inversions, and exposes at
most \(t+1\) node outputs. A fixed number of programs with total node count
\(T(k)\) therefore yields
\[
E(k)\le T(k)+O(1),\qquad
L(k)\le T(k)+1
\]
after zero removal and absolute-value normalization.

When \(T(k)=O(k\log k)\), these are exactly the polynomial-list and
exponent-length hypotheses of BAR-008. Its hit-set bound follows, and BAR-003
gives the displayed stipulated-population density bound. No population
existence, recognition, or natural-density assertion is used. \(\square\)

## Falsification attempts

EXP-0013 exhaustively enumerates bounded parent/sign programs, checks every
node against the signed growth bound, compares formal exponents with direct
modular residues on unit bases, and separately checks positive/negative GCD
equality over a larger modulus/base/exponent box. It retains cancellations,
negative outputs, proper nonunit prechecks, and invalid full nonunits.
Selected signed programs and lower bounds are compared across Python, Rust,
and C#.

## Limitations

- The program is same-base and factor-oblivious.
- Every node, inverse, table entry, and retained output is charged.
- The total-node transfer uses \(T(k)=O(k\log k)\).
- BAR-008's fixed factor scale and stipulated-population hypotheses remain.
- Direct proper-factor exits from the base precheck are outside the
  exponent-mediated hit-set conclusion.
- No lower bound is claimed for implicit batches, fixed-modulus shortcuts,
  other groups, or general classical factoring.

## Independent review

An independent adversarial review reproduced the focused unit tests,
EXP-0013, and all 24 selected Python/Rust/C# differential checks. It also
enumerated a separate bounded full syntax including self-ratios, checked
prime-power GCD equality and lower-bound boundaries, and found no
counterexample. An independent source-scope audit confirmed that the proof
is elementary apart from internal BAR-003 and BAR-008 and requires no new
external citation.
