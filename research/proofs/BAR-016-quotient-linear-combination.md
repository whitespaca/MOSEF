# BAR-016: Signed stage addition invalidates the product component implication

## Claim status

- `DEF-021`: `DEFINITION`.
- `BAR-016`: `PROVED`; exact adversarial audit passed.
- `REF-017`: `REFUTED`.

No external theorem is imported. The result is an exact counterexample at a
repeated prime power. The separate audit is
`research/proofs/BAR-016-adversarial-audit.md`.

## DEF-021: charged signed stage combination

Start with a DEF-020 public factor chain \(A_1,\ldots,A_r\), prefix products
\(M_0=1\), \(M_i=\prod_{j\le i}A_j\), and explicit stage quotients
\[
Q_i=S_{A_i}(g^{M_{i-1}}).
\]
Let \(c_1,\ldots,c_r\) be public signed integers. Retain every DEF-020 stage
and denominator exit, and additionally compute
\[
W_i=c_iQ_i\pmod N,\qquad
R=\sum_{i=1}^{r}W_i\pmod N.
\]
The evaluator records the GCDs of every coefficient, quotient, weighted
stage, and requested aggregate. The coefficient encodings, reductions,
\(r\) scalar multiplications, \(r-1\) additions, outputs, GCDs, and
extraction are charged.

The exact formal output is
\[
F(X)=\sum_{i=1}^{r}c_iS_{A_i}(X^{M_{i-1}})
    =\sum_{i=1}^{r}\sum_{j=0}^{A_i-1}c_iX^{jM_{i-1}}.       \tag{1}
\]
The compact descriptor consists of the aligned public factor and coefficient
lists. Its degree is at most
\[
D=\max_i(M_i-M_{i-1}),
\]
and the uncollected sparse list has exactly \(\sum_iA_i\) term records.
Collecting equal exponents can only reduce that count. A requested dense list
has \(D+1\) coefficient slots; requested sparse or dense output is charged by
its actual size and coefficient bit lengths.

This model permits one explicit signed linear aggregate only. It does not
cover adaptive coefficients, hidden factor-dependent construction,
multiplication or division between aggregates, arbitrary output subsets,
other groups, or general arithmetic circuits.

## BAR-016

The product implication from BAR-015 does not extend to addition or
subtraction, even when every charged component is a unit.

Specifically, take
\[
N=9,\qquad g=2,\qquad (A_1,A_2)=(5,5),\qquad(c_1,c_2)=(-1,1).
\]
Then \(M_0=1\), \(M_1=5\), and \(M_2=25\). Direct modular evaluation gives
\[
\begin{array}{c|cccccc}
i&L_i&Q_i&U_i&C_i&E_i&A_i\\ \hline
1&1&4&4&1&4&5\\
2&4&7&1&4&1&5
\end{array}
\pmod 9.
\]
Every displayed value has GCD one with \(9\). The base, both coefficients,
and both weighted stages also have GCD one:
\[
\gcd(2,9)=\gcd(-1,9)=\gcd(1,9)=1,
\]
\[
W_1\equiv-4\equiv5,\qquad W_2\equiv7\pmod9.
\]
Nevertheless,
\[
R\equiv Q_2-Q_1\equiv7-4\equiv3\pmod9,
\qquad \gcd(R,9)=3.
\]
Thus the signed aggregate produces a proper factor absent from every charged
stage, prefix, denominator, endpoint, public multiplier, coefficient, and
weighted-stage GCD.

The corresponding exact polynomial is
\[
\begin{aligned}
F(X)
 &=S_5(X^5)-S_5(X)\\
 &=-X-X^2-X^3-X^4+X^5+X^{10}+X^{15}+X^{20}.
\end{aligned}
\]
Its eight nonzero monomials are explicitly charged; the counterexample does
not rely on hidden expansion.

## Proof and cost boundary

The table follows from repeated modular multiplication:
\[
S_5(2)=1+2+4+8+7\equiv4\pmod9,\qquad 2^5\equiv5\pmod9,
\]
\[
S_5(5)=1+5+7+8+4\equiv7\pmod9.
\]
The linked prefix identity gives \(U_2\equiv Q_1Q_2\equiv1\pmod9\).
Also \(C_1=2-1=1\), \(E_1=2^5-1\equiv4\),
\(C_2=2^5-1\equiv4\), and \(E_2=2^{25}-1\equiv1\pmod9\).
These calculations verify every table entry and GCD. Subtracting the two unit
quotients gives the proper aggregate above, proving BAR-016.

Let \(L=\sum_i\operatorname{bitlength}(A_i)\) and
\(C=\sum_i\operatorname{bitlength}(|c_i|+1)\). Reusing DEF-020 costs
\(O(rL)\) modular operations. The extra \(r\) scalar multiplications and
\(r-1\) additions, coefficient reductions, GCDs, and extraction are
polynomial in the charged base, modulus, factor, and coefficient lengths.
Equation (1) proves the formal degree and output counts. Compact evaluation
therefore remains polynomial even though its extraction behavior is genuinely
stronger than product-only aggregation.

## Refuted statement

`REF-017` states that a proper DEF-021 signed aggregate must be accompanied by
a proper GCD among its charged stage quotients, prefixes, denominators,
endpoints, public multipliers, coefficients, or weighted stages. The witness
above refutes that implication. It establishes neither a universal factoring
algorithm nor a lower bound or success guarantee for broader arithmetic
circuits.
