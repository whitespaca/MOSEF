# M94 adversarial review - complete-graph incidence certificates

Date: 2026-07-31

## Review target

- `research/proofs/THM-023-clique-incidence-cover-certificate.md`
- `schemas/m94-clique-incidence-certificates-v1.json`
- `scripts/run_m94_clique_incidence_audit.py`
- `scripts/check_m94_clique_incidence_certificate.py`
- `tests/test_m94_clique_incidence_certificate.py`

## Falsification checks

1. **Coverer direction.** The coverer set is defined by type membership:
   \(D(u)=\{T_i\in T:u\in T_i\}\). The proof uses no reversed edge
   convention.
2. **Every column reconstructed.** The checker scans every type mask at every
   universe position before applying the graph theorem. It does not infer
   incidence from the M93 lower witnesses.
3. **Exactly two coverers.** Both applications have column degree exactly two.
   A source-rebound mutation producing degree three is rejected.
4. **All graph edges present.** The observed coverer pairs equal all three
   pairs of the length-16 type set and all six pairs of the length-24 type
   set. Pair counts alone are not trusted.
5. **Upper direction.** Omitting one type cannot omit both endpoints of an
   edge, so the implicit \(t-1\)-type selection covers every universe element.
6. **Lower direction.** Any at-most-\(t-2\) selection omits two types. The
   complete-graph premise supplies an element covered by precisely that pair,
   so the element remains uncovered.
7. **Complete-type premise.** The application inherits exhaustive type
   reconstruction from EMP-064 and binds the exact M93 file and summary
   hashes. THM-023 does not manufacture that external premise.
8. **Redundant trace boundary.** JSON `coverer_sets` are audit traces. The
   verifier reconstructs them from masks, and the payload theorem does not
   charge them as necessary witness data.
9. **Cost comparison.** The 56-bit saving is not converted into a verifier
   speedup. The conservative test ledger is five tests larger in total.
10. **Bounded defense.** Exact-cover enumeration confirms minima two and
    three, but the proof uses the vertex-cover argument rather than the
    exponential defense.
11. **Independence boundary.** The production checker has no generator or
    earlier-checker import. It reconstructs incidence independently, but it
    does not claim a second number-theoretic enumeration of the M93 types.
12. **Factoring scope.** The certificate concerns two frozen finite repair
    instances. It does not supply factor recognition or a universal factoring
    algorithm.

## Mutation review

Eleven tests cover deterministic generation, import and line boundaries,
complete edge incidence, exact minima, payload/test comparisons, four rehashed
schema mutations, a non-clique source-rebound mutation, and a direct-mask
incidence differential. All targeted tests passed.

## Severity result

- P0 findings: none.
- P1 findings: none after the complete-type dependency and redundant-trace
  exclusion were made explicit.
- P2 finding: the first cost interpretation treated payload compression as
  verifier compression. The final ledger records 130 versus 186 payload bits
  but 75 versus 70 core tests.

The result is suitable for `THM-023` as an unconditional finite structural
theorem and `EMP-065` as its two-instance application. General classical
polynomial-time factoring remains open.
