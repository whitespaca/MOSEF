# BAR-013: An arbitrary geometric sum reduces to three charged GCD paths

## Claim status

- `DEF-018`: `DEFINITION`.
- `BAR-013`: `PROVED`, subject to independent adversarial review.
- `REF-014`: `REFUTED`.

No external theorem is imported. The argument uses exact geometric-sum
identities, Euclid's algorithm, and explicit binary-circuit accounting.

## DEF-018: charged binary geometric-sum circuit

Fix an integer modulus \(N\ge2\), a public integer base \(g\), and a public
positive exponent \(M\). The algorithm first computes \(\gcd(g,N)\). A proper
result is a direct factor and a full result is a separate invalid-base branch.
The circuit below is entered only when \(g\) is a unit modulo \(N\).

Write
\[
 S_M(X)=\sum_{i=0}^{M-1}X^i,\qquad
 P_M(X)=X^M.
\]
The uniform binary grammar starts with
\[
 (P_1,S_1)=(X,1)
\]
and uses two composition gates:
\[
\begin{aligned}
 (P_r,S_r)&\longmapsto
 (P_{2r},S_{2r})
   =(P_r^2,S_r(1+P_r)),\\
 (P_{2r},S_{2r})&\longmapsto
 (P_{2r+1},S_{2r+1})
   =(XP_{2r},S_{2r}+P_{2r}).
\end{aligned}                                      \tag{1}
\]
Reading the binary expansion of \(M\) from left to right applies the first
gate at every remaining bit and the second gate exactly at a one bit. The
residue evaluator stores
\[
 P=g^M\bmod N,\qquad Q=S_M(g)\bmod N,
\]
and also
\[
 D=g-1\bmod N,\qquad E=g^M-1\bmod N.
\]
It computes the endpoint GCD \(\gcd(E,N)\), denominator GCD \(\gcd(D,N)\),
quotient GCD \(\gcd(Q,N)\), and public exponent GCD \(\gcd(M,N)\).

Modular division has total semantics. Let \(\delta=\gcd(D,N)\).

1. If \(\delta=1\), the circuit may compute \(ED^{-1}\bmod N\).
2. If \(1<\delta<N\), it returns the proper factor \(\delta\); division is
   unavailable, while the binary value \(Q\) remains defined.
3. If \(\delta=N\), it records a full denominator collision; division is
   unavailable, while \(Q\) again remains defined.

Let \(\ell=\lfloor\log_2M\rfloor+1\) and let
\(b=\lceil\log_2(|g|+1)\rceil\). The accounting charges the encoded base,
its reduction and base-GCD precheck, the \(\ell\)-bit public exponent, its
factorization-free binary constructor, every modular multiplication and
addition in (1), every retained residue or formal descriptor, the
extended-GCD division attempt, every requested GCD, and factor extraction.
The formal degree \(M-1\) and monomial count \(M\) are compact metadata, but
a requested coefficient list contains exactly \(M\) entries and is charged
accordingly.

This is one arbitrary-exponent geometric sum. It is not an arbitrary
rational straight-line program, a family of independently extracted
monomials, a cancellation-obscured division, an adaptive factor-dependent
circuit, another base or group, or a general arithmetic circuit.

## BAR-013

Every DEF-018 circuit satisfies:

1. the exact odd/even identities (1) and
   \[
   (X-1)S_M(X)=X^M-1;                            \tag{2}
   \]
2. if \(\gcd(D,N)=1\), then division returns \(Q\) and
   \[
   \gcd(Q,N)=\gcd(E,N);
   \]
3. if \(1<\gcd(D,N)<N\), the denominator path has already returned a proper
   factor, although \(Q\) may expose a different proper divisor;
4. if \(\gcd(D,N)=N\), then
   \[
   Q\equiv M\pmod N,\qquad \gcd(Q,N)=\gcd(M,N);
   \]
5. compact residue construction uses at most \(3(\ell-1)\) modular
   multiplications and \(2(\ell-1)\) modular additions, hence
   \(O(\ell\operatorname{poly}(k))\) bit operations after base reduction for
   \(k=\operatorname{bitlength}(N)\), with total preprocessing, GCD, extended-GCD,
   and circuit work polynomial in the charged length \(b+k+\ell\);
6. compact formal metadata uses \(O(\ell)\) bits, while expanded coefficient
   output costs \(\Omega(M)\).

Consequently, a proper quotient-GCD success is never an unaccounted
factorization success: it is exactly the endpoint GCD in the unit branch,
is accompanied by the already successful denominator GCD in the proper
branch, or is exactly the public exponent GCD in the full branch. The
proper divisor values need not agree in the middle branch.

## Proof

### Exact binary grammar

