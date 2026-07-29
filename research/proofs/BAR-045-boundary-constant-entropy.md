# BAR-045: packing-aware constants at the compact-gap boundary

## Claim status and exact scope

- `DEF-038`: `DEFINITION`.
- `BAR-045`: `PROVED`.
- `REF-047`: `REFUTED`.
- `OPEN-004`: `OPEN`.

The result applies only to the exact public compact \(\Phi_4\) family
\[
A=3,\qquad B_t=2^t+3,\qquad g=2
\]
from `DEF-035`. It closes the uniform range
\[
\Delta_m\le(c+o(1))
\frac{m^2}{\ell_m},
\qquad
\ell_m=\lceil\log_2(r_m+1)\rceil,
\qquad
0<c<\frac18.
\tag{1}
\]
It does not close the endpoint \(c=1/8\), larger constants, other compact
families, adaptive schedules, arbitrary circuits, or general factoring.

## DEF-038: rational boundary-order ledger

Fix a constant \(x>0\), and put
\[
\widehat h_m=\left\lceil\frac{x m}{\ell_m}\right\rceil,
\qquad
h_m=\min\{r_m,\widehat h_m\}.
\tag{2}
\]
If \(h_m<r_m\), use the exact `BAR-043` high-weight union bound at threshold
\(h_m+1\) and the exact low-weight capacity
\[
\sum_{j=0}^{h_m}\binom{r_m}{j}.
\tag{3}
\]
If \(h_m=r_m\), use the complete \(2^{r_m}\) signature space. The
implementation accepts rational \(x\), uses integer ceiling arithmetic, and
depends only on \((m,r_m,\Delta_m)\).

## Packing lemma

The levels are distinct integers, so
\[
r_m\le\Delta_m+1.
\tag{4}
\]
Under (1), (4) gives
\[
r_m=O(m^2/\ell_m).
\]
Since \(\ell_m=\log_2 r_m+O(1)\), taking logarithms yields
\[
\ell_m\le2\log_2m-\log_2\ell_m+O(1).
\tag{5}
\]
This list-geometry constraint is essential. Treating \(r_m\) and
\(\Delta_m\) as independent would admit impossible densely packed lists and
would lose the sharp uniform constant.

## Entropy bound

Suppose first that \(h_m=r_m\), or that \(h_m\ge r_m/2\). If
\(\ell_m\) is bounded, then \(r_m\) is bounded. Otherwise
\(\widehat h_m=o(m)\). In both cases \(r_m=o(m)\), and the complete signature
space \(2^{r_m}\) is \(2^{o(m)}\).

It remains to consider \(h_m<r_m/2\). The standard binomial bounds give
\[
\binom{r_m}{h_m+1}
\le
\left(\frac{e r_m}{h_m+1}\right)^{h_m+1}
\tag{6}
\]
and
\[
\sum_{j=0}^{h_m}\binom{r_m}{j}
\le
(h_m+1)\left(\frac{e r_m}{h_m}\right)^{h_m}.
\tag{7}
\]
By (2) and (5),
\[
\begin{aligned}
\log_2\frac{e r_m}{h_m}
&\le
\ell_m-\log_2m+\log_2\ell_m+O(1)\\
&\le
\left(\frac12+o(1)\right)\ell_m.
\end{aligned}
\tag{8}
\]
Therefore the logarithm of (7) is at most
\[
\left(\frac{x}{2}+o(1)\right)m.
\tag{9}
\]

The exact `BAR-043` high-weight bound retains every
\(\binom{r_m}{h_m+1}\) subset. Equations (1), (2), (6), and (8) give
\[
\log_2(U_{m,h_m}+1)
\le
\left(\frac{x}{2}+\frac{c}{x}+o(1)\right)m.
\tag{10}
\]

## BAR-045

For \(0<c<1/8\), choose a rational \(x>0\) with
\[
\frac{x}{2}+\frac{c}{x}<\frac12.
\tag{11}
\]
Such an \(x\) exists because
\[
\min_{x>0}\left(\frac{x}{2}+\frac{c}{x}\right)
=\sqrt{2c}<\frac12.
\tag{12}
\]
Equation (11) also implies \(x/2<1/2\). Thus both (9) and (10) are bounded
by \(2^{(1/2-\eta)m}\) for some \(\eta>0\), while `BAR-041` supplies
\[
|\mathcal P_m|=2^{m/2-O(\log m)}.
\tag{13}
\]
The population eventually exceeds the high-weight exception bound plus all
remaining signature cells. Hence two balanced primes have the same complete
signature, and `BAR-024` supplies a failed balanced semiprime pair. This
proves `BAR-045` and refutes `REF-047`.

## Growth-refined constants

Suppose additionally
\[
\frac{\ell_m}{\log_2m}\longrightarrow a.
\tag{14}
\]
Packing forces \(a\le2\). If \(a<1\), then \(r_m=o(m)\) and the full
signature space is already subexponential. If \(a=1\), the entropy term in
(8) is \(o(\ell_m)\); choosing any fixed \(x>2c\) closes every fixed
boundary constant \(c\).

For \(1<a\le2\), (8) sharpens to
\[
\log_2\frac{e r_m}{h_m}
=\left(\frac{a-1}{a}+o(1)\right)\ell_m.
\]
The leading high-weight coefficient becomes
\[
\frac{a-1}{a}x+\frac{c}{x},
\]
whose minimum is \(2\sqrt{c(a-1)/a}\). Therefore the growth-refined range is
\[
c<\frac{a}{16(a-1)}.
\tag{15}
\]
Representative thresholds are \(1/4\) at \(a=4/3\), \(3/16\) at
\(a=3/2\), \(5/32\) at \(a=5/3\), and \(1/8\) at \(a=2\).

## Endpoint and adversarial review

- At \(c=1/8\), the uniform coefficient in (12) is exactly \(1/2\).
  The present asymptotic upper ledger has no fixed exponential slack against
  (13). This is a limitation of the proof ledger, not an injective
  construction or a lower bound on all possible refinements.
- For \(c>1/8\), the same uniform leading coefficient exceeds \(1/2\) for
  every constant \(x\). Shared overlap divisors or reduced subset
  multiplicity could still improve the high-weight charge.
- The exact finite EXP-0050 records confirm collision certificates for its 12
  below-endpoint profiles and no certificates for its eight endpoint-or-above
  profiles. Those finite classifications do not prove the asymptotic theorem
  or the endpoint's openness.
- Polynomial charged construction, compact evaluation, GCD, output, and
  extraction cost remains a hypothesis. Span and packing alone are not an
  algorithmic cost proof.
- No factor, support signature, or population enumeration is supplied to the
  online evaluator.
- The result is not a lower bound for other selectors or general classical
  integer factoring.
