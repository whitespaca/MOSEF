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

## BLK-005 - M3 remote delivery requires explicit approval

- First observed: 2026-07-26.
- Scope: push `research/20260725-m3-semismooth-class` and create its draft pull
  request.
- Evidence: the environment safety reviewer rejected
  `git push -u origin research/20260725-m3-semismooth-class` because publishing
  the new theorem, code, experiment, and manuscript to the configured GitHub
  remote is sensitive content egress and this payload lacks explicit user
  authorization.
- Impact: M3 is validated and committed locally at `2ccd608`, but the branch
  has not been pushed and no M3 pull request exists.
- Required resolution: the repository owner must explicitly authorize pushing
  this M3 branch to `origin`. After a successful push, create a draft pull
  request targeting `main` and mark this blocker resolved.

## BLK-006 - M4 remote delivery requires explicit approval

- First observed: 2026-07-26.
- Scope: push `research/20260726-m4-difference-cover` and create its draft pull
  request.
- Evidence: the environment safety reviewer rejected
  `git push -u origin research/20260726-m4-difference-cover` because publishing
  the new barrier proof, source audit, code, experiment, and manuscript to the
  configured GitHub remote is content egress and this payload lacks explicit
  user authorization.
- Impact: M4 is validated and committed locally at `8c874d8`, but the branch
  has not been pushed and no M4 pull request exists.
- Required resolution: the repository owner must explicitly authorize pushing
  this M4 branch to `origin`. After a successful push, create a draft pull
  request targeting `main` and mark this blocker resolved.

## BLK-007 - M5 draft pull request lacks GitHub CLI authentication

- First observed: 2026-07-26.
- Scope: push `research/20260726-m5-multigroup-correlation` and create its draft
  pull request.
- Evidence: the first policy-reviewed push attempt was rejected, but the
  remote-tracking branch was later observed at
  `origin/research/20260726-m5-multigroup-correlation`, containing the reviewed
  M5 completion commit `ccc3a9368a015f9d4f1d840dda79d7a3c9a28ecf`.
  `gh pr list` cannot run because `gh` has no authenticated account or
  `GH_TOKEN`.
- Impact: the M5 branch is remotely visible, but no M5 pull request was
  verified or created in this environment.
- Required resolution: authenticate `gh`, then create or verify a draft pull
  request targeting `main` and mark this blocker resolved.

## BLK-008 - M6 remote delivery requires explicit approval

- First observed: 2026-07-26.
- Scope: push `research/20260726-m6-publishable-manuscript` and create its
  draft pull request.
- Evidence: the environment safety reviewer rejected
  `git push -u origin research/20260726-m6-publishable-manuscript` because the
  branch contains newly created repository content and the user has not
  explicitly authorized sending that payload to the configured external
  GitHub remote.
- Impact: M6 is validated and committed locally, but its branch is not pushed
  and no M6 pull request exists.
- Required resolution: the repository owner must explicitly authorize pushing
  this branch to `origin`. After a successful push, authenticate `gh` and
  create a draft pull request targeting `main`.

## BLK-009 - M7 remote delivery requires explicit approval

- First observed: 2026-07-26.
- Scope: push `research/20260726-m7-nonsplit-lucas` and create its draft pull
  request.
- Evidence: the environment safety reviewer rejected
  `git push -u origin research/20260726-m7-nonsplit-lucas` because publishing
  the new theorem, proof, code, experiment, and manuscript to the configured
  external GitHub remote requires explicit authorization for this payload.
- Impact: M7 is validated and committed locally at
  `0bf86f7d1668c2b60cccde69d398ef5e74c8af55`, but its branch is not pushed and
  no M7 pull request exists.
- Required resolution: the repository owner must explicitly authorize pushing
  this M7 branch to `origin`. After a successful push, authenticate `gh` and
  create a draft pull request targeting `main`.

## BLK-010 - M8 remote delivery requires explicit approval

- First observed: 2026-07-26.
- Scope: push `research/20260726-m8-promise-recognition` and create its draft
  pull request.
- Evidence: the environment safety reviewer rejected
  `git push --set-upstream origin
  research/20260726-m8-promise-recognition` because publishing the new
  barrier proof, implementations, experiment, ledgers, and manuscript to the
  configured external GitHub remote requires explicit authorization for this
  M8 payload.
- Impact: M8 is validated and committed locally at `eb3776d`, but its branch
  is not pushed and no M8 pull request exists.
- Required resolution: the repository owner must explicitly authorize pushing
  this M8 branch to `origin`. After a successful push, authenticate `gh` and
  create a draft pull request targeting `main`.
- Update observed during M9 preflight: the branch now tracks
  `origin/research/20260726-m8-promise-recognition` at
  `142e312727675625cbcefecf1cf6d6d47cec30cd`, so the branch-push portion is
  resolved. GitHub CLI authentication remains absent, and no M8 pull request
  was verified or created.

## BLK-011 - M9 remote delivery requires explicit approval

- First observed: 2026-07-26.
- Scope: push `research/20260726-m9-divisor-rich-schedules` and create its
  draft pull request.
- Evidence: the environment safety reviewer rejected
  `git push --set-upstream origin
  research/20260726-m9-divisor-rich-schedules` because publishing the new
  proof, implementations, experiment, ledgers, and manuscript to the
  configured external GitHub remote requires explicit authorization for this
  M9 payload. GitHub CLI also remains unauthenticated.
