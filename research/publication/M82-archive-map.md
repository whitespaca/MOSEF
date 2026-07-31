# M82 focused-paper archive map

Date: 2026-07-31

## Purpose

M82 is an editorial projection milestone. It does not promote, demote, or
delete a mathematical claim. The authoritative full record remains:

- English archival monograph: `paper/main.tex`
- Korean archival monograph: `paper/main-ko.tex`
- claim and evidence ledger: `research/CLAIMS.md`
- negative-result ledger: `research/NEGATIVE_RESULTS.md`

The machine-readable projection is
`schemas/m82-paper-portfolio-v1.json`.

## Focused papers

| Paper | English | Korean | Representative claims |
|---|---|---|---|
| A: promise factorization | `paper/focused/promise-factorization-en.tex` | `paper/focused/promise-factorization-ko.tex` | THM-001, BAR-001, BAR-002, LEM-003, THM-002, BAR-003, BAR-004 |
| B: cyclotomic extraction | `paper/focused/cyclotomic-extraction-en.tex` | `paper/focused/cyclotomic-extraction-ko.tex` | BAR-018, BAR-019, THM-003, BAR-020, BAR-021, BAR-022, BAR-023 |
| C: finite certificates | `paper/focused/finite-certificates-en.tex` | `paper/focused/finite-certificates-ko.tex` | BAR-024, THM-021, THM-022, THM-004, THM-005, THM-014, THM-019, BAR-041, BAR-046 |

The promise and cyclotomic pairs have seven front-facing claim IDs each; the
finite pair has nine. The papers use the same status token as
`research/CLAIMS.md`, link to their proof or reproduction anchors, and state
their own exclusions.

## Coverage and trust boundary

- 279 authoritative claim IDs are projected.
- 23 claim IDs are front-facing in exactly one focused paper pair.
- 256 claim IDs remain archival-only.
- A claim is not absent merely because it is not front-facing.
- The focused paper source is not a second authority for status.
- The generator records source hashes and the full archive-only list.
- The independent checker does not import the generator and fixes the
  authoritative ledger, archive, focused-paper, reproduction-anchor, and
  required source-hash paths in its own implementation.
- M85 and M86 reduce the finite-certificate trusted computing base for the
  representative M41 and final M46 rows. The other 24 rows retain the
  integrated semantic path.
- M87 adds a synchronized four-row cost ledger before section 1 of every
  focused manuscript and enforces 200--300 lexical-token abstracts. It
  changes no representative claim ID or status; the complete editorial audit
  is `research/reviews/2026-07-31-m87-focused-cost-model-editorial-audit.md`.
- M88 adds a reader-facing heading to every representative claim using five
  bilingual label families. The stable ID and `PROVED` status remain visible,
  ordered, and machine checked; the complete map is
  `research/reviews/2026-07-31-m88-reader-label-editorial-audit.md`.
- M89 moves primary-source positioning and repository-facing reproduction,
  chronology, limitation, and archive material behind one explicit appendix
  boundary in every focused manuscript. The 34 mathematical main sections
  retain their order; the complete anchor audit is
  `research/reviews/2026-07-31-m89-appendix-boundary-editorial-audit.md`.
- M90 moves the generated 26-row finite threshold chronology into the finite
  paper's reproduction appendix. The main narrative retains the five
  reviewer-prioritized cases and all nine current focused claim IDs; the complete
  row audit is
  `research/reviews/2026-07-31-m90-finite-chronology-editorial-audit.md`.
- M91 reconstructs all 26 finite rows from the shared public grammar without
  importing project code. Its 16-source inventory and measured reviewer bound
  are in `research/reviews/2026-07-31-m91-cleanroom-inventory.md` and
  `research/experiments/EXP-0062-m91-all-row-semantic-checker.md`.
- M92 quotients the nine repair searches to 19 exact pair-coverage types and
  certifies their minima with covering upper witnesses and private-pair lower
  witnesses. The proof and source-bound execution record are
  `research/proofs/THM-021-pair-cover-certificate.md` and
  `research/experiments/EXP-0063-m92-pair-cover-certificates.md`.
- M93 independently reconstructs the ten early repairs, refutes completeness
  of private-pair witnesses at lengths 16 and 24, and supplies exact
  cardinality or subset-obstruction alternatives. Its proof and execution
  record are `research/proofs/THM-022-subset-obstruction-certificate.md` and
  `research/experiments/EXP-0064-m93-early-repair-certificates.md`.

## Reproduction

```powershell
python scripts/generate_m82_paper_portfolio.py --check
python scripts/check_m82_paper_portfolio.py
pytest tests/test_paper_portfolio.py -q
python scripts/check_m87_focused_papers.py
pytest -p no:cacheprovider tests/test_m87_focused_papers.py -q
python scripts/check_m88_reader_labels.py
pytest -p no:cacheprovider tests/test_m88_reader_labels.py -q
python scripts/check_m89_appendix_boundaries.py
pytest -p no:cacheprovider tests/test_m89_appendix_boundaries.py -q
python scripts/check_m90_finite_chronology.py
pytest -p no:cacheprovider tests/test_m90_finite_chronology.py -q
python scripts/check_m91_all_rows_semantic_certificate.py
pytest -p no:cacheprovider tests/test_m91_all_rows_semantic_certificate.py -q
python scripts/check_m92_pair_cover_certificate.py
pytest -p no:cacheprovider tests/test_m92_pair_cover_certificate.py -q
python scripts/check_m93_early_repair_certificate.py
pytest -p no:cacheprovider tests/test_m93_early_repair_certificate.py -q
```

Compile the six papers from the repository root with XeLaTeX:

```powershell
latexmk -xelatex -interaction=nonstopmode -halt-on-error `
  paper/focused/promise-factorization-en.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error `
  paper/focused/promise-factorization-ko.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error `
  paper/focused/cyclotomic-extraction-en.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error `
  paper/focused/cyclotomic-extraction-ko.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error `
  paper/focused/finite-certificates-en.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error `
  paper/focused/finite-certificates-ko.tex
```

## Scope

Paper A proves restricted Las Vegas algorithms under unrecognized hereditary
promises. Paper B proves algebraic results for one charged signed
geometric-sum grammar. Paper C proves finite family-relative certificates
through input length 34 and scoped barriers for the same selector family.
None establishes general classical polynomial-time factorization.
