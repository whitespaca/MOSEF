# THM-028 - Iterative-compression discovery of an odd-cycle transversal

## Status and scope

`THM-028` is an unconditional fixed-parameter algorithmic theorem for an
explicit finite graph and a public integer cap. It reconstructs the
iterative-compression OCT method inspected in
`research/literature/M99-odd-cycle-transversal-iterative-compression.md`,
proves the local implementation, and composes its output with `THM-027`.

The theorem removes the need to supply the transversal itself at the
explicit-graph layer. It does not construct the factor-dependent complete
type list or coverer graph from an integer, prove a logarithmic cap for
graphs arising from arbitrary integers, recognize a factor promise, solve
unrestricted vertex cover in polynomial time, or give a general classical
polynomial-time factoring algorithm.

## DEF-055: capped OCT discovery

Let \(G=(V,E)\) be an explicit undirected loopless multigraph with
\(t=|V|\) and \(q=|E|\). A set \(X\subseteq V\) is an **odd-cycle
transversal** (OCT) when \(G-X\) is bipartite. Given a public cap \(k\), the
capped discovery
contract is:

- return an OCT of minimum cardinality if \(\tau_{\rm OCT}(G)\leq k\);
- otherwise return `rejected_above_cap`.

Parallel edge occurrences retain their indices. Residual inputs are
loopless because the forced loop set of `THM-024` is removed before this
algorithm. A deterministic witness is returned, but no claim is made that
every maximum-flow tie is resolved to the globally lexicographically first
optimum.

### Compression subproblem

Suppose \(S\) is a known OCT with \(|S|\leq k+1\). Enumerate every ordered
partition

\[
 S=L\mathbin{\dot\cup}R\mathbin{\dot\cup}D,
\]

where \(D\) is proposed for deletion and \(L,R\) are proposed color
classes. Reject a partition when \(|D|>k\), when \(G[L]\) has an edge, or
when \(G[R]\) has an edge.

Put \(B=G-S\) and fix one bipartition \(A\mathbin{\dot\cup}C=V(B)\). Define

\[
\begin{aligned}
 U&=(N_B(L)\cap A)\cup(N_B(R)\cap C),\\
 W&=(N_B(R)\cap A)\cup(N_B(L)\cap C).
\end{aligned}
\]

Find a minimum \(U\)-\(W\) vertex separator \(Y\) in \(B\), allowing
vertices of \(U\cup W\) themselves to be deleted. Retain the partition only
if \(|D|+|Y|\leq k\), and form \(D\cup Y\). Return a smallest retained
candidate.

### Iterative compression

Fix an order \(v_1,\ldots,v_t\). Begin with the empty OCT on the empty
prefix. At prefix \(i\), the previous OCT together with \(v_i\) is an OCT
of \(G[\{v_1,\ldots,v_i\}]\) of size at most \(k+1\). Apply the compression
subproblem. Reject when no candidate of size at most \(k\) exists;
otherwise continue with the minimum candidate.

## Separator lemma

**Lemma.** For a fixed accepted partition
\(S=L\mathbin{\dot\cup}R\mathbin{\dot\cup}D\), a set
\(Y\subseteq V(B)\) makes \(G-(D\cup Y)\) bipartite with \(L\) and \(R\)
on opposite color classes if and only if \(Y\) separates \(U\) from \(W\)
in \(B\).

**Proof.** Each connected component of the bipartite graph \(B-Y\) has two
possible orientations relative to the fixed classes \(A,C\). An attachment
from \(L\) forbids the orientation in which its neighbor has the color of
\(L\); an attachment from \(R\) gives the analogous opposite constraint.
Under the fixed \(A,C\) orientation, precisely the vertices in \(U\)
represent one orientation requirement and those in \(W\) the other.

If a component contains both a vertex of \(U\) and a vertex of \(W\), its
two requirements demand opposite orientations, so no extension of the
coloring of \(L\cup R\) exists. Conversely, if no component contains both,
orient a component containing only \(U\) to satisfy its \(U\) attachments,
orient one containing only \(W\) the other way, and orient an unconstrained
component arbitrarily. The tests on \(G[L]\) and \(G[R]\) ensure that edges
inside \(S-D\) are proper. Hence the resulting coloring is proper exactly
when \(Y\) separates \(U\) and \(W\). \(\square\)

## Exact separator construction

Split every \(v\in V(B)\) into \(v_{\rm in}\) and \(v_{\rm out}\) with a
unit-capacity arc \(v_{\rm in}\to v_{\rm out}\). Replace every undirected
edge by both directed arcs of capacity \(k+1\) between the corresponding
out- and in-nodes. Add a super-source with capacity-\(k+1\) arcs to
\(u_{\rm in}\), \(u\in U\), and capacity-\(k+1\) arcs from
\(w_{\rm out}\), \(w\in W\), to a super-sink.

