# BAR-014: A nested geometric quotient reduces despite failed intermediate division

## Claim status

- `DEF-019`: `DEFINITION`.
- `BAR-014`: `PROVED`.
- `REF-015`: `REFUTED`.

The proof is elementary and imports no external theorem.

Two independent adversarial reviews passed after the statement was repaired
to distinguish residue equality from GCD equality and to charge sparse and
dense quotient outputs separately.

## DEF-019: charged two-stage quotient

Fix \(N\ge2\), an integer base \(g\), and public positive integers \(A,B\).
After reducing \(g\) and applying the direct base-GCD precheck, enter the
circuit only for a unit base. Define
\[
L=S_A(g),\quad h=g^A,\quad Q=S_B(h),\quad U=S_{AB}(g)\pmod N,
\]
and
\[
C=h-1,\qquad E=h^B-1=g^{AB}-1\pmod N.
\]
Three charged DEF-018 binary evaluators compute \((h,L)\), \((h^B,Q)\), and
\((g^{AB},U)\), giving independent rational and division-free composed paths.
The exact formal certificate is
\[
S_{AB}(X)=S_A(X)S_B(X^A),                         \tag{1}
\]
or equivalently
\[
\frac{S_{AB}(X)}{S_A(X)}=S_B(X^A).                \tag{2}
\]

Both divisions have total semantics. The rational path attempts \(U/L\);
the composed path attempts \(E/C\). Each denominator GCD is classified as a
unit, proper factor, or full collision, and \(Q\) remains defined in every
case. The accounting charges the encoded base, reduction and precheck,
encoded \(A,B\), computing \(AB\), all three binary circuits, every retained
residue or formal descriptor, both division attempts, requested GCDs, and
extraction.

If \(\alpha=\operatorname{bitlength}(A)\) and
\(\beta=\operatorname{bitlength}(B)\), the compact certificate (1) uses
\(O(\alpha+\beta)\) bits. Its quotient has degree \(A(B-1)\) and \(B\)
nonzero monomials. Expanded \(S_A\) and \(S_{AB}\) dense outputs have
respectively \(A\) and \(AB\) entries. A dense quotient coefficient vector
has \(A(B-1)+1\) entries; a sparse quotient list has \(B\) coefficient-index
pairs, with every \(O(\alpha+\beta)\)-bit exponent index charged.

The model is one nested geometric quotient. Arbitrary rational straight-line
programs, unrelated or cancellation-obscured denominators without certificate
(1), adaptive factor dependence, other groups, and general arithmetic
circuits remain outside.

## BAR-014

Every DEF-019 circuit satisfies:

1. the exact identity (1), \(U\equiv LQ\pmod N\), and
   \(E\equiv CQ\pmod N\);
2. if \(\gcd(L,N)=1\), rational division returns \(Q\) and
   \(\gcd(U,N)=\gcd(Q,N)\);
3. if \(1<\gcd(L,N)<N\), the intermediate denominator already returns a
   proper factor, although \(Q\) may return a different divisor;
4. if \(\gcd(L,N)=N\), then \(h\equiv1\pmod N\),
   \(Q\equiv B\pmod N\), and \(\gcd(Q,N)=\gcd(B,N)\);
5. independently, the composed denominator \(C\) has the DEF-018
   unit/proper/full trichotomy: unit division returns \(Q\) and
   \(\gcd(Q,N)=\gcd(E,N)\), \(\gcd(C,N)\) is the returned proper factor in
   the proper case, and \(Q\equiv B\pmod N\) with quotient GCD
   \(\gcd(B,N)\) in the full case;
6. construction, residue evaluation, and extraction are polynomial in the
   charged base, modulus, \(A\), and \(B\) bit lengths. Dense expanded output
   is linear in its stated slot count; a sparse quotient output costs
   \(O(B(\alpha+\beta))\) bits for its exponent-coefficient pairs.

Thus a proper quotient success cannot be created solely by cancellation of a
nonunit intermediate denominator. Relative to \(L\), it is identical to the
rational numerator success, accompanied by an already proper denominator, or
identical to the public multiplier GCD.

## Proof

Partition the \(AB\) exponents uniquely as \(i=Ar+j\), with
\(0\le r<B\) and \(0\le j<A\). Then
\[
\begin{aligned}
S_{AB}(X)
 &=\sum_{r=0}^{B-1}\sum_{j=0}^{A-1}X^{Ar+j}\\
 &=\left(\sum_{j=0}^{A-1}X^j\right)
   \left(\sum_{r=0}^{B-1}(X^A)^r\right)
 =S_A(X)S_B(X^A),
\end{aligned}
\]
proving (1). Evaluation gives \(U\equiv LQ\). Applying the geometric identity
to base \(h=g^A\) gives \(E\equiv CQ\).

If \(L\) is a unit, multiplication by \(L\) preserves the GCD with \(N\);
hence rational division returns \(Q\) and
\(\gcd(U,N)=\gcd(Q,N)\). If \(L\) has a proper GCD, that value is already a
factor. Exact divisor equality is false: at \(N=15,g=2,A=2,B=2\),
intermediate and quotient GCDs are \(3\) and \(5\), while the rational
numerator GCD is full.

If \(L\equiv0\pmod N\), then
\[
h-1=(g-1)S_A(g)\equiv0\pmod N.
\]
Therefore \(h\equiv1\), so \(Q=S_B(h)\equiv B\pmod N\) and its GCD is the
public \(\gcd(B,N)\). This proves the rational-denominator trichotomy.
Applying BAR-013 directly at base \(h\) proves the independent composed
trichotomy for \(C=h-1\).

The three binary evaluators use
\(O(\alpha)\), \(O(\beta)\), and
\(O(\operatorname{bitlength}(AB))=O(\alpha+\beta)\) modular operations.
Computing \(AB\), reducing the base, GCDs, inversions, and extraction are
polynomial in the charged input lengths. Identity (1) is a compact
\((A,B)\)-described certificate. The quotient monomials have exponents
\(0,A,\ldots,A(B-1)\), so its degree and nonzero monomial count are as
stated. Its dense vector has one slot through degree \(A(B-1)\); its sparse
list has \(B\) pairs whose exponent fields use \(O(\alpha+\beta)\) bits.
Expanded output costs follow from these exact representations. This proves
BAR-014.

## Refuted statement

`REF-015` states that cancellation in
\(S_{AB}(g)/S_A(g)=S_B(g^A)\) can create a proper quotient success not
accounted for by the rational numerator, a proper intermediate denominator,
or the public multiplier GCD. BAR-014 refutes it only for DEF-019.
