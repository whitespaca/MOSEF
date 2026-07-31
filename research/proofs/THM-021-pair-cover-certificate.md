# THM-021 - Pair-cover repair certificates

## Status and scope

`THM-021` is an unconditional finite combinatorial theorem. It identifies
bucket refinement by binary coordinates with a set-cover problem on unresolved
pairs, and gives a compact sufficient certificate for an exact minimum.

The theorem does not establish that a proposed list contains every coverage
type realized by an external number-theoretic coordinate family. In the nine
M38--M46 applications, that exhaustiveness is supplied by `EMP-062`. Thus the
abstract theorem is `PROVED`, while the executable reconstruction of the
frozen raw coordinate types remains `EMPIRICAL`.

## DEF-048: repair instance

Let \(X\) be a finite set and let
\(\Pi=\{B_1,\ldots,B_s\}\) be a partition of \(X\). A binary coordinate is a
map \(h:X\to\{0,1\}\). Define the unresolved pair universe

\[
 U(\Pi)=\bigcup_{i=1}^s\{\{x,y\}:x,y\in B_i,\ x\ne y\}.
\]

For a coordinate \(h\), its coverage set is

\[
 C(h)=\{\{x,y\}\in U(\Pi):h(x)\ne h(y)\}.
\]

Coordinates with the same coverage set have the same **coverage type**.
The repair number for a finite coordinate family \(\mathcal H\) is

\[
 \rho(\Pi,\mathcal H)=
 \min\left\{|W|:W\subseteq\mathcal H,\
 \bigcup_{h\in W}C(h)=U(\Pi)\right\},
\]

when such a cover exists.

## Pair-cover equivalence

**Theorem 1.** A subfamily \(W\subseteq\mathcal H\) refines every block of
\(\Pi\) to singletons if and only if its coverage sets cover \(U(\Pi)\).

**Proof.** The refined signature of \(x\in X\) is
\((h(x))_{h\in W}\). Two points \(x,y\) in a common original block remain
together exactly when \(h(x)=h(y)\) for every \(h\in W\), equivalently when
\(\{x,y\}\notin\bigcup_{h\in W}C(h)\). Hence every refined block is a
singleton exactly when every pair in \(U(\Pi)\) is covered. \(\square\)

Binary complementation does not change coverage:
\(C(1-h)=C(h)\). Repeated coordinates of one type cannot improve a cover.
Therefore the minimum depends only on the distinct nonzero coverage types,
not on their multiplicities or complement orientation.

## Private-pair exact-minimum certificate

Let \(T\) be the complete set of distinct nonzero coverage types. Suppose
that distinct types \(t_1,\ldots,t_k\in T\) satisfy:

1. **upper witness:** \(t_1\cup\cdots\cup t_k=U(\Pi)\);
2. **private-pair lower witness:** for every \(i\), there is
   \(u_i\in t_i\) such that \(u_i\notin t\) for every
   \(t\in T\setminus\{t_i\}\).

**Theorem 2.** Under these conditions,
\(\rho(\Pi,\mathcal H)=k\).

**Proof.** The upper witness gives a repair using \(k\) types, so
\(\rho\le k\). Any repair must cover \(u_i\). Completeness of \(T\) and the
private-pair condition imply that only type \(t_i\) can cover \(u_i\).
Consequently every repair contains all \(k\) distinct types
\(t_1,\ldots,t_k\), so \(\rho\ge k\). The bounds agree. \(\square\)

Completeness is essential. If an unlisted type covers a purportedly private
pair, the lower bound is invalid. The source hashes and `EMP-062` dependency
in the registered schema make this premise explicit rather than silently
assuming it.

## Verifier bit complexity

Write

\[
 b=\sum_i|B_i|,\qquad
 q=|U(\Pi)|=\sum_i\binom{|B_i|}{2},\qquad
 t=|T|.
\]

Let \(k\) be the upper-witness size and let \(\lambda\) be the sum of the bit
lengths of the point labels. Store each type as a \(b\)-bit pattern and a
\(q\)-bit coverage mask. Store the selected type indices and private-pair
indices in fixed width. The abstract payload has

\[
 \lambda+t(b+q)
 +k\lceil\log_2t\rceil
 +k\lceil\log_2q\rceil
\]

bits, with a zero-width index when its domain has size one.

Pattern normalization costs \(O(tb)\) bit tests, rebuilding all masks costs
\(O(tq)\), the upper witness costs \(O(kq)\), and checking private-pair
uniqueness costs \(O(kt)\). Thus the abstract certificate verifier runs in

\[
 O(tb+tq+kq+kt+\lambda)
\]

bit operations and uses \(O(t(b+q)+\lambda)\) bits. Binding the abstract
certificate to external JSON sources adds linear hashing and parsing cost in
their total byte length \(S\); it does not change the combinatorial bound.

The registered checker also performs a redundant exhaustive set-cover
confirmation. That defense path uses \(2^t\) subsets and at most
\(qt2^{t-1}\) mask-bit operations. It is not needed by the theorem and is
safe here only because every registered instance has \(t\le5\).

## Nine frozen applications

The source-bound schema
`schemas/m92-pair-cover-certificates-v1.json` records the following exact
instances. Here \(b\) is the number of tracked primes, \(q\) the unresolved
pair count, \(t\) the complete coverage-type count, and \(k\) the certified
minimum.

| \(m\) | baseline cap | repair cap | \(b\) | \(q\) | \(t=k\) | payload bits |
|---:|---:|---:|---:|---:|---:|---:|
| 26 | 70 | 71 | 3 | 3 | 2 | 57 |
| 27 | 72 | 87 | 6 | 15 | 5 | 224 |
| 28 | 88 | 104 | 6 | 15 | 5 | 224 |
| 29 | 102 | 103 | 2 | 1 | 1 | 33 |
| 30 | 122 | 123 | 3 | 3 | 2 | 63 |
| 31 | 143 | 144 | 2 | 1 | 1 | 35 |
| 32 | 166 | 167 | 2 | 1 | 1 | 35 |
| 33 | 194 | 195 | 2 | 1 | 1 | 37 |
| 34 | 200 | 201 | 2 | 1 | 1 | 37 |

Across the portfolio there are 28 tracked primes, 41 pairs, 19 coverage
types, and 19 private pairs. The abstract payload is 745 bits. The core
certificate ledger performs 167 pattern/pair tests, 167 upper-mask bit tests,
and 63 private-type tests, totaling 397. The redundant defense path checks 82
subsets with a 2,429 mask-bit upper ledger.

Every chosen type has a pair covered by no other registered type. The five
types at each of \(m=27,28\) therefore are individually forced. The generic
cardinality lower bound gives only
\(\lceil\log_2 6\rceil=3\) coordinates for those six-prime buckets and cannot
certify the exact value five; this failed shortcut is recorded as NR-060.

The two nonadjacent baselines are preserved: cap 72 at \(m=27\) and cap 88 at
\(m=28\). No application is extrapolated beyond its frozen finite population
or used as evidence for a general classical polynomial-time factoring
algorithm.
