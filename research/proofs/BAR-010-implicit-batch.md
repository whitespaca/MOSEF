# BAR-010 - Leaf-materialized product trees do not create implicit coverage

## Status and scope

Status: `PROVED`.

This result concerns a selector-described **standard product tree that
materializes every selected leaf**. It proves exact root-GCD semantics,
one-way preservation of successful individual leaves, possible masking by
aggregation, and the linear leaf/tree cost forced by this model.

It does not prove a lower bound for a specialized arithmetic circuit that
computes the same formal product without materializing its leaves. It does
not cover adaptive factor-dependent selectors, unrelated multi-base
expressions, other algebraic channels, or general classical factoring.

The initial computation of \(\gcd(g,N)\) is a separate algorithmic precheck.
A proper factor returned there is not silently attributed to the batch.

## DEF-015

Fix \(N\ge2\). The base precheck returns a proper \(\gcd(g,N)\), rejects
\(\gcd(g,N)=N\), or enters the unit branch with \(g\in(\mathbb Z/N\mathbb
Z)^\times\).

A DEF-015 batch consists of a finite strictly increasing sequence of
positive exponents
\[
\Delta=(d_1,\ldots,d_n).
\]
A selector may describe \(\Delta\) compactly, but evaluation enumerates every
selected exponent and materializes every leaf
\[
r_i=g^{d_i}-1\pmod N.
\]
The standard binary product tree pairs adjacent nodes, carries an unpaired
node unchanged, and continues until it obtains
\[
R=\prod_{i=1}^n r_i\pmod N.
\]

The charged record includes selector enumeration, every exponent and its
ordinary binary length, every modular-power leaf evaluation and stored leaf,
every internal modular multiplication and stored subtree product, every
requested subtree or root output, every GCD, and factor extraction. A direct
nonunit-base exit remains separate.

## BAR-010 statement

Let
\[
N=\prod_{p^e\parallel N}p^e.
\]
Use the conventional extended valuation \(\nu_p(0)=+\infty\).
For every DEF-015 batch,
\[
\gcd(R,N)
=
\prod_{p^e\parallel N}
p^{\min\{e,\sum_{i=1}^n\nu_p(g^{d_i}-1)\}}.
\tag{1}
\]
In particular:

1. if the root GCD is proper, at least one leaf GCD
   \(\gcd(g^{d_i}-1,N)\) is proper;
2. the converse is false: aggregation can turn individual proper separators
   into the full collision \(N\);
3. an \(n\)-leaf standard binary product tree has exactly \(n-1\) internal
   modular multiplications, in addition to its \(n\) charged leaf
   evaluations and materializations.

Consequently, any DEF-015 family with polynomial total charged work has only
polynomially many materialized exponents. If, for each input length \(k\),
the complete materialized leaf list is also common and
factorization-independent and its exponents have binary lengths
\(O(k\log k)\), then BAR-008 applies: at every fixed target factor cap
\(2^{\beta k}\), its combined \(p-1/p+1\) hit set has size \(2^{o(k)}\),
and on every stipulated population of size at least \(2^{\alpha k}\) its
promised-pair fraction is at most
\[
2^{-\alpha k+o(k)}.
\]
Root aggregation can reduce the number of GCD calls, but it cannot add a
proper-factor success absent from all individual leaves and can mask
existing successes.

## Proof

### 1. Exact prime-power valuation

Choose ordinary integer representatives
\[
a_i=g^{d_i}-1
\]
and let \(A=\prod_i a_i\). The computed root satisfies \(R\equiv A\pmod
N\), so
\[
\gcd(R,N)=\gcd(A,N).
\]
For each exact prime power \(p^e\parallel N\), the exponent of \(p\) in this
GCD is
\[
\min\{e,\nu_p(A)\}
=
\min\{e,\sum_i\nu_p(a_i)\}.
\]
Multiplying these relatively prime prime-power contributions proves (1).

### 2. A proper root success already occurs at a leaf

Suppose \(1<\gcd(R,N)<N\). Choose a prime \(p\mid\gcd(R,N)\). Since \(p\)
divides the product \(\prod_i a_i\), it divides some \(a_j\). Hence
\(\gcd(a_j,N)>1\).

That leaf GCD cannot equal \(N\): if \(N\mid a_j\), then \(N\mid A\), which
would make the root GCD equal \(N\). Therefore
\[
1<\gcd(a_j,N)<N.
\]
This proves the one-way success implication.

The converse fails. For
\[
N=21,\qquad g=2,\qquad\Delta=(2,3),
\]
the leaves are \(2^2-1=3\) and \(2^3-1=7\). Their GCDs with \(21\) are the
proper factors \(3\) and \(7\), but their product is divisible by \(21\), so
the root GCD is the full collision \(21\).

### 3. Exact tree cost

Start with \(n\) connected components, one per materialized leaf. Every
binary multiplication combines exactly two components and decreases their
number by one. A single root therefore requires exactly \(n-1\)
multiplications. The usual adjacent-pair tree, including odd-node carries,
achieves this count, so it is exact.

The compactness of the selector does not alter the charged DEF-015
evaluation: it still enumerates, evaluates, and stores \(n\) distinct
leaves. Thus the charged work is at least linear in \(n\). Polynomial total
work forces \(n=k^{O(1)}\).

### 4. Factor-scale transfer

Assume in addition that, for each input length \(k\), the complete
materialized leaf list is common and factorization-independent and every
materialized exponent has ordinary binary length \(O(k\log k)\). It is then
a polynomial-size explicit schedule satisfying BAR-008. That theorem gives
the stated \(2^{o(k)}\) factor-scale hit-set bound, and BAR-003 gives the
stipulated-population upper bound.

The root implication above shows that aggregation cannot enlarge the
individual-leaf proper-success set. The \(N=21\) witness shows that it can
strictly shrink what a single root GCD reveals. This completes the scoped
claim. \(\square\)

## Falsification attempts

EXP-0014 enumerates every nonempty subset of a bounded exponent interval
over bounded composite moduli and unit bases. It independently reconstructs
the root GCD from capped prime-power valuation sums, checks that every proper
root has a proper leaf, records masked leaf separators, verifies odd-size
trees, and checks the exact \(n-1\) count over a larger leaf-count interval.
Selected batches are compared across Python, Rust, and C#.

The search deliberately includes prime powers, zero leaves, full
collisions, multiple proper leaf factors, and the \(N=21\) union-collision
witness. Nonunit bases are counted only as separate precheck branches.

## Limitations

- Leaf materialization and its output record are definitional and charged.
- The result does not establish a general arithmetic-circuit lower bound.
- The BAR-008 transfer separately assumes \(O(k\log k)\)-bit exponents, a
  fixed factor scale, a common factorization-independent schedule, and a
  stipulated population.
- Reducing GCD calls is not the same as reducing leaf construction cost.
- No population existence, recognition, natural-density, novelty, or
  general factoring conclusion is asserted.

## Independent review

Independent adversarial review reproduced the focused tests, EXP-0014, and
all selected Python/Rust/C# differential checks, then audited singleton,
odd-tree, zero-leaf, and prime-power cases. The first review rejected an
equality wording for the population upper bound and an unstated common-list
hypothesis. After repair, it confirmed that the BAR-008 transfer separately
requires a common factorization-independent leaf list at each input length
and returned PASS. Independent source-scope review found no external citation
requirement and confirmed that no non-materializing-circuit or general
factoring lower bound is claimed.
