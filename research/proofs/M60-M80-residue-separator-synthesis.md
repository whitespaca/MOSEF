# M60--M80 residue and separator synthesis

Statuses: `PROVED`, `CONDITIONAL`, `OPEN`, `REFUTED`, and `EMPIRICAL` as
marked below.

## M60: the exact residue-union ledger (`BAR-053`, `REF-055`)

For \(M_q=2^q-1\), let
\[
\mathcal D_{m,q}=\{d\mid M_q:d\ge\delta_m\}.
\]
BAR-052 implies that every balanced prime divisor of \(R_q\) lies in
\[
\bigcup_{d\in\mathcal D_{m,q}}\{x:x\equiv1\pmod{2d}\}.
\]
On an integer interval of length \(H\), this union has size at most
\[
\sum_{d\in\mathcal D_{m,q}}\left(\left\lfloor
\frac{H}{2d}\right\rfloor+1\right).
\]
This is an unconditional necessary-support upper bound. At the endpoint its
elementary relaxation is not uniformly smaller than the existing
\(\Theta(2^{m/2}/m)\) population scale, so the naive residue sum does not
close OPEN-005.

## M61: endpoint-compatible small moduli (`BAR-054`, `REF-056`)

For \(a\ge8\), put
\[
k_a=\left\lfloor\frac{2^{a-4}}a\right\rfloor,\quad
q_a=ak_a,\quad m_a=2q_a,\quad d_a=2^a-1.
\]
Then \(d_a\mid2^{q_a}-1\), \(d_a\ge\delta_{m_a}\), and
\(2d_a=\Theta(m_a)\). Thus the necessary residue class
\(1\bmod2d_a\) alone contains \(\Theta(2^{m_a/2}/m_a)\) integers in the
balanced interval. This proves a method barrier for size-plus-residue
counting, not occurrence of primes in that class.

## M62: exact nested-class compression (`BAR-055`)

If \(d\mid e\), then \(1\bmod2e\) is contained in \(1\bmod2d\).
Consequently the residue union is unchanged after deleting every admissible
divisor that is a multiple of a smaller admissible divisor. The remaining
minimal divisors form a divisibility antichain. The M61 witness can retain a
minimal \(\Theta(m)\) modulus, so this exact de-duplication does not remove
the barrier.

## M63: first-period rebucketing (`BAR-056`, `REF-057`)

BAR-051 maps every admissible \(d\) to
\(a(d)=\operatorname{ord}_d(2)\), and \(d\mid2^q-1\) iff \(a(d)\mid q\).
Partitioning the residue union by \(a(d)\) is therefore an exact reindexing,
not a smaller set. Without a distribution theorem inside the buckets,
first-period accounting supplies no further support bound.

## M64--M65: multiple channels (`BAR-057`, `OPEN-006`)

For \(K\) binary channels and \(r\) public positions, signatures have
\(Kr\) coordinates and their weight-\(\le h\) capacity is
\(\sum_{j\le h}\binom{Kr}{j}\). For fixed \(K\), replacing \(r\) by \(Kr\)
changes \(\log r\) by \(O(1)\); at the endpoint threshold this is only an
\(o(m)\) correction and does not change the leading \(1/2\) balance.
For polynomially growing \(K\), the correction can be \(\Theta(m)\).
The current single/fixed-channel barrier therefore does not decide that
case (`OPEN-006`).

## M66: uniform compact support separators (`DEF-046`)

A UCSS family is a deterministic algorithm which, from bit length \(m\)
and a public window index, constructs polynomially many factor-independent
descriptors of polynomial encoding length. Every descriptor is evaluable
modulo an \(m\)-bit input in polynomial bit time with branch-total handling.
The resulting divisibility signatures must be distinct for every two
candidate primes in the window. Offline factor enumeration or advice is
not allowed.

## M67--M70: conditional reduction to factoring

`COND-002`: a UCSS for the balanced window factors every square-free
balanced semiprime. Distinct signatures provide a coordinate hitting
exactly one prime, and its GCD with the input is proper.

`COND-003`: UCSS schedules for all \(O(m)\) factor-bit windows factor every
square-free semiprime by trying every public window.

`BAR-058`: exact primality and perfect-power preprocessing reduces recursive
factoring to composites that are neither prime nor perfect powers; recovered
bases and exponents reconstruct multiplicities without exponential output.

`COND-004`: if window-indexed UCSS also separates a prime divisor from the
complement at every residual non-power composite, recursive GCD splitting,
primality testing, and perfect-power preprocessing give a deterministic
classical polynomial-time factoring algorithm.

This is a conditional theorem. The UCSS existence premise is not proved.

## M71--M72: cost and uniformity (`BAR-059`, `REF-058`)

The reduction is polynomial only if descriptor construction, descriptor
length, modular evaluation, failed-inversion branches, GCD count, recursion,
and output multiplicities are all polynomial in \(m\). A compact exponent
description is insufficient when evaluation is superpolynomial.

Finite signature tables, even when exhaustive at each recorded length, do
not prove UCSS: they are nonuniform unless one algorithm constructs every
future schedule within the stated bounds. Thus extrapolating M31--M46
tables to a uniform theorem is refuted.

## M73--M75: unconditional restricted algorithm (`DEF-047`, `THM-020`,
`BAR-060`)

Let \(L_m=\{2,3,\ldots,m+12\}\), and let \(\mathcal R\) be the class of
square-free \(m\)-bit semiprimes \(pq\) for which this public Phi4 level list
has distinct signatures at \(p\) and \(q\). On \(\mathcal R\), scanning the
list and computing the
compact residue and GCD returns a proper factor in polynomial time. This is
`THM-020`, an unconditional restricted-input algorithm.

Every coordinate is branch-total: GCD \(1\) or \(N\) merely continues, a
failed inversion exposes a nonunit through its denominator GCD, and a
proper GCD terminates. The algorithm receives neither factor nor signature.

## M76--M77: present barrier and dependency closure (`REF-059`, `BAR-061`)

BAR-042--BAR-057 show that the current single/fixed-channel proof machinery
does not establish UCSS at the \(c=1/2\) endpoint. This does not prove that
UCSS or polynomial-time factoring is impossible.

The dependency audit has three disjoint leaves:

1. `THM-020` is unconditional but restricted to \(\mathcal R\);
2. `COND-004` is general but assumes UCSS;
3. OPEN-002, OPEN-003, OPEN-005, and OPEN-006 remain open.

No empirical claim feeds a universal theorem.

## M78--M79: reproducibility and adversarial review (`EMP-058`, `BAR-062`)

EXP-0058 independently reconstructs exact endpoint residue ledgers and
finite restricted-factor outcomes. The adversarial review checks nesting
direction, necessary-versus-sufficient residue conditions, public-before-
input construction, branch totality, exponent evaluation cost, recursive
cost, finite-versus-asymptotic scope, and bilingual claim synchronization.
All scoped checks pass.

## M80: final scoped conclusion (`BAR-063`)

The program has not proved a classical polynomial-time algorithm for
factoring arbitrary integers. It has proved an unconditional algorithm for
the explicitly defined restricted class \(\mathcal R\), a complete
conditional reduction from UCSS to general factoring, and a chain of exact
barriers showing why the present compact-gap single/fixed-channel route does
not discharge UCSS. This is the final M80 status and the required pause
point.
