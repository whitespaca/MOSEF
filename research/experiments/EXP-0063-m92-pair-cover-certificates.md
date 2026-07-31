# EXP-0063: M92 pair-cover certificates

## Status

`EMPIRICAL` for schema generation, source binding, differential raw-pattern
reconstruction, mutation tests, and recorded execution counts. The general
pair-cover and private-pair arguments are proved as `THM-021` in
`research/proofs/THM-021-pair-cover-certificate.md`.

## Deterministic commands

```powershell
python scripts/run_m92_pair_cover_audit.py
python scripts/generate_m92_pair_cover_schema.py
python scripts/check_m92_pair_cover_certificate.py
pytest -p no:cacheprovider tests/test_m92_pair_cover_certificate.py -q
ruff check scripts/run_m92_pair_cover_audit.py scripts/generate_m92_pair_cover_schema.py scripts/check_m92_pair_cover_certificate.py tests/test_m92_pair_cover_certificate.py
mypy --strict --explicit-package-bases scripts/run_m92_pair_cover_audit.py scripts/generate_m92_pair_cover_schema.py scripts/check_m92_pair_cover_certificate.py tests/test_m92_pair_cover_certificate.py
```

No random seed is used. The independent checker is 412 lines, uses only the
Python standard library, and imports neither the generator nor M91.

## Registered result

```text
M92 pair-cover audit: PASS
(9 instances, 41 pairs, 19 coverage types, 745 payload bits)

M92 pair-cover certificate checker: PASS
(9 instances, 41 pairs, 19 coverage types, 19 selected types,
745 payload bits)

11 passed in 4.99s
```

The standalone checker completed in 1.19 seconds under the external process
stopwatch. The attempted post-exit Windows peak-working-set property returned
zero and is therefore not recorded as a memory measurement.

The complete repository suite subsequently reported:

```text
383 passed, 593 subtests passed in 372.04s (0:06:12)
```

Repository-wide Ruff, Python compilation, mypy, M0 foundation validation,
Rust formatting/Clippy/36 tests, and the C# Release build also passed.

The schema SHA-256 is

```text
3bf4b744d30d31f5e52725ca9cb70302bc4654ab1e7cfbe1707448392dbc19b0
```

The nine exact minima are \(2,5,5,1,2,1,1,1,1\). The abstract portfolio
contains 28 tracked prime labels, 41 pair-universe elements, 19 complete
coverage types, 19 selected upper-witness types, and 19 private-pair lower
witnesses. Its combinatorial payload is 745 bits, excluding JSON syntax,
paths, hashes, and human-readable source names.

The core certificate ledger contains 397 bit tests: 167 pattern/pair tests,
167 upper-mask tests, and 63 private-type tests. A redundant exact set-cover
check enumerates 82 subsets under a 2,429 mask-bit upper ledger. The nine
frozen source files total 5,939,505 bytes and are bound by exact SHA-256
digests before their registered pattern lists are projected.

## Differential and mutation coverage

The eleventh targeted test loads the separately implemented M91 semantic
checker only as a differential oracle and re-enumerates every raw coordinate
between each baseline and repair cap. The resulting complete coverage-type
sets equal the 19 registered M92 masks. The M92 production checker itself
does not import M91.

Rehashed mutations reject a coverage mask, private pair, incomplete upper
witness, source path, collision bucket, and cost ledger. Additional tests
enforce deterministic regeneration, the 450-line standard-library boundary,
and the presence of one private pair for every selected type.

## Interpretation

EXP-0063 supplies a compact independently checkable combinatorial layer over
the raw semantic reconstruction of EMP-062. It does not independently
re-evaluate number-theoretic primitive exits in production, recognize the
factor-dependent promise, establish an asymptotic cap law, or solve general
classical polynomial-time factoring.
