# M98 adversarial review - odd-cycle-transversal repair

Date: 2026-07-31

## Review target

- `research/proofs/THM-027-odd-cycle-transversal-repair.md`
- `schemas/m98-oct-cover-v1.json`
- `scripts/run_m98_oct_cover_profile.py`
- `scripts/check_m98_oct_cover.py`
- `tests/test_m98_oct_cover.py`

## Falsification checks

1. **Transversal validity.** The constructor verifies that \(H-X\) is
   bipartite. The undersized \(K_5\) input is rejected with the surviving
   triangle \(T_2,T_3,T_4,T_2\).
2. **Complete branch coverage.** Every \(A\subseteq X\) is enumerated once;
   a vertex cover \(C\) maps to \(A=C\cap X\), so no optimum branch is
   omitted.
3. **Internal-edge infeasibility.** If both endpoints of an edge in \(H[X]\)
   lie in \(X\setminus A\), neither endpoint is selected and the branch
   cannot be a cover.
4. **Forced cross neighbors.** Every neighbor in \(B\) of
   \(X\setminus A\) is mandatory. Omitting such a neighbor leaves its cross
   edge uncovered.
5. **Remainder scope.** After forced cross neighbors are selected and
   removed, all undecided edges lie in an induced subgraph of the bipartite
   graph \(B=H-X\).
6. **Use of THM-026.** Maximum-matching equality is invoked only on that
   bipartite remainder, not on the original non-bipartite graph.
7. **Candidate cover.** \(A\), \(P_A\), and \(Q_A\) respectively cover
   incident, forced cross, and remaining base edges; their union covers
   every edge category.
8. **Optimality inequality.** For any cover \(C\), its corresponding branch
   has \(P_A\subseteq C\) and a bipartite optimum no larger than the
   remaining part of \(C\).
9. **Forced loops.** The transversal algorithm operates on
   \(H=G_D[T\setminus F]\); `THM-024` adds \(|F|\) only after residual
   exactness is proved.
10. **Parallel edges and isolates.** Edge-occurrence indices are preserved;
    duplicates do not alter feasibility or neighbor forcing, and isolates
    never need selection.
11. **Exponential ledger.** The claim exposes exactly \(2^s\) branches. It
    does not call the method polynomial for unrestricted \(s\).
12. **Logarithmic boundary.** The \(s=O(\log m)\) polynomial consequence is
    conditional on polynomial explicit graph parameters and on obtaining
    the transversal; neither fact is asserted here.
13. **Input versus output.** The 63-bit aggregate transversal payload is
    supplied input, while the 84-bit aggregate cover payload is output.
14. **Source binding.** The checker pins the exact M95 file/content hashes,
    M92 length-27 seed, and M97 constructor source before reconstruction.
15. **Synthetic boundary.** Column deletion defines synthetic systems; it
    is not described as factor-selector enumeration.
16. **Bounded defense.** Exact cover/matching enumeration on at most five
    vertices and the 1,024-pair exhaustive differential validate the
    implementation only and are absent from the theorem algorithm.

## Mutation review

Nineteen tests cover deterministic generation, checker independence, exact
totals, all branch ledgers, valid and invalid \(K_5\) transversals, explicit
minimum covers, all 1,024 four-vertex graph/transversal pairs, and rehashed
mutations of source anchors, case grammar, transversal membership, branch
status, forced vertices, candidate cover, reported minimum, rejection
cycle, payload, and scope.

## Severity result

- P0 findings: none.
- P1 finding (corrected): an early complexity draft did not distinguish the
  supplied transversal payload from the constructed cover output. The proof
  now states both bit lengths and identifies transversal discovery as open.
- P1 finding (corrected): a preliminary summary could be read as polynomial
  for arbitrary \(s\). The theorem now displays \(2^s\) in both indexed and
  bit bounds and restricts the polynomial consequence to a separately
  justified \(s=O(\log m)\) regime.
- P2 boundary: the experiment stores all branches for transparent audit,
  although the theorem algorithm can keep only the current best branch.

The result is suitable for `THM-027` as an unconditional
fixed-parameter theorem on explicit graphs with a supplied valid
transversal and `EMP-069` as an eight-system synthetic application. General
classical polynomial-time factoring remains open.
