# M89 appendix-boundary editorial audit

Date: 2026-07-31

## Question and scope

M89 asks whether repository-facing audit material can move behind explicit
appendix boundaries without changing the focused papers' mathematical
narratives or losing a reproduction anchor. This is an editorial integrity
milestone. It does not change a theorem, proof status, experiment result,
promise, cost model, or the open status of general classical polynomial-time
integer factoring.

## Boundary inventory

The six focused manuscripts retain 34 mathematical main sections in their
previous order and all 21 bilingual representative claim IDs with visible
`PROVED` status. Each manuscript now contains exactly one `\appendix` command
and two labeled appendices:

1. primary-source positioning;
2. reproduction, limitations, and archival map.

The exact audit registry contains:

- 12 appendix headings and 12 stable appendix labels;
- 32 raw reproduction commands;
- 38 proof, implementation, experiment, schema, and ledger paths;
- 14 inspected-source citation anchors;
- six explicit limitation statements.

Raw commands, repository paths, experiment IDs, SHA-256 values, and internal
`Mxx` chronology tokens occur only after the appendix boundary. Claim IDs
remain in the main narrative because they are the stable evidence keys rather
than operational chronology.

## Independent checker

`scripts/check_m89_appendix_boundaries.py` does not derive its expected
section, appendix, command, path, citation, or claim registries from the
manuscript sources. It independently fixes those values, checks English/Korean
equality where required, and fails on either main-body leakage or appendix
anchor loss.

Reproduction:

```powershell
python scripts/check_m89_appendix_boundaries.py
pytest -p no:cacheprovider tests/test_m89_appendix_boundaries.py -q
```

Observed results:

```text
M89 appendix-boundary checker: PASS (6 papers, 34 main sections, 12 appendices, 32 commands, 38 paths, 14 source anchors)
12 passed in 0.04s
```

The 12 tests comprise one current-state check and 11 mutations: missing
appendix boundary, command leakage, path leakage, milestone leakage, main
section reordering, claim relocation to an appendix, command loss, path loss,
citation loss, limitation loss, and bilingual path drift.

## Projection and repository gates

The regenerated M82 projection accounts for 270 ledger claims, 21 focused
claims, and 249 archive-only claims. Its canonical summary SHA-256 is:

```text
e11189195fbdc904ffc0d5217555072555db1149de67f21bf66f4cafda16e6f8
```

The regenerated M83 audit retains six inspected sources, seven synchronized
rows, and no priority claim. Its file SHA-256 is:

```text
f53cc75e6b39e49bc53f488dd4401efb250d3ae7a54cdde11cece397ef487ac2
```

The complete Python suite passed with 348 tests and 593 subtests in 258.56
seconds. Foundation, M50, M82, M83, M84, M87, M88, publication consistency,
compileall, Ruff, mypy, Rust formatting/Clippy/36 tests, and the C# Release
build also passed.

## PDF build and visual review

All six focused manuscripts built with XeLaTeX. Their final page counts and
SHA-256 values are:

| Manuscript | Pages | PDF SHA-256 |
|---|---:|---|
| promise factorization EN | 6 | `31f761983b8d77a1ecbc98c9de8b9d56e57db0a2f8120482471f80433a41038b` |
| promise factorization KO | 5 | `8c94f656cdf253d7850e73687cb5a63fa74efeb1133d56a887e19325ac44a720` |
| cyclotomic extraction EN | 5 | `f8d02e325c89cd31ec4d2b3612133c767bd3627fbfae1e70317ce8b97926fb66` |
| cyclotomic extraction KO | 5 | `4eeef81fc123b366f15105edfcd3ac2bc58e741ec37efc10cc5d13dd6c4c13dc` |
| finite certificates EN | 6 | `b2ad126c639eda78ab6e18522a42b7986e8ddfdc508b9d4f33b7d011c6c373f8` |
| finite certificates KO | 6 | `f364d06581f711bd382e3134af79d17c0942d7499604bfee4f35698c3feb3427` |

Every page was rendered and inspected. No clipped appendix path, hidden
command, overlapping table, missing Korean glyph, or broken page transition
was found. The final logs contain zero selected undefined-reference,
undefined-citation, missing-character, overfull, underfull, LaTeX, package, or
rerun warnings.

## Conclusion

The narrative/audit split is complete and machine checked. The main
mathematical order and claim statuses are unchanged, while every registered
source and reproduction anchor remains reachable in an appendix. M90 will
apply the same principle inside the finite-certificate paper by keeping the
five reviewer-prioritized cases in the main narrative and moving the complete
26-row threshold chronology to a synchronized appendix.