- Impact: M9 is validated and committed locally at
  `12f2172aaaca8016baccca109d28e0e7cbb8db98`, but its branch is not pushed and
  no M9 pull request exists.
- Required resolution: the repository owner must explicitly authorize
  publishing this M9 branch to `origin`. After a successful push, authenticate
  `gh` and create a draft pull request targeting `main`.

## BLK-012 - M10 remote delivery requires explicit approval

- First observed: 2026-07-26.
- Scope: push
  `research/20260726-m10-straight-line-compression` and create its draft pull
  request.
- Evidence: the policy-reviewed
  `git push --set-upstream origin
  research/20260726-m10-straight-line-compression` attempt was rejected
  because publishing the new model, proof, implementations, experiment,
  ledgers, and manuscript to the configured external GitHub remote requires
  explicit authorization for this M10 payload. The local `gh auth status`
  also reports no authenticated GitHub host.
- Impact: M10 is validated and committed locally at
  `bd822de928ff14fd6ee0e270d50862591ee36918`, but its branch is not pushed and
  no M10 pull request exists.
- Required resolution: the repository owner must explicitly authorize
  publishing this M10 branch to `origin`. After a successful push,
  authenticate `gh` and create a draft pull request targeting `main`.

## BLK-013 - M11 remote delivery requires explicit approval

- First observed: 2026-07-26.
- Scope: push `research/20260726-m11-boundary-constant` and create its draft
  pull request.
- Evidence: the policy-reviewed
  `git push --set-upstream origin
  research/20260726-m11-boundary-constant` attempt was rejected because
  publishing the new proof, implementation, experiment, ledgers, and
  manuscript to the configured external GitHub remote requires explicit
  authorization for this M11 payload. The local `gh auth status` also reports
  no authenticated GitHub host.
- Impact: M11 is validated and committed locally through
  `a681071f73a22f02e0007923fa03d9e1c4b30d98`, but its branch is not pushed and
  no M11 pull request exists.
- Required resolution: the repository owner must explicitly authorize
  publishing this M11 branch to `origin`. After a successful push,
  authenticate `gh` and create a draft pull request targeting `main`.
## BLK-014 - M12 remote delivery requires explicit approval

- Date: 2026-07-27.
- Status: resolved externally before M13 preflight.
- Evidence: `git push --set-upstream origin
  research/20260726-m12-prime-yield` failed in the sandbox with
  `SEC_E_NO_CREDENTIALS`. The unsandboxed external push was rejected because
  publishing this repository payload was not explicitly authorized by the
  user.
- Impact: M12 is validated and committed locally. The local branch is two
  commits ahead of the existing `origin/research/20260726-m12-prime-yield`
  ref, so commits `53915509bc257f343f61a814b1ec90bcd0ed8aeb` and
  `4daa926` are not published and no M12 pull request exists.
- Resolution: obtain explicit user authorization before publishing this M12
  branch. After a successful push, create or update a draft pull request if
  GitHub authentication is available.
- Resolution evidence: M13 preflight found both local and
  `origin/research/20260726-m12-prime-yield` at
  `1f8d504129394d74ad8203abc0338c7785fc59df`. GitHub CLI remains
  unauthenticated, so no pull request was created or verified.

## BLK-015 - M13 remote delivery requires explicit approval

- Date: 2026-07-27.
- Status: resolved externally before M14 preflight.
- Scope: push `research/20260727-m13-general-factor-scale` and create its
  draft pull request.
- Evidence: the sandboxed `git push --set-upstream origin
  research/20260727-m13-general-factor-scale` failed with
  `SEC_E_NO_CREDENTIALS`. The external push was rejected because publishing
  this newly created branch and repository payload to GitHub was not
  explicitly authorized by the user. `gh auth status` reports no
  authenticated GitHub host.
- Impact: M13 is validated and committed locally at
  `6628ea8158458ba2b3c660ee9d70fc651fa0bbfa`, but the branch is not
  published and no M13 pull request exists.
- Required resolution: the repository owner must explicitly authorize
  publishing this M13 branch to `origin`. After a successful push,
  authenticate GitHub CLI and create a draft pull request targeting `main`.
- Resolution evidence: M14 preflight found both local and
  `origin/research/20260727-m13-general-factor-scale` at
  `843fb411920ca5cba7109871a6daefe1717b0342`. GitHub CLI remains
  unauthenticated, so no M13 pull request was created or verified.

## BLK-016 - M14 remote delivery lacks Windows Git credentials

- Date: 2026-07-27.
- Scope: push `research/20260727-m14-addition-subtraction` and create its
  draft pull request.
- Evidence: after local commits `e80115bd27200c0ec0f37a388cd4e9a4bbac9769`
  and `4f92cbe`, the sandboxed command
  `git push --set-upstream origin
  research/20260727-m14-addition-subtraction` failed with
  `schannel: AcquireCredentialsHandle failed: SEC_E_NO_CREDENTIALS
  (0x8009030e)`.
- Impact: M14 is complete and locally committed, but the branch is not
  published and no pull request exists.
- Required resolution: provide an authenticated Windows Git credential
  context and authorize the push; then authenticate GitHub CLI or use the
  repository UI to create a draft pull request targeting `main`.
