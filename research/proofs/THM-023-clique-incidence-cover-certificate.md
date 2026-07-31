# THM-023 - Complete-graph incidence repair certificate

## Status and scope

`THM-023` is an unconditional finite combinatorial theorem over the complete
coverage-type family of `DEF-048`. It identifies a structural case in which
the repair problem is exactly a complete-graph vertex-cover problem. The two
M94 applications depend on `EMP-064` for exhaustive reconstruction of their
finite type families.

The theorem does not reconstruct the number-theoretic types, recognize a
factor promise, extend the frozen range beyond length 34, or give a general
classical polynomial-time factoring algorithm.

## DEF-050: coverer graph and clique incidence

Let \(U\) be a finite unresolved universe and let
\(T=\{T_0,\ldots,T_{t-1}\}\) be the complete set of distinct nonzero coverage
types. For \(u\in U\), define its **coverer set**

\[
 D(u)=\{T_i\in T:u\in T_i\}.
\]

When every \(D(u)\) has size two, the coverer sets are the edges of a
multigraph \(G_D\) on vertex set \(T\). We say that the instance has
**complete-graph incidence** when every unordered pair of distinct types
occurs as some \(D(u)\). Equivalently, the underlying simple graph of \(G_D\)
is \(K_t\). Repeated universe elements with the same coverer pair are allowed
by the definition.

In the two M94 applications, the stronger property holds: the map
\(u\mapsto D(u)\) is a bijection from \(U\) to
\(\binom{T}{2}\).

## Coverer-graph equivalence

**Lemma 1.** If every universe element has exactly two coverers, a type
subset \(W\subseteq T\) covers \(U\) if and only if \(W\) is a vertex cover
of \(G_D\).

**Proof.** An element \(u\) is covered by \(W\) exactly when
\(W\cap D(u)\ne\varnothing\). Since \(D(u)\) is one edge of \(G_D\), this is
exactly the condition that \(W\) meets that edge. Requiring it for every
\(u\in U\) is the vertex-cover condition. \(\square\)

## Complete-graph exact minimum

**Theorem 2.** Let \(t\ge2\). If a finite repair instance has complete-graph
incidence on its complete type family \(T\), its exact repair number is
\(t-1\).

**Proof.** Any \(t-1\) types cover the universe: only one type is omitted, so
no two-element coverer set can be wholly omitted. Conversely, a selection of
at most \(t-2\) types omits two distinct types \(T_i,T_j\). Complete-graph
incidence supplies an element \(u\) with
\(D(u)=\{T_i,T_j\}\), and neither of its only coverers is selected. Hence
\(u\) remains uncovered. The upper and lower bounds agree at \(t-1\).
\(\square\)

Unlike the general subset-obstruction witness of `THM-022`, the complete-graph
criterion does not store one obstruction entry for every undersized subset.
The already stored coverage masks determine all coverer sets, and the theorem
also makes an upper witness implicit: omit any fixed type.

## Verifier and payload cost

Retain the notation

\[
 b=\sum_i|B_i|,\qquad q=|U|,\qquad t=|T|,
\]

and let \(\lambda\) be the bit length of all point labels. Store the \(t\)
normalized \(b\)-bit patterns and their \(q\)-bit coverage masks. No upper
type indices or lower-witness indices are required. The abstract payload is

\[
 \lambda+t(b+q)
\]

bits.

Pattern normalization and mask reconstruction take
\(O(tb+tq)\) bit operations. Scanning every mask column takes \(tq\) bit
tests, and checking the resulting unordered type pairs against a
\(\binom t2\)-slot table takes
\(O(q\log t)\) bit operations. Thus the complete verifier uses

\[
 O(tb+2tq+q\log t+\lambda)
\]

bit operations and \(O(t(b+q)+t^2+\lambda)\) bits of certificate plus
working storage. The \(t^2\) seen-pair table may be replaced by sorting pair
indices without changing polynomiality.

The registered narrow ledger counts mask reconstruction, incidence-mask
tests, and one pair-slot test per universe element. It deliberately omits
JSON syntax, redundant coverer traces, source paths and hashes, and source
bytes. Binding to an external source of \(S\) bytes adds \(O(S)\) hashing and
parsing work.

## Two frozen bijective applications

The M94 schema records the following incidence bijections.

| input length | tracked points \(b\) | pairs \(q\) | types \(t\) | graph | exact repair |
|---:|---:|---:|---:|:---|---:|
| 16 | 3 | 3 | 3 | \(K_3\) | 2 |
| 24 | 4 | 6 | 4 | \(K_4\) | 3 |

At length 16, the masks \(3,5,6\) give

\[
 \{191,227\}\leftrightarrow\{T_0,T_1\},\quad
 \{191,233\}\leftrightarrow\{T_0,T_2\},\quad
 \{227,233\}\leftrightarrow\{T_1,T_2\}.
\]

At length 24, the masks \(07,19,2a,34\) give the six lexicographically
ordered correspondences

\[
\begin{aligned}
 \{3049,3643\}&\leftrightarrow\{T_0,T_1\},&
 \{3049,3863\}&\leftrightarrow\{T_0,T_2\},\\
 \{3049,4057\}&\leftrightarrow\{T_0,T_3\},&
 \{3643,3863\}&\leftrightarrow\{T_1,T_2\},\\
 \{3643,4057\}&\leftrightarrow\{T_1,T_3\},&
 \{3863,4057\}&\leftrightarrow\{T_2,T_3\}.
\end{aligned}
\]

The compact structural payloads are 42 and 88 bits, compared with the M93
cardinality/subset-obstruction payloads 50 and 136. This saves 8 and 48 bits,
56 bits total.

The conservative bit-test ledger is not strictly smaller. At length 16 it
uses 21 tests rather than the incumbent cardinality certificate's 16; at
length 24 both ledgers use 54. The complete-graph criterion therefore
compresses these two payloads but does not strictly dominate the incumbent
verifiers in work.
