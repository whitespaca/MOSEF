# THM-024 - Looped coverer-graph reduction and boundary

## Status and scope

`THM-024` is an unconditional finite combinatorial theorem for complete
coverage-type families whose nonempty coverer sets have size at most two. It
extends `THM-023` by treating singleton coverers as graph loops and isolates
the exact residual vertex-cover problem after all looped types are forced.

The M95 application depends on `EMP-062` and `EMP-064` for exhaustive
reconstruction of the nineteen frozen type families. The theorem does not
establish rank at most two for another selector, recognize a factor promise,
or give a general classical polynomial-time factoring algorithm.

## DEF-051: looped coverer graph

Let \(U\) be a finite unresolved universe and let
\(T=\{T_0,\ldots,T_{t-1}\}\) be the complete set of distinct nonzero
coverage types, with \(\bigcup T=U\). As in `DEF-050`, define

\[
 D(u)=\{T_i\in T:u\in T_i\}.
\]

Assume \(1\le |D(u)|\le2\) for every \(u\in U\). The **looped coverer
multigraph** \(G_D\) has vertex set \(T\). A singleton
\(D(u)=\{T_i\}\) is a loop at \(T_i\), and a two-element set
\(D(u)=\{T_i,T_j\}\) is an ordinary edge. Repeated slots are allowed.
Let

\[
 F=\{T_i\in T:\text{\(G_D\) has a loop at \(T_i\)}\}
\]

be the forced set.

## Graph equivalence and forced-loop decomposition

**Theorem 1.** A subset \(W\subseteq T\) covers \(U\) if and only if it is a
vertex cover of the looped multigraph \(G_D\), where meeting a loop requires
selecting its unique endpoint.

**Proof.** An element \(u\) is covered exactly when
\(W\cap D(u)\ne\varnothing\). For a singleton this forces its sole type; for
a two-element set it is the ordinary edge-cover condition. Requiring the
condition for every universe element is exactly looped vertex cover.
\(\square\)

Let \(\tau(H)\) denote the minimum vertex-cover size of a loopless graph
\(H\), with \(\tau(\varnothing)=0\).

**Theorem 2.** The exact repair number is

\[
 \rho(T,U)=|F|+\tau\!\left(G_D[T\setminus F]\right),
\]

where the graph inside \(\tau\) retains only ordinary edges whose endpoints
both lie outside \(F\).

**Proof.** Every loop forces its endpoint, so every cover contains \(F\).
After selecting \(F\), every loop and every ordinary edge incident with
\(F\) is already met. The only remaining constraints are ordinary edges
with both endpoints in \(T\setminus F\), and meeting them is precisely a
vertex cover of the indicated induced graph. The two independent costs add.
\(\square\)

Two special cases give the complete M95 portfolio:

1. If \(F=T\), then \(\rho=t\).
2. If \(F=\varnothing\) and the underlying simple graph is \(K_t\), then
   \(\rho=t-1\), recovering `THM-023`.

## Rank-two universality boundary

**Theorem 3.** Every finite simple graph \(H=(V,E)\) with no isolated
vertices and no connected component isomorphic to \(K_2\) is the coverer
graph of a finite coverage system in complete normal form (nonempty,
pairwise-distinct types).

**Proof.** Let the universe contain one element \(u_e\) for each edge
\(e\in E\). For each vertex \(v\in V\), define a type

\[
 T_v=\{u_e:e\text{ is incident with }v\}.
\]

No type is empty because \(H\) has no isolated vertices. The types are
pairwise distinct: if \(T_v=T_w\) for distinct vertices, choose an edge
incident with \(v\). Equality forces that edge to be \(\{v,w\}\), and any
second edge incident with either endpoint would contradict equality in a
simple graph. Hence \(\{v,w\}\) would be a \(K_2\) component, which was
excluded. For an edge \(e=\{v,w\}\), the only types containing \(u_e\) are
\(T_v\) and \(T_w\). Thus \(D(u_e)=\{T_v,T_w\}\), and the coverer graph is
\(H\). By Theorem 1, the repair number is \(\tau(H)\). \(\square\)

Consequently, the rank-two premise alone does not provide a closed-form exact
minimum. In particular, the star \(K_{1,3}\) and path \(P_4\) both have four
types, three universe elements, and three degree-two coverer columns, but
their exact cover numbers are one and two. This is the registered
counterexample `REF-064`.

This statement does not invoke an unproved complexity separation. It only
shows that a graph class or a separate lower certificate remains necessary
after the rank-two reduction.

## Exact portfolio templates

M95 reconstructs three exact slot templates. Every listed slot occurs once.

- **Loop-only:** the \(t\) singleton slots and no ordinary edge.
- **Looped clique:** the \(t\) singleton slots and all
  \(\binom t2\) ordinary pairs.
- **Loopless clique:** no singleton slot and all \(\binom t2\) ordinary
  pairs.

The first two templates have \(F=T\) and exact repair number \(t\). The third
has \(F=\varnothing\) and exact repair number \(t-1\). No stored upper or
lower witness indices are needed: select all types in the looped templates,
or omit a fixed last type in the loopless clique.

## Verifier and payload cost

Retain the notation

\[
 b=\sum_i|B_i|,\qquad q=|U|,\qquad t=|T|,
\]

and let \(\lambda\) be the bit length of all tracked point labels. Store the
\(t\) normalized \(b\)-bit patterns and their \(q\)-bit masks. The template
kind is reconstructed from the masks. The abstract payload is therefore

\[
 \lambda+t(b+q)
\]

bits.

Pattern normalization and mask reconstruction take \(O(tb+tq)\) bit
operations. Reconstructing every coverer column costs another \(tq\) bit
tests. Comparing the observed singleton/pair slots with a canonical template
costs \(O(q\log t+t^2)\) bit operations using indexed slots. Hence a
conservative full bound is

\[
 O(tb+2tq+q\log t+t^2+\lambda)
\]

bit operations and \(O(t(b+q)+t^2+\lambda)\) bits of certificate plus
working storage. Binding an external source of \(S\) bytes adds \(O(S)\)
hashing and parsing work.

The narrow registered ledger counts \(tq\) pattern-pair tests, \(tq\)
incidence-mask tests, and \(q\) canonical slot comparisons. It excludes JSON
syntax, redundant coverer traces, paths, hashes, and source bytes.

## Frozen portfolio application

The M95 checker reconstructs all nineteen M92/M93 instances.

| template | instances | exact rule |
|:---|---:|:---|
| loop-only | 12 | \(t\) forced types |
| looped clique | 5 | \(t\) forced types |
| loopless clique | 2 | \(t-1\) |

Across 55 tracked points and 64 universe columns, there are exactly 30
singleton columns and 34 two-coverer columns, for 98 positive incidences.
There are no empty columns and no coverer sets of size at least three.

The graph-template payload totals 1,063 bits instead of the incumbent 1,228,
saving 165. The narrow verifier ledger totals 520 rather than 542 tests,
saving 22 in aggregate. This is not strict per-instance dominance: the
length-16 clique still costs five more registered tests, ten one-type cases
save no payload, and several rows tie in verifier work.
