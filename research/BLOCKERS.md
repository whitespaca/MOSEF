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

## BLK-002 — Draft pull request authentication unavailable (resolved)

- First observed: 2026-07-25
- Resolved: 2026-07-25
- Scope: GitHub pull-request creation.
- Evidence: `gh auth status` reports that no GitHub host is authenticated.
- Resolution evidence: Git credentials successfully pushed the research branch,
  and the connected GitHub app created draft pull request
  `https://github.com/whitespaca/MOSEF/pull/1`.
- Impact: none for the current delivery. The local `gh` CLI remains
  unauthenticated and should not be treated as the source of PR credentials.

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

## BLK-004 - M2 remote delivery requires explicit approval (resolved)

- First observed: 2026-07-25
- Scope: push `research/20260725-m2-formal-spec` and create its draft pull
  request.
- Evidence: the environment safety reviewer rejected
  `git push -u origin research/20260725-m2-formal-spec` because sending the new
  research content to the configured GitHub remote requires explicit user
  authorization for that payload.
- Impact: M2 is validated and committed locally, but its branch is not on the
  remote and no M2 pull request exists.
- Required resolution: the repository owner must explicitly authorize pushing
  this branch to `origin`. After a successful push, create a stacked draft pull
  request against `research/20260725-m0-foundation` and mark this blocker
  resolved.

### Resolution

- Resolved: 2026-07-26.
- Evidence: the connected GitHub app reported pull request
  `https://github.com/whitespaca/MOSEF/pull/2` merged into `main`, with M2 head
  commit `a1861b4f19ca645e9f6b6553396976105764f7d3`.
- Impact: no M2 delivery blocker remains. M3 remote delivery is tracked
  separately only if its eventual push or draft pull request fails.