For \(r\ge1\),
\[
\begin{aligned}
S_{2r}(X)
 &=\sum_{i=0}^{r-1}X^i+\sum_{i=r}^{2r-1}X^i\\
 &=S_r(X)+X^rS_r(X)
 =S_r(X)(1+P_r(X)),
\end{aligned}
\]
and \(P_{2r}=P_r^2\). Appending the final term gives
\[
S_{2r+1}(X)=S_{2r}(X)+X^{2r}
           =S_{2r}(X)+P_{2r}(X)
\]
and \(P_{2r+1}=XP_{2r}\). These are exactly the two gates in (1).
Induction over the processed binary prefix therefore gives
\((P_M,S_M)=(X^M,\sum_{i<M}X^i)\).

Multiplying the finite sum by \(X-1\) cancels adjacent terms and proves
(2). Evaluating at \(g\) and reducing modulo \(N\) yields
\[
E\equiv DQ\pmod N.                               \tag{3}
\]

### Extraction trichotomy

If \(\gcd(D,N)=1\), \(D\) has a unique inverse modulo \(N\), so (3) proves
that modular division returns \(Q\). Multiplication by an integer coprime to
\(N\) preserves the GCD with \(N\):
\[
\gcd(DQ,N)=\gcd(Q,N).
\]
Because \(E\equiv DQ\pmod N\), reduction modulo \(N\) also preserves the GCD,
and therefore \(\gcd(E,N)=\gcd(Q,N)\).

If \(1<\gcd(D,N)<N\), DEF-018 returns that GCD before division. Nothing
requires the quotient to return the same divisor. Indeed,
\(N=15,g=4,M=2\) gives
\[
\gcd(D,N)=3,\qquad \gcd(Q,N)=5,\qquad \gcd(E,N)=15.
\]
Thus the sound statement is that a proper-factor success already exists,
not that the factor value is preserved.

If \(\gcd(D,N)=N\), then \(g\equiv1\pmod N\). Every one of the \(M\) terms
in \(S_M(g)\) is congruent to one, hence
\[
Q\equiv M\pmod N.
\]
Taking GCDs with \(N\) gives
\(\gcd(Q,N)=\gcd(M,N)\). This remains exact for repeated prime powers; for
\(N=8,g=1,M=4\), both GCDs are \(4\).

The three cases exhaust all denominator GCDs and prove the extraction
trichotomy.

### Construction and output costs

The leading binary bit initializes \((P,Q)=(g,1)\). Each of the remaining
\(\ell-1\) bits performs two multiplications and one addition for the
doubling gate. A one bit performs one further multiplication and one further
addition. Thus the exact counts are
\[
2(\ell-1)+(\operatorname{popcount}(M)-1)
\]
multiplications and
\[
(\ell-1)+(\operatorname{popcount}(M)-1)
\]
additions, bounded respectively by \(3(\ell-1)\) and \(2(\ell-1)\).
Reducing \(g\) and computing its base GCD are polynomial in \(b+k\).
Thereafter all residues have \(O(k)\) bits. Computing \(\gcd(M,N)\) is
polynomial in the explicitly charged \(\ell+k\) input bits, so compact
evaluation and extraction are polynomial in the full input length
\(b+k+\ell\).

The degree \(M-1\) and monomial count \(M\) take \(O(\ell)\) bits as
metadata. The expanded polynomial has coefficient one at every exponent
from zero through \(M-1\), so materializing it needs \(M\) output entries.
When \(\ell=\operatorname{poly}(k)\), \(M\) may be exponential in \(k\);
the compact residue circuit remains polynomial while an expanded output
does not. Those \(M\) monomials are terms of one value \(Q\), not \(M\)
independent GCD tests. This proves BAR-013.

## Falsification cases

- Unit denominator and proper endpoint:
  \(N=15,g=2,M=2\) gives \(D=1\) and
  \(\gcd(Q,N)=\gcd(E,N)=3\).
- Proper denominator with a different quotient factor:
  \(N=15,g=4,M=2\) gives denominator GCD \(3\), quotient GCD \(5\), and
  full endpoint collision \(15\).
- Full denominator and public-exponent factor:
  \(N=15,g=1,M=5\) gives \(Q\equiv5\) and both relevant GCDs equal \(5\).
- Repeated prime power:
  \(N=8,g=1,M=4\) gives quotient and exponent GCDs equal to \(4\).
- Base case:
  \(M=1\) has \((P,Q)=(g,1)\), zero composition operations, degree zero,
  and one monomial.

## Refuted statement

`REF-014` is the statement that a compact arbitrary-exponent geometric sum
or its exact modular division can produce a proper-factor success not
accounted for by the endpoint GCD, a proper denominator GCD, or the public
exponent GCD. BAR-013 refutes that statement for DEF-018. It makes no claim
about general rational or compositional circuits.
