# M95 adversarial review - portfolio-wide coverer graphs

Date: 2026-07-31

## Review target

- `research/proofs/THM-024-looped-coverer-graph-certificate.md`
- `schemas/m95-coverer-graph-profile-v1.json`
- `scripts/run_m95_coverer_graph_profile.py`
- `scripts/check_m95_coverer_graph_certificate.py`
- `tests/test_m95_coverer_graph_certificate.py`

## Falsification checks

1. **All columns reconstructed.** The production checker recomputes every
   coverage mask from its point pattern and scans all 37 types over all 64
   universe columns. It does not trust the stored coverer traces.
2. **No rank assumption imported.** The checker rejects empty, rank-three, and
   non-template columns after reconstruction. A source-rebound rank-three
   mutation is rejected.
3. **Template multiplicity.** Observed singleton/pair slots are compared as
   sorted lists, not sets, so duplicate or missing slots fail.
4. **Loop semantics.** A singleton coverer is treated as a graph loop and
   forces its unique type. It is not confused with an isolated vertex.
5. **Forced-set decomposition.** Once every looped type is selected, only
   ordinary edges between unlooped types remain. This proves the additive
   \(|F|+\tau(G[T\setminus F])\) formula in both directions.
6. **Clique case.** The two loopless systems contain every ordinary type pair
   exactly once. Their minima \(t-1\) reuse the omitted-pair lower argument,
   not bounded enumeration.
7. **Upper witnesses.** All types are implicit in looped templates; the fixed
   last type is omitted in loopless cliques. Both paths are recomputed from
   masks.
8. **Graph boundary.** The star/path counterexample has the same
   \(t=4,q=3\), and degree-two column histogram but exact minima one and two.
   Thus rank/count data alone are not promoted to an exact formula.
9. **Universality scope.** The realization theorem excludes isolated
   vertices so every type remains nonzero and excludes \(K_2\) components so
   two endpoints never collapse to the same incident-edge type. It does not
   use or claim a complexity-class separation.
10. **Complete-type premise.** M92 and M93 file/content hashes are pinned.
    Exhaustiveness remains an external finite dependency on EMP-062 and
    EMP-064.
11. **Payload boundary.** Patterns, masks, and labels are charged; redundant
    JSON coverer traces, syntax, paths, hashes, and source bytes are excluded
    consistently with the predecessor ledgers.
12. **Work comparison.** The 22-test aggregate saving is not described as
    strict per-instance dominance; length 16 remains five tests worse.
13. **Factoring scope.** The graph profile neither recognizes a factor
    promise nor extends the selector beyond the frozen range.

## Mutation review

Eighteen tests cover deterministic generation, import and line boundaries,
three template classes, direct-mask incidence, exact minima, aggregate and
per-instance cost checks, seven rehashed mutations, the rank-three rebound,
the star/path counterexample, the \(K_2\) distinct-type regression, and
duplicate-free slot lists. All targeted tests passed.

## Severity result

- P0 findings: none.
- P1 finding (corrected): the initial universality statement excluded
  isolated vertices but not a \(K_2\) component, whose two endpoints induce
  duplicate types. The final theorem also excludes \(K_2\) components and
  proves pairwise distinctness.
- P2 finding: the initial rank-two interpretation implicitly suggested a
  universal exact formula. The final theorem includes graph universality and
  `REF-064`, showing that residual vertex cover still needs graph-specific
  structure or another lower certificate.

The result is suitable for `THM-024` as an unconditional finite graph
reduction and `EMP-066` as its nineteen-instance source-bound application.
General classical polynomial-time factoring remains open.
