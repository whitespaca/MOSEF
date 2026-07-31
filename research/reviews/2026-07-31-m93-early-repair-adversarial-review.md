# M93 adversarial review - early repair certificates

Date: 2026-07-31

## Review target

- `research/proofs/THM-022-subset-obstruction-certificate.md`
- `schemas/m93-early-repair-certificates-v1.json`
- `scripts/run_m93_early_repair_audit.py`
- `scripts/check_m93_early_repair_certificate.py`
- `tests/test_m93_early_repair_certificate.py`

## Falsification checks

1. **Complete-type premise.** The production checker does not trust a
   registered type list. It independently evaluates all eight primitive exits
   for every descriptor newly admitted between cap \(L^\star-1\) and
   \(L^\star\), then compares the complete nonzero mask set and its first
   representative sources.
2. **Frozen-row binding.** M50 is fixed by its exact file and canonical
   digests. Every input length, repair cap, predecessor bucket, source path,
   and source digest is re-read from that frozen summary.
3. **Private-pair incompleteness.** Lengths 16 and 24 have exact covers but no
   private pair for any selected type. The review therefore rejects extending
   `THM-021` by assuming that every finite minimum has such a witness.
4. **Cardinality boundary.** The three-point bucket at length 16 gives the
   exact lower bound two. The four-point bucket at length 24 gives only two,
   below the exact minimum three, so cardinality is not silently reused there.
5. **Subset-obstruction lower direction.** All
   \(\binom{4}{2}=6\) two-type subsets at length 24 are present exactly once,
   and each registered pair is outside that subset's coverage union. Any
   smaller cover can be padded to two types, so it also cannot cover.
6. **Upper witnesses.** OR-ing the selected masks covers every unresolved pair
   in all ten instances. The independent bounded exact-cover search obtains
   the same lexicographically first minimum witnesses.
7. **Complement quotient.** Patterns are normalized modulo global binary
   complement only after primitive evaluation. Complement preserves pair
   coverage and cannot create or delete a type.
8. **Branch-total arithmetic.** The independent evaluator handles a base
   divisible by the tracked prime before unit-only formulas, and handles
   simple cyclotomic roots by exact derivative division.
9. **Cost separation.** The 145-test core certificate path is distinct from
   the 48-subset brute-force defense. The exponential defense is bounded by
   \(t\le4\) and is not advertised as the theorem's verifier complexity.
10. **Payload boundary.** The 483-bit abstract count excludes JSON syntax,
    paths, hashes, source strings, and frozen-source bytes. These exclusions
    are stated rather than hidden.
11. **M91 differential independence.** The production checker contains no M91
    import. Only a test loads M91 as a separate differential oracle.
12. **Factoring scope.** The result covers ten frozen predecessor partitions,
    not arbitrary inputs, \(m>34\), other selector families, or a general
    factoring algorithm.

## Mutation review

Fourteen targeted tests cover the registered portfolio, deterministic
generation, clean-room import/line boundary, exact minima and witness kinds,
the two private-pair failures, complete length-24 subset enumeration, seven
rehashed semantic mutations, and full raw-type/count differential comparison.
All targeted tests passed.

## Severity result

- P0 findings: none.
- P1 findings: none after replacing the attempted universal private-pair claim
  with `REF-062` and proving the subset-obstruction alternative.
- P2 findings: the first draft did not charge lower-witness type indices or
  distinguish repeated source-byte references. Both conventions are now
  explicit in the ledger and experiment record.

The result is suitable for `THM-022` as a general finite combinatorial theorem
and `EMP-064` as its ten-instance finite application. General classical
polynomial-time factoring remains open.