Integral maximum flow and the residual reachable cut give a minimum
vertex separator whenever its size is at most the remaining budget.
Because every non-vertex arc has capacity \(k+1\), a cut of value at most
\(k\) uses only split arcs. This includes the case \(U\cap W\ne\varnothing\):
the common terminal's split arc deletes that terminal. If an augmenting
flow reaches budget \(+1\), no separator within budget exists and the
search may stop.

## Exact discovery theorem

**Theorem.** `DEF-055` returns `rejected_above_cap` exactly when
\(\tau_{\rm OCT}(G)>k\). Otherwise it returns an OCT \(X\) satisfying
\(|X|=\tau_{\rm OCT}(G)\).

**Proof.** First consider one compression call. Every retained candidate is
an OCT by the separator lemma. Conversely, let \(Z\) be any OCT of size at
most \(k\). Choose a proper two-coloring of \(G-Z\), set
\(D=Z\cap S\), and place each vertex of \(S\setminus Z\) into \(L\) or
\(R\) according to that coloring. This partition is enumerated and passes
the internal-edge tests. The set \(Z\setminus S\) separates its associated
\(U,W\), again by the lemma. The minimum separator for that partition is
therefore no larger, so the compression call returns a candidate of size at
most \(|Z|\). Since every returned candidate is an OCT, minimizing over all
partitions yields the exact minimum among OCTs of size at most \(k\).

Induct on the vertex prefixes. The previous prefix's minimum OCT, together
with the new vertex, is an OCT of size at most \(k+1\), so it is valid
compression input. The compression result is the exact minimum for the new
prefix when that minimum is at most \(k\). If a prefix has no such OCT, no
later graph can have one because OCT number is monotone under taking
induced supergraphs. Thus early rejection is sound. At the final prefix the
returned cardinality is \(\tau_{\rm OCT}(G)\). \(\square\)

## Complexity and payload

There are at most \(t\) compression calls and at most \(3^{k+1}\)
partitions per call. A budget-truncated integral flow makes at most
\(k+1\) augmentations, each with a breadth-first residual search in
\(O(t+q)\) indexed operations. Graph construction, partition checks, and
candidate validation fit within the same conservative envelope. Therefore
the local implementation uses

\[
 O\!\left(3^{k+1}(k+1)t(t+q)\right)
\]

indexed operations and polynomial working storage. Charging
\(\ell_t+\ell_q\) bits per stored or compared index gives

\[
 O\!\left(
 tb+2tq+t+q+\lambda+
 3^{k+1}(k+1)t(t+q)(\ell_t+\ell_q)
 \right)
\]

bit operations, plus \(O(S)\) parsing and hashing for \(S\) source-bound
bytes. Here \(b,q,t,\lambda,\ell_t,\ell_q\) retain the meanings used in
`THM-027`. An output OCT of size \(s\leq k\) uses
\(\ell_s+s\ell_t\) bits, with
\(\ell_s=\lceil\log_2(t+1)\rceil\).

The inspected source states the sharper established bound
\(O(3^k k|E||V|)\). The displayed local bound is deliberately conservative
and is the one attached to this implementation.

## Composition with exact repair

Feed the discovered \(X\) to `THM-027`. The additional repair phase uses

\[
 O\!\left(t+q+2^{|X|}\bigl(|X|+t(t+q)\bigr)\right)
\]

indexed operations and returns a minimum residual vertex cover. Thus an
explicit graph with \(t,q=\operatorname{poly}(m)\) and a public cap
\(k=O(\log m)\) admits polynomial-time OCT discovery and exact repair:
both \(3^k\) and \(2^k\) are polynomial in the original bit length \(m\).
This consequence begins only after the explicit graph is available.

## REF-068: naive subset search does not preserve the boundary

Enumerating every subset of at most \(k\) vertices costs

\[
 \sum_{i=0}^{k}\binom{t}{i}\leq (k+1)t^k.
\]

This is XP: polynomial in \(t\) only for fixed \(k\). If
\(t=m^{O(1)}\) and \(k=\Theta(\log m)\), it becomes
\(2^{O((\log m)^2)}\), which is quasi-polynomial rather than polynomial in
\(m\). The FPT separation of the exponent from \(t\), not mere bounded
subset enumeration, is what preserves the logarithmic M98 boundary. This
accounting refutes the proposed promotion of the naive search; it is not a
lower bound against all OCT algorithms or a complexity-class separation.
