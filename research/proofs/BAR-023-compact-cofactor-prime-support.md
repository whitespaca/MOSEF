# BAR-023 - Compact cofactor prime support is one signature cut

## Status

`PROVED`

## Model and definition

Fix an integer \(m\ge2\). In the exceptional \(\Phi_4\) family take

\[
A=3,\qquad B_m=2^m+3,\qquad g=2,
\]

and let \(C_m=C_4(2)\) be the exact integer cofactor defined by

\[
S_3(X)+S_{B_m}(X^3)=\Phi_4(X)C_4(X).
\]

The public algorithm never has to materialize \(C_m\). It evaluates the
existing M26 compact formula modulo the input and takes one GCD. For an odd
prime population \(\mathcal P\), define the analytical support

\[
H_m(\mathcal P)=\{p\in\mathcal P:p\mid C_m\}.
\]

This support is used only to state and prove the outcome count. It is not an
input to the constructor and is not claimed to be recognizable without
factoring the modulus.

## Exact statement

Put

\[
E_m=3\cdot2^m+5.
\]

Then:

1. the exact cofactor satisfies
   \[
   C_m=\frac{16(2^{E_m}+3)}{35};
   \]
2. \(v_2(C_m)=4\) and \(3\nmid C_m\);
3. \(5\mid C_m\) exactly when \(m\equiv2\pmod4\);
4. \(7\mid C_m\) exactly when \(m\equiv2\pmod3\);
5. for every prime \(p>7\),
   \[
   p\mid C_m
   \quad\Longleftrightarrow\quad
   2^{E_m}\equiv-3\pmod p;
   \]
6. consecutive exact cofactors have
   \[
   \gcd(C_m,C_{m+1})=16.
   \]

For any finite set \(\mathcal P\) of \(s\ge2\) distinct odd primes, write
\(h=|H_m(\mathcal P)|\). Among the \(\binom{s}{2}\) square-free pair
moduli \(pq\) with \(p,q\in\mathcal P\), the single compact cofactor GCD has
exactly

\[
h(s-h)
\]

proper-factor outcomes,

\[
\binom h2
\]

full collisions, and

\[
\binom{s-h}{2}
\]

unit outcomes. Consequently

\[
h(s-h)\le\left\lfloor\frac{s^2}{4}\right\rfloor,
\]

and one candidate cannot cover every pair when \(s\ge3\), regardless of how
large or how broad its exact prime support is.

Applied to the M28 balanced population

\[
\mathcal P_m=\{p\text{ prime}:2^{m-1}\le p^2<2^m\},
\]

this is an exact compact-ledger coverage theorem. It does not require the
exact cofactor or its prime factorization to be constructed.

## Proof

At \(g=2\), the M26 exceptional identity gives

\[
5C_m=S_3(2)+S_{B_m}(8)
=7+\frac{8^{B_m}-1}{7}.
\]

Therefore

\[
35C_m=8^{B_m}+48
=16(2^{3B_m-4}+3)
=16(2^{E_m}+3).
\]

For \(m\ge2\), \(E_m\equiv1\pmod4\), so
\(2^{E_m}+3\equiv2+3\equiv0\pmod5\). Also
\(E_m\equiv2\pmod3\), so
\(2^{E_m}+3\equiv4+3\equiv0\pmod7\). Thus the displayed quotient is an
integer. Since \(2^{E_m}+3\) and 35 are odd, the exact power of two in
\(C_m\) is \(2^4\), proving \(v_2(C_m)=4\). Because \(E_m\) is odd,

\[
2^{E_m}+3\equiv-1+0\equiv2\pmod3,
\]

so 3 does not divide \(C_m\).

For the prime 5, a further factor survives the quotient by 35 exactly when

\[
2^{E_m}+3\equiv0\pmod{25}.
\]

The element 2 has order 20 modulo 25, and
\(2^{17}\equiv22\equiv-3\pmod{25}\). Hence the condition is
\(E_m\equiv17\pmod{20}\), equivalently
\(2^m\equiv4\pmod{20}\). Starting at \(m=2\), the residues
\(4,8,16,12\) repeat with period four. Therefore
\[
5\mid C_m\quad\Longleftrightarrow\quad m\equiv2\pmod4.
\]

