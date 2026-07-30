# BAR-012: Dyadic telescoping does not create an exponential test batch

## Claim status

- `DEF-017`: `DEFINITION`.
- `BAR-012`: `PROVED`, subject to independent adversarial review.
- `REF-013`: `REFUTED`.

No external theorem is imported. The argument uses an elementary polynomial
identity, Euclid's algorithm, prime valuations, and explicit operation
counting.

## DEF-017: charged dyadic exact-division circuit

Fix an integer modulus \(N\ge 2\), a public integer base \(g\), and a
nonnegative integer level \(t\). The algorithm first computes
\(\gcd(g,N)\). A proper result is a direct factor; a full result is a
separate invalid-base branch. The circuit below is entered only when \(g\)
is a unit modulo \(N\).

The uniform constructor receives only \((N,g,t)\), never the factorization of
\(N\). It creates
\[
 x_0=g,\qquad x_{j+1}=x_j^2\pmod N\quad(0\le j<t),
\]
the explicit factor residues
\[
 F_j=x_j+1\pmod N\quad(0\le j<t),
\]
and
\[
 D=g-1,\qquad E=x_t-1,\qquad
 Q=\prod_{j=0}^{t-1}F_j\pmod N.
\]
The empty product at \(t=0\) is \(Q=1\).

The exact formal identity represented by the circuit is
\[
 \frac{X^{2^t}-1}{X-1}
 =\sum_{i=0}^{2^t-1}X^i
 =\prod_{j=0}^{t-1}(X^{2^j}+1).                 \tag{1}
\]
The quotient polynomial has degree \(2^t-1\) and \(2^t\) nonzero
coefficients, but the circuit retains the factorized representation in
(1). If a complete coefficient list is requested, all \(2^t\) coefficients
and their output cost are charged.

Modular division has total semantics. Let
\(\delta=\gcd(D,N)\).

1. If \(\delta=1\), the circuit may compute
   \(E D^{-1}\pmod N\) by extended GCD.
2. If \(1<\delta<N\), it returns the proper factor \(\delta\); the modular
   division output is unavailable, while the division-free product \(Q\)
   remains defined.
3. If \(\delta=N\), it records a full denominator collision; the modular
   division output is unavailable, while \(Q\) again remains defined.

The accounting charges the encoding of \(t\), every one of the \(t\)
squarings, every one of the \(t\) additions producing \(F_j\), the
\(\max(0,t-1)\) product multiplications, the extended-GCD division attempt,
every requested GCD, every retained residue or formal descriptor, and
factor extraction. A polynomial total-work claim therefore requires
\(t=\operatorname{poly}(k)\), where \(k=\operatorname{bitlength}(N)\). A compact
binary encoding of a larger \(t\) does not waive the \(t\) sequential
squarings or outputs.

This is a restricted exact-division/composition model. It does not cover
arbitrary rational straight-line programs, cancellation-obscured
denominators, arbitrary polynomial composition, adaptive factor-dependent
branches, other bases or groups, or general arithmetic circuits.

## BAR-012

For every DEF-017 circuit:

1. identity (1) and its modular specialization hold;
2. the unit-denominator division output equals the division-free product
   \(Q\);
3. if \(1<\gcd(Q,N)<N\), then some explicit \(F_j\) has
   \(1<\gcd(F_j,N)<N\);
4. if \(1<\gcd(E,N)<N\), then \(D\) or some explicit \(F_j\) has a proper
   GCD with \(N\);
5. a proper denominator GCD is already a returned factor;
6. the factorized circuit has \(O(t)\) modular operations and explicit
   components, while a full coefficient output has \(2^t\) entries.

Consequently, dyadic telescoping compactly evaluates one degree-\(2^t-1\)
geometric quotient and one exponent endpoint, but it does not create
\(2^t\) separately extractable same-base exponent tests. Every proper-factor
success from the denominator, numerator, quotient, or factor-GCD paths
implies a proper, not necessarily identical, GCD from one of the \(t+1\)
explicit components
\[
 \{D,F_0,\ldots,F_{t-1}\}.
\]

## Proof

### Formal identity

For \(t=0\), both sides of (1) equal \(1\). If
\[
 \prod_{j=0}^{t-1}(X^{2^j}+1)
 =\frac{X^{2^t}-1}{X-1},
\]
then multiplication by \(X^{2^t}+1\) gives
\[
 \frac{(X^{2^t}-1)(X^{2^t}+1)}{X-1}
 =\frac{X^{2^{t+1}}-1}{X-1}.
\]
Induction proves the product identity. The geometric-sum identity follows
by multiplying \(\sum_{i=0}^{2^t-1}X^i\) by \(X-1\). Its degree and
coefficient count are immediate.

