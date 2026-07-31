# THM-027 - Exact repair from a supplied odd-cycle transversal

## Status and scope

`THM-027` is an unconditional fixed-parameter algorithmic theorem for an
explicit finite coverer graph and a supplied odd-cycle transversal. It
extends `THM-026` beyond bipartite residual graphs without treating the
transversal as free or hiding the exponential dependence on its size.

The theorem does not discover an odd-cycle transversal, bound its size for
coverer graphs arising from integer inputs, construct a factor-independent
complete type list, recognize a factor promise, or give a general classical
polynomial-time factoring algorithm.

## DEF-054: transversal-branch constructor

Let \(G_D\) be a finite looped coverer multigraph on type set \(T\). As in
`THM-024`, let \(F\) be the forced set of looped types and put

\[
 H=G_D[T\setminus F].
\]

Let \(X\subseteq V(H)\) be supplied and let \(s=|X|\). The input is accepted
only if \(B=H-X\) is bipartite. For every subset \(A\subseteq X\), interpret
\(A\) as the transversal vertices selected into a candidate cover and
\(X\setminus A\) as those excluded from it.

1. If \(H[X\setminus A]\) contains an edge, mark the branch infeasible.
2. Otherwise force

\[
 P_A=N_B(X\setminus A)
\]

into the cover.
3. Run the `THM-026` bipartite constructor on

\[
 B_A=B-P_A
\]

and let its minimum cover be \(Q_A\).
4. Form

\[
 C_A=A\cup P_A\cup Q_A.
\]

Return a minimum-cardinality \(C_A\) over all feasible branches, with a
deterministic lexicographic tie break.

The constructor enumerates exactly \(2^s\) branches. Parallel edge
occurrences are retained by column index. A branch is infeasible when even
one occurrence has both endpoints in \(X\setminus A\).

## Exact constructive theorem

**Theorem.** If the supplied \(X\) satisfies that \(H-X\) is bipartite, the
`DEF-054` constructor returns a minimum vertex cover of \(H\). Consequently,
if the returned cover is \(C^\star\), then the exact repair number is

\[
 \rho(T,U)=|F|+|C^\star|=|F|+\tau(H).
\]

**Proof.** Fix a feasible branch \(A\). Edges with both endpoints in
\(X\setminus A\) do not exist by the feasibility test. Every edge between
\(X\setminus A\) and \(B\) has its endpoint in \(P_A\), so it is covered.
Every edge incident to \(A\) is covered by \(A\). Deleting \(P_A\) from the
bipartite graph \(B\) leaves \(B_A\), and `THM-026` constructs a cover
\(Q_A\) of all remaining edges. Thus \(C_A\) covers every edge of \(H\).

For optimality, let \(C\) be any vertex cover of \(H\) and define
\(A=C\cap X\). Because \(C\) covers \(H[X]\), there is no edge with both
endpoints in \(X\setminus A\); hence the corresponding branch is feasible.
Every neighbor in \(B\) of a vertex in \(X\setminus A\) must belong to
\(C\), so \(P_A\subseteq C\). The remaining set

\[
 C\cap(V(B)\setminus P_A)
\]

covers \(B_A\). By exactness of `THM-026`,
\(|Q_A|\leq |C\cap(V(B)\setminus P_A)|\). The three sets \(A\), \(P_A\),
and \(V(B)\setminus P_A\) are disjoint, and therefore

\[
 |C_A|
 =|A|+|P_A|+|Q_A|
 \leq |C|.
\]

Applying this inequality to an optimum \(C\) shows that the minimum
constructed candidate has size at most \(\tau(H)\). Every constructed
candidate is a cover, so its size is also at least \(\tau(H)\). Equality
follows. `THM-024` then adds the forced loops. \(\square\)

This proof does not use maximum-matching equality on the original
non-bipartite graph. Matching is used only inside each bipartite remainder
\(B_A\), under the hypotheses of `THM-026`.

## Completeness of the branch cases

The proof gives a useful falsification checklist.

- Selecting \(x\in A\) covers every edge incident to \(x\).
- Excluding both endpoints of an edge inside \(X\) is impossible, which is
  exactly the infeasible-branch rule.
- Excluding \(x\in X\setminus A\) forces every neighbor of \(x\) in \(B\);
  omitting any such neighbor leaves an uncovered cross edge.
- After those forced vertices are removed, no uncovered cross edge remains
  and every undecided edge lies in the bipartite graph \(B_A\).
- Every vertex cover \(C\) appears in the branch \(A=C\cap X\), so the
  enumeration cannot omit an optimum.

These statements remain valid with isolated vertices and parallel edge
occurrences.

## Complexity, input payload, and polynomial boundary

Retain

\[
 b=\sum_i|B_i|,\qquad q=|U|,\qquad t=|T|,
\]

let \(\lambda\) be the tracked point-label bit length, and define

\[
 \ell_t=\lceil\log_2\max(2,t)\rceil,\quad
 \ell_q=\lceil\log_2\max(2,q)\rceil,\quad
 \ell_s=\lceil\log_2(t+1)\rceil,\quad
 \ell_k=\lceil\log_2(t+1)\rceil.
\]

Checking \(H-X\) and computing one bipartition costs \(O(t+q)\) indexed
operations. For each of the \(2^s\) branches, subset decoding and the
internal-edge, forced-neighbor, and remainder passes cost
\(O(s+t+q)\), while `THM-026` costs \(O(t(t+q))\). A conservative combined
bound is therefore

\[
 O\!\left(t+q+2^s\bigl(s+t(t+q)\bigr)\right)
\]

indexed operations. Charging \(\ell_t+\ell_q\) bits per stored or compared
index gives the complete conservative bit bound

\[
 O\!\left(
 tb+2tq+t+q+\lambda+
 \bigl(t+q+2^s(s+t(t+q))\bigr)(\ell_t+\ell_q)
 \right)
\]

plus \(O(S)\) hashing and parsing for \(S\) source-bound bytes. The working
implementation stores one branch at a time in the theorem algorithm; its
additional working storage is polynomial in \(t+q+s\), even though a
diagnostic ledger that retains all branches has exponential output size.

The supplied transversal itself is an input certificate using

\[
 \ell_s+s\ell_t
\]

bits under the explicit type registry. A returned cover of size \(k\) uses

\[
 \ell_k+k\ell_t
\]

bits. The algorithm is fixed-parameter tractable in \(s\). If the explicit
graph/type-system parameters are polynomial in the original input bit
length \(m\) and \(s=O(\log m)\), then \(2^s\) is polynomial in \(m\).
Without such a proved bound, the displayed algorithm is exponential in
\(s\) and is not an unrestricted polynomial-time algorithm.

## REF-067: the FPT-to-polynomial promotion is invalid

The statement “a \(2^s\operatorname{poly}(t,q)\) exact algorithm is
polynomial for unrestricted transversal size” is false. For example,
\(s=\Theta(t)\) gives \(2^{\Theta(t)}\) branches. Even when \(t\) is
polynomial in \(m\), that dependence is generally exponential in \(m\).
Only a separately proved logarithmic bound such as \(s=O(\log m)\), together
with a public polynomial-size explicit graph and a way to obtain the
transversal, supports a polynomial consequence.
