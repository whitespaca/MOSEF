# BAR-048: exact overlap GCDs do not shrink the prefix exponent

## Claim status and scope

- `DEF-041`: `DEFINITION`.
- `BAR-048`: `PROVED`.
- `REF-050`: `REFUTED`.

For
\[
R_q=3^{n_q}+32^{n_q},\qquad n_q=2^q-1,
\]
this result computes every pairwise GCD and the asymptotic scale of the exact
prefix LCM. It is a method barrier for shared-divisor accounting, not a
statement that any particular balanced prime divides \(R_q\).

## Sum-of-odd-powers GCD lemma

Let \(\gcd(X,Y)=1\), let \(r,s\) be positive odd integers, and put
\(d=\gcd(r,s)\). Then
\[
\gcd(X^r+Y^r,X^s+Y^s)=X^d+Y^d.
\tag{1}
\]

The right side divides both terms because \(r/d\) and \(s/d\) are odd.
Conversely, set \(U=X^d,V=Y^d\), \(u=r/d\), and \(v=s/d\). For every prime
power \(p^e\) dividing both sums, \(UV\) is a unit modulo \(p^e\). With
\(z=UV^{-1}\), one has \(z^u=z^v=-1\). Choose
\(\alpha u+\beta v=1\). Since \(u,v\) and the right side are odd,
\(\alpha+\beta\) is odd, and therefore
\[
z=(-1)^{\alpha+\beta}=-1\pmod{p^e}.
\]
Thus \(p^e\mid U+V\), proving (1).

## BAR-048

The Mersenne exponent identity
\[
\gcd(2^a-1,2^b-1)=2^{\gcd(a,b)}-1
\tag{2}
\]
and (1) give
\[
\gcd(R_a,R_b)=R_{\gcd(a,b)}.
\tag{3}
\]
Consequently
\[
R_a\mid R_b\quad\Longleftrightarrow\quad a\mid b.
\tag{4}
\]
The forward implication follows from (3), and the reverse implication
follows because \(n_b/n_a\) is odd when \(a\mid b\).

Define the exact shared-prime ledger
\[
L_D=\operatorname{lcm}(R_1,\ldots,R_D).
\tag{5}
\]
Since \(R_D\mid L_D\) and \(L_D\mid\prod_{q\le D}R_q\),
\[
5(2^D-1)
<\log_2 L_D
\le 5\cdot2^{D+1}-10-4D.
\tag{6}
\]
Hence
\[
\log_2 L_D=\Theta(2^D).
\tag{7}
\]
After dividing by the minimum balanced-prime logarithm, the logarithm of
the resulting population upper bound is still \(D+O(\log m)\). Exact
shared-divisor removal changes constants and finite ledgers, but not the
leading \(D\) exponent used by BAR-046. This proves BAR-048 and refutes
REF-050.

## Limitations

- Equation (7) is a barrier for the exact LCM/prime-union charging method.
  It does not exclude a different structural argument about which balanced
  prime divisors can occur.
- No primitive-prime theorem or unproved factorization property is assumed.
- The uniform \(c=1/2\) endpoint, other selector families, and general
  classical factoring remain open.
