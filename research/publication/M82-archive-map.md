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
| C: finite certificates | `paper/focused/finite-certificates-en.tex` | `paper/focused/finite-certificates-ko.tex` | BAR-024, THM-004, THM-005, THM-014, THM-019, BAR-041, BAR-046 |

Each pair has exactly seven front-facing claim IDs. The papers use the same
status token as `research/CLAIMS.md`, link to their proof or reproduction
anchors, and state their own exclusions.

## Coverage and trust boundary

- 269 authoritative claim IDs are projected.
- 21 claim IDs are front-facing in exactly one focused paper pair.
- 248 claim IDs remain archival-only.
- A claim is not absent merely because it is not front-facing.
- The focused paper source is not a second authority for status.
- The generator records source hashes and the full archive-only list.
- The independent checker does not import the generator and fixes the
  authoritative ledger, archive, focused-paper, reproduction-anchor, and
  required source-hash paths in its own implementation.
- M85 will further reduce the finite certificate trusted computing base with
  a minimal semantic checker.

## Reproduction

```powershell
python scripts/generate_m82_paper_portfolio.py --check
python scripts/check_m82_paper_portfolio.py
pytest tests/test_paper_portfolio.py -q
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
