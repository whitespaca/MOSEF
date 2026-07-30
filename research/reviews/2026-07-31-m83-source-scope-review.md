# M83 adversarial source-scope review

## Review target

- Source ledgers `SRC-005` and `SRC-008`--`SRC-012`.
- `research/literature/M83-primary-source-search.md`.
- The seven-row bilingual positioning matrix and its JSON projection.
- Related-work text in the three focused paper pairs and both archival
  manuscripts.
- Bibliographic metadata and citation-key coverage.

This was a second-pass adversarial scope review of the repository changes. It
is not represented as an independent external priority survey.

## Threat checklist

| Threat | Test | Outcome |
|---|---|---|
| Search absence promoted to novelty | Inspect every matrix row, paper conclusion, and search limitation | Rejected; all seven rows use `NO_PRIORITY_CLAIM` |
| Abstract-only source used as a proof | Trace SRC-012 into BAR-018/BAR-019 prose | Rejected; Yao is context only and project proofs remain self-contained |
| Classical signature language presented as new | Compare BAR-001/BAR-024 wording with Katona pp. 174--175 | Repaired; abstract separating systems are explicitly established background |
| Cyclotomic proof technique hidden | Compare THM-003 positioning with Conway--Jones pp. 229--240 | Repaired; Galois, short vanishing sums, and rational-cosine methods are prior |
| Pollard procedure conflated with THM-001 | Compare Pollard pp. 526--528 with the theorem hypotheses | Rejected; hereditary recursion, fresh sampling, \(5/12\), and bit-cost closure are separated |
| Williams imported outside hypotheses | Recheck split/nonsplit and zero-discriminant boundary | Rejected; SRC-005 and both paper languages preserve the exclusion |
| Product tree treated as separator coverage | Compare Bernstein Algorithm 2.1 with finite-paper prose | Rejected; trees are charged evaluators, not coverage or injectivity theorems |
| Finite result generalized | Inspect M83 rows and focused finite conclusion | Rejected; one family and \(m\le34\) remain explicit |
| Source provenance overstated | Audit retrieval records and checksums | Repaired; Pollard distinguishes official metadata from mirrored page images, Katona marks partial inspection, Bernstein marks draft status |
| Bilingual drift | Parse language-independent row markers and paper row order | Rejected by the independent M83 checker and mutation tests |

## Source reconstruction notes

- Pollard's complete pages 521--528 were inspected in order. The practical
  method begins on page 526 and is distinct from the earlier theoretical
  result. The paper uses a fixed small base in the displayed practical
  procedure and does not state THM-001's recursive promise theorem.
- Williams's complete article had already been inspected under SRC-005. No
  change was made to the Lehmer-attribution boundary.
- Katona pages 174--175 suffice only for the separating-system definition,
  origin, and bounded-set-size problem statement. No later quantitative
  theorem is imported.
- Conway--Jones pages 229--240 were visually inspected. Their Galois and
  short-vanishing-sum machinery is close enough that THM-003 must not be
  advertised by search absence. The exact repository observable remains a
  self-contained specialization.
- Bernstein's seven-page author draft was inspected completely. Algorithm
  2.1 and Theorems 2.2--2.3 establish evaluation semantics and cost, not
  selector construction.
- Yao's official metadata and abstract were inspected. The full article was
  not used; the checker has a regression test that rejects promotion from
  `ABSTRACT_ONLY`.

## Review result

PASS for M83's bounded acceptance criterion after the repairs above. The
review establishes conservative positioning, not novelty. It found no basis
to label any row "plausibly new" and no basis to label the exact project
results known duplicates. General classical polynomial-time factoring
remains open.
