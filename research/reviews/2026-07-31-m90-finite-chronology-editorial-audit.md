# M90 finite-chronology editorial audit

Date: 2026-07-31

## Question and scope

M90 asks whether the finite-certificate paper can present the five
reviewer-prioritized threshold cases in its main narrative while retaining
the complete 26-row chronology in a synchronized, auditable appendix. It is
an editorial and artifact-integrity milestone. No threshold, population,
collision, repair coordinate, theorem status, or asymptotic claim changes.

## Main narrative

Both English and Korean papers retain:

1. base-cap injectivity for \(m=9,\ldots,15\);
2. the first base-cap failure at \(m=16\), on
   \(\{191,227,233\}\);
3. the length-28 threshold jump to \(L_{28}^\star=104\), its
   \(\{11867,12791\}\) predecessor collision, and five-coordinate repair;
4. the length-29 nonmonotonicity
   \(L_{29}^\star=103<L_{28}^\star=104\);
5. the length-34 endpoint \(L_{34}^\star=201\).

All seven focused claim IDs remain in main with `PROVED` status:
BAR-024, THM-004, THM-005, THM-014, THM-019, BAR-041, and BAR-046. The
asymptotic barriers and finite-scope warning remain adjacent to the
representative cases.

## Complete appendix chronology

The generated English and Korean table fragments now enter only inside the
certificate-reproduction appendix. Each retains all 26 rows
\(m=9,\ldots,34\), including population size, family-relative least cap,
local offset, predecessor collision buckets, repair-coordinate count, and
evidence IDs.

`scripts/check_m90_finite_chronology.py` is a 647-line standard-library
checker. It hard-codes the semantic fields of every row rather than deriving
expectations from the generator. It compares that registry independently
against:

- `schemas/m50-finite-threshold-summary-v1.json`;
- `paper/tables/finite-threshold-summary-en.tex`;
- `paper/tables/finite-threshold-summary-ko.tex`;
- the two finite-paper main/appendix boundaries.

Reproduction:

```powershell
python scripts/check_m90_finite_chronology.py
pytest -p no:cacheprovider tests/test_m90_finite_chronology.py -q
```

Observed targeted result:

```text
M90 finite-chronology checker: PASS (2 papers, 5 main representative cases each, 26 appendix rows each, 7 main claims each)
13 passed in 0.05s
```

The 13 tests comprise one current-state check and 12 mutations: full table
leakage into main, missing appendix input, subsection reordering, length-28
cap drift, length-28 repair-count drift, claim relocation, English cap drift,
Korean collision drift, reduced-endpoint drift, repair-status drift,
frozen-artifact cap drift, and a missing row. The complete repository suite
passed with 361 tests and 593 subtests in 262.07 seconds. Foundation, M50, M82,
M83, M84, M87, M88, M89, publication, compileall, Ruff, mypy, Rust
formatting/Clippy/36 tests, and the C# Release build passed.

## Projection and publication review

The regenerated M82 projection accounts for 270 claims, 21 focused and 249
archive-only. Its summary SHA-256 is:

```text
8a46a0805c8fb997b95da1996c638d2a7db9c5c52abac43abce8f2991e516ab1
```

The regenerated M83 audit retains six inspected sources, seven synchronized
rows, and no priority claim. Its file SHA-256 is:

```text
ae74638d4e3c3a7c8484607a7626ceb1f1ed041a1f5e1fc5b52ee1d55218d540
```

All six focused manuscripts built with XeLaTeX. Final logs contain zero
selected undefined-reference, undefined-citation, missing-character,
overfull, underfull, LaTeX, package, or rerun warnings.

| Manuscript | Pages | PDF SHA-256 |
|---|---:|---|
| promise factorization EN | 6 | `338223291e59365f201153f5eaa0a3cefedc15a5b1c614650034666f4b4d9acb` |
| promise factorization KO | 5 | `e545937c73c25a03810dc3ab9b6f23c8083bacb326c8b51526e21fa45bd4ce24` |
| cyclotomic extraction EN | 5 | `9981f149ec7c2e8dde89197b0b1db1b910dd478cb685ab90bdcbb08b9ad1c1f5` |
| cyclotomic extraction KO | 5 | `bde9a19f69ba282ecd701a051c484bcced987b9b8210a746271d156f01abbb26` |
| finite certificates EN | 7 | `803d3a2fcb02e58b61caa204eb61dd6346adfbc23b11e33cf9bd7c1952584275` |
| finite certificates KO | 6 | `97c63263317985aed21854f7fb340bed0d9dee76475f55d7d1210365781f7f5d` |

Every page was rendered and inspected. The longtable starts under the
chronology appendix heading, repeats its header across the page break, and
ends before the semantic-reproduction subsection. No row, heading, Korean
glyph, equation, or archive path is clipped or hidden.

## Conclusion

The five-case main narrative and complete 26-row appendix are synchronized
and independently machine checked. The paper remains a finite,
family-relative computer-assisted result through \(m=34\), not a
cryptographic-scale or general factoring result. M91 will investigate
whether the remaining 24 rows can receive a bounded no-project-import
semantic reconstruction, or whether a precise trusted-base barrier prevents
that consolidation.
