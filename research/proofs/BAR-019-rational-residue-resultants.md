# BAR-019: Primitive rational residue, stage resultants, and cyclotomic scope

## Claim status

- `DEF-024`: `DEFINITION`.
- `BAR-019`: `PROVED`; exact adversarial audit passed.
- `REF-020`: `REFUTED`.

No external theorem is imported. The proof uses integer-polynomial
identities, the root-product definition of the resultant, modular
inversion, and exact cyclotomic divisibility.

## DEF-024: primitive rational-residue audit

Fix public unequal integers \(A,B\ge2\), nonzero public integers \(c_1,c_2\),
and
\[
 Q_1(X)=S_A(X),\qquad Q_2(X)=S_B(X^A),\qquad
 F(X)=c_1Q_1(X)+c_2Q_2(X).
\]
Let
\[
 d=\gcd(|c_1|,|c_2|),\qquad a_i=c_i/d,\qquad
 P(X)=a_1Q_1(X)+a_2Q_2(X).
\]
Thus \(F=dP\) and \(\gcd(|a_1|,|a_2|)=1\).

For a public unit \(g\bmod N\), the audit retains the content trichotomy,
both stages and their GCDs, \(F(g)\), \(P(g)\), the total first-prefix
branch, and both stage-overlap GCDs. The exact resultants are retained as
compact base--exponent descriptors. An optional cyclotomic audit takes an
explicit order bound and performs exact monic polynomial divisions.

The public inputs and their encodings, binary geometric-sum evaluations,
coefficient arithmetic, modular operations, inversions on unit branches,
GCDs, requested cyclotomic divisions, extraction, and requested formal
output are charged. A compact power descriptor is not its expanded integer:
materializing a resultant or dense polynomial is charged by the actual
output bit length.

## Content and unit-prefix trichotomies

The coefficient content gives a total first exit:

1. if \(\gcd(d,N)=1\), multiplication by \(d\) is a unit and
   \(\gcd(F(g),N)=\gcd(P(g),N)\);
2. if \(1<\gcd(d,N)<N\), the public content already factors \(N\);
3. if \(\gcd(d,N)=N\), then \(F(g)=0\pmod N\).

If \(Q_1(g)\) is a unit, define
\[
 R=c_1+c_2Q_2(g)Q_1(g)^{-1},\qquad
 R_0=a_1+a_2Q_2(g)Q_1(g)^{-1}\pmod N.
\]
Then
\[
 F(g)=Q_1(g)R,\qquad P(g)=Q_1(g)R_0,\qquad R=dR_0,
\]
so their GCDs agree on each unit multiplication. Proper and full
\(Q_1(g)\) branches remain exactly the M23 exits.

## Exact stage resultants and public overlap bounds

The exact resultants are
\[
 \operatorname{Res}(Q_1,F)=(c_2B)^{A-1},                 \tag{1}
\]
\[
 \operatorname{Res}(Q_2,F)
 =c_1^{A(B-1)}B^{A-1}.                                  \tag{2}
\]
They imply the sharper evaluation bounds
\[
 \gcd(Q_1(g),F(g),N)\mid\gcd(c_2B,N),                    \tag{3}
\]
\[
 \gcd(Q_2(g),F(g),N)\mid\gcd(c_1B,N).                    \tag{4}
\]
Thus every overlap between the aggregate and an already charged stage is
controlled by a public coefficient--multiplier GCD. These bounds do not
classify a proper \(F(g)\)-GCD when both stages and both public bounds are
units.

To prove (1), evaluate \(F\) at the \(A-1\) roots of \(Q_1\). At each root,
\(Q_2=B\), so every root-product factor is \(c_2B\). For (2), at every root
of the monic degree-\(A(B-1)\) polynomial \(Q_2\), the value is \(c_1Q_1\).
Moreover
\(\operatorname{Res}(Q_2,Q_1)=B^{A-1}\): reversing the M23 resultant adds
the sign
\((-1)^{A(A-1)(B-1)}=1\).

For a direct proof of (3), the M23 identity gives
\[
 F-c_2B
 =Q_1\left(c_1+c_2(X-1)T_B(X^A)\right).                 \tag{5}
\]
Every common divisor of \(Q_1(g)\), \(F(g)\), and \(N\) therefore divides
\(c_2B\). For (4), a common divisor of \(Q_2(g)\) and \(F(g)\) divides
\(c_1Q_1(g)\). Multiplying
\[
 Q_2-B=(X-1)Q_1T_B(X^A)
\]
by \(c_1\) shows that the same divisor divides \(c_1B\).

## Exact root-of-unity condition

No root of \(F\) is a root of \(Q_1\) or \(Q_2\): at a root of \(Q_1\),
\(F=c_2B\ne0\), while coprimality of the stages gives \(F=c_1Q_1\ne0\) at
a root of \(Q_2\). Hence for a root of unity \(\zeta\ne1\),
\[
 F(\zeta)=0
 \iff
 c_1(\zeta^A-1)^2+
 c_2(\zeta-1)(\zeta^{AB}-1)=0.                          \tag{6}
\]
The equivalence follows by multiplying \(F\) by
\((X-1)(X^A-1)\). At \(\zeta=1\), the exact condition is
\(c_1A+c_2B=0\). For any explicit order \(n\), the statement
\(\Phi_n\mid F\) is decidable by exact monic division; an order search is
charged by its explicit bound. Equation (6) is an exact criterion, not a
uniform arithmetic classification of all possible orders.

## Exceptional cyclotomic obstruction

Take
\[
 (A,B,c_1,c_2)=(3,7,1,1).
\]
At \(\zeta=i\),
\[
 Q_1(i)=i,\qquad Q_2(i)=-i,
\]
so \(\Phi_4(X)=X^2+1\) divides \(F\). This is not the \(X-1\) boundary
because \(3+7\ne0\), and it is not a difference common-step factor because
\(c_1+c_2\ne0\).

The modular witness
\[
 (N,g,A,B,c_1,c_2)=(55,2,3,7,1,1)
\]
has
\[
 Q_1(g)=7,\quad Q_2(g)=8,\quad F(g)=15,\quad
 \gcd(F(g),55)=5.
\]
Both stages, the coefficient content, and both public overlap bounds are
units modulo \(55\); the unit-prefix rational residue is \(10\) and also
has GCD \(5\). Therefore resultants isolate stage overlap but do not absorb
the exceptional cyclotomic residue.

## Complexity and scope

The residues use two binary geometric-sum evaluations and a constant number
of modular operations and GCDs, polynomial in the input encodings and
\(\log N\). The descriptors
\[
 (|c_2|B,A-1),\qquad
 (|c_1|,A(B-1)),\qquad (B,A-1)
\]
are compact. Expanding either resultant can require
\(\Theta(A\log(|c_2|B))\) or comparable output bits and is not silently
treated as polynomial in \(\log A+\log B\). Exact numerator coefficient
lists and cyclotomic searches are likewise charged by their actual output
or explicit search bound.

`REF-020` claimed that every cyclotomic factor of a primitive numerator is
forced by the value at one or, for opposite coefficients, by the M23
common-step factor. The \(\Phi_4\) example refutes it. BAR-019 proves no
uniform classification of exceptional orders, no schedule, recognizer,
density, probability, general classical factoring result, or general
arithmetic-circuit lower bound.
