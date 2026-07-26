# BAR-008 - General factor-scale divisor scarcity at the exact boundary

## Status and scope

Status: `PROVED`.

This result concerns common factorization-independent polynomial-size lists of
explicit positive exponents whose ordinary binary lengths are
\(O(k\log k)\). Through BAR-005 it also covers fixed-base DEF-010
multiplication-only schedules with \(O(k\log k)\) total charged nodes. It
does not cover longer exponents, exponentially many exponents, adaptive
factor-dependent schedules, richer compressed representations, other
algebraic channels, or general factoring.

## DEF-013

For input length \(k\ge1\), put
\[
b_k=\lceil\log_2(k+1)\rceil,\qquad
Y_k=\max\{2,\lfloor k/b_k^2\rfloor\}.
\]
For an exponent
\[
d=\prod_p p^{a_p},
\]
a target cap \(X\ge3\), and an integer threshold \(Y\ge2\), define
\[
S_Y(d)=\prod_{p\le Y}(a_p+1),\qquad
A_Y(d)=\sum_{p>Y}a_p,
\]
\[
J_Y(X)=\max\{j\ge0:(Y+1)^j\le X+1\},
\]
and define the factor-scale divisor budget
\[
F_Y(d,X)=
S_Y(d)\sum_{j=0}^{\min\{A_Y(d),J_Y(X)\}}
\binom{A_Y(d)}j.
\]

## BAR-008 statement

Fix \(C,\beta>0\). Let \(\Delta(k)\) be a common
factorization-independent schedule with \(k^{O(1)}\) explicit exponents, each
of bit length at most \(Ck\log_2k\) for sufficiently large \(k\). Then
\[
\#\{e\mid d:e\le2^{\beta k}+1\}
\le
2^{O(k\log\log k/\log k)}
=2^{o(k)}
\]
uniformly for every \(d\in\Delta(k)\). Consequently the combined
\(p-1/p+1\) global hit set on odd primes \(q\le2^{\beta k}\) has size
\(2^{o(k)}\).

On every stipulated common-input-length odd-prime population \(S_k\) with
\(|S_k|\ge2^{\alpha k}\), fixed \(\alpha>0\), and members at most
\(2^{\beta k}\), the schedule's promised-pair fraction is at most
\[
2^{-\alpha k+o(k)}
\]
and tends to zero. The same holds for fixed-base DEF-010 schedules with
\(O(k\log k)\) total charged multiplication nodes.

The exponent \(d=1\), if present, has one divisor and is absorbed into the
polynomial schedule factor; the proof below treats \(d\ge2\).

## Proof

### 1. Exact split bound

Fix \(d=\prod_p p^{a_p}\), \(X\ge3\), and \(Y\ge2\). A divisor
\[
e=\prod_p p^{f_p},\qquad0\le f_p\le a_p,
\]
has at most \(S_Y(d)\) possible small-prime exponent vectors.

Put \(j=\sum_{p>Y}f_p\). Since every large prime is at least \(Y+1\),
\[
(Y+1)^j\le e\le X+1,
\]
so \(j\le J_Y(X)\). Label the \(A_Y(d)\) available large-prime
occurrences. Every exponent vector with total multiplicity \(j\) has a
canonical representation by selecting the first \(f_p\) labeled occurrences
of each prime. It therefore injects into the \(j\)-subsets of these
\(A_Y(d)\) labels. Hence the number of large-prime exponent vectors is at
most
\[
\sum_{j=0}^{\min\{A_Y(d),J_Y(X)\}}\binom{A_Y(d)}j.
\]
Multiplying the independent small and large overcounts proves the exact bound
\[
\#\{e\mid d:e\le X+1\}\le F_Y(d,X).
\tag{1}
\]

### 2. Small-prime choices are subexponential

Take \(Y=Y_k\), let \(L=\ell(d)\le Ck\log_2k\), and set
\(X=2^{\beta k}\). Since \(2^{a_p}\le d<2^L\), every
\(a_p+1\le L+1\). There are at most \(Y_k\) primes no larger than \(Y_k\),
so
\[
\log_2S_{Y_k}(d)
\le Y_k\log_2(L+1)
=O(k/\log k)
=o(k).
\tag{2}
\]
No prime-counting theorem is needed.

### 3. Large-prime choices are subexponential

Writing \(A=A_{Y_k}(d)\), we have
\[
(Y_k+1)^A\le d<2^L,
\]
and hence
\[
A\le \frac{L}{\log_2(Y_k+1)}=O(k).
\tag{3}
\]
Likewise,
\[
J=J_{Y_k}(2^{\beta k})
\le\frac{\beta k+1}{\log_2(Y_k+1)}
=O(k/\log k).
\tag{4}
\]

If \(A<2J\), the binomial sum is at most
\[
2^A\le2^{2J}=2^{O(k/\log k)}.
\]
If \(A\ge2J\), then
\[
\sum_{j=0}^J\binom Aj
\le(J+1)\binom AJ
\le(J+1)(eA/J)^J.
\]
The last inequality is elementary:
\(\binom AJ\le A^J/J!\), while
\[
\log J!=\sum_{i=1}^J\log i
\ge\int_1^J\log x\,dx
=J\log J-J+1,
\]
so \(J!\ge(J/e)^J\).
For \(A\le C'k\), the function \(t\mapsto t\log(eC'k/t)\) is increasing on
the relevant interval. Evaluating it at \(O(k/\log k)\) gives
\[
\log_2\sum_{j=0}^J\binom Aj
=O(k\log\log k/\log k)
=o(k).
\tag{5}
\]
The cases \(A=0\) or \(J=0\) are immediate.

Combining (1), (2), and (5) proves the uniform factor-scale divisor bound.

### 4. Hit-set and density transfer

If an odd prime \(q\le2^{\beta k}\) has nonzero combined signature, then
\(q-1\mid d\) or \(q+1\mid d\) for some scheduled exponent \(d\).
Each factor-scale divisor supplies at most two candidates. A polynomial
schedule therefore has
\[
|H(k)|
\le2\sum_{d\in\Delta(k)}
\#\{e\mid d:e\le2^{\beta k}+1\}
=2^{o(k)}.
\]
BAR-003 now gives
\[
\rho_k\le\frac{2|H(k)|}{|S_k|-1}
\le2^{-\alpha k+o(k)}\longrightarrow0.
\]

For a fixed number of DEF-010 base programs with total charged node count
\(T(k)=O(k\log k)\), BAR-005 gives a polynomial number of exposed exponents,
each with bit length at most \(T(k)+1=O(k\log k)\). The same conclusion
follows.

## Falsification attempts

EXP-0012 exhaustively factors bounded exponents, enumerates their divisors,
and tests the exact split bound at multiple target caps and thresholds. It
separately records prime powers, squareful smooth exponents, noninitial
square-free supports, and mixed noninitial squareful supports. Selected
divisor, signature, asymmetry, and hit-count vectors are compared across
Python, Rust, and C#.

## Limitations

- The population is stipulated; existence and recognition are not asserted.
- The target factors have a fixed linear bit cap \(2^{\beta k}\).
- The schedule is explicit and polynomial-size, or lies inside the stated
  fixed-base DEF-010 transfer.
- This is not a lower bound for general factoring or for other group channels.
