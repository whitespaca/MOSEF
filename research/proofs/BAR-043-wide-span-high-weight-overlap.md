# BAR-043: linearly wide compact-gap selectors are not injective

## Claim status and exact scope

- `DEF-036`: `DEFINITION`.
- `BAR-043`: `PROVED`.
- `REF-045`: `REFUTED`.

The result applies to public lists from the exact compact \(\Phi_4\) family
\[
A=3,\qquad B_t=2^t+3,\qquad g=2,\qquad t\ge2
\]
defined in `DEF-035`. It extends `BAR-042` from span strictly below
\(m/2\) to every fixed linear span \(O(m)\). It does not cover superlinear
span, other bases or exceptional families, adaptive or input-dependent
schedules, other compact grammars, arbitrary circuits, or general factoring.

## DEF-036: high-weight overlap ledger

Fix an integer \(h\ge1\). For a public increasing level list
\[
\Lambda_m=(t_{m,1},\ldots,t_{m,r_m}),
\qquad
\Delta_m=t_{m,r_m}-t_{m,1},
\]
let \(K_{m,h}\) be the balanced population primes whose exact compact-gap
support signature has Hamming weight at least \(h+1\). Primes outside
\(K_{m,h}\) have signatures in the low-weight family
\[
\mathcal L_{m,h}
=
\{v\in\{0,1\}^{r_m}:\operatorname{wt}(v)\le h\},
\qquad
|\mathcal L_{m,h}|
=
\sum_{j=0}^{h}\binom{r_m}{j},
\tag{1}
\]
where \(\binom{r_m}{j}=0\) for \(j>r_m\).

This is an analytical proof ledger. The public algorithm receives the level
list and evaluates the compact recurrences; it does not receive
\(K_{m,h}\), prime factors, or support signatures.

## Higher-order overlap collapses to a GCD gap

Let one prime \(p>7\) divide the compact cofactors at
\[
t_0<t_1<\cdots<t_h.
\]
Put \(d_i=t_i-t_0\), \(q=\gcd(d_1,\ldots,d_h)\), and
\[
R_d=3^{2^d-1}+32^{2^d-1}.
\]
Then
\[
p\mid R_q.
\tag{2}
\]

By `BAR-042`, \(p\mid R_{d_i}\) for every \(i\). In the multiplicative
group modulo \(p\), let \(x=3\cdot32^{-1}\). With
\[
k_i=2^{d_i}-1,
\]
the pair-overlap relations are \(x^{k_i}=-1\). The standard identity
\[
\gcd(2^{d_1}-1,\ldots,2^{d_h}-1)=2^q-1
\]
follows by repeated Euclidean reduction of the exponents. Set
\(k=2^q-1\) and \(s_i=k_i/k\). Each \(s_i\) is the odd geometric sum
\[
s_i=1+2^q+\cdots+2^{q(d_i/q-1)},
\]
and \(\gcd(s_1,\ldots,s_h)=1\). Choose integers \(z_i\) with
\(\sum_i z_i s_i=1\). Reducing this equality modulo two shows
\(\sum_i z_i\) is odd. Therefore
\[
x^k
=
\prod_i(x^{k_i})^{z_i}
=
(-1)^{\sum_i z_i}
=-1\pmod p,
\]
which is exactly (2).

The \(h\) positive integers \(d_i/q\) are distinct, so their maximum is at
least \(h\). Hence
\[
q\le\left\lfloor\frac{t_h-t_0}{h}\right\rfloor
\le\left\lfloor\frac{\Delta_m}{h}\right\rfloor.
\tag{3}
\]
This is the gain unavailable to the pairwise union bound: \(h+1\) common
hits charge to an overlap integer controlled by only one \(h\)-th of the
full span.

## Finite high-weight and collision bounds

Write
\[
b_m=\left\lfloor\frac{m-1}{2}\right\rfloor.
\]
For each \((h+1)\)-subset of the level list, the square-free product of all
balanced primes hitting every selected level divides the corresponding
\(R_q\). Equations (2)--(3) and the `BAR-042` bit bound give
\[
|K_{m,h}|
\le
U_{m,h}
:=
\left\lfloor
\frac{
\binom{r_m}{h+1}
\left(5(2^{\lfloor\Delta_m/h\rfloor}-1)+1\right)
}{b_m}
\right\rfloor.
\tag{4}
\]
The union bound can count a high-weight prime repeatedly, which only makes
the bound more conservative.

After removing at most \(U_{m,h}\) primes, every remaining signature lies
in (1). Thus the finite inequality
\[
|\mathcal P_m|-U_{m,h}
>
\sum_{j=0}^{h}\binom{r_m}{j}
\tag{5}
\]
forces two balanced primes to have equal complete signatures. By `BAR-024`,
their square-free \(m\)-bit product produces no proper GCD from the whole
selector.

## BAR-043 and REF-045

Suppose that for fixed constants \(a,C\ge0\), and all sufficiently large
\(m\),
\[
r_m\le m^a,
\qquad
\Delta_m\le Cm,
\]
and that the charged branch-total compact evaluation, GCD, and extraction
cost is polynomial in \(m\). Choose a fixed integer \(h>2C\). When
\(r_m\ge h+1\), equation (4) gives
\[
U_{m,h}
=
O\left(
m^{a(h+1)-1}2^{(C/h)m}
\right).
\tag{6}
\]
The inspected prime-counting consequence used in `BAR-041` gives
\[
|\mathcal P_m|
=
\Omega\left(\frac{2^{m/2}}m\right).
\tag{7}
\]
The ratio of (6) to (7) is
\[
O\left(
m^{a(h+1)}2^{-(1/2-C/h)m}
\right),
\]
which tends to zero because \(h>2C\). Meanwhile (1) is
\(O(m^{ah})\). Therefore (5) holds eventually. If \(r_m\le h\) for
infinitely many lengths, at most \(2^h\) signatures are available there,
so the same conclusion follows directly from (7).

This proves `BAR-043`: no polynomial-size, polynomial-cost public level list
from this exact family whose span is \(O(m)\) is eventually injective on all
complete balanced-prime populations. It refutes `REF-045`, the proposed
linear-span compact-gap escape from `BAR-042`.

## Falsification and scope audit

- **GCD reduction:** the proof uses all pair relations against the same
  first level. It does not assume that a divisor of several \(R_d\) divides
  an arbitrary smaller overlap integer.
- **Parity:** the quotients
  \((2^{d_i}-1)/(2^q-1)\) are odd. This is what preserves the minus sign
  under Bezout reduction.
- **Subset union:** a prime with weight above \(h+1\) may be charged many
  times but is never omitted.
- **Low-weight cells:** the capacity is the exact Hamming-ball size in (1),
  not the full \(2^{r_m}\) signature space.
- **Finite profiles:** the conservative bound (4) need not force a collision
  at small \(m\). Finite observed sparsity is implementation evidence only.
- **Absolute levels and cost:** the theorem controls span but separately
  requires the complete compact recurrence and GCD ledger to be polynomial.
- **Superlinear span:** if \(\Delta_m/m\) is unbounded, no fixed \(h\)
  makes (6) exponentially smaller than (7). That regime remains unresolved.
- **General factoring:** this is a family-specific, public-schedule barrier,
  not a lower bound for adaptive schedules, other circuits, or general
  classical factoring.
