# THM-026 - Constructive bipartite residual repair

## Status and scope

`THM-026` is an unconditional algorithmic theorem for an explicit finite
coverer graph. It applies after `THM-024` has reconstructed the looped
coverer multigraph, forced every looped type, and exposed a bipartite
residual graph. It constructs the `THM-025` equality witness instead of
assuming that witness is supplied.

The theorem does not construct a factor-independent complete type list,
prove that every residual coverer graph is bipartite, recognize a factor
promise, or give a general classical polynomial-time factoring algorithm.

## DEF-053: bipartite residual constructor

Let \(G_D\) be a finite looped coverer multigraph on type set \(T\). Let
\(F\) be the set of looped types and

\[
 H=G_D[T\setminus F].
\]

A **bipartite residual constructor** performs the following operations on the
explicit edge occurrences of \(H\).

1. Two-color every connected component. If an edge has equal-colored
   endpoints, reject this restricted constructor as non-bipartite.
2. For a valid bipartition \(L\mathbin{\dot\cup}R=T\setminus F\), start with
   the empty matching and repeatedly find an augmenting path from an
   unmatched vertex of \(L\) to an unmatched vertex of \(R\).
3. Flip matching membership on the path. Stop only when no augmenting path
   remains.
4. From the final matching \(M\), let \(Z_L\cup Z_R\) be the vertices
   reachable from unmatched vertices of \(L\) by traversing nonmatching
   edges \(L\to R\) and matching edges \(R\to L\).
5. Output

\[
 C=(L\setminus Z_L)\cup(R\cap Z_R)
\]

together with \(M\).

Parallel edge occurrences are retained by column index. They do not alter
the two-coloring, and at most one occurrence with a given endpoint pair can
enter a matching.

## Augmenting-path lemma

**Lemma.** A finite matching \(M\) has maximum cardinality if and only if
there is no \(M\)-augmenting path.

**Proof.** Flipping membership on an augmenting path replaces one fewer
matching edge by one more nonmatching edge, increasing the cardinality by
one. Thus a maximum matching has no augmenting path.

Conversely, suppose a larger matching \(M^\star\) exists. In the multigraph
of edge occurrences \(M\mathbin{\triangle}M^\star\), every vertex has degree
at most two, so every nontrivial component is an alternating path or cycle.
Because \(|M^\star|>|M|\), some path component contains one more
\(M^\star\)-edge than \(M\)-edge. Its endpoints are unmatched by \(M\), so
it is an \(M\)-augmenting path. This contradicts the assumed absence of such
a path. \(\square\)

The constructor terminates because every flip increases \(|M|\), which is
at most \(\lfloor |T\setminus F|/2\rfloor\).

## Exact constructive theorem

**Theorem.** If \(H\) is bipartite, the `DEF-053` constructor outputs a
matching \(M\) and vertex cover \(C\) satisfying

\[
 |C|=|M|=\tau(H)=\nu(H)
\]

and therefore

\[
 \rho(T,U)=|F|+|M|.
\]

**Proof.** The augmenting-path lemma shows that the final \(M\) is maximum.
There is no unmatched vertex of \(R\) in \(Z_R\), because its alternating
path from an unmatched vertex of \(L\) would augment \(M\).

For every matching edge \(\ell r\), its endpoints are either both reachable
or both unreachable. Indeed, a reached \(r\) is followed through its
matching edge to \(\ell\); and a reached matched \(\ell\) was itself entered
through that matching edge from \(r\). Hence \(C\) contains exactly one
endpoint of every matching edge: \(\ell\) when both are unreachable and
\(r\) when both are reachable. Unmatched left vertices are starting
vertices in \(Z_L\), and unmatched right vertices are not in \(Z_R\), so no
unmatched vertex enters \(C\). Therefore \(|C|=|M|\).

It remains to prove that \(C\) covers every edge. If an edge \(\ell r\) were
uncovered, then \(\ell\in Z_L\) and \(r\notin Z_R\). If the edge were not in
\(M\), the allowed traversal \(L\to R\) would put \(r\) in \(Z_R\). If it
were in \(M\), reachability of the matched endpoint \(\ell\) would imply
reachability of its matched endpoint \(r\). Both cases are contradictions.

Thus \(C\) is a cover and \(M\) is a matching of the same size. `THM-025`
gives \(\tau(H)=|C|=|M|\), and `THM-024` adds the forced loops:
\(\rho(T,U)=|F|+\tau(H)\). \(\square\)

This proof is constructive and includes the maximum-matching and
minimum-cover arguments; it does not invoke equality as an unexplained
oracle.

## Complexity and output certificate

Retain

\[
 b=\sum_i|B_i|,\qquad q=|U|,\qquad t=|T|,
\]

let \(\lambda\) be the tracked point-label bit length, and define

\[
 \ell_t=\lceil\log_2\max(2,t)\rceil,\quad
 \ell_q=\lceil\log_2\max(2,q)\rceil,\quad
 \ell_k=\lceil\log_2(t+1)\rceil.
\]

Two-coloring costs \(O(t+q)\) indexed operations. Each augmenting-path
search costs \(O(t+q)\), and there are at most
\(\lfloor t/2\rfloor+1\) searches including the final unsuccessful search.
Alternating reachability costs one more \(O(t+q)\) pass. Thus the constructor
uses

\[
 O(t(t+q))
\]

indexed operations. Charging \(\ell_t+\ell_q\) bits per stored or compared
index gives the conservative complete bit bound

\[
 O\!\left(
 tb+2tq+t+q+\lambda+
 t(t+q)(\ell_t+\ell_q)
 \right)
\]

plus \(O(S)\) hashing and parsing for \(S\) source-bound bytes. Additional
graph-algorithm storage is
\(O((t+q)(\ell_t+\ell_q))\) bits.

The constructor needs no cover/matching witness as input. Its explicit
output can be independently checked as a `THM-025` certificate. For
\(k=|M|\), that output uses

\[
 \ell_k+k(\ell_t+\ell_q)
\]

bits beyond the reconstructed graph.

Polynomiality here is in the explicit graph and type-system representation.
It does not imply that the hidden-factor-dependent type system can be
constructed in polynomial time from the integer input alone.

## Bipartiteness is sufficient, not necessary

The graph consisting of a triangle with one pendant edge is non-bipartite,
yet a matching containing the pendant edge and the opposite triangle edge
has size two, while the pendant attachment vertex and either endpoint of the
opposite edge form a two-vertex cover. Hence

\[
 \nu=2=\tau.
\]

This is `REF-066`: bipartiteness is sufficient for the constructor but is
not necessary for a `THM-025` equality certificate. Conversely, the
five-cycle has \(\nu(C_5)=2<3=\tau(C_5)\), so non-bipartite equality is not
automatic.
