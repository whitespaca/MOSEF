# BAR-050: the exact endpoint LCM/Hamming ledger has no threshold slack

## Claim status and scope

- `DEF-043`: `DEFINITION`.
- `BAR-050`: `PROVED`.
- `REF-052`: `REFUTED`.
- `OPEN-005`: remains `OPEN`.

This is a method barrier for the exact two-ledger certificate used in
BAR-046. It does not prove that the endpoint signatures are injective, that
balanced primes actually divide the charged overlap integers, or that the
general factoring problem is hard.

## DEF-043: endpoint-dense witness family

For every integer \(\lambda\ge6\), put
\[
\Delta_\lambda=2^\lambda-2,\qquad
r_\lambda=2^\lambda-1,\qquad
m_\lambda=\left\lceil
\sqrt{2\lambda\Delta_\lambda}
\right\rceil .
\tag{1}
\]
Use the dense public interval of \(r_\lambda\) levels and the exact
two-ledger certificate consisting of:

1. the prefix LCM \(L_D=\operatorname{lcm}(R_1,\ldots,R_D)\) for primes
   hitting at least \(h+1\) levels, where
   \(D=\lfloor\Delta_\lambda/h\rfloor\); and
2. the low-weight Hamming capacity
   \(\sum_{j=0}^{h}\binom{r_\lambda}{j}\).

The list has
\(\ell_\lambda=\lceil\log_2(r_\lambda+1)\rceil=\lambda\) and satisfies the
endpoint inequality
\[
\Delta_\lambda\le
\frac{m_\lambda^2}{2\ell_\lambda}.
\tag{2}
\]

## Leading coefficient balance

For \(h=\lceil x m/\ell\rceil\) at \(c=1/2\), the BAR-046 leading
coefficients are
\[
\frac{1}{2x}
\quad\hbox{and}\quad
\frac{x}{2}.
\tag{3}
\]
For every \(x>0\),
\[
\max\left\{\frac{1}{2x},\frac{x}{2}\right\}\ge\frac12,
\tag{4}
\]
with equality only at \(x=1\). Thus no fixed rational choice gives leading
slack.

## BAR-050

Let
\[
H_\lambda=
\left\lfloor\frac{2\Delta_\lambda}{m_\lambda}\right\rfloor.
\tag{5}
\]
For every threshold \(1\le h\le r_\lambda\), one of the exact ledger terms
already matches or exceeds the conservative balanced-population lower
bound for all sufficiently large \(\lambda\).

If \(h\le H_\lambda\), then
\[
D=\left\lfloor\frac{\Delta_\lambda}{h}\right\rfloor
\ge\left\lfloor\frac{m_\lambda}{2}\right\rfloor.
\tag{6}
\]
BAR-048 gives
\[
\log_2L_D>5(2^D-1).
\tag{7}
\]
After division by the minimum balanced-prime bit length, the resulting
LCM charge is larger than
\(2^{\lfloor m_\lambda/2\rfloor}/(81m_\lambda)\). Hence the high-weight
charge alone prevents the BAR-046 pigeonhole inequality.

Suppose \(h>H_\lambda\), and put \(h_0=H_\lambda+1\). Hamming capacity is
monotone in \(h\), so it is enough to lower-bound
\(\binom{r_\lambda}{h_0}\). Equations (1) and (5) give
\[
h_0=\frac{m_\lambda}{\lambda}+O(1),\qquad
\frac{r_\lambda}{h_0}=\frac{m_\lambda}{2}(1+o(1)),
\tag{8}
\]
while
\[
\log_2m_\lambda
=\frac{\lambda}{2}
+\frac12\log_2(2\lambda)+o(1).
\tag{9}
\]
Using \(\binom rh\ge(r/h)^h\),
\[
\begin{aligned}
\log_2\binom{r_\lambda}{h_0}
&\ge h_0\log_2(r_\lambda/h_0)\\
&=\frac{m_\lambda}{2}
+\Omega\left(
\frac{m_\lambda\log\lambda}{\lambda}
\right).
\end{aligned}
\tag{10}
\]
This exceeds the balanced-population logarithm
\(m_\lambda/2-O(\log m_\lambda)\). The low-weight ledger therefore blocks
the certificate on the other side of (5).

The two cases cover every \(h\), including choices depending arbitrarily on
\(\lambda\). This proves BAR-050 and refutes REF-052.

## Limitations

- Failure of this sufficient collision certificate is not evidence of an
  injective endpoint selector.
- The LCM charge covers possible balanced-prime divisors; it does not prove
  their occurrence.
- A prime-residue restriction, a different signature invariant, another
  compact family, or an adaptive algorithm could use information absent from
  this ledger.
- OPEN-005 and general classical polynomial-time factoring remain open.
