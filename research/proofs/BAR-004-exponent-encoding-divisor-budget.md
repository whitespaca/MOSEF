# BAR-004 - Exponent-encoding divisor-budget barrier

Status: `PROVED`; bounded falsification and independent adversarial and
source-scope review passed on 2026-07-26.

## Computation model and scope

For a positive integer \(d\), let

\[
\ell(d)=\lceil\log_2(d+1)\rceil
\]

be its ordinary unsigned binary representation length. Let

\[
T_\ell=\lfloor\sqrt\ell\rfloor
\]

and define \(A_\ell\) to be the largest nonnegative integer satisfying

\[
(T_\ell+1)^{A_\ell}<2^\ell.
\]

Define the exact integer one-length budget

\[
B(\ell)=(\ell+1)^{T_\ell}2^{A_\ell}
\]

and its monotone envelope

\[
Q(L)=\max_{1\le\ell\le L}B(\ell).                \tag{1}
\]

The schedule model is an explicit, factorization-independent finite list
\(\Delta(k)\subset\mathbb Z_{>0}\) used for every prime pair in a declared
common-input-length population. Write

\[
E(k)=|\Delta(k)|,\qquad
L(k)=\max_{d\in\Delta(k)}\ell(d).
\]

This model permits exponent values above the prime factors. It charges the
binary representation and the individual modular evaluations. It does not
cover a compressed circuit, product tree, or batch representation that
evaluates exponentially many implicit exponents without listing them; such a
mechanism would require a separate exact semantics and cost analysis.

## DEF-009 - bit-length divisor budget

Equation (1) is the bit-length divisor budget. Both \(B\) and \(Q\) are
integer valued and can be checked without floating-point approximation.

## BAR-004 statement

The following assertions hold.

1. **Exact divisor budget.** For every positive integer \(d\),

   \[
   \tau(d)\le B(\ell(d))\le Q(\ell(d)).            \tag{2}
   \]

2. **Asymptotic budget.**

   \[
   \log_2 Q(L)
   =
   O\!\left(\frac{L}{\log L}\right).               \tag{3}
   \]

3. **Combined hit-set bound.** Let \(H(k)\) be the set of all odd primes
   whose combined \(p-1/p+1\) signature for \(\Delta(k)\) is nonzero. Then

   \[
   |H(k)|
   \le
   2\sum_{d\in\Delta(k)}\tau(d)
   \le
   2E(k)Q(L(k)).                                   \tag{4}
   \]

4. **Encoding barrier.** If

   \[
   E(k)=k^{O(1)}
   \quad\text{and}\quad
   L(k)=o(k\log k),
   \]

   then \(|H(k)|\le2^{o(k)}\). In particular this applies when every exponent
   has \(O(k)\) bits, even if its numerical value exceeds the prime factors.

5. **Exponential-population density barrier.** Fix \(\alpha>0\). For every
   finite odd-prime set \(S_k\) such that all distinct-prime products use
   common input length \(k\) and

   \[
   |S_k|\ge2^{\alpha k},
   \]

   the uniform unordered-pair fraction \(\rho_k\) in the local, hence
   square-free-semiprime hereditary, union of the M3 and M7 promises satisfies

   \[
   \rho_k
   \le
   \frac{2|H(k)|}{|S_k|-1}
   \le
   2^{-\alpha k+o(k)}
   \longrightarrow0.                              \tag{5}
   \]

This is an explicit-list encoding barrier. It does not exclude schedules with
\(\Omega(k\log k)\)-bit exponents, exponentially many explicit exponents,
adaptive factor-dependent choices, or a separately justified compressed
evaluation mechanism.

## Proof

### Exact divisor budget

Write

\[
d=\prod_i p_i^{a_i},\qquad \ell=\ell(d),\qquad T=T_\ell.
\]

Because \(d<2^\ell\), every exponent satisfies \(a_i\le\ell\). Split the
prime divisors at \(T\).

There are at most \(T\) small primes \(p_i\le T\), and each contributes at
most \(\ell+1\) to \(\tau(d)=\prod_i(a_i+1)\). Their total contribution is at
most

\[
(\ell+1)^T.                                       \tag{6}
\]

Let

\[
A=\sum_{p_i>T}a_i.
\]

Every large prime is at least \(T+1\), so

\[
(T+1)^A
\le
\prod_{p_i>T}p_i^{a_i}
\le d
<2^\ell.
\]

Thus \(A\le A_\ell\). Since \(a+1\le2^a\) for every nonnegative integer
\(a\), the large-prime contribution is at most \(2^A\le2^{A_\ell}\).
Multiplying with (6) proves
\(\tau(d)\le B(\ell(d))\). The remaining inequality in (2) follows from the
definition of the monotone envelope.

