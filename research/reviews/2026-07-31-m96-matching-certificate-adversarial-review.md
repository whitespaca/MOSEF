# M96 adversarial review - matching-equality certificates

Date: 2026-07-31

## Review target

- `research/proofs/THM-025-matching-equality-repair-certificate.md`
- `schemas/m96-matching-certificates-v1.json`
- `scripts/run_m96_matching_certificate_profile.py`
- `scripts/check_m96_matching_certificate.py`
- `tests/test_m96_matching_certificate.py`

## Falsification checks

1. **Lower-bound direction.** A matching supplies one disjoint endpoint pair
   per edge. A cover must spend at least one distinct vertex on each pair.
2. **Upper-bound direction.** The registered cover is scanned against every
   residual edge occurrence; equality of list lengths is not trusted alone.
3. **Forced loops.** Matching and cover indices are restricted to unlooped
   types. The exact full repair adds the forced set only after the residual
   equality is established.
4. **No maximum-matching oracle.** The theorem verifies one matching and one
   cover of equal size. It does not need to prove maximality or maximum
   cardinality separately.
5. **Framing cost.** The common size \(k\) is charged in
   \(\lceil\log_2(t+1)\rceil\) bits. The initial 28-bit count that omitted
   these five length fields was rejected; the final aggregate is 43 bits.
6. **Source binding.** The checker pins the M95 file/content hashes and the
   exact M92 length-27 instance hash before reading its fifteen slots.
7. **Synthetic boundary.** Deleting columns creates synthetic finite type
   systems. They are not described as newly enumerated selector outputs.
8. **Complete normal form.** Every retained type signature is recomputed and
   checked nonempty and pairwise distinct.
9. **Non-template status.** Full duplicate-sensitive slot lists are compared
   with all three M95 templates. All eight perturbations are outside them.
10. **Gap cases.** \(K_3\), \(K_4\), and \(K_5-e\) retain exact gaps
    \(\tau-\nu=1\). Their stored matchings are marked insufficient.
11. **Bounded defense.** The checker independently enumerates covers and
    matchings on at most five vertices, but this enumeration is defense for
    EXP-0067 and is not part of the THM-025 certificate verifier.
12. **Factoring scope.** No perturbation is a promise recognizer or an
    asymptotic selector construction.

## Mutation review

Fifteen tests cover deterministic generation, import and line boundaries,
the frozen looped-\(K_5\) seed, all eight non-template complete-normal-form
systems, five equality certificates, three gap cases, and rehashed mutations
of the source anchor, grammar, deleted loops, cover, matching, cost, gap, and
scope.

## Severity result

- P0 findings: none.
- P1 finding (corrected): the first witness ledger treated the common list
  length as free. The final theorem, generator, checker, schema, and paper
  charge a three-bit size field in every successful fixed-seed certificate.
- P2 boundary: matching equality is not automatic. `REF-065` preserves the
  triangle failure, and EXP-0067 also retains \(K_4\) and \(K_5-e\) gaps.

The result is suitable for `THM-025` as an unconditional finite certificate
theorem and `EMP-067` as an eight-system synthetic, source-bound application.
General classical polynomial-time factoring remains open.
