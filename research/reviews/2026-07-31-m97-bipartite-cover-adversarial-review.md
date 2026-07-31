# M97 adversarial review - constructive bipartite repair

Date: 2026-07-31

## Review target

- `research/proofs/THM-026-constructive-bipartite-repair.md`
- `schemas/m97-bipartite-cover-v1.json`
- `scripts/run_m97_bipartite_cover_profile.py`
- `scripts/check_m97_bipartite_cover.py`
- `tests/test_m97_bipartite_cover.py`

## Falsification checks

1. **Maximum matching.** The symmetric-difference proof establishes both
   directions of the augmenting-path lemma for edge occurrences, including
   parallel edges.
2. **Termination.** Every flip raises matching size by one, so there are at
   most \(\lfloor t/2\rfloor\) successful searches.
3. **Terminal search.** The cost ledger includes the final unsuccessful
   search; the six cases therefore use ten augmentations and sixteen
   searches.
4. **Alternating directions.** Reachability traverses nonmatching edges
   \(L\to R\) and matching edges \(R\to L\). Reversing either rule can fail
   to produce the stated cover.
5. **No unmatched right endpoint in \(Z_R\).** Such an endpoint would close
   an augmenting path, contradicting termination.
6. **Cover cardinality.** Every matched pair is either wholly reachable or
   wholly unreachable, and the cover selects exactly one endpoint. Unmatched
   vertices do not enter the cover.
7. **Cover property.** An uncovered edge from reached \(L\) to unreached
   \(R\) contradicts either the nonmatching traversal rule or the matched-pair
   reachability relation.
8. **Forced loops.** The constructor operates only on
   \(G_D[T\setminus F]\); `THM-024` adds \(|F|\) after residual exactness is
   proved.
9. **Explicit-input complexity.** The final claim is polynomial in the
   reconstructed graph/type-system representation. It does not promote that
   result to a factor-independent constructor from the integer input.
10. **Output versus advice.** The 88-bit aggregate equality records are
    outputs that permit independent checking, not hidden inputs to the
    constructor.
11. **Non-bipartite equality.** Triangle plus pendant has
    \(\tau=\nu=2\), so bipartiteness is not mislabeled necessary.
12. **Non-bipartite gap.** \(C_5\) has \(\nu=2<3=\tau\), so the review does
    not extrapolate equality to every non-bipartite graph.
13. **Source binding.** The checker pins the exact M95 file/content hashes
    and the M92 length-27 seed before reconstructing target graphs.
14. **Synthetic boundary.** Column deletion defines synthetic systems; it
    is not described as new factor-selector enumeration.
15. **Bounded defense.** Exhaustive cover and matching enumeration on at
    most five vertices validates the experiment only and is absent from the
    theorem algorithm.

## Mutation review

Nineteen tests cover deterministic generation, checker independence, the
frozen seed, all eight complete non-template targets, six constructed
repairs, all 689 simple bipartite graphs with at most three vertices per
side, a parallel-edge/isolate regression, both non-bipartite boundaries, and
rehashed mutations of the source anchor, case grammar, deleted edges,
bipartition, matching, cover, cost, odd cycle, and scope.

## Severity result

- P0 findings: none.
- P1 finding (corrected): an early wording could be read as polynomiality
  from the original integer input. The theorem and paper now charge the
  explicit graph/type-system representation and state that factor-independent
  type construction is not supplied.
- P2 boundary: the repeated single-path method has the sufficient
  \(O(t(t+q))\) indexed-operation bound; no faster Hopcroft--Karp claim is
  made.

The result is suitable for `THM-026` as an unconditional constructive theorem
on explicit bipartite residual graphs and `EMP-068` as an eight-system
synthetic application. General classical polynomial-time factoring remains
open.
