# BAR-044: variable overlap order closes subquadratic compact-gap spans

## Claim status and exact scope

- `DEF-037`: `DEFINITION`.
- `BAR-044`: `PROVED`.
- `REF-046`: `REFUTED`.

The result applies only to the exact public compact \(\Phi_4\) family
\[
A=3,\qquad B_t=2^t+3,\qquad g=2,\qquad t\ge2
\]
from `DEF-035`. It extends `BAR-043` from every fixed linear span to every
polynomial-size list satisfying
\[
\Delta_m\log_2(r_m+1)=o(m^2).
\tag{1}
\]
In particular, it covers \(\Delta_m=O(m^{2-\varepsilon})\) for every fixed
\(\varepsilon>0\) when \(r_m\) is polynomial. It does not cover the full
\(\Theta(m^2/\log m)\) boundary, quadratic or larger spans, other compact
families, adaptive or input-dependent schedules, arbitrary circuits, or
general factoring.

## DEF-037: variable overlap-order ledger

Let
\[
\Lambda_m=(t_{m,1},\ldots,t_{m,r_m})
\]
be a public strictly increasing level list, and put
\[
\Delta_m=t_{m,r_m}-t_{m,1},\qquad
\ell_m=\left\lceil\log_2(r_m+1)\right\rceil.
\]
For \(r_m\ge1\), define the uncapped balancing order
\[
\widehat h_m=
\max\left\{1,
\left\lceil\sqrt{\frac{\Delta_m}{\ell_m}}\right\rceil
\right\},
\]
and the actual analytical order
\[
h_m=\min\{r_m,\widehat h_m\}.
\tag{2}
\]
When \(h_m<r_m\), `DEF-036` is applied with this input-length-dependent
integer \(h_m\). When \(h_m=r_m\), all \(2^{r_m}\) signatures are counted
directly. Neither \(h_m\), the high-weight support set, nor any factor data
is supplied to the public evaluator.

The repository implementation uses the equivalent exact integer rule:
\(h_m\) is the smallest positive integer, capped by \(r_m\), satisfying
\[
h_m^2\ell_m\ge\Delta_m.
\tag{3}
\]

## Reusing the exact higher-overlap bound

For any integer \(1\le h<r_m\), `BAR-043` proves
\[
|K_{m,h}|
\le U_{m,h}:=
\left\lfloor
\frac{\binom{r_m}{h+1}
\left(5(2^{\lfloor\Delta_m/h\rfloor}-1)+1\right)}
{\lfloor(m-1)/2\rfloor}
\right\rfloor
\tag{4}
\]
and shows that every signature outside \(K_{m,h}\) has weight at most \(h\).
Consequently,
\[
|\mathcal P_m|-U_{m,h}>
\sum_{j=0}^{h}\binom{r_m}{j}
\tag{5}
\]
forces a duplicate complete signature and a failed balanced semiprime pair.
Equation (4) is valid for an input-length-dependent \(h\): its proof is a
separate finite union bound at each \(m\) and uses no uniformity assumption
on \(h\).

## BAR-044

Assume that \(r_m\) and the charged branch-total compact evaluation, GCD,
output, and extraction cost are polynomial in \(m\), and assume (1).
Polynomial size gives
\[
\ell_m=O(\log m).
\tag{6}
\]
The uncapped order in (2) satisfies
\[
\widehat h_m\ell_m
\le
\sqrt{\Delta_m\ell_m}+\ell_m
=o(m),
\tag{7}
\]
and
\[
\frac{\Delta_m}{\widehat h_m}
\le\sqrt{\Delta_m\ell_m}
=o(m).
\tag{8}
\]

First suppose \(h_m=r_m\). Then \(r_m\le\widehat h_m=o(m)\), so the complete
signature space has size
\[
2^{r_m}=2^{o(m)}.
\tag{9}
\]
The audited balanced-population bound from `BAR-041` is
\[
|\mathcal P_m|
=\Omega\left(\frac{2^{m/2}}m\right)
=2^{m/2-O(\log m)}.
\tag{10}
\]
Thus the full signature space in (9) is eventually smaller than the
population.

Now suppose \(h_m<r_m\), so \(h_m=\widehat h_m\). Using
\(\binom{r}{h+1}\le r^{h+1}\), equations (4), (7), and (8) give
\[
\begin{aligned}
\log_2(U_{m,h_m}+1)
&\le
(h_m+1)\log_2 r_m
+\frac{\Delta_m}{h_m}
+O(\log m)\\
&=o(m).
\end{aligned}
\tag{11}
\]
The low-weight Hamming ball obeys the deliberately coarse bound
\[
\sum_{j=0}^{h_m}\binom{r_m}{j}
\le(h_m+1)r_m^{h_m},
\]
so by (7),
\[
\log_2\left(\sum_{j=0}^{h_m}\binom{r_m}{j}\right)=o(m).
\tag{12}
\]
Equations (10)--(12) imply (5) for all sufficiently large \(m\).

Therefore every polynomial-size, polynomial-cost public list in this exact
compact-gap family satisfying (1) is eventually noninjective on the complete
balanced-prime population. By `BAR-024`, the corresponding balanced
square-free semiprime pair defeats every candidate GCD in the list. This
proves `BAR-044`.

## Polynomial subquadratic corollary

If \(r_m\le m^a\) and
\[
\Delta_m\le C m^{2-\varepsilon}
\]
for fixed \(a,C\ge0\) and \(\varepsilon>0\), then
\[
\Delta_m\log_2(r_m+1)
=O(m^{2-\varepsilon}\log m)
=o(m^2).
\]
Hence no such list is eventually injective. This refutes `REF-046`, the
proposed polynomial subquadratic-span escape from `BAR-043`.

## Falsification and scope audit

- **Variable \(h_m\):** the proof does not insert a growing parameter into
  the public algorithm. It applies the finite `BAR-043` union bound
  separately at each input length.
- **Subset multiplicity:** the factor
  \(\binom{r_m}{h_m+1}\) remains in (4). Its logarithm is charged in (11);
  it is not discarded.
- **Capped order:** if the balancing order reaches the candidate count, the
  proof switches to the complete \(2^{r_m}\) signature space rather than
  invoking an empty high-weight subset incorrectly.
- **Ceilings and small spans:** the \(+\,\ell_m\) term in (7) charges the
  ceiling. Linear and bounded spans are included but were already closed by
  `BAR-043`.
- **Population scale:** finite profile sparsity is not used in the theorem.
  The exponential separation comes from the inspected population lower
  bound and the analytic \(o(m)\) exponents.
- **Cost:** span alone is not a cost certificate. Polynomial branch-total
  descriptor construction, compact evaluation, GCD, output, and extraction
  remain explicit hypotheses.
- **Boundary:** condition (1) is silent when
  \(\Delta_m\log(r_m+1)=\Theta(m^2)\). Constants at
  \(m^2/\log m\), quadratic spans, and larger spans remain open.
- **General factoring:** this is a barrier for one exact factor-independent
  public family, not a lower bound for all selectors or for classical
  factoring.
