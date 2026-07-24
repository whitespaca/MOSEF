# Research Status

## Execution snapshot

- Date: 2026-07-25
- Branch: `research/20260725-m0-foundation`
- Starting commit: `e1b747655eb26055a577198df51ea0112a1ba443`
- Completed milestone: M0 — repository and evidence foundation
- Active milestone: M1 — trusted baseline algorithm suite
- Working-tree policy: the starting tree was clean; the three existing user files
  (`AGENTS.md`, `CODEX.md`, and `PROMPT.md`) are preserved unchanged.

## Evidence target

- Research question: can the repository establish a reproducible, claim-safe
  foundation without asserting progress on general polynomial-time factoring?
- Expected artifacts: state ledgers, source-quality protocol, inspected baseline
  notes, minimal manuscript and bibliography, versioned experiment-result schema,
  toolchain record, and an offline validation harness.
- Acceptance criteria: all M0 files exist; claim labels are valid; the example
  record satisfies the executable schema contract; malformed records are rejected;
  manuscript citations resolve to bibliography keys; validation is dependency-free.
- Falsification test: delete a required field, corrupt a hash/status/citation, or
  omit a required foundation file and confirm that validation fails.
- Validation commands:
  - `python scripts/validate_foundation.py`
  - `python -m unittest discover -s tests -v`
  - `latexmk -xelatex -interaction=nonstopmode -halt-on-error paper/main.tex`
- Paper sections affected: all sections are initialized conservatively; no novel
  theorem or experimental result is claimed.

## Current plan

1. Complete the M0 artifacts and source ledger.
2. Run structural and negative-path validation.
3. Attempt the paper gate and record the unavailable TeX engine precisely.
4. Review the complete diff, commit, and attempt remote delivery.

## Completed work and results

- M0 state ledgers, source policy, inspected baseline notes, minimal manuscript,
  bibliography, versioned experiment schema, example record, toolchain record,
  and dependency-free validation harness are present.
- No mathematical claim has been promoted, weakened, or refuted in this execution.
- `OPEN-001` records that universal POSF existence and polynomial-time
  constructibility remain open project targets.
- Three primary journal sources were inspected for baseline orientation; see
  `research/literature/BASELINE.md`.
- An adversarial wording scan found no assertion that general classical
  polynomial-time factorization or universal POSF existence has been proved.

## Toolchain snapshot

See `research/toolchains/windows-amd64-20260725.json`.

## Validation, remote state, blockers, and next action

- `python scripts/validate_foundation.py`: PASS.
- `python -m unittest discover -s tests -v`: PASS (5 tests).
- `python -m compileall -q scripts tests`: PASS.
- Independent Node.js parsing of the schema, example, and toolchain JSON: PASS.
- `git diff --check`: PASS.
- `latexmk -xelatex -interaction=nonstopmode -halt-on-error paper/main.tex`:
  BLOCKED because `latexmk` is not installed; see BLK-001.
- Remote: `origin` is configured; GitHub CLI is not authenticated.
- Blockers: see `research/BLOCKERS.md`.
- M0 commit: pending final diff review.
- Next action: specify M1 canonical vectors and implement dependency-free Python
  reference algorithms before the authoritative Rust implementation.

## 한국어 요약

M0 연구 기반의 구조 검증과 테스트 5개가 통과했다. TeX 도구 부재로 PDF
컴파일만 외부 차단 상태다. 일반 고전 다항시간 소인수분해 또는 보편적
POSF의 존재를 증명했다는 주장은 하지 않는다. 다음 단계는 M1 기준
알고리즘과 정답 벡터 구축이다.
