# EXP-0065: M94 complete-graph incidence certificates

## Status

`EMPIRICAL` for the frozen M93 source binding, exhaustive incidence
reconstruction, registered cost comparison, deterministic schema, and
mutation tests. The coverer-graph equivalence and complete-graph minimum are
proved separately as `THM-023`.

## Deterministic commands

```powershell
python scripts/run_m94_clique_incidence_audit.py
python scripts/generate_m94_clique_incidence_schema.py --check
python scripts/check_m94_clique_incidence_certificate.py
pytest -p no:cacheprovider tests/test_m94_clique_incidence_certificate.py -q
ruff check scripts/run_m94_clique_incidence_audit.py scripts/generate_m94_clique_incidence_schema.py scripts/check_m94_clique_incidence_certificate.py tests/test_m94_clique_incidence_certificate.py
mypy --strict --explicit-package-bases scripts/run_m94_clique_incidence_audit.py scripts/generate_m94_clique_incidence_schema.py scripts/check_m94_clique_incidence_certificate.py tests/test_m94_clique_incidence_certificate.py
```

No random seed is used. The production checker uses only the Python standard
library and imports neither the generator nor an earlier checker. It reads the
frozen M93 schema, independently reconstructs every mask from its binary
pattern, reconstructs every universe element's complete coverer set, checks
the complete-graph incidence property, and runs a bounded exact-cover defense.

## Registered result

```text
M94 clique-incidence audit: PASS
(2 instances, 9 pairs, 18 incidences, 56 payload bits saved)

M94 clique-incidence certificate checker: PASS
(2 instances, 9 pairs, 18 incidences, 56 payload bits saved)

11 passed
```

The registered schema is
`schemas/m94-clique-incidence-certificates-v1.json`. Its canonical summary
SHA-256 is

```text
9219f1aeb26d1e50b33d30437ee9bab29b27792d37af667c0c7a3547e43b1053
```

The source M93 file SHA-256 is
`3fba1bc8ef78594e32083f8576a43874159390bbccbcc669b658015ce8431641`,
and its canonical summary SHA-256 is
`77c8ae289277875815e7744b37456627f619fc601d4fb2ccca35031b7f248aae`.

## Incidence result

The length-16 instance has three universe elements and three types. Every
element has exactly two coverers, and the coverer sets are the three edges of
\(K_3\). The length-24 instance has six universe elements and four types,
with coverer sets equal to the six edges of \(K_4\). Thus `THM-023` gives the
exact repair numbers two and three without an explicit upper-index list or
one lower entry per undersized subset.

Across the two instances, the checker audits seven tracked points, nine
universe pairs, seven complete types, and eighteen incidence bits equal to
one. The explicit `coverer_sets` records in the JSON are redundant audit
traces reconstructed from the masks; they are not charged as mathematical
certificate payload.

## Cost comparison

| input length | incumbent witness | incumbent payload | clique payload | saved | incumbent tests | clique tests | delta |
|---:|:---|---:|---:|---:|---:|---:|---:|
| 16 | cardinality | 50 | 42 | 8 | 16 | 21 | +5 |
| 24 | subset obstructions | 136 | 88 | 48 | 54 | 54 | 0 |
| total | mixed | 186 | 130 | 56 | 70 | 75 | +5 |

The structural certificate removes all upper-witness and lower-witness index
payload. The conservative checker must instead scan the complete incidence
matrix and its pair slots. Therefore the criterion strictly reduces payload
for both instances but does not strictly reduce verifier work. The attempted
strict-dominance shortcut is preserved as `REF-063` and NR-062.

## Mutation and differential coverage

Eleven targeted tests cover the registered portfolio, deterministic
regeneration, standard-library/import and line budgets, both exact repairs,
the complete \(K_3/K_4\) edge lists, direct-mask incidence differential,
payload/test deltas, and rehashed mutations of a coverer trace, source anchor,
coverage mask, and cost ledger. A source-rebound mutation that gives one
universe element three coverers is also rejected.

## Interpretation

EXP-0065 answers the M94 structural question positively: the two private-pair
failures share the same complete-graph incidence certificate. The result is a
finite combinatorial compression of already reconstructed type systems. It
does not independently repeat the M93 number-theoretic enumeration, extend
the selector, establish an asymptotic law, recognize hidden factors, or solve
general classical polynomial-time integer factorization.
