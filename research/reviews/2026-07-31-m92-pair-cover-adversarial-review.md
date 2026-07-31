# M92 adversarial review - pair-cover certificates

Date: 2026-07-31

## Review target

- `research/proofs/THM-021-pair-cover-certificate.md`
- `schemas/m92-pair-cover-certificates-v1.json`
- `scripts/run_m92_pair_cover_audit.py`
- `scripts/check_m92_pair_cover_certificate.py`
- `tests/test_m92_pair_cover_certificate.py`

## Falsification checks

1. **Refinement versus cover.** A pair stays in one refined bucket exactly
   when every added binary coordinate agrees on it. Therefore covering every
   within-bucket pair is both necessary and sufficient, not merely
   sufficient.
2. **Multiplicity and complement.** Repeated patterns and their global
   complements have identical coverage masks. They are quotient types, not
   additional repair power.
3. **Incomplete-type attack.** A private pair proves a lower bound only
   against a complete type list. The schema binds every row to its frozen
   source digest and names EMP-062 as the exhaustiveness dependency. The
   differential test re-enumerates the raw types with M91.
4. **Cardinality shortcut.** Six points need only three arbitrary binary
   labels, so \(\lceil\log_2 6\rceil\) cannot prove the two exact
   five-coordinate minima. This shortcut is rejected as NR-060.
5. **Baseline drift.** Lengths 27 and 28 retain cap 72 and cap 88. Replacing
   them by the adjacent predecessor caps changes the repair question.
6. **Lower-witness distinctness.** Each of the 19 chosen types has a pair
   covered by no other registered type. A cover must contain every one.
7. **Upper-witness completeness.** OR-ing the selected masks gives the full
   target in all nine instances. Rehashed removal of a type is rejected.
8. **Cost accounting.** The polynomial certificate path is separated from
   the redundant \(2^t\) brute-force confirmation. The latter is bounded
   only because \(t\le5\) here and is not advertised as the theorem's
   asymptotic verifier.
9. **Bit-cost boundary.** The 745-bit payload excludes JSON syntax,
   provenance hashes, paths, and source names. External source binding is
   separately charged by the 5,939,505-byte hashing/parsing input.
10. **Factoring scope.** The theorem is combinatorial and the applications
    are frozen finite certificates. Neither supplies promise recognition,
    an \(m>34\) threshold, or a general factoring algorithm.

## Mutation review

Eleven targeted tests cover the registered portfolio, deterministic
regeneration, import/line boundary, private-pair completeness, six rehashed
semantic mutations, and a full raw-coverage differential against M91. All
passed in 4.99 seconds.

## Severity result

- P0 findings: none.
- P1 findings: none after preserving the nonadjacent baselines and explicit
  EMP-062 completeness dependency.
- P2 findings: the first cost draft omitted the stored pattern bits and the
  redundant brute-force ledger. Both were added before registration.

The result is suitable for `THM-021` as a general finite combinatorial
theorem and `EMP-063` as the recorded nine-instance application.
