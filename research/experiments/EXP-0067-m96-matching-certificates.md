# EXP-0067: M96 matching-equality perturbation certificates

## Status

`EMPIRICAL` for the exact frozen source binding, deterministic eight-case
perturbation grammar, finite cover/matching classifications, registered
witness costs, and mutation tests. The matching-equality implication is
proved separately as `THM-025`; the triangle counterexample is `REF-065`.

## Deterministic commands

```powershell
python scripts/run_m96_matching_certificate_profile.py
python scripts/generate_m96_matching_certificate_schema.py --check
python scripts/check_m96_matching_certificate.py
pytest -p no:cacheprovider tests/test_m96_matching_certificate.py -q
ruff check scripts/run_m96_matching_certificate_profile.py scripts/generate_m96_matching_certificate_schema.py scripts/check_m96_matching_certificate.py tests/test_m96_matching_certificate.py
mypy --strict --explicit-package-bases scripts/run_m96_matching_certificate_profile.py scripts/generate_m96_matching_certificate_schema.py scripts/check_m96_matching_certificate.py tests/test_m96_matching_certificate.py
```

No random seed is used. The 431-line production checker uses only the Python
standard library and imports neither the generator nor an M95 checker. It
pins the exact M95 schema, independently recovers the length-27 M92 looped
\(K_5\) seed, applies the hard-coded perturbation grammar, reconstructs every
residual edge, verifies the cover and matching witnesses, and independently
enumerates the bounded five-vertex optima as defense.

## Registered result

```text
M96 matching-certificate profile: PASS
(8 perturbations, 5 equality certificates, 3 matching gaps,
43 witness bits)

M96 matching-certificate checker: PASS
(8 perturbations, 5 equality certificates, 3 matching gaps,
43 witness bits)

15 passed
```

The registered schema is
`schemas/m96-matching-certificates-v1.json`. Its canonical summary SHA-256
is

```text
cb8f8a2f5d88e3bcba34260b41a73e0ff1d87a052d348a83fa709af2da738fb4
```

and its exact file SHA-256 is

```text
3326cda404240bdb1f60febdc71129a6d8215d39793d47c2b5f169fbeb46f3d1
```

The M95 source anchor has file SHA-256
`e5e069554a3249e04084b505b590ff197ff26e75e4fd2467115caeeca1d08e03`
and canonical summary SHA-256
`0b99798516bda32cc78e8fd7474fbaddce9cd024a021d81c08fca8514c64154a`.
The selected M92 length-27 instance hash is
`55830ccb41686b432fc7710380652937209fd24885c2ad4de81607784d0a6348`.

## Perturbation grammar

The seed has types \(T_0,\ldots,T_4\), one loop at every type, and every ten
ordinary type pair. For \(r=1,\ldots,5\), delete the loops on
\(T_0,\ldots,T_{r-1}\). Where registered, also delete the ordinary edge
\(\{T_0,T_1\}\). The eight retained systems are all nonempty,
pairwise-distinct complete normal forms and none is one of the three exact
M95 templates.

| perturbation | forced types | residual graph | \(\tau\) | \(\nu\) | result |
|:---|---:|:---|---:|---:|:---|
| U1-keep-edges | 4 | isolated \(T_0\) | 0 | 0 | equality |
| U2-keep-edges | 3 | \(K_2\) | 1 | 1 | equality |
| U2-drop-e01 | 3 | two isolated vertices | 0 | 0 | equality |
| U3-keep-edges | 2 | \(K_3\) | 2 | 1 | gap |
| U3-drop-e01 | 2 | \(P_3\) | 1 | 1 | equality |
| U4-keep-edges | 1 | \(K_4\) | 3 | 2 | gap |
| U4-drop-e01 | 1 | \(K_4-e\) | 2 | 2 | equality |
| U5-drop-e01 | 0 | \(K_5-e\) | 3 | 2 | gap |

The residual cover numbers sum to 12, matching numbers sum to 9, and full
repair numbers including forced loops sum to 28. Every observed gap is one.

## Certificate cost

For the fixed seed, a type index costs three bits, a column index costs four
bits, and the shared witness length costs three bits. The five tight cases
therefore require

\[
\sum (3+7k)=43
\]

aggregate witness bits. Their narrow witness-verification ledger contains 21
tests: one size check per case, one scan per residual edge, and two endpoint
checks per matching edge. These costs exclude the already reconstructed
graph, JSON syntax, paths, hashes, and bound source bytes.

The three gap cases store cover and maximum-matching witnesses for finite
audit, but they are explicitly marked `insufficient`; their exact cover
numbers are not attributed to matching equality.

## Interpretation

EXP-0067 shows that matching equality extends the M95 graph method to five
synthetic systems outside the loop-only/clique template grammar, including
\(P_3\) and \(K_4-e\), without subset-enumeration payload. It also preserves
three exact finite failures, beginning with \(K_3\). This bounded experiment
does not claim that equality witnesses exist or can be found efficiently for
arbitrary coverer graphs, does not recognize hidden factors, and does not
support a general factoring claim.