For the prime 7, use the equivalent numerator. Since \(8=1+7\),

\[
16(2^{E_m}+3)=8^{B_m}+48
\equiv1+7B_m+48
\equiv7B_m\pmod{49}.
\]

The factor 16 is a unit modulo 49. Thus a second factor of 7 survives the
quotient exactly when \(7\mid B_m\), or
\(2^m\equiv4\pmod7\). Powers of 2 modulo 7 have period three, giving
\[
7\mid C_m\quad\Longleftrightarrow\quad m\equiv2\pmod3.
\]

For every prime \(p>7\), both 16 and 35 are units modulo \(p\). The closed
form therefore gives

\[
p\mid C_m
\quad\Longleftrightarrow\quad
2^{E_m}+3\equiv0\pmod p,
\]

which is the claimed generic criterion.

It remains to compare consecutive levels. The exact two-adic calculation
already shows that their common power of two is exactly 16. The prime 3
divides neither cofactor. The congruence classes for 5 and 7 never occur at
two consecutive levels. Suppose now that a prime \(p>7\) divides both
\(C_m\) and \(C_{m+1}\). Since

\[
E_{m+1}=2E_m-5,
\]

the generic criterion gives

\[
-3\equiv2^{E_{m+1}}
=2^{2E_m-5}
\equiv\frac{(-3)^2}{32}
=\frac9{32}\pmod p.
\]

Thus \(105\equiv0\pmod p\), contradicting \(p>7\). No odd prime is common,
and \(\gcd(C_m,C_{m+1})=16\).

Finally fix distinct odd primes \(p,q\in\mathcal P\). The GCD
\(\gcd(C_m,pq)\) is proper exactly when precisely one of \(p,q\) lies in
\(H_m(\mathcal P)\). There are \(h(s-h)\) such cross-cut pairs. Two hit
primes produce the full collision \(pq\), and two missed primes produce the
unit outcome. This proves the three exact counts. The product \(h(s-h)\) is
maximized when the two sides are as equal as possible, giving
\(\lfloor s^2/4\rfloor\). For \(s\ge3\),
\(\lfloor s^2/4\rfloor<\binom{s}{2}\), so universal pair coverage is
impossible for this single candidate.

## Complexity and recognition boundary

- \(B_m\) and \(E_m\) have \(O(m)\) bits.
- The existing M26 binary geometric-sum formula evaluates \(C_m\bmod N\) in
  \(O(m)\) modular composition steps and polynomial bit complexity in
  \(m+\operatorname{bitlength}(N)\).
- The congruence criterion is an analytical local characterization when a
  prime \(p\) is supplied. It does not reveal the unknown factors of \(N\).
- The public algorithm evaluates the compact residue modulo \(N\) directly;
  it does not list \(H_m\), factor \(C_m\), or materialize \(C_m\).
- The theorem treats one square-free semiprime GCD candidate. Repeated
  primes, several bases or parameter tuples, adaptive schedules, and
  cross-candidate signature vectors require separate statements.

## Adversarial review

The following failure modes were checked explicitly.

1. **Division by 35.** The generic congruence is not used for 5 or 7. Their
   quotient valuations are handled modulo 25 and 49.
2. **The prime 2.** The exact valuation is four. Balanced populations used in
   the registered range are odd; an even input is already exposed by the
   standard base GCD.
3. **Full collisions.** Pairs with both factors in the support are counted as
   failures, not successes.
4. **Hidden factor access.** Support membership is analytical. The public
   evaluator receives only \(m\) and \(N\).
5. **Magnitude-to-support leakage.** No support lower bound is inferred from
   the exponential exact bit length.
6. **Finite-to-asymptotic leakage.** EXP-0028's zero balanced hits are
   empirical only and are not used in the proof.
7. **Overbroad lower bound.** The signature-cut barrier is for one compact
   cofactor candidate. It is not a lower bound for multi-candidate,
   \(N\)-dependent, adaptive, or general arithmetic-circuit schedules.

The proof survives these checks with the stated scope.
