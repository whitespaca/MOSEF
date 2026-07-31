# EXP-0071: M100 public coverer-graph construction audit

## Status

`EMPIRICAL` for the frozen \(16\le m\le34\) public reconstruction, exact
work ledger, \(k(m)=\lceil\log_2m\rceil\) cap checks, deterministic schema,
and mutation tests. The factor-independent finite constructor and its
explicit-size boundary are proved separately as `THM-029`.

## Deterministic commands

```powershell
python scripts/run_m100_public_coverer_graph_audit.py
python scripts/generate_m100_public_coverer_graph_schema.py --check
python scripts/check_m100_public_coverer_graph.py
pytest -p no:cacheprovider tests/test_m100_public_coverer_graph.py -q
ruff check scripts/run_m100_public_coverer_graph_audit.py scripts/generate_m100_public_coverer_graph_schema.py scripts/check_m100_public_coverer_graph.py tests/test_m100_public_coverer_graph.py
mypy --strict --explicit-package-bases scripts/run_m100_public_coverer_graph_audit.py scripts/generate_m100_public_coverer_graph_schema.py scripts/check_m100_public_coverer_graph.py tests/test_m100_public_coverer_graph.py
```

No random seed is used. The independent checker uses only the Python
standard library and imports neither the M100 generator nor M91. It
separately implements the balanced-prime sieve, DEF-032 descriptor grammar,
all eight primitive modular exits including the simple-root cofactor branch,
pair coverage, complete-type enumeration, graph reduction, and bounded exact
OCT defense.

## Registered result

```text
M100 public coverer-graph audit: PASS
(19 instances, 37 complete types, 4650888 primitive tests, max OCT 2)

M100 public coverer-graph checker: PASS
(19 instances, 37 complete types, 4650888 primitive tests, max OCT 2)

19 passed
```

The registered schema is
`schemas/m100-public-coverer-graph-v1.json`. Its canonical and exact file
SHA-256 values are respectively

```text
6a91891acef634c31e6a05accd38240d959740168816b163bd25763258473181
7fe9253740e42cdd7c31cb63d3768dad45764010c2f9e5e7ebf46a705ba7981d
```

## Public dependency chain

| layer | public role | semantic status |
|:---|:---|:---|
| M50 | finite row, cap, and source registry | source registry |
| M91 | population, selected-coordinate confinement, raw-selector persistence | EMP-062 |
| M92 | late repair cap/type comparison | EMP-063 |
| M93 | early repair cap/type comparison | EMP-064 |
| M95 | coverer-graph comparison target | EMP-066 |
| M100 | direct new-coordinate type reconstruction and public cap audit | EMP-071 |

The M100 generator does not accept tracked primes, collision blocks, complete
types, graph edges, or a per-row OCT cap as construction inputs. It enumerates
the balanced population from \(m\), derives the baseline partition from
public baseline coordinates, enumerates every new public coordinate from the
two caps, and derives the cap by the fixed formula
\(k(m)=\lceil\log_2m\rceil\). The M95 graph is opened only as a
post-construction semantic comparison oracle; bucket and type order are
ignored in that comparison.

The selected coordinate lists remain public collision-completeness
certificates. M91 verifies them semantically; their hashes alone are not
treated as completeness evidence.

## Exact finite ledger

| quantity | total |
|:---|---:|
| instances | 19 |
| public population entries | 12,209 |
| population-label bits | 193,753 |
| baseline public coordinates | 421,541 |
| selected/raw baseline primitive evaluations | 39,426,052 |
| baseline persistence descriptor/point evaluations | 5,253,406 |
| baseline persistence primitive tests | 42,027,248 |
| tracked collision points | 55 |
| unresolved pairs | 64 |
| newly admitted descriptors | 152,879 |
| new descriptor/prime evaluations | 581,361 |
| primitive coordinate tests | 4,650,888 |
| complete nonzero coverage types | 37 |
| forced types | 30 |
| residual vertices / edges | 7 / 9 |
| exact OCT-number sum / maximum | 3 / 2 |
| M95 graph payload | 1,063 bits |

The nine M92 rows use a selected baseline subfamily plus exhaustive raw
persistence. The ten M93 rows use full-raw-family refinement. Counting the
baseline evaluation and persistence phases together with the new-coordinate
phase gives 86,104,188 public primitive tests.

The early M93 rows contribute 7,398 descriptors, 19,365 descriptor/prime
evaluations, 154,920 primitive tests, and 18 types. The late M92 rows
contribute 145,481 descriptors, 4,495,968 primitive tests, and 19 types.

## Public OCT schedule

The schedule is not supplied row advice:
\[
k(m)=\lceil\log_2m\rceil.
\]
Seventeen graphs become empty after forced loops. The length-16 loopless
\(K_3\) has exact OCT number one, and the length-24 loopless \(K_4\) has
exact OCT number two. Both are below the public cap, as are the empty
graphs. This is a finite observation, not an asymptotic theorem.

## Falsification

The schema includes the two-element-universe hash-only counterexample from
THM-029. A digest correctly binds two claimed singleton types and their
claimed minimum two, yet an omitted realized full-universe type makes the
actual minimum one. Mutation tests also change source bindings, the
constructor contract, caps, type masks, OCT minima, the counterexample,
the bit-polynomial boundary, and the scope exclusions.

## Interpretation

M100 resolves the hidden-factor question for the frozen graph layer:
candidate prime labels, coverage types, graph edges, and the logarithmic cap
are public and reconstructible without knowing the factors of a particular
integer. It does not resolve the complexity question. The registered route
explicitly enumerates \(\mathcal P_m\), whose size is
\(\Omega(2^{m/2}/m)\) by BAR-041, so it is not polynomial in \(m\).
No compact asymptotic completeness proof, future logarithmic-OCT theorem,
general promise recognizer, or general classical polynomial-time factoring
algorithm is supplied.
