# BAR-020 - Exceptional cyclotomic quotient and extraction theorem

## Status

`PROVED` in the exact M26 depth-two model. This result gives a compact,
factorization-independent evaluator and total extraction grammar for the two
fixed exceptional families from THM-003. It does not guarantee that any
public schedule contains a successful base.

## Statement

Write \(S_M(X)=\sum_{j=0}^{M-1}X^j\). For unequal public integers
\(A,B\ge2\), define

\[
 F_4(X)=S_A(X)+S_B(X^A)
\]

when \(A\equiv B\equiv3\pmod4\), and

\[
 F_6(X)=2S_A(X)+S_B(X^A)
\]

when \(A\equiv5\pmod6\) and \(B\equiv3\pmod6\). Then:

1. there are unique monic \(C_4,C_6\in\mathbb Z[X]\) with
   \(F_4=\Phi_4C_4\) and \(F_6=\Phi_6C_6\);
2. \(\deg C_i=A(B-1)-2\), so a requested dense coefficient list has
   \(A(B-1)-1\) entries and is charged at that output size;
3. for every modulus \(N\ge2\) and unit \(g\bmod N\), both
   \(\Phi_i(g)\) and \(C_i(g)\) can be evaluated without modular division
   in \(O(\log A+\log B)\) modular additions and multiplications, up to a
   constant number of binary geometric-sum evaluations;
4. for every \(p^e\parallel N\),

   \[
   \min(v_p(F_i(g)),e)=
   \min(v_p(\Phi_i(g))+v_p(C_i(g)),e);
   \]

5. the GCD branches are total: a proper
   \(\gcd(\Phi_i(g),N)\) or \(\gcd(C_i(g),N)\) is immediately a factor;
   a unit \(\Phi_i(g)\) gives
   \(\gcd(F_i(g),N)=\gcd(C_i(g),N)\); and a full cyclotomic collision
   forces \(\gcd(F_i(g),N)=N\) but does not suppress the independently
   evaluated cofactor GCD.

Consequently the public algorithm that performs the usual base GCD, the two
M24 stage GCDs and public overlap-bound GCDs, recognizes the applicable
exceptional congruences, evaluates the fixed cyclotomic and compact cofactor,
and returns either proper GCD is factorization-independent and polynomial in
the binary input lengths of \(N,A,B\). It succeeds exactly on the restricted
class of candidates for which at least one of those computed GCDs is proper.
No density, schedule coverage, or universal factoring conclusion follows.

## Exact Phi4 quotient

Put \(A=4a+3\), \(B=4b+3\), and

\[
 U_4(4t+3;x)=(1+x)S_t(x^4)+x^{4t}.
\]

Block decomposition gives

\[
 S_{4t+3}(x)=\Phi_4(x)U_4(4t+3;x)+x^{4t+1}.
\]

Because \(A\) is odd,

\[
 D_4(A;x)=\frac{\Phi_4(x^A)}{\Phi_4(x)}
          =S_A(-x^2).
\]

Let \(r=A-2\), \(s=A(B-2)\), and \(k=(s-r)/2\). The congruences imply
\(r\equiv1\), \(s\equiv3\pmod4\), so \(k\) is a positive odd integer and

\[
 \frac{x^r+x^s}{\Phi_4(x)}=x^rS_k(-x^2).
\]

Therefore

\[
 C_4(x)=U_4(A;x)+D_4(A;x)U_4(B;x^A)+x^rS_k(-x^2).
\]

Every exponent and geometric-sum count in this formula has bit length
\(O(\log A+\log B)\).

## Exact Phi6 quotient

Let

\[
 H(x)=x^3+2x^2+2x+1,\qquad
 J(x)=x^4+x^3-x-1.
\]

The identities \(S_6=\Phi_6H\) and \(x^6-1=\Phi_6J\) are direct
multiplications. Put \(A=6a+5\), \(B=6b+3\), \(y=x^A\). Then

\[
 S_A(x)=\Phi_6(x)H(x)S_{a+1}(x^6)-x^A
\]

and

\[
 S_B(y)=\Phi_6(y)\bigl(H(y)S_b(y^6)+y^{6b}\bigr)
         +2y^{6b+1}.
\]

For the remaining substitution quotient, use the periodic sequences

\[
 h=(1,1,0,-1,-1,0),\qquad
 k=(-1,0,1,1,0,-1).
\]

Exact monic division, or equivalently the recurrence
\(q_j=p_j+q_{j-1}-q_{j-2}\), gives

\[
 D_6(A;x)=\frac{\Phi_6(x^A)}{\Phi_6(x)}
 =\sum_{j=0}^{A-1}h_{j\bmod6}x^j
  +x^A\sum_{j=0}^{A-2}k_{j\bmod6}x^j.
\]

The recurrence starts with the impulse response \(h\); the coefficient
\(-1\) at degree \(A\equiv5\pmod6\) changes the second segment to \(k\).
The final coefficient at degree \(2A\) makes the next two recurrence terms
zero, proving exact termination.

It follows that

\[
\begin{split}
 C_6(x)={}&2H(x)S_{a+1}(x^6)\\
 &+D_6(A;x)\bigl(H(y)S_b(y^6)+y^{6b}\bigr)\\
 &+2x^AJ(x)S_{Ab}(x^6).
\end{split}
\]

A length-\(L\) periodic sum with period six is one fixed block polynomial
times \(S_{\lfloor L/6\rfloor}(x^6)\), plus a tail of at most five terms.
Thus \(D_6\), and hence \(C_6(g)\), has the claimed logarithmic modular
evaluation cost without expanding \(A(B-1)-1\) coefficients.

## Valuations and extraction

The polynomial identities remain integer identities after substituting the
least positive representative of a unit \(g\bmod N\). Additivity of the
\(p\)-adic valuation on nonzero integer products proves the valuation
formula; capping at \(e\) gives exactly the exponent of \(p\) in the GCD
with \(p^e\).

Both \(\Phi_i(g)\) and \(C_i(g)\) are computed before their GCDs, so no
unknown prime divisor or factor-dependent parameter enters construction.
If the cyclotomic value is a unit, multiplication by it is an automorphism
of \(\mathbb Z/N\mathbb Z\), proving equality of the aggregate and cofactor
GCDs. If it is zero modulo \(N\), the product is zero modulo \(N\), while
the independent compact formula for \(C_i(g)\) remains valid.

## Adversarial review

- **Circularity:** rejected. Family recognition uses only congruences of
  public \(A,B\); every extraction decision is an ordinary computed GCD.
- **Hidden output cost:** dense output is explicitly
  \(A(B-1)-1\) coefficients and is not called polynomial in
  \(\log A+\log B\). Compact modular evaluation uses the displayed
  formulas instead.
- **Hidden exponent cost:** the largest counts are products such as \(Ab\)
  and \(A(B-2)\); their bit lengths are additive in the input bit lengths.
- **Nonunit division:** none occurs. In particular, the full
  \(\Phi_i(g)\) branch evaluates \(C_i(g)\) independently.
- **Repeated primes:** the capped valuation identity covers every
  \(p^e\parallel N\), not only square-free inputs.
- **Stage masking:** the theorem does not assert that stage or public-bound
  GCDs are units. The four minimized residual witnesses record the stricter
  unit-stage boundary separately.
- **Coverage:** the theorem is an exact evaluator and extraction criterion,
  not a proof that a polynomial-size base or parameter schedule succeeds.

The symbolic identities, 61,277 compact-versus-dense evaluations, 122,583
prime-power valuation checks, and independent Rust/C# vectors in EXP-0025
all passed. Those finite checks support the implementation but are not used
as the proof.