The recurrence gives \(x_j\equiv g^{2^j}\pmod N\) by induction. Evaluating
(1) at \(g\) and reducing modulo \(N\) therefore gives
\[
 E\equiv DQ\pmod N.                              \tag{2}
\]
If \(\gcd(D,N)=1\), multiplication of (2) by the unique modular inverse of
\(D\) proves that the division output equals \(Q\).

### Extraction implications

Write \(N=\prod_{p\mid N}p^{e_p}\), and set
\[
\widetilde D=g-1,\qquad
\widetilde F_j=g^{2^j}+1,\qquad
\widetilde E=g^{2^t}-1.
\]
These unreduced lifts satisfy the exact integer identity
\(\widetilde E=\widetilde D\prod_j\widetilde F_j\), and reducing any one of
them modulo \(N\) preserves its GCD with \(N\). With
\(\nu_p(0)=+\infty\),
\[
 \gcd(Q,N)
 =\prod_{p\mid N}
 p^{\min(e_p,\sum_{j=0}^{t-1}\nu_p(\widetilde F_j))}. \tag{3}
\]
If the left side is proper, at least one prime-power component has positive
valuation and at least one is not saturated. Choose a \(j\) contributing
positive valuation to a positive component. Its individual GCD cannot be
\(1\). If every contributing factor GCD were \(N\), every prime-power
component would be saturated in the product, contradicting properness.
Thus some \(F_j\) has a proper GCD. This also handles repeated prime powers;
at \(t=0\), \(Q=1\) and the premise is false.

The exact lifted identity gives the analogous valuation formula with
\(\nu_p(\widetilde D)\) added. The same argument proves that a proper
numerator GCD implies a proper GCD for \(D\) or an \(F_j\). When \(D\) itself
has a proper GCD, DEF-017 returns it before attempting inversion. Aggregation
can change the proper factor value: at \(N=8,g=1,t=2\), both dyadic factor
GCDs are \(2\), while the quotient GCD is \(4\). It may also turn proper
component successes into a full collision. What it cannot do is create a
proper success when every component GCD is only \(1\) or \(N\).

### Cost and batch interpretation

There are exactly \(t\) squarings and \(t\) explicit factors. Their product
uses \(\max(0,t-1)\) multiplications. Standard modular multiplication,
addition, GCD, and extended-GCD inversion operate on \(O(k)\)-bit residues,
so the compact evaluation and all \(t+1\) component GCDs cost
\(O((t+1)\operatorname{poly}(k))\) bit operations. The formal degree and
monomial count need only \(O(t+1)\) bits as metadata, but a requested
expanded coefficient list contains \(2^t\) entries and costs at least that
many output operations.

The \(2^t\) monomials are terms of one polynomial value. They are not
separate residues \(g^d-1\), do not have separate GCD extraction paths, and
do not constitute an exponentially indexed order-separator family. The
only explicit component tests in the factorized evaluation are \(D\) and
the \(t\) factors \(F_j\). This proves BAR-012.

## Falsification cases

- Proper denominator and complementary factor:
  \(N=15,g=4,t=1\). Then
  \(\gcd(g-1,N)=3\), \(\gcd(g+1,N)=5\), and
  \(\gcd(g^2-1,N)=15\). Aggregating the two proper components masks both.
- Full denominator with a usable division-free quotient:
  \(N=6,g=1,t=3\). Modular division is unavailable because the denominator
  GCD is \(6\), but \(Q\equiv2\pmod6\) and each explicit factor has GCD \(2\).
- Unit denominator:
  \(N=15,g=2,t=1\). Division is valid and both quotient paths give residue
  \(3\), whose GCD is \(3\).
- Full quotient masking:
  \(N=45,g=8,t=5\). Explicit factor GCDs include \(9\) and \(5\), while the
  quotient and numerator GCDs are both \(45\).
- Different proper aggregate value:
  \(N=8,g=1,t=2\). Both explicit dyadic factors have GCD \(2\), while their
  quotient product has proper GCD \(4\).

## Refuted statement

`REF-013` is the statement that the compressed formal sum
\(\sum_{i<2^t}g^i\), or the exact division producing it, supplies
\(2^t\) separately extractable exponent tests at \(O(t)\) charged cost or a
proper-factor success when every denominator and dyadic-factor GCD is
trivial or full. BAR-012 refutes that statement for DEF-017. It makes no
claim about general rational or compositional circuits.
