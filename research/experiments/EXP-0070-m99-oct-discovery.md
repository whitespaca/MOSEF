# EXP-0070: M99 iterative-compression OCT discovery audit

## Status

`EMPIRICAL` for the frozen M98 source binding, eight capped discovery
instances, seven exact discoveries, one above-cap rejection, composed M98
covers, deterministic ledgers, exhaustive five-vertex differential, and
mutation tests. Algorithmic correctness is proved separately as `THM-028`;
the naive XP promotion is refuted as `REF-068`.

## Deterministic commands

```powershell
python scripts/run_m99_oct_discovery_profile.py
python scripts/generate_m99_oct_discovery_schema.py --check
python scripts/check_m99_oct_discovery.py
pytest -p no:cacheprovider tests/test_m99_oct_discovery.py -q
ruff check scripts/run_m99_oct_discovery_profile.py scripts/generate_m99_oct_discovery_schema.py scripts/check_m99_oct_discovery.py tests/test_m99_oct_discovery.py
mypy --strict --explicit-package-bases scripts/run_m99_oct_discovery_profile.py scripts/generate_m99_oct_discovery_schema.py scripts/check_m99_oct_discovery.py tests/test_m99_oct_discovery.py
```

No random seed is used. The 367-line production checker uses only the
Python standard library and imports neither the M99 generator nor the M98
constructor. It pins the exact M98 schema and constructor hashes,
reconstructs the eight explicit graphs, independently enumerates their OCT
and vertex-cover optima, validates every discovery and composed cover, and
checks the complete recorded metric and payload totals.

## Registered result

```text
M99 OCT-discovery profile: PASS
(8 cases, 7 discovered, 1 rejected)

M99 OCT-discovery checker: PASS
(8 cases, 7 exact discoveries, 1 cap rejection, 204 partitions)

20 passed
```

The registered schema is `schemas/m99-oct-discovery-v1.json`. Its canonical
summary SHA-256 is

```text
aa950a9ad2d2a40262b051ba4b8db9c5d799ba22edd48cefbf6cebafd81a349b
```

and its exact file SHA-256 is

```text
f53143cb773973ed2937a4c1b31cb8c3145e6b7eb3d52241325ef7a1484d69c6
```

The source M98 schema has file SHA-256
`c25cacc1e1e4217e87e6ff15b95c5c0356e7025b19833095feeef3f44bd45cb3`
and canonical summary SHA-256
`745cab13a67cae8f1e09ac084b75d78e870a0aacc88892be4facf032a5f3478f`.
The pinned M98 constructor source hash is
`6d2eba94384f2b09e6b1f06f1346d8fbdd68914b34c406d76cd0d9797566c1a4`.

## Source-bound discovery results

The public caps are the transversal sizes supplied in M98, but the M99
algorithm receives only the explicit graph and cap. It discovers the
following minimum OCTs or rejects when the cap is too small.

| case | cap | result | OCT size | compression calls | partitions | flow calls | augmentations |
|:---|---:|:---|---:|---:|---:|---:|---:|
| O1-triangle-pendant | 1 | exact | 1 | 4 | 18 | 17 | 8 |
| O2-C5 | 1 | exact | 1 | 5 | 15 | 15 | 2 |
| O3-bowtie | 1 | exact | 1 | 5 | 27 | 21 | 12 |
| O4-house | 1 | exact | 1 | 5 | 15 | 15 | 2 |
| O5-K4 | 2 | exact | 2 | 4 | 18 | 16 | 10 |
| O6-K5-e | 2 | exact | 2 | 5 | 21 | 19 | 12 |
| O7-K5-valid | 3 | exact | 3 | 5 | 45 | 29 | 28 |
| R1-K5-invalid | 2 | rejected | -- | 5 | 45 | 28 | 28 |

Across the eight cases, caps sum to 13 and discovered OCT sizes to 11.
There are 38 compression calls, 204 three-way partitions, 160 flow calls,
102 augmentations, and 158 residual searches. The seven OCT payloads use
51 bits. Composing them with M98 gives exact cover-number sum 21 and
79 output bits.

The rejected \(K_5\) case has OCT number three but cap two. Rejection occurs
at the fifth prefix; it is not inherited from M98's supplied-transversal
validity check.

## Exhaustive differential and adversarial cases

All \(2^{10}=1{,}024\) simple labeled graphs on five vertices are tested at
caps \(0,1,2,3\), for 4,096 exact comparisons. When the independent
enumerator finds an OCT within the cap, the constructor must return a valid
OCT of the same minimum size; otherwise it must reject. Tests also cover
parallel edges with an isolate, a separator that deletes a shared terminal,
and a zero-budget source-to-sink path.

The generator's deterministic witness need not be the lexicographically
first optimum under every flow tie. Exactness refers to minimum cardinality
and bipartite deletion, which are the theorem properties.

## Interpretation

EXP-0070 removes supplied OCT membership from seven small explicit M98
graphs and reconstructs exact covers through M98. It does not show that the
finite selector naturally emits the synthetic deleted-column systems,
construct complete factor-dependent types from an integer, prove that
arbitrary coverer graphs have logarithmic OCT number, or solve OCT for an
unrestricted cap in polynomial time. No general factoring claim follows.
