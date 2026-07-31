# EXP-0060: M85 independent M41 semantic checker

## Status

`EMPIRICAL` for the recorded execution and mutation-test outcomes. The
finite implication from the recomputed signatures and raw collision to
`THM-014`/`BAR-035` is documented in
`research/proofs/M85-independent-m41-semantic-checker.md`.

## Deterministic commands

```powershell
python scripts/check_m85_m41_semantic_certificate.py
python -m pytest tests/test_m85_semantic_certificate.py -q
ruff check scripts/check_m85_m41_semantic_certificate.py tests/test_m85_semantic_certificate.py
mypy --strict scripts/check_m85_m41_semantic_certificate.py tests/test_m85_semantic_certificate.py
```

No random seed is used. The checker uses only the Python standard library.

## Recorded environment

- OS/architecture: Windows 11 `10.0.26200`, AMD64.
- System checker runtime: Python 3.12.8.
- Isolated test runtime: CPython 3.12.13, pytest 9.1.1, Ruff 0.16.1,
  mypy 2.3.0.
- Git base: `e6b931fa5dfd99e622923cfb976791661a7cf925` on
  `research/20260731-m85-semantic-certificate-checker`; the reviewed M85
  staged diff is delivered by its milestone commit and pull request.
- Checker wall time: 15.6 seconds.
- Full Python regression wall time: 243.35 seconds.

## Frozen input

- Schema: `schemas/m41-length-29-cap-v1.json`
- Embedded summary SHA-256:
  `a9d61b984cf77c3c875ddbcdfaa2d6c6d1cd9bd6939d4c35ba4e1433a91d1589`
- Input length: 29
- Predecessor cap: 102
- Repair cap: 103

The embedded hash excludes the four primitive vectors because the legacy
generator appended them after computing the summary hash. The checker
evaluates those vectors directly.

## Registered result

The clean-room checker reconstructed:

- 685 balanced primes;
- 89,789 cap-102 descriptors;
- 95,778 cap-103 descriptors;
- 1,528 certificate coordinates;
- 234,270 unordered certificate pairs;
- the sole predecessor collision \(\{18979,21031\}\);
- 5,989 newly admitted descriptors and 47,912 new primitive coordinates; and
- the unique repair source
  `phi4:87:95:103:cofactor`, with pattern \((0,1)\).

It recomputed every registered certificate signature and found 685 distinct
cap-103 signatures. The cap-102 subcertificate has exactly the tracked
collision, and a raw descriptor-by-descriptor check confirms that the pair
collides across the complete predecessor selector.

Eight focused tests passed. Rehashed mutations of the population, descriptor,
and primitive vector were rejected, as was a packed-signature mutation. An
AST check confirmed no project or relative imports and a source length below
1,000 lines. A synthetic valid \(\Phi_4\) descriptor at the simple root
\((g,p)=(2,5)\) checked the derivative branch against the exact integer
quotient; the M41 certificate itself has no cyclotomic-root case.

## Interpretation

EXP-0060 reduces the trusted computing base for one representative frozen
finite row. It does not independently reconstruct the M31--M40 or M42--M46
rows, does not recognize the balanced promise, and does not imply any result
for \(m>29\) or general integer factoring.
