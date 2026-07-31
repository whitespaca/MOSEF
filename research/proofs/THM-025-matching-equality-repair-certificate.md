# THM-025 - Matching-equality repair certificate

## Status and scope

`THM-025` is an unconditional finite graph-certificate theorem. It applies
after the looped coverer graph of `DEF-051` has been reconstructed and its
forced loop endpoints have been removed. It gives a sufficient exactness
certificate, not a method that finds such a certificate for every graph.

The M96 experiment is synthetic and source-bound to one frozen M95 graph. It
does not recognize a factor promise, extend the finite selector, or give a
general classical polynomial-time factoring algorithm.

## DEF-052: residual matching-equality witness

Let \(G_D\) be a finite looped coverer multigraph on type set \(T\), and let
\(F\) be its looped type set. Let

\[
 H=G_D[T\setminus F]
\]

retain only ordinary edge occurrences with both endpoints outside \(F\).
A **residual matching-equality witness of size \(k\)** consists of:

1. a set \(C\subseteq T\setminus F\) of \(k\) type vertices that meets every
   edge occurrence of \(H\); and
2. \(k\) edge occurrences \(M\) of \(H\) whose \(2k\) endpoints are pairwise
   distinct.

Parallel edge occurrences may exist, but two parallel edges cannot both
belong to \(M\) because they share endpoints.

## Exactness theorem

**Theorem.** If \((C,M)\) is a residual matching-equality witness of size
\(k\), then

\[
 \tau(H)=k
 \qquad\text{and}\qquad
 \rho(T,U)=|F|+k.
\]

**Proof.** Since \(C\) meets every residual edge, it is a vertex cover and
\(\tau(H)\le |C|=k\). Every vertex cover must meet all \(k\) edges of \(M\).
Those edges have disjoint endpoint sets, so one selected vertex can meet at
most one of them. Therefore every vertex cover has at least \(k\) vertices,
and \(\tau(H)\ge k\). Equality follows. Applying the forced-loop
decomposition of `THM-024` gives
\(\rho(T,U)=|F|+\tau(H)=|F|+k\). \(\square\)

No maximum-matching computation or minimum-cover enumeration is needed to
verify this witness. Equality between one valid cover and one valid matching
already proves that both are optimal.

## Encoding and verification cost

Retain the M95 notation:

\[
 b=\sum_i|B_i|,\qquad q=|U|,\qquad t=|T|,
\]

and let \(\lambda\) be the bit length of all tracked point labels. Define

\[
 \ell_t=\lceil\log_2\max(2,t)\rceil,\quad
 \ell_q=\lceil\log_2\max(2,q)\rceil,\quad
 \ell_k=\lceil\log_2(t+1)\rceil.
\]

After the \(t\) patterns and \(q\)-bit masks have reconstructed \(G_D\),
store the common size \(k\), \(k\) type indices for \(C\), and \(k\)
universe-column indices for \(M\). The additional structural payload is

\[
 \ell_k+k(\ell_t+\ell_q)
\]

bits. The \(\ell_k\) term is mandatory framing; the common witness length is
not treated as free metadata.

The verifier:

1. validates and reconstructs every coverage mask;
2. reconstructs every coverer column and the forced set \(F\);
3. checks that the \(C\) indices are distinct and outside \(F\);
4. scans every residual edge and checks that \(C\) meets it;
5. checks that every indexed matching column is a residual ordinary edge and
   that all matching endpoints are distinct; and
6. checks that both lists have the declared common size \(k\).

Using indexed bitsets, the complete bound is

\[
 O\!\left(
 tb+2tq+t+q+k(\ell_t+\ell_q)+\lambda
 \right)
\]

bit operations, plus \(O(S)\) hashing and parsing for \(S\) bound source
bytes. Working storage is
\(O(t(b+q)+t+q+\lambda)\) bits. The verifier never enumerates vertex
subsets.

For the fixed five-type, fifteen-column M96 seed,
\(\ell_t=\ell_k=3\) and \(\ell_q=4\). The five successful perturbations use
43 aggregate witness bits including all five size fields.

## Matching is not universally tight

Maximum-matching size is always a lower bound for vertex-cover size, but it
need not be exact. In the M96 `U3-keep-edges` perturbation the residual graph
is \(K_3\). Its three edges meet pairwise, so every matching has size at most
one. One vertex misses the opposite edge, while any two vertices cover all
edges; hence

\[
 \nu(K_3)=1<2=\tau(K_3).
\]

This is `REF-065`. The failure does not weaken the theorem: it only shows
that an equality witness is a sufficient certificate rather than a
universal residual-graph solver.
