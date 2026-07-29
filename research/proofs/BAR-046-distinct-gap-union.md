# BAR-046: distinct-gap charging removes subset multiplicity

## Claim status and scope

- `DEF-039`: `DEFINITION`.
- `BAR-046`: `PROVED`.
- `REF-048`: `REFUTED`.
- `OPEN-005`: `OPEN`.

The result applies only to the exact DEF-035 family
\[
A=3,\qquad B_t=2^t+3,\qquad g=2.
\]
It improves the uniform boundary constant from \(1/8\) to \(1/2\). The
endpoint \(c=1/2\), larger constants, other compact families, adaptive
schedules, arbitrary circuits, and general factoring remain outside the
theorem.

## DEF-039: distinct-gap high-weight ledger

For a public list of \(r_m\) distinct levels with span \(\Delta_m\), choose
the M52 rational order
\[
h_m=\min\left\{r_m,
\left\lceil\frac{x m}{\ell_m}\right\rceil\right\},
\qquad
\ell_m=\lceil\log_2(r_m+1)\rceil.
\tag{1}
\]
If \(h_m<r_m\), put
\[
D_m=\left\lfloor\frac{\Delta_m}{h_m}\right\rfloor.
\tag{2}
\]
Instead of charging the same overlap integer once for every
\((h_m+1)\)-subset, charge each of
\[
R_q=3^{2^q-1}+32^{2^q-1},
\qquad 1\le q\le D_m,
\tag{3}
\]
only once. Keep the exact low-weight Hamming capacity from `DEF-038`. If
\(h_m=r_m\), count all complete signatures.

The exact prefix bit bound is
\[
\begin{aligned}
\sum_{q=1}^{D_m}
\bigl(5(2^q-1)+1\bigr)
&=5(2^{D_m+1}-2)-4D_m\\
&=5\cdot2^{D_m+1}-10-4D_m.
\end{aligned}
\tag{4}
\]

## Distinct-gap lemma

Let a balanced prime \(p>7\) hit at least \(h_m+1\) levels. Select any
\(h_m+1\) hit levels \(t_0<\cdots<t_{h_m}\). `BAR-043` proves
\[
p\mid R_q,\qquad
q=\gcd(t_1-t_0,\ldots,t_{h_m}-t_0)
\le\frac{\Delta_m}{h_m}.
\tag{5}
\]
Thus every high-weight balanced prime divides at least one integer in (3).
The chosen subset need not be remembered: all subsets producing the same
\(q\) point to the same \(R_q\).

Every balanced prime has logarithm at least \((m-1)/2\). Equations (3)--(5)
therefore bound the high-weight population by
\[
V_{m,h_m}
\le
\frac{5\cdot2^{D_m+1}-10-4D_m}
{\lfloor(m-1)/2\rfloor}.
\tag{6}
\]
In particular,
\[
\log_2(V_{m,h_m}+1)
\le D_m+O(\log m).
\tag{7}
\]
No \(\binom{r_m}{h_m+1}\) term remains.

## BAR-046

Assume polynomial charged cost and
\[
\Delta_m\le(c+o(1))\frac{m^2}{\ell_m}
\tag{8}
\]
for a fixed \(c>0\). As in `BAR-045`, distinct-level packing gives the
uniform low-weight bound
\[
\log_2\left(
\sum_{j=0}^{h_m}\binom{r_m}{j}
\right)
\le\left(\frac{x}{2}+o(1)\right)m
\tag{9}
\]
unless the complete signature space is already \(2^{o(m)}\). Equations
(1), (2), (7), and (8) give
\[
\log_2(V_{m,h_m}+1)
\le\left(\frac{c}{x}+o(1)\right)m.
\tag{10}
\]

If \(0<c<1/2\), choose a rational \(x\) with
\[
2c<x<1.
\tag{11}
\]
Then both leading coefficients \(c/x\) and \(x/2\) are strictly below
\(1/2\). The sum of the high-weight exception bound and all low-weight
signature cells is \(2^{(1/2-\eta)m}\) for some \(\eta>0\), while
`BAR-041` supplies
\[
|\mathcal P_m|=2^{m/2-O(\log m)}.
\]
Hence a duplicate complete signature and a failed balanced semiprime pair
exist for all sufficiently large \(m\). This proves `BAR-046` and refutes
`REF-048`.

## Growth-refined constants

If
\[
\ell_m/\log_2m\longrightarrow a,
\]
packing forces \(a\le2\). For \(1<a\le2\), the low-weight coefficient
in (9) sharpens to \(x(a-1)/a\). A rational \(x\) satisfying
\[
2c<x<\frac{a}{2(a-1)}
\]
exists exactly when
\[
c<\frac{a}{4(a-1)}.
\tag{12}
\]
The representative thresholds are \(1\) at \(a=4/3\), \(3/4\) at
\(a=3/2\), \(5/8\) at \(a=5/3\), and \(1/2\) at \(a=2\). If \(a<1\),
the full signature space is already subexponential. If \(a=1\), the
low-weight exponent is \(o(m)\), so every fixed \(c\) is excluded by choosing
any rational \(x>2c\).

## Endpoint and adversarial review

- At the uniform endpoint \(c=1/2\), (10) needs \(x>1\), while (9) needs
  \(x<1\). The current worst-packing ledger therefore has no fixed
  exponential slack. This is not an injective construction.
- The proof charges every \(q\le D_m\), even when no \(h_m+1\)-subset of the
  public level list has offset GCD \(q\). M54 will audit that remaining
  realizability overcount.
- The exact overlap integers may share prime divisors. Charging them
  separately is still an upper bound and may be further reducible.
- EXP-0051 has 25 finite collision certificates and 15 noncertificates.
  Neither finite class is used to prove the asymptotic theorem or endpoint
  openness.
- Polynomial branch-total construction, compact evaluation, GCD, output, and
  extraction cost remains an explicit hypothesis.
- No factor data, support signature, or population enumeration enters the
  public evaluator.
- This is not a lower bound for other selectors or for general classical
  factoring.
