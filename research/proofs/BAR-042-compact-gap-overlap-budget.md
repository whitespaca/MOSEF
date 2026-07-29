# BAR-042: short-span compact-gap selectors are not injective

## Claim status and exact scope

- `DEF-035`: `DEFINITION`.
- `BAR-042`: `PROVED`.
- `REF-044`: `REFUTED`.

The result applies to public lists from the exact compact \(\Phi_4\) family
\[
A=3,\qquad B_t=2^t+3,\qquad g=2,\qquad t\ge2.
\]
It proves an asymptotic obstruction when the number of levels is polynomial
and their span is at most \((1/2-\varepsilon)m\) for a fixed
\(\varepsilon>0\). It does not cover wider level lists, other bases or
families, adaptive or input-dependent schedules, other compact grammars, or
general factoring algorithms.

## DEF-035: compact-gap level selector

For each input length \(m\), before the particular input \(N\) is received,
choose a strictly increasing public level list
\[
\Lambda_m=(t_{m,1},\ldots,t_{m,r_m}),\qquad t_{m,j}\ge2.
\]
Let \(C_t\) be the exact cofactor from `DEF-029`,
\[
C_t=\frac{16(2^{E_t}+3)}{35},
\qquad E_t=3\cdot2^t+5.
\]
The public algorithm evaluates \(C_t\bmod N\) by the existing compact
recurrence and takes its GCD with \(N\). It does not materialize \(C_t\) or
receive its prime support.

The charged compact evaluation cost is
\[
O\left(\sum_{j=1}^{r_m}t_{m,j}\right)
\operatorname{poly}(m)r_m
\text{the cost of }r_m\text{ GCDs}.
\]
This includes the \(t+O(1)\)-bit ordinary binary parameters and the
corresponding modular recurrence steps. Thus
\(\sum_jt_{m,j}=\operatorname{poly}(m)\) gives polynomial branch-total cost
even though each \(B_t\) is exponentially large numerically.

Put
\[
\Delta_m=t_{m,r_m}-t_{m,1}
\]
when \(r_m\ge2\), and \(\Delta_m=0\) when \(r_m=1\). On the balanced
population \(\mathcal P_m\), let \(J_m\) be the primes whose support
signature has Hamming weight at least two.

## Exact pair-overlap integer

Let \(2\le t<u\), put
\[
d=u-t,\qquad k=2^d-1,\qquad R_d=3^k+32^k.
\]
For every prime \(p>7\),
\[
p\mid C_t\ \text{and}\ p\mid C_u
\quad\Longrightarrow\quad p\mid R_d.
\tag{1}
\]

Indeed, `BAR-023` gives \(2^{E_t}\equiv2^{E_u}\equiv-3\pmod p\).
Since
\[
E_u=2^dE_t-5(2^d-1)=2^dE_t-5k,
\]
we obtain
\[
-3
\equiv(-3)^{2^d}32^{-k}\pmod p.
\]
After multiplying by \(32^k\) and dividing by the unit \(-3\),
\[
32^k\equiv(-3)^{2^d-1}=(-3)^k=-3^k\pmod p,
\]
because \(k\) is odd. This is exactly (1).

Moreover,
\[
0<R_d<2\cdot32^k=2^{5k+1},
\]
so
\[
\operatorname{bitlength}(R_d)\le5(2^d-1)+1.
\tag{2}
\]
The special denominator primes do not enter the balanced population for
\(m\ge9\), where every population prime is greater than seven.

## Finite overlap and collision bound

Write
\[
b_m=\left\lfloor\frac{m-1}{2}\right\rfloor.
\]
For each pair \(i<j\), the square-free product of balanced primes dividing
both \(C_{t_{m,i}}\) and \(C_{t_{m,j}}\) divides
\(R_{t_{m,j}-t_{m,i}}\). Equations (1)--(2) therefore give
\[
|J_m|
\le
U_m:=
\sum_{1\le i<j\le r_m}
\left\lfloor
\frac{5(2^{t_{m,j}-t_{m,i}}-1)+1}{b_m}
\right\rfloor.
\tag{3}
\]
The union bound may count one prime several times and is deliberately
conservative.

Every prime outside \(J_m\) has signature Hamming weight zero or one. There
are only \(r_m+1\) such signatures: the all-zero vector and the \(r_m\)
one-hot vectors. Consequently,
\[
|\mathcal P_m|-U_m>r_m+1
\tag{4}
\]
forces two population primes to have the same complete compact signature.
By `BAR-024`, their square-free \(m\)-bit product yields no proper GCD from
the selector.

## BAR-042 and REF-044

Suppose that for fixed constants \(a\ge0\) and \(\varepsilon>0\),
\[
r_m\le m^a,\qquad
\Delta_m\le(1/2-\varepsilon)m
\]
for all sufficiently large \(m\). From (3),
\[
U_m
\le
\binom{r_m}{2}
\frac{5(2^{\Delta_m}-1)+1}{b_m}
=O\left(m^{2a-1}2^{(1/2-\varepsilon)m}\right).
\tag{5}
\]
The inspected prime-counting consequence already used in `BAR-041` gives
\[
|\mathcal P_m|
=\Omega\left(\frac{2^{m/2}}m\right).
\tag{6}
\]
The ratio of (5) to (6) is
\(O(m^{2a}2^{-\varepsilon m})\), which tends to zero. Therefore (4) holds
eventually, and the selector is not injective on every sufficiently large
balanced population.

This proves `BAR-042`. It refutes `REF-044`, the hypothesis that a
polynomial-size short-span list from this exact encoded compact-gap family
can separate all sufficiently large balanced prime pairs. The two explicit
shifted schedules
\[
\{m,\ldots,m+\lfloor m/4\rfloor\},
\qquad
\{2m,\ldots,2m+\lfloor m/4\rfloor\}
\]
have \(O(m^2)\) compact branch-total work and satisfy the theorem.

## Falsification and scope audit

- **Absolute level versus span:** the overlap integer depends only on
  \(u-t\). Shifting a window to larger public levels does not evade the
  proof, provided branch-total evaluation remains polynomial.
- **Magnitude leakage:** no lower or upper support estimate is inferred from
  the exponentially long cofactors themselves. Only the exact overlap
  consequence (1) is charged.
- **Pairwise union bound:** a prime hitting three candidates is overcounted,
  never omitted.
- **Low-weight signatures:** removing all possible multi-hit primes leaves
  at most the zero and one-hot signatures, not \(2^{r_m}\) arbitrary cells.
- **Full collisions:** equal one bits give full collisions, and equal zero
  bits give units. Equal complete signatures therefore never yield a proper
  GCD.
- **Denominator primes:** the implication uses \(p>7\); balanced populations
  at the stated lengths meet that condition.
- **Compact cost:** polynomial list size alone is not enough. The ledger also
  charges \(\sum_jt_{m,j}\) modular recurrence steps and every GCD.
- **Wide-span escape:** when \(\Delta_m\) approaches or exceeds \(m/2\),
  (5) no longer beats the population lower bound. Such schedules remain
  open.
- **General factoring:** this is a family-specific public-schedule barrier,
  not a lower bound for adaptive schedules, other circuits, or general
  classical factoring.
