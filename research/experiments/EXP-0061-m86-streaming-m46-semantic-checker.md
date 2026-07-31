# EXP-0061: M86 streaming M46 semantic checker

## Status

`EMPIRICAL` for the recorded execution, streaming bound, and mutation-test
outcomes. The finite implication for `THM-019` and `BAR-040` is documented in
`research/proofs/M86-streaming-m46-semantic-checker.md`.

## Deterministic commands

```powershell
python scripts/check_m86_m46_streaming_certificate.py
python -m pytest tests/test_m86_streaming_semantic_certificate.py -q
ruff check scripts/check_m86_m46_streaming_certificate.py tests/test_m86_streaming_semantic_certificate.py
mypy --strict scripts/check_m86_m46_streaming_certificate.py tests/test_m86_streaming_semantic_certificate.py
```

No random seed is used. The checker uses only the Python standard library.

## Recorded environment

- OS/architecture: Windows 11 `10.0.26200`, AMD64.
- System checker and initial tests: Python 3.12.8.
- Git base: `304bc5ae0c5a9593b46b88a7fa34200fd0a38744` on
  `research/20260731-m86-final-row-semantic-checker`; the reviewed M86 diff
  is delivered by its milestone commit and pull request.
- Checker source: 624 lines.
- Initial checker wall time: 53.24 seconds.
- Initial nine-test wall time: 53.78 seconds.

Final isolated tool versions and full-suite wall time are recorded in
`research/STATUS.md`.

## Frozen input

- Schema: `schemas/m46-length-34-cap-v1.json`
- File SHA-256:
  `34942d674d0451b219bde70fc65909ef3baa6516b08d61df36bf6ea91e8cde61`
- Embedded summary SHA-256:
  `52c7899c6d93a747b52fa531e4261ba842acbceb06ae28f420005f8606c85a11`
- Input length: 34.
- Predecessor cap: 200.
- Repair cap: 201.

The legacy embedded hash excludes the four later-appended primitive vectors.
The checker evaluates those vectors directly.

## Registered result

The checker independently reconstructed:

- 3,299 balanced primes and 5,440,051 unordered pairs;
- 3,298 certificate coordinates and 10,880,102 streamed
  coordinate/prime evaluations;
- the exact cap-200 descriptor count of 704,261;
- the sole predecessor collision \(\{97927,99527\}\);
- 10,139 newly admitted cap-201 descriptors and 81,112 raw coordinates;
- the unique repair `phi6:149:201:45:cofactor` with pattern \((1,0)\); and
- the cap-201 descriptor count of 714,400 and injective certificate.

Only 3,299 mutable packed-signature slots are retained during certificate
evaluation. The checker does not materialize the 10,880,102-cell
coordinate/prime matrix or either complete descriptor set.

Nine focused tests passed. Rehashed mutations of the population, one
certificate source, and one primitive vector were rejected semantically. A
packed-signature mutation was rejected against the recomputed certificate.
The streaming assembly was checked against a small materialized oracle, and
the cap-200/cap-201 descriptor counts were independently enumerated.

## Interpretation

EXP-0061 reduces the trusted computing base for the final M46 row and
demonstrates bounded reviewer memory for its full construction certificate.
Together M85 and M86 still leave the other 24 M50 rows, including M42--M45,
without this clean-room path. EXP-0061 does not recognize the balanced
promise, prove an asymptotic cap rate, or provide evidence for general
classical polynomial-time factoring.
