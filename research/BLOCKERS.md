# Blockers

## BLK-001 — TeX quality gate unavailable

- First observed: 2026-07-25
- Scope: M0 paper compilation and PDF visual inspection.
- Evidence: preflight found no `latexmk`, `xelatex`, `lualatex`, `pdflatex`,
  `tectonic`, or `bibtex` executable.
- Impact: the manuscript source and citation keys can be validated structurally,
  but Gate Q4 cannot be completed in this environment.
- Required resolution: provide an approved XeLaTeX-compatible toolchain, then run
  `latexmk -xelatex -interaction=nonstopmode -halt-on-error paper/main.tex` and
  inspect the generated PDF.
- Workaround status: none; absence of a compiler is not treated as proof of a
  manuscript build failure.

## BLK-002 — Draft pull request authentication unavailable

- First observed: 2026-07-25
- Scope: GitHub pull-request creation.
- Evidence: `gh auth status` reports that no GitHub host is authenticated.
- Impact: local research and commits can proceed. Push will be attempted
  independently because Git may have a separate credential helper.
- Required resolution: authenticate GitHub CLI with repository-authorized
  credentials before creating a draft pull request.
