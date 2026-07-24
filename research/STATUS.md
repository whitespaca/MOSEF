# Research Status

## Execution snapshot

- Date: 2026-07-25
- Branch: `research/20260725-m0-foundation`
- Starting commit: `e1b747655eb26055a577198df51ea0112a1ba443`
- M0 foundation commit: `6e3631c`
- Completed milestone: M0 — repository and evidence foundation
- Completed milestone: M1 — trusted baseline algorithm suite
- Active milestone: M2 — formal MOSEF/POSF specification
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

## M1 evidence target

- Research question: can a small, deterministic baseline suite serve as a trusted
  semantic oracle for later MOSEF/POSF counterexample work?
- Expected artifacts: canonical vectors; arbitrary-precision Python reference
  functions; overflow-safe Rust `u64` implementations and CLI; an independent
  C# `BigInteger` verifier for selected operations; differential runner.
- Acceptance criteria: exact modular exponentiation, trial division, perfect-power
  detection, validation primality, Pollard rho, Pollard p-1 stage 1, a scoped
  Williams-style p+1 stage 1, and batch GCD are implemented and tested. Rust
  agrees with Python on all canonical vectors, and C# independently agrees on
  modular exponentiation, primality, trial factors, and batch GCD.
- Falsification tests: include 0/1, primes, repeated prime powers, Carmichael
  numbers, products of three primes, nontrivial factors, method failure, and
  invalid modulus paths; use deterministic seeds and iteration bounds.
- Validation commands:
  - `python -m unittest discover -s tests -v`
  - `cargo fmt --all --check`
  - `cargo clippy --workspace --all-targets --all-features -- -D warnings`
  - `cargo test --workspace --all-features`
  - `dotnet build verification/csharp/MosefVerifier.csproj`
  - `python scripts/check_baseline_differential.py`
- Paper section affected: add a baseline algorithms and validation section, with
  explicit `u64` and finite-test limitations.

## Execution plan

1. Preserve the committed M0 evidence foundation.
2. Complete M1 reference, authoritative, and independent implementations.
3. Run unit, lint, build, and differential gates.
4. Synchronize claims, decisions, roadmap, status, and manuscript.
5. Commit M1, attempt remote delivery, and leave M2 as the next active target.

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
- M1 implements exact modular exponentiation, trial division, perfect-power
  detection, validation primality, bounded Pollard rho, Pollard p-1 stage 1, a
  scoped `Q=1` Williams-style p+1 stage 1, and per-item batch GCD.
- Python supplies arbitrary-precision reference semantics, Rust supplies the
  overflow-audited `u64` implementation and CLI, and C# independently verifies
  selected operations with `BigInteger`.
- `EMP-001` records only finite agreement on the canonical vector corpus; it is
  not a complexity or universal factoring claim.

## Toolchain snapshot

See `research/toolchains/windows-amd64-20260725.json`.

## Validation, remote state, blockers, and next action

- `python scripts/validate_foundation.py`: PASS.
- `python -m unittest discover -s tests -v`: PASS (20 tests).
- `python -m compileall -q python scripts tests`: PASS.
- `python -m pytest`: BLOCKED because pytest is not installed.
- `python -m ruff check python tests scripts`: BLOCKED because Ruff is not installed.
- `python -m mypy python`: BLOCKED because mypy is not installed; see BLK-003.
- Independent Node.js parsing of the schema, example, and toolchain JSON: PASS.
- `cargo fmt --all --check`: PASS.
- `cargo clippy --workspace --all-targets --all-features -- -D warnings`: PASS.
- `cargo test --workspace --all-features`: PASS (10 Rust unit tests).
- `dotnet build verification/csharp/MosefVerifier.csproj --nologo --no-restore`:
  PASS with 0 warnings and 0 errors.
- `python scripts/check_baseline_differential.py`: PASS (58 checks).
- `git diff --check`: PASS.
- `latexmk -xelatex -outdir=tmp/pdfs -interaction=nonstopmode -halt-on-error
  paper/main.tex`: PASS in the approved MiKTeX environment; citations resolve
  and the final log contains no LaTeX warnings, undefined references, or
  overfull boxes.
- Poppler rendering and page-by-page visual inspection: PASS (4 pages; no
  clipping, overlap, malformed mathematics, broken citations, or unreadable text).
- M1 implementation commit: `a138e4a5f4ec326ca6983b2ca420eb13f75492e6`.
- Remote: branch `research/20260725-m0-foundation` is pushed and tracks
  `origin/research/20260725-m0-foundation`.
- Draft pull request: `https://github.com/whitespaca/MOSEF/pull/1`.
- Unresolved blocker: optional pytest/Ruff/mypy gates are unavailable; see
  BLK-003. BLK-001 and BLK-002 are resolved.
- Next action: formalize M2 square-free and prime-power branches, prove the basic
  separator lemma, and build its bounded counterexample harness.

## 한국어 요약

M0 기반에 이어 M1 기준 알고리즘을 Python, Rust, C#으로 구축했다. Python
테스트 20개, Rust 테스트 10개, 교차언어 검사 58개가 통과했다. 이는 유한
벡터의 구현 일치 결과일 뿐 일반 고전 다항시간 소인수분해 증명이 아니다.
논문은 XeLaTeX 컴파일과 4쪽 시각 검사를 통과했다. 다음 단계는 M2의 정확한
분기와 기본 분리자 보조정리 형식화다.
