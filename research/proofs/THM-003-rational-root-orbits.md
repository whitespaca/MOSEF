# THM-003: Complete rational root-of-unity orbit classification

## Claim status

- `DEF-025`: `DEFINITION`.
- `THM-003`: `PROVED`; self-contained proof and exact adversarial audit.
- `REF-021`: `REFUTED`.

No external theorem is imported. The proof uses Galois conjugation in a
cyclotomic field, algebraic-integer norms, the elementary value of a
cyclotomic polynomial at one, and exact modular arithmetic.

## DEF-025: rational root orbit

Let \(A,B\ge2\) be unequal public integers,
\[
Q_1(X)=S_A(X),\qquad Q_2(X)=S_B(X^A),
\]
and let \(\zeta\) be a primitive root of unity of order \(n>1\). The M25
ratio is
\[
R_{A,B}(\zeta)=-\frac{Q_2(\zeta)}{Q_1(\zeta)}
\]
only when both stage values are nonzero. A primitive integer coefficient
pair \((c_1,c_2)\), unique up to simultaneous sign, makes
\(c_1Q_1(\zeta)+c_2Q_2(\zeta)=0\) exactly when
\(R_{A,B}(\zeta)=c_1/c_2\in\mathbb Q\).

Rationality is equivalently Galois-orbit fixedness:
\[
R_{A,B}(\zeta^j)=R_{A,B}(\zeta)
\quad\text{for every }j\in(\mathbb Z/n\mathbb Z)^\times.
\]
For a requested order it is also equivalent to exact rational
proportionality of the remainders of \(Q_1,Q_2\) modulo \(\Phi_n\).

For fixed \(A,B\), the compact order descriptor consists of
\[
h=\gcd(A-1,B-1),
\]
the Boolean condition \(A\equiv B\equiv3\pmod4\), and the Boolean condition
\(A\equiv5,\ B\equiv3\pmod6\). Listing all divisors of \(h\), or expanding
their cyclotomic polynomials, is separate output and is charged by the
factorization and output work actually requested.

## THM-003: complete classification

Outside both stage zero sets, \(R_{A,B}(\zeta)\) is rational if and only if
exactly one of the following descriptions applies:

1. \(n\mid\gcd(A-1,B-1)\), in which case
   \(R_{A,B}(\zeta)=-1\) and the canonical primitive pair is \((-1,1)\);
2. \(n=4\) and \(A\equiv B\equiv3\pmod4\), in which case
   \(R_{A,B}(\zeta)=1\) and the pair is \((1,1)\);
3. \(n=6\), \(A\equiv5\pmod6\), and \(B\equiv3\pmod6\), in which case
   \(R_{A,B}(\zeta)=2\) and the pair is \((2,1)\).

Thus the only exceptional orders beyond the M23 common-step family are
four and six. The value at \(n=1\) remains the separate M24 boundary
\(-B/A\).

## Conjugation and the phase restriction

Geometric sums obey
\[
S_A(\zeta^{-1})=\zeta^{1-A}S_A(\zeta),\qquad
S_B(\zeta^{-A})=\zeta^{-A(B-1)}S_B(\zeta^A).
\]
Therefore
\[
R_{A,B}(\zeta^{-1})
=\zeta^{-\{A(B-2)+1\}}R_{A,B}(\zeta).
\]
If the nonzero ratio is rational, complex conjugation fixes it, so
\[
n\mid K,\qquad K=A(B-2)+1. \tag{1}
\]
In particular \(\gcd(A,n)=1\). Let \(bA\equiv1\pmod n\), and put
\(k\equiv b-1\pmod n\), \(0\le k<n\).

The cleared M24 formula and (1) give
\[
\begin{aligned}
R_{A,B}(\zeta)+1
&=\zeta\left(\frac{\zeta^{A-1}-1}{\zeta^A-1}\right)^2.
\end{aligned}
\]
Because a rational value is fixed by the automorphism
\(\zeta\mapsto\zeta^b\),
\[
T:=R_{A,B}(\zeta)+1
=\frac{(1-\zeta^k)(1-\zeta^{-k})}
        {(1-\zeta)(1-\zeta^{-1})}
=u\overline u,\qquad
u=\frac{1-\zeta^k}{1-\zeta}. \tag{2}
\]
The element \(u\) is an algebraic integer. Hence rational \(T\) is a
rational algebraic integer and therefore an integer. In the distinguished
complex embedding,
\[
T=\frac{\sin^2(k\pi/n)}{\sin^2(\pi/n)}\ge0. \tag{3}
\]

If \(T=0\), then \(k=0\), so \(A\equiv1\pmod n\); (1) then gives
\(B\equiv1\pmod n\). This is family 1. If \(T=1\), then \(R=0\), contrary
to the assumption \(Q_2(\zeta)\ne0\). It remains to classify \(T\ge2\).
At \(n=2\), being outside both stage zero sets forces \(A\) and \(B\) odd,
which is already family 1, so the remaining norm argument has \(n>2\).

## Norm classification

