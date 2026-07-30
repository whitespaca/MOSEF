# BAR-051: overlap-prime occurrence is an exact order-periodic set

## Claim status and scope

- `DEF-044`: `DEFINITION`.
- `BAR-051`: `PROVED`.
- `REF-053`: `REFUTED`.

This theorem characterizes which indices \(q\) can contain one fixed prime
divisor of
\[
R_q=3^{2^q-1}+32^{2^q-1}.
\]
It does not bound how many balanced primes have each order, prove a useful
prime-distribution theorem, or close OPEN-005.

## DEF-044

For a prime \(p>7\), set
\[
z_p=3\cdot32^{-1}\pmod p,\qquad
t_p=\operatorname{ord}_p(z_p).
\tag{1}
\]
If \(t_p=2d_p\) with \(d_p\) odd, define
\[
a_p=
\begin{cases}
1,&d_p=1,\\
\operatorname{ord}_{d_p}(2),&d_p>1.
\end{cases}
\tag{2}
\]
Otherwise leave \(a_p\) undefined.

## BAR-051

For every \(q\ge1\),
\[
p\mid R_q
\quad\Longleftrightarrow\quad
t_p=2d_p
\text{ with \(d_p\) odd and }
d_p\mid2^q-1.
\tag{3}
\]
Equivalently, whenever occurrence is possible,
\[
\{q\ge1:p\mid R_q\}
=\{a_p,2a_p,3a_p,\ldots\}.
\tag{4}
\]

Indeed, put \(n=2^q-1\), which is odd. Since \(p\nmid96\),
\[
p\mid R_q\quad\Longleftrightarrow\quad z_p^n=-1.
\tag{5}
\]
If (5) holds, then \(t_p\mid2n\) but \(t_p\nmid n\). Because \(n\) is odd,
\(t_p=2d_p\) for an odd divisor \(d_p\mid n\). Conversely, if
\(t_p=2d_p\) and \(d_p\mid n\), then \(z_p^{d_p}=-1\); the quotient
\(n/d_p\) is odd, so (5) follows.

For \(d_p>1\), the divisibility
\(d_p\mid2^q-1\) is exactly
\(2^q\equiv1\pmod{d_p}\), which holds precisely when
\(a_p\mid q\). The case \(d_p=1\) would give \(z_p=-1\), hence
\(p\mid35\), and therefore does not occur for \(p>7\). This proves
(3)--(4).

## Consequence for exact LCM charging

The periodic repeats in (4) are exactly the index-divisibility repetitions
already removed by BAR-048:
\[
R_a\mid R_q\quad\Longleftrightarrow\quad a\mid q.
\tag{6}
\]
Thus occurrence periodicity supplies no additional de-duplication beyond
the exact prefix LCM. It refutes REF-053, the hypothesis that treating each
prime's repeated occurrence levels as a progression automatically shrinks
that LCM.

## Limitations

- The theorem gives a necessary and sufficient condition for a fixed prime,
  not an upper bound on the number of balanced primes satisfying it.
- Finite hit density among small primes is `EMPIRICAL` and is not
  extrapolated.
- Strong distribution information for the orders \(t_p\), other compact
  families, adaptive algorithms, and general factoring remain open.