### Asymptotic budget

For \(\ell\to\infty\),

\[
T_\ell=O(\sqrt\ell)
\]

and the defining inequality for \(A_\ell\) gives

\[
A_\ell
<
\frac{\ell}{\log_2(T_\ell+1)}
=
O\!\left(\frac{\ell}{\log\ell}\right).
\]

Therefore

\[
\log_2 B(\ell)
=
T_\ell\log_2(\ell+1)+A_\ell
=
O(\sqrt\ell\log\ell)
+
O\!\left(\frac{\ell}{\log\ell}\right)
=
O\!\left(\frac{\ell}{\log\ell}\right),
\]

The function \(x/\log x\) is increasing for all sufficiently large \(x\).
Therefore every \(1\le j\le L\) obeys the same
\(O(L/\log L)\) bound after enlarging the constant to cover finitely many
small arguments. Taking the maximum proves (3) for \(Q(L)\).

### Schedule consequence

If an odd prime \(p\) has nonzero signature, then for some
\(d\in\Delta(k)\), either \(p-1\mid d\) or \(p+1\mid d\). For fixed \(d\),
each such prime is one more or one less than a positive divisor of \(d\).
There are at most \(2\tau(d)\) candidates before primality is imposed.
Taking the union over the explicit list and applying (2) proves (4).

If \(E(k)=k^{O(1)}\) and \(L(k)=o(k\log k)\), then
\(\log_2Q(L(k))=o(k)\), without any monotonicity assumption on \(L\).
Choose a fixed \(L_0\) beyond the increasing range of \(x/\log x\). For each
sufficiently large \(k\), if \(L(k)\le L_0\), then \(Q(L(k))\) is bounded. If
\(L_0<L(k)\le k\), (3) and monotonicity give
\(\log_2Q(L(k))=O(k/\log k)=o(k)\). If \(L(k)>k\), then
\[
\frac{L(k)}{\log L(k)}
\le
\frac{L(k)}{\log k}
=o(k).
\]

Equations (3) and (4), with the polynomial factor absorbed into
\(2^{o(k)}\), give \(|H(k)|\le2^{o(k)}\). This proves assertion 4.

Finally put \(h_k=|H(k)\cap S_k|\). Every promised pair in \(S_k\)
intersects this set, by BAR-003, and \(h_k\le|H(k)|\). Consequently

\[
\rho_k
\le
\frac{\binom{|S_k|}{2}
      -\binom{|S_k|-h_k}{2}}
     {\binom{|S_k|}{2}}
\le
\frac{2|H(k)|}{|S_k|-1}.
\]

The exponential lower bound on \(|S_k|\) and the subexponential hit-set bound
give (5). \(\square\)

## REF-005 - refuted large-value coverage claim

The following claim is refuted:

> Once a common exponent exceeds both prime factors plus one, the
> \(p-1/p+1\) magnitude obstruction disappears and combined-promise coverage
> follows.

For

\[
\Delta=\{7\},\qquad N=15=3\cdot5,
\]

the exponent exceeds both \(p+1=4\) and \(q+1=6\), but none of
\(2,4,4,6\) divides \(7\). Both combined signatures are zero, so neither
channel supplies an asymmetry. Numerical magnitude does not replace divisor
structure.

The bounded search must verify that this is the smallest positive exponent
strictly above both \(p+1\) and \(q+1\) for a distinct odd-prime all-zero
pair.

## Limitations

- BAR-004 counts only explicit exponents and their individual divisor sets.
- The theorem supplies no promise recognizer and does not compute signatures
  from \(N\).
- The prime-population result is an implication for explicitly stated sets
  satisfying \(|S_k|\ge2^{\alpha k}\); no unproved prime-distribution transfer
  is used.
- The theorem does not say that \(\Omega(k\log k)\) bits are necessary or
  sufficient for separation in general. Under its other hypotheses, escaping
  this particular subexponential hit-set obstruction requires
  \(L(k)\not=o(k\log k)\).
- No general classical factoring algorithm or lower bound is claimed.

## Falsification plan

1. Exhaust positive exponents through a registered bit-length bound.
2. Compute exact prime factorizations, divisor counts, and the integer budget
   \(Q(\ell)\); stop at the first violation of (2).
3. Enumerate the global prime hit set from every divisor \(r\mid d\) via
   candidates \(r-1,r+1\), and verify (4).
4. Directly scan bounded odd primes to check the divisor-generated hit oracle.
5. Exhaust small exponents and prime pairs to minimize REF-005.
6. Differentially check selected divisor counts, signatures, asymmetries, and
   hit counts in Python, Rust, and C#.