Let \(d=\gcd(n,k)\) and \(m=n/d>1\), the order of \(\zeta^k\). In
\(\mathbb Q(\zeta)\),
\[
\left|\operatorname N(u)\right|
=\frac{\Phi_m(1)^{\varphi(n)/\varphi(m)}}{\Phi_n(1)}. \tag{4}
\]
Indeed, the conjugates of \(\zeta^k\) run through each primitive
\(m\)-th root \(\varphi(n)/\varphi(m)\) times. Since \(T=u\overline u\)
is rational, (4) becomes
\[
T^{\varphi(n)/2}
=\frac{\Phi_m(1)^{\varphi(n)/\varphi(m)}}{\Phi_n(1)}. \tag{5}
\]

For \(s>1\),
\[
\Phi_s(1)=
\begin{cases}
p,&s=p^a\text{ for a prime }p,\\
1,&s\text{ has at least two distinct prime divisors}.
\end{cases} \tag{6}
\]
For a prime power, (6) follows by dividing
\(X^{p^a}-1\) by \(X^{p^{a-1}}-1\) and taking \(X\to1\). If
\(s=p^a r\), \(r>1\), and \(p\nmid r\), the identity
\(\Phi_{p^a r}(X)=\Phi_r(X^{p^a})/\Phi_r(X^{p^{a-1}})\) gives value one.

If \(n=p^a\), then \(m=p^c\). Equation (5) gives
\[
v_p(T)=\frac{2}{\varphi(m)}-\frac{2}{\varphi(n)}.
\]
When \(m=n\), this is zero and \(T=1\). When \(m<n\), an integer value at
least one occurs only for \(p=2,a=2,c=1\). Hence
\[
(n,m,T)=(4,2,2).
\]
Then \(k=2\), \(b=3\), \(A\equiv3\pmod4\), and (1) forces
\(B\equiv3\pmod4\). This is family 2.

Suppose that \(n\) is not a prime power. If \(m\) is also not a prime
power, (5) gives \(T=1\). Otherwise \(m=p^c\), and
\[
T=p^{2/\varphi(m)}.
\]
Integrality forces \(\varphi(m)\mid2\), so the only prime-power
possibilities are
\[
(m,T)=(2,4),(3,3),(4,2).
\]
Equation (3) now finishes without approximation. For \(m=2\), the numerator
is one and \(T=4\) forces \(\sin^2(\pi/n)=1/4\), hence \(n=6\). For
\(m=3\), the numerator is \(3/4\), and \(T=3\) again forces \(n=6\).
For \(m=4\), the numerator is \(1/2\), and \(T=2\) would force \(n=6\),
contradicting \(4\mid n\).

At \(n=6,m=2\), one has \(k=3\), so \(b=k+1=4\) is not a unit; this cannot
be the inverse of \(A\). At \(n=6,m=3\), \(k=2\) or \(4\), but only
\(k=4\) makes \(b=k+1\) a unit. Thus \(A\equiv5\pmod6\), and (1) gives
\(B\equiv3\pmod6\). Here \(T=3\), so \(R=2\), proving family 3.

Conversely, direct substitution in (2), or exact reduction modulo
\(\Phi_n\), gives the stated rational value in each of the three families.
This completes the classification.

## Recognition, construction, and output cost

Given \(A,B,n\) in binary, membership is decided by a constant number of
integer comparisons, GCDs, and modular reductions. This is polynomial in
\(\log A+\log B+\log n\); it does not require factoring
\(A(B-2)+1\). Given only \(A,B\), the complete compact descriptor is
\[
\{n>1:n\mid h\}\quad\text{plus the enabled fixed orders }4,6.
\]
Producing the divisor list of \(h\) is not silently polynomial-time:
factoring \(h\), enumerating its divisors, and writing them are charged.
The fixed exceptional coefficients require constant output. Requested
\(\Phi_n\), dense numerator coefficients, or modular evaluations are charged
by their construction and output sizes. No schedule, density, success
probability, or general factoring result follows from the classification.

## Minimized phase-only obstruction and modular witnesses

The tempting sufficiency claim \(n\mid A(B-2)+1\) is false. At
\((A,B,n)=(2,4,5)\), the phase condition holds and neither stage vanishes,
but
\[
R_{2,4}(\zeta)=\frac{1+\sqrt5}{2}
\]
for a suitable primitive fifth root embedding, so the ratio is irrational.
Exact remainders modulo \(\Phi_5\) reproduce the obstruction.

The exceptional families also occur on both square-free and repeated-prime
moduli without being absorbed by the M24 public overlap bounds:

- \((N,g,A,B,c_1,c_2)=(55,2,3,7,1,1)\) gives aggregate GCD \(5\);
- \((75,2,3,7,1,1)\) gives aggregate GCD \(25\);
- \((35,12,5,3,2,1)\) gives aggregate GCD \(7\).

In all three cases both stage GCDs and both public coefficient--multiplier
bounds are units. These witnesses demonstrate nonempty modular paths; they
do not establish a success rate or universal algorithm.
