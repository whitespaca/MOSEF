# EXP-0064: M93 early repair certificates

## Status

`EMPIRICAL` for frozen-source reconstruction, exhaustive primitive-coordinate
evaluation, schema generation, recorded counts, differential comparison, and
mutation tests. The cardinality and subset-obstruction lower arguments are
proved separately as `THM-022`.

## Deterministic commands

```powershell
python scripts/run_m93_early_repair_audit.py
python scripts/generate_m93_early_repair_schema.py
python scripts/check_m93_early_repair_certificate.py
pytest -p no:cacheprovider tests/test_m93_early_repair_certificate.py -q
ruff check scripts/run_m93_early_repair_audit.py scripts/generate_m93_early_repair_schema.py scripts/check_m93_early_repair_certificate.py tests/test_m93_early_repair_certificate.py
mypy --strict --explicit-package-bases scripts/run_m93_early_repair_audit.py scripts/generate_m93_early_repair_schema.py scripts/check_m93_early_repair_certificate.py tests/test_m93_early_repair_certificate.py
```

No random seed is used. The 679-line production checker uses only the Python
standard library and imports neither the generator nor M91. It independently
implements the public descriptor grammar, all eight primitive exits, pair
coverage, exact cover search, and all three lower-witness forms.

## Registered result

```text
M93 early repair audit: PASS
(10 instances, 23 pairs, 18 coverage types, 16 selected types,
483 payload bits)

M93 early repair certificate checker: PASS
(10 instances, 23 pairs, 18 coverage types, 16 selected types,
154920 raw coordinate tests, 483 payload bits)

14 passed
```

The registered schema SHA-256 is

```text
77c8ae289277875815e7744b37456627f619fc601d4fb2ccca35031b7f248aae
```

The exact minima at input lengths 16 through 25 are
\(2,2,1,1,1,3,1,1,3,1\). The portfolio contains 27 tracked prime labels,
23 within-bucket pairs, 18 complete nonzero coverage types, and 16 selected
upper-witness types.

The clean-room checker enumerates 7,398 newly admitted descriptors, performs
19,365 descriptor/prime evaluations and 154,920 primitive-coordinate tests,
then reconstructs the exact 18-type inventory. The core abstract certificate
ledger contains 145 bit tests: 61 pattern/pair tests, 52 upper-mask tests, and
32 lower-witness tests. A redundant exact-cover defense checks 48 subsets
under a 314 mask-bit upper ledger. The abstract payload is 483 bits, excluding
JSON syntax, paths, hashes, representative-source strings, and source bytes.

The ten referenced source files total 144,242 bytes when counted once per
instance. Repeated references to the common M32 source are intentionally
charged per instance in that ledger. The M50 summary is fixed by file SHA-256
`2f9974d45a350f65694bd048bf67dae4b27a90493b07ecd895c251d102aab75b`;
each source is also checked against the digest frozen inside M50.

## Lower-witness boundary

Eight instances admit the private-pair certificate of `THM-021`. The two
exceptions are exact and constructive:

- at \(m=16\), no selected type has a private pair, while the three-point
  cardinality bound and a two-type upper witness prove the exact minimum two;
- at \(m=24\), no selected type has a private pair, while six explicit
  two-type obstructions and a three-type upper witness prove the exact minimum
  three.

The second case is not certified by cardinality alone: its four-point bucket
gives only the lower bound two. This is the smallest registered instance in
which both the private-pair criterion and the cardinality criterion fail to
prove the exact minimum, while subset obstructions succeed.

## Differential and mutation coverage

The targeted suite compares every complete coverage-mask set and every
descriptor/prime evaluation count against the separately implemented M91
semantic checker. M91 is loaded only by the differential test; it is absent
from the production checker.

Rehashed mutations reject a raw coverage type, source path, upper witness,
cardinality witness, private pair, subset-obstruction entry, and cost ledger.
Additional tests enforce deterministic generation, the 700-line
standard-library clean-room boundary, all exact minima, both private-pair
failures, and completeness of the six \(m=24\) two-type obstruction entries.

## Interpretation

EXP-0064 closes the incremental-repair certificate gap for all ten
non-domain-floor M50 rows at lengths 16 through 25. Together with EXP-0063,
all 19 frozen finite repair transitions at lengths 16 through 34 now have
compact exact upper/lower certificates.

This is finite, selector-specific evidence. It neither recognizes balanced
factors from an arbitrary input, proves a threshold law beyond 34, minimizes
over other selector families, nor solves general classical polynomial-time
integer factorization.
