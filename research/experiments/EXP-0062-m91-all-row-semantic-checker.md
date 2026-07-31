# EXP-0062: M91 table-wide clean-room semantic checker

## Status

`EMPIRICAL` for the recorded execution, resource measurement, and mutation
tests. The finite logical implication is documented in
`research/proofs/M91-all-row-semantic-certificate.md`.

## Deterministic commands

```powershell
python scripts/check_m91_all_rows_semantic_certificate.py
pytest -p no:cacheprovider tests/test_m91_all_rows_semantic_certificate.py -q
ruff check scripts/check_m91_all_rows_semantic_certificate.py tests/test_m91_all_rows_semantic_certificate.py
mypy --strict scripts/check_m91_all_rows_semantic_certificate.py tests/test_m91_all_rows_semantic_certificate.py
```

No random seed is used. The checker imports only the Python standard library.

## Recorded environment

- OS/architecture: Windows 11 `10.0.26200`, AMD64.
- Python: 3.12.8.
- pytest: 9.1.1.
- Ruff: 0.16.0.
- mypy: 2.3.0.
- Git base: M90 squash merge
  `28bd51c27c92e739af56d350688d1241f7daddfe`.
- Checker source: 987 lines.
- Reviewer budget: at most 1,000 lines, 300 seconds, and 128 MiB peak working
  set.

## Frozen inputs

The checker reads `schemas/m50-finite-threshold-summary-v1.json` and the exact
16 M31--M46 source files registered there. It verifies every registered
source file SHA-256 before semantic reconstruction. The finite window is
\(9\le m\le34\).

## Recorded result

The low-overhead Windows process measurement reported:

```text
M91 all-row semantic checker: PASS (26 rows, 16 sources, 12245 population entries, 17515 certificate coordinates, 28245185 certificate evaluations, 7520669 raw mask evaluations, 155.31s)
PeakWorkingSetMiB=29.15
```

The resource gate therefore passed with 144.69 seconds and 98.85 MiB of
headroom.

The checker reconstructed every balanced-prime list, parsed every selected
coordinate from the shared public grammar, recomputed every packed
construction signature, proved exact predecessor collisions, and verified
the nine certified repair minima at lengths 26 through 34. It explicitly
uses cap 72 and cap 88 as the five-coordinate repair baselines at lengths 27
and 28 rather than conflating them with the adjacent predecessor caps.

The targeted suite reported:

```text
11 passed in 83.41s (0:01:23)
```

After synchronizing the finite-paper Korean abstract-count fixture, the
complete repository suite reported:

```text
372 passed, 593 subtests passed in 345.40s (0:05:45)
```

The mutations cover packed signatures, a source-consistent but false
predecessor bucket, exhaustive repair patterns, source-path registration, and
M50 cap projection. Separate tests cover the import/line budget, exact
descriptor counts, population endpoints, source grammar, and the small
cyclotomic-root derivative branch.

## Rejected measurement path

An in-process `tracemalloc` run exceeded the 600-second command ceiling and
was rejected as the reviewer resource method. The identical semantic checker
then passed under external Windows peak-working-set sampling. The timed-out
run is not counted as mathematical evidence or as a semantic failure.

## Interpretation

EXP-0062 closes the 24-row clean-room gap left by M85 and M86 for the frozen
M50 table. It remains finite evidence for one public selector family. It does
not recognize the promise, prove any statement for \(m>34\), establish an
asymptotic cap law, minimize over other selectors, or support a claim that
general classical polynomial-time factoring is solved.
