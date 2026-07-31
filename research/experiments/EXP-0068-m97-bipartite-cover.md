# EXP-0068: M97 constructive bipartite-cover audit

## Status

`EMPIRICAL` for the frozen source binding, eight synthetic target graphs,
deterministic constructor outputs, finite exact audits, operation and output
ledgers, and mutation tests. Constructor correctness is proved separately as
`THM-026`; the non-bipartite equality boundary is `REF-066`.

## Deterministic commands

```powershell
python scripts/run_m97_bipartite_cover_profile.py
python scripts/generate_m97_bipartite_cover_schema.py --check
python scripts/check_m97_bipartite_cover.py
pytest -p no:cacheprovider tests/test_m97_bipartite_cover.py -q
ruff check scripts/run_m97_bipartite_cover_profile.py scripts/generate_m97_bipartite_cover_schema.py scripts/check_m97_bipartite_cover.py tests/test_m97_bipartite_cover.py
mypy --strict --explicit-package-bases scripts/run_m97_bipartite_cover_profile.py scripts/generate_m97_bipartite_cover_schema.py scripts/check_m97_bipartite_cover.py tests/test_m97_bipartite_cover.py
```

No random seed is used. The 668-line production checker uses only the Python
standard library and imports neither the generator nor the M96 checker. It
pins the exact M95 schema and M92 length-27 looped-\(K_5\) seed, reconstructs
all deleted columns, verifies every bipartition, cover, matching, and odd
cycle, and independently enumerates the bounded five-vertex optima as
defense.

## Registered result

```text
M97 bipartite-cover profile: PASS
(8 cases, 6 constructed bipartite repairs,
1 nonbipartite equality, 1 matching gap)

M97 bipartite-cover checker: PASS
(8 cases, 6 constructed repairs,
1 nonbipartite equality, 1 matching gap)

19 passed
```

The registered schema is `schemas/m97-bipartite-cover-v1.json`. Its
canonical summary SHA-256 is

```text
4e421881658b411e636bf8abe862cd73c09a8def1ff609f9ef5eb66659790492
```

and its exact file SHA-256 is

```text
46c79936ec625a462d39880c8ddc8f1ce7e4416a23d590afffe428a729a13db0
```

The M95 source anchor has file SHA-256
`e5e069554a3249e04084b505b590ff197ff26e75e4fd2467115caeeca1d08e03`
and canonical summary SHA-256
`0b99798516bda32cc78e8fd7474fbaddce9cd024a021d81c08fca8514c64154a`.
The selected M92 length-27 instance hash is
`55830ccb41686b432fc7710380652937209fd24885c2ad4de81607784d0a6348`.

## Target-graph grammar

For each case, delete the loops on a prefix of
\(T_0,\ldots,T_4\), making that prefix residual. Delete every ordinary edge
inside the prefix that is absent from the registered target graph. Edges
incident to the remaining forced types are retained. Every full retained
system remains a nonempty, pairwise-distinct complete normal form and is
outside the three M95 templates.

| case | forced | residual graph | edges | \(\tau\) | \(\nu\) | repair | constructor |
|:---|---:|:---|---:|---:|---:|---:|:---|
| B1-P3 | 2 | \(P_3\) | 2 | 1 | 1 | 3 | exact |
| B2-P4 | 1 | \(P_4\) | 3 | 2 | 2 | 3 | exact |
| B3-K1-3 | 1 | \(K_{1,3}\) | 3 | 1 | 1 | 2 | exact |
| B4-C4 | 1 | \(C_4\) | 4 | 2 | 2 | 3 | exact |
| B5-P5 | 0 | \(P_5\) | 4 | 2 | 2 | 2 | exact |
| B6-K2-3 | 0 | \(K_{2,3}\) | 6 | 2 | 2 | 2 | exact |
| N1-triangle-pendant | 1 | triangle + pendant | 4 | 2 | 2 | 3 | non-bipartite reject |
| N2-C5 | 0 | \(C_5\) | 5 | 3 | 2 | 3 | non-bipartite reject |

The six bipartite cases require ten augmentations and sixteen searches
including one unsuccessful terminal search per case. Their residual cover
and matching numbers both sum to ten. Across all eight cases, cover numbers
sum to 15, matching numbers to 14, and full repair numbers to 21.

The implementation differential additionally covers all 689 simple
bipartite graphs with zero through three vertices on each side, comparing
the constructed matching and cover sizes against bounded exact oracles. A
separate regression covers parallel edge occurrences and isolated vertices.

## Constructed output and boundary

For the fixed five-type, fifteen-column seed, type, column, and size fields
cost three, four, and three bits. The six constructed equality outputs use
88 framed bits and 48 narrow verification tests. These are output
certificates, not advice required by the constructor.

The triangle-with-pendant case is intentionally rejected by the restricted
bipartite constructor, but its finite audit records
\(\tau=\nu=2\). Its independent `THM-025` equality certificate costs 17
bits. This shows that bipartiteness is not necessary for matching equality.
The \(C_5\) case records the complementary one-unit gap.

## Interpretation

EXP-0068 demonstrates a deterministic constructive path on six small
bipartite residual coverer graphs outside the M95 templates. It does not
claim that the frozen selector naturally produces these deleted-column
systems, that every coverer graph is bipartite, or that the factor-dependent
complete type list is publicly constructible. The bounded exact enumeration
belongs only to experiment defense and is not part of the `THM-026`
constructor. No general factoring claim follows.
