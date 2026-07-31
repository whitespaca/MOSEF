# EXP-0069: M98 odd-cycle-transversal cover audit

## Status

`EMPIRICAL` for the frozen source binding, eight synthetic target graphs,
seven deterministic exact constructors, one invalid-transversal rejection,
the complete 24-branch ledger, finite exact audits, payload totals, and
mutation tests. Constructor correctness is proved separately as `THM-027`;
the unrestricted-polynomial promotion is refuted as `REF-067`.

## Deterministic commands

```powershell
python scripts/run_m98_oct_cover_profile.py
python scripts/generate_m98_oct_cover_schema.py --check
python scripts/check_m98_oct_cover.py
pytest -p no:cacheprovider tests/test_m98_oct_cover.py -q
ruff check scripts/run_m98_oct_cover_profile.py scripts/generate_m98_oct_cover_schema.py scripts/check_m98_oct_cover.py tests/test_m98_oct_cover.py
mypy --strict --explicit-package-bases scripts/run_m98_oct_cover_profile.py scripts/generate_m98_oct_cover_schema.py scripts/check_m98_oct_cover.py tests/test_m98_oct_cover.py
```

No random seed is used. The 819-line production checker uses only the Python
standard library and imports neither the M98 generator nor the M97
constructor. It pins the exact M95 schema, the M92 length-27 looped-\(K_5\)
seed, and the exact M97 constructor source. It reconstructs all deleted
columns, validates each supplied transversal, independently rebuilds every
branch, and enumerates bounded cover and matching optima only as defense.

## Registered result

```text
M98 OCT-cover profile: PASS
(8 cases, 7 exact constructors, 1 rejection, 24 explicit branches)

M98 OCT-cover checker: PASS
(8 cases, 7 exact constructors, 1 rejection, 24 branches)

19 passed
```

The registered schema is `schemas/m98-oct-cover-v1.json`. Its canonical
summary SHA-256 is

```text
745cab13a67cae8f1e09ac084b75d78e870a0aacc88892be4facf032a5f3478f
```

and its exact file SHA-256 is

```text
c25cacc1e1e4217e87e6ff15b95c5c0356e7025b19833095feeef3f44bd45cb3
```

The M95 source anchor has file SHA-256
`e5e069554a3249e04084b505b590ff197ff26e75e4fd2467115caeeca1d08e03`
and canonical summary SHA-256
`0b99798516bda32cc78e8fd7474fbaddce9cd024a021d81c08fca8514c64154a`.
The selected M92 length-27 instance hash is
`55830ccb41686b432fc7710380652937209fd24885c2ad4de81607784d0a6348`.
The pinned M97 constructor source hash is
`d811f6cf39c0ae00b28e17bb93d322b07a2fac22da236a66d31e4f75fc1dfa39`.

## Target-graph grammar and results

For each case, delete the loops on a prefix of
\(T_0,\ldots,T_4\), making that prefix residual. Delete every ordinary edge
inside the prefix that is absent from the registered target graph, then
supply the listed transversal. Edges incident to the remaining forced types
are retained. Every full retained system remains a nonempty,
pairwise-distinct complete normal form.

| case | forced | residual graph | edges | \(s\) | branches | feasible | \(\tau\) | \(\nu\) | repair | result |
|:---|---:|:---|---:|---:|---:|---:|---:|---:|---:|:---|
| O1-triangle-pendant | 1 | triangle + pendant | 4 | 1 | 2 | 2 | 2 | 2 | 3 | exact |
| O2-C5 | 0 | \(C_5\) | 5 | 1 | 2 | 2 | 3 | 2 | 3 | exact |
| O3-bowtie | 0 | two triangles sharing a vertex | 6 | 1 | 2 | 2 | 3 | 2 | 3 | exact |
| O4-house | 0 | four-cycle with roof | 6 | 1 | 2 | 2 | 3 | 2 | 3 | exact |
| O5-K4 | 1 | \(K_4\) | 6 | 2 | 4 | 3 | 3 | 2 | 4 | exact |
| O6-K5-e | 0 | \(K_5-e_{01}\) | 9 | 2 | 4 | 3 | 3 | 2 | 3 | exact |
| O7-K5-valid | 0 | \(K_5\) | 10 | 3 | 8 | 4 | 4 | 2 | 4 | exact |
| R1-K5-invalid | 0 | \(K_5\) | 10 | 2 | 0 | 0 | 4 | 2 | 4 | rejected |

The seven valid cases enumerate 24 branches, of which 18 are feasible. The
eight supplied transversal sizes sum to 13. Across all cases, residual
cover numbers sum to 25, matching numbers to 16, and full repair numbers to
27. The maximum matching gap is two and the maximum registered transversal
size is three.

The invalid \(K_5\) input supplies only \(\{T_0,T_1\}\); deleting it leaves
the explicit odd cycle
\(T_2,T_3,T_4,T_2\). The constructor therefore rejects before branch
enumeration. The valid \(K_5\) case supplies three vertices and exposes all
eight branches, four of them feasible.

## Independent exhaustive differential and payloads

The implementation differential covers all 64 simple labeled graphs on
four vertices and all 16 proposed transversal subsets, for 1,024
graph/transversal pairs. Whenever deleting the subset leaves a bipartite
graph, the constructor output is compared with a bounded exact
minimum-cover oracle. Otherwise rejection is required.

For the fixed five-type seed, type and framed-size fields each cost three
bits. All eight supplied transversal records use 63 bits in aggregate. The
seven valid minimum-cover outputs use 84 framed bits. The experimental
schema retains every branch for auditability; the theorem algorithm need
not retain the full exponential ledger.

## Interpretation

EXP-0069 demonstrates a deterministic exact path on seven small
non-bipartite residual coverer graphs when a valid transversal is supplied,
including examples with matching gaps. It does not discover those
transversals, prove a logarithmic transversal bound, show that the frozen
selector naturally produces the deleted-column systems, or construct the
factor-dependent complete type list publicly. The \(2^s\) dependence is
explicit. No general factoring claim follows.
