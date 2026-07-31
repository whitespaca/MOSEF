# EXP-0066: M95 portfolio-wide coverer-graph profile

## Status

`EMPIRICAL` for the two frozen source bindings, nineteen complete coverer
matrices, exact template classification, registered cost comparison,
deterministic schema, and mutation tests. The looped-graph reduction,
forced-set decomposition, and rank-two universality boundary are proved
separately as `THM-024`.

## Deterministic commands

```powershell
python scripts/run_m95_coverer_graph_profile.py
python scripts/generate_m95_coverer_graph_schema.py --check
python scripts/check_m95_coverer_graph_certificate.py
pytest -p no:cacheprovider tests/test_m95_coverer_graph_certificate.py -q
ruff check scripts/run_m95_coverer_graph_profile.py scripts/generate_m95_coverer_graph_schema.py scripts/check_m95_coverer_graph_certificate.py tests/test_m95_coverer_graph_certificate.py
mypy --strict --explicit-package-bases scripts/run_m95_coverer_graph_profile.py scripts/generate_m95_coverer_graph_schema.py scripts/check_m95_coverer_graph_certificate.py tests/test_m95_coverer_graph_certificate.py
```

No random seed is used. The 571-line production checker uses only the Python
standard library and imports neither the generator nor any M92--M94 checker.
It binds both predecessor schemas, independently reconstructs every mask from
its binary point pattern, reconstructs every coverer column, checks its exact
loop/clique template, verifies the implicit upper witness, and performs a
bounded exact-cover defense.

## Registered result

```text
M95 coverer-graph profile: PASS
(19 instances, 64 columns, 30 loops, 34 ordinary edges,
165 payload bits saved)

M95 coverer-graph certificate checker: PASS
(19 instances, 64 columns, 30 loops, 34 ordinary edges,
165 payload bits saved)

18 passed
```

The registered schema is
`schemas/m95-coverer-graph-profile-v1.json`. Its canonical summary SHA-256 is

```text
0b99798516bda32cc78e8fd7474fbaddce9cd024a021d81c08fca8514c64154a
```

and its exact file SHA-256 is

```text
e5e069554a3249e04084b505b590ff197ff26e75e4fd2467115caeeca1d08e03
```

The two source anchors are:

| source | complete-type dependency | file SHA-256 | summary SHA-256 |
|:---|:---|:---|:---|
| M92 | EMP-062 | `0c58d6d28079aac4975861836b714c9c8d63e805bbc86c5c3b101b3c85ae636e` | `3bf4b744d30d31f5e52725ca9cb70302bc4654ab1e7cfbe1707448392dbc19b0` |
| M93 | EMP-064 | `3fba1bc8ef78594e32083f8576a43874159390bbccbcc669b658015ce8431641` | `77c8ae289277875815e7744b37456627f619fc601d4fb2ccca35031b7f248aae` |

## Portfolio classification

All nineteen coverer systems have rank at most two. More strongly, every
system is one exact duplicate-free template:

- 12 loop-only systems;
- 5 looped cliques containing every singleton and every ordinary pair;
- 2 loopless cliques, the M94 \(K_3\) and \(K_4\) systems.

The first seventeen systems have a singleton coverer for every type, so every
type is forced and the exact repair number is \(t\). The two loopless cliques
have exact repair number \(t-1\). The portfolio contains 55 tracked points,
64 universe columns, 37 types, 30 singleton columns, 34 two-coverer columns,
98 positive incidences, and total exact repair count 35.

## Cost comparison

| source | instances | incumbent payload | graph payload | saved | incumbent tests | graph tests | delta |
|:---|---:|---:|---:|---:|---:|---:|---:|
| M92 | 9 | 745 | 663 | 82 | 397 | 375 | -22 |
| M93 | 10 | 483 | 400 | 83 | 145 | 145 | 0 |
| total | 19 | 1,228 | 1,063 | 165 | 542 | 520 | -22 |

The graph templates remove all explicit upper-index and lower-witness-index
payload. The JSON coverer lists remain redundant audit traces and are not
charged. Aggregate compression is not per-instance strict dominance:
one-type rows save no payload, several rows tie in tests, and length 16 uses
five more registered tests.

## Rank-two boundary

The schema also records a finite counterexample to the shortcut that the
rank-two column profile determines the exact minimum. Both \(K_{1,3}\) and
\(P_4\) have four types, three universe elements, and three degree-two
coverer columns. Their exact vertex-cover numbers are respectively one and
two. `REF-064` therefore preserves the need for graph-class structure or a
separate lower certificate.

## Mutation and differential coverage

Eighteen tests cover deterministic generation, standard-library/import and
line budgets, all nineteen templates, forced-loop and clique minima, direct
mask/coverer differential equality, cost totals, the star/path boundary,
seven rehashed schema mutations, a source-rebound rank-three mutation, the
\(K_2\) distinct-type regression, and duplicate-free template slots.

## Interpretation

EXP-0066 answers M95 for the frozen portfolio: higher-rank coverer
hypergraphs are absent, and all nineteen instances admit one unified looped
graph certificate. This is a compression and classification of already
complete finite type lists. It does not establish rank at most two beyond the
registered sources, provide an exact solver for arbitrary graphs, recognize
hidden factors, establish an asymptotic selector law, or solve general
classical polynomial-time integer factorization.
