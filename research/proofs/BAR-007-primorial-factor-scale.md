# BAR-007 - Factor-scale scarcity for first-primes primorials

## Status and scope

Status: `PROVED`.

This result concerns only the nested family
\[
P_r=\prod_{j=1}^r p_j
\]
of products of the first \(r\) primes and the combined divisibility channels
\(q-1\mid P_r\) and \(q+1\mid P_r\). It is not a statement about arbitrary
boundary-size exponents, a natural distribution of semiprimes, recognition
without factoring, or a lower bound for general factoring.

## DEF-012

For integers \(r\ge1\) and \(X\ge3\), define
\[
T(X)=\max\{t\ge0:(t+1)!\le X+1\}
\]
and
\[
D(r,X)=\sum_{i=0}^{\min\{r,T(X)\}}\binom ri.
\]
These are respectively the factor-scale support threshold and divisor
candidate bound. The corresponding two-channel prime-candidate bound is
\(2D(r,X)\).

## BAR-007 statement

Fix constants \(C,\beta>0\), and let \(r(k)\le Ck\). Define
\[
H_k(\beta)=\{q\le2^{\beta k}:q\text{ is an odd prime and }
q-1\mid P_{r(k)}\text{ or }q+1\mid P_{r(k)}\}.
\]
Then
\[
|H_k(\beta)|
\le 2D(r(k),2^{\beta k})
=2^{O(k\log\log k/\log k)}
=2^{o(k)}.
\]

Consequently, let \(S_k\) be any stipulated set of odd primes no larger than
\(2^{\beta k}\), with \(|S_k|\ge2^{\alpha k}\) for a fixed \(\alpha>0\), such
that products of distinct members have the declared common input length.
Under the one-exponent schedule \(P_{r(k)}\), the fraction of unordered pairs
in \(S_k\) having distinct combined signatures is at most
\[
2^{-\alpha k+o(k)}.
\]
In particular it tends to zero for every fixed \(C\), including critical and
supercritical constants not resolved by BAR-006.

The same conclusion holds for a nested list
\(P_{r_1(k)},\ldots,P_{r_s(k)}\) with every \(r_i(k)\le Ck\): its hit union is
contained in the hit set of \(P_{\max_i r_i(k)}\).

## Proof

### 1. A factor-scale divisor has sparse support

Let \(d\mid P_r\) and let \(t=\omega(d)\). The primorial is square-free, so
\(d\) is a product of \(t\) distinct primes. The least possible such product
is the product of the first \(t\) primes. Since the \(j\)-th prime satisfies
\(p_j\ge j+1\),
\[
d\ge\prod_{j=1}^t p_j\ge\prod_{j=1}^t(j+1)=(t+1)!.
\]
Therefore \(d\le X+1\) implies \(t\le T(X)\). Choosing the support from the
\(r\) available primes gives at most
\[
\sum_{i=0}^{\min\{r,T(X)\}}\binom ri=D(r,X)
\]
such divisors.

Every \(q\in H_k(\beta)\) supplies a divisor \(d=q-1\) or \(d=q+1\) with
\(d\le2^{\beta k}+1\). Conversely, each divisor supplies at most the two
candidates \(d-1,d+1\), before parity and primality are imposed. Thus
\[
|H_k(\beta)|\le2D(r(k),2^{\beta k}).
\]
No prime-distribution hypothesis is used.

### 2. The support threshold is \(O(k/\log k)\)

For \(t\ge2\), at least \(t/2\) factors of \((t+1)!\) are at least \(t/2\).
Hence
\[
(t+1)!\ge(t/2)^{t/2}.
\]
If \((t+1)!\le2^{\beta k}+1\), then
\[
\frac t2\log_2(t/2)\le\beta k+1.
\]
This implies \(t=O(k/\log k)\): otherwise, along a subsequence with
\(t/(k/\log k)\to\infty\), the left side divided by \(k\) would be
unbounded. Therefore \(T(2^{\beta k})=O(k/\log k)\).

### 3. The binomial sum is subexponential

Write \(r=r(k)\) and \(T=T(2^{\beta k})\). If \(r<2T\), then
\(D(r,2^{\beta k})\le2^r\le2^{2T}=2^{O(k/\log k)}\). Otherwise \(T\le r/2\)
and
\[
\sum_{i=0}^T\binom ri
\le(T+1)\binom rT
\le(T+1)\left(\frac{er}{T}\right)^T.
\]
For \(r\le Ck\), the function
\(t\mapsto t\log(eCk/t)\) is increasing throughout the relevant range.
Its maximum for \(1\le t\le O(k/\log k)\) is therefore attained at the
upper endpoint. Taking base-two logarithms gives
\[
\log_2 D(r,2^{\beta k})
=O(\log k)+O\!\left(\frac{k}{\log k}\log\log k\right)
=O\!\left(\frac{k\log\log k}{\log k}\right)
=o(k).
\]
This proves the hit-set bound.

### 4. Transfer to promised-pair density

For a single primorial exponent and an odd prime \(q\), the two nonzero
coordinates cannot both occur: one of the consecutive even integers
\(q-1,q+1\) is divisible by \(4\), whereas \(4\nmid P_r\). Thus signatures
are \((1,0),(0,1),(0,0)\).

Let their counts on \(S_k\) be \(a,b,z\), respectively. The exact number of
distinct-signature pairs is
\[
ab+z(a+b).
\]
It is at most the number of pairs incident to the hit set, and BAR-003 gives
the same elementary bound
\[
\frac{\text{promised pairs}}{\binom{|S_k|}{2}}
\le \frac{2|H_k(\beta)|}{|S_k|-1}
\le2^{-\alpha k+o(k)}.
\]
This tends to zero.

### 5. Boundary straight-line consequence

Suppose \(P_{r(k)}\) is exactly realized in the DEF-010 multiplication-only
model using \(O(k\log k)\) charged nodes. BAR-005 gives
\(\ell(P_{r(k)})=O(k\log k)\). But
\[
P_{r(k)}\ge(r(k)+1)!.
\]
The factorial estimate from step 2 then implies \(r(k)=O(k)\). Hence every
first-primes primorial available at this boundary falls under BAR-007.

## Falsification attempts

EXP-0011 exhaustively enumerates bounded primorial divisors and checks the
factorial support threshold, the binomial candidate count, actual
\(d\pm1\) prime hits, and the exact three-signature pair formula. Selected
signature and hit-count vectors are independently evaluated by the Python,
Rust, and C# implementations. These finite checks do not prove the
asymptotic statement; they test its exact combinatorial premises.

## Limitations

- The theorem is specific to first-primes primorials and their nested
  subfamily.
- The prime population is stipulated; existence and recognizability are not
  asserted.
- The theorem uses a fixed linear factor-bit cap \(2^{\beta k}\).
- It is a schedule-specific promise-density barrier, not a factoring lower
  bound.
