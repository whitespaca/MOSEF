# Blockers

## BLK-001 — TeX quality gate unavailable (resolved)

- First observed: 2026-07-25
- Resolved: 2026-07-25
- Scope: M0 paper compilation and PDF visual inspection.
- Initial evidence: the sandboxed preflight could not resolve `latexmk`,
  `xelatex`, or `bibtex`.
- Resolution evidence: the approved escalated environment exposed MiKTeX 25.4
  and latexmk 4.87. The manuscript compiled through BibTeX with citations
  resolved; the final PDF was rendered to PNG for visual inspection.
- Impact: none remaining. Re-run the same escalated gate after manuscript changes
  until the TeX binaries are also visible in the default sandbox.

## BLK-002 — Draft pull request authentication unavailable

- First observed: 2026-07-25
- Scope: GitHub pull-request creation.
- Evidence: `gh auth status` reports that no GitHub host is authenticated.
- Impact: local research and commits can proceed. Push will be attempted
  independently because Git may have a separate credential helper.
- Required resolution: authenticate GitHub CLI with repository-authorized
  credentials before creating a draft pull request.

## BLK-003 — Optional Python quality tools unavailable

- First observed: 2026-07-25
- Scope: the repository-default `pytest`, Ruff, and mypy gates.
- Evidence: `python -m pytest`, `python -m ruff check python tests scripts`, and
  `python -m mypy python` each report that the requested module is not installed;
  the active Python 3.12 interpreter also has no `pip` module.
- Impact: dependency-free `unittest` coverage and bytecode compilation pass, but
  the optional third-party lint/type gates have not run.
- Required resolution: provide an approved environment containing pinned
  versions of pytest, Ruff, and mypy. Do not add or download them merely to hide
  this environmental limitation.
