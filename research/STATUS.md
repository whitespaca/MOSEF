# Research Status

## Execution snapshot

- Date: 2026-07-25
- Branch: `research/20260725-m2-formal-spec`
- Starting commit: `fdd9489cd5655782d6990a5c9593d047976493c4`
- M2 core commit: `7691b61dfef292d0da8af5eb022d62cc52383634`
- M2 manuscript and evidence commit:
  `e296443b0605e785c87e6b5e6bf1f9bee100aaf6`
- Completed milestone: M2 - formal multiplicative-channel specification
- Active milestone: M3 - restricted semismooth-order theorem search
- Working-tree policy: the run started clean; existing repository and user files
  were preserved, and generated build/PDF artifacts remain ignored.

## M2 result

M2 now gives exact square-free and repeated-prime semantics for one
multiplicative order candidate:

- `LEM-001` proves that a nonempty proper order support yields a nontrivial GCD.
- `LEM-002` gives the exact capped-valuation formula for every \(N\), including
  prime powers and mixed repeated-prime inputs.
- Candidate pseudocode covers direct factors, invalid bases, misses,
  nontrivial factors, and simultaneous collisions.
- Complete-factorization pseudocode covers primality, exact perfect powers,
  validated recursive splits, constructor failure, unresolved leaves, and
  multiplicities.
- The complexity ledger charges construction, Cartesian-product size, canonical
  base representation, exponent bit length, modular evaluation, GCD, and fewer
  than \(2m\) recursive factor-tree nodes.

The independent adversarial review found no counterexample or missing
hypothesis in either lemma. It did identify a definitional obstruction:
support-only POSF coverage cannot include prime powers because their
distinct-prime support is a singleton. `OPEN-001` is therefore `REFUTED`.
`OPEN-002` repairs the support target by preprocessing perfect powers, while
`OPEN-003` asks for an all-input valuation-separating family. Both repaired
constructor questions remain open.

## Reproducible evidence

- Proof and algorithm specification:
  `research/proofs/M2-formal-specification.md`.
- Negative result: `research/NEGATIVE_RESULTS.md` NR-001.
- Registered experiment: `research/experiments/EXP-0002-m2-separator-search.md`.
- Python oracle: `python/mosef_reference/separator.py`.
- Rust and C# selected-outcome verifiers:
  `crates/mosef-arithmetic` and `verification/csharp`.
- Selected vectors: `schemas/m2-separator-vectors-v1.json`.
- Deterministic search bounds: composite \(4\le N\le500\), unit bases
  \(2\le g\le20\), and \(1\le d\le20\); no seed.
- Search result: 78,860 candidates, 46,140 square-free candidates, and 5,672
  nonsquarefree support-only false negatives.
- Smallest witnesses: \((4,3,1)\) overall and \((9,2,2)\) for odd \(N\).
- Canonical summary SHA-256:
  `89bda0d3ea8054542151fda07d00c1e2711536b7339952618aea692c1d74cc59`.

## Validation

- `python scripts/validate_foundation.py`: PASS.
- `python -m unittest discover -s tests -v`: PASS (28 tests).
- `python -m compileall -q python scripts tests`: PASS.
- `python -m pytest`, Ruff, and mypy: unavailable under BLK-003; no dependency
  was added merely to hide the environment limitation.
- `cargo fmt --all --check`: PASS.
- `cargo clippy --workspace --all-targets --all-features -- -D warnings`: PASS.
- `cargo test --workspace --all-features`: PASS (11 Rust tests).
- Repository-local no-source NuGet restore and
  `dotnet build verification/csharp/MosefVerifier.csproj --nologo --no-restore`:
  PASS with zero warnings and errors.
- `python scripts/check_baseline_differential.py`: PASS (58 comparisons).
- `python scripts/run_m2_separator_search.py --n-max 500 --base-max 20
  --exponent-max 20`: PASS (78,860 candidates).
- `python scripts/check_m2_separator_differential.py`: PASS (24 comparisons).
- Independent clean-room review enumeration: PASS (193,200 cases, including
  73,632 mixed repeated-prime and 3,672 order-one cases).
- `latexmk -xelatex -outdir=tmp/pdfs -interaction=nonstopmode -halt-on-error
  paper/main.tex`: PASS; the final log has no LaTeX warnings, undefined
  references, or overfull/underfull boxes.
- Poppler render and visual inspection: PASS (6 pages; no clipping, overlap,
  orphaned claim labels, malformed mathematics, or broken references).
- Final PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `2cf029694b6978a9e7c020076a77e92483520f8f8e5b4d1be82e0e30831054cf`.

## Remote state, blockers, and next action

- Existing draft PR for M0/M1: `https://github.com/whitespaca/MOSEF/pull/1`.
- M2 branch push was rejected by the environment safety reviewer because
  remote content egress requires explicit user approval. The branch remains
  local and no M2 draft PR exists; see BLK-004.
- Unresolved blocker: optional pytest/Ruff/mypy tools are unavailable; see
  BLK-003. Remote delivery additionally awaits explicit approval under BLK-004.
  No M2 correctness gate is blocked.
- Next action: M3 should state the strongest noncircular multiplicative-channel
  semismooth-order promise class, distinguish promise from recognition, and
  attack its boundary cases before promoting any theorem.

## 한국어 요약

M2에서 제곱인수 없는 입력과 중복 소인수 입력을 구분하는 정확한 조건을
정리했습니다. 기본 분리 보조정리와 소인수 지수값을 이용한 정확한 GCD
조건을 증명했고, 모든 실패 분기와 재귀 복잡도를 명시했습니다. 소수 거듭제곱은
지지집합 방식의 분리 조건을 만족할 수 없으므로 기존의 모든 합성수 대상
주장은 반박되었습니다. 완전거듭제곱 전처리 방식과 지수값 분리 방식은 각각
새로운 열린 문제로 남습니다. 다음 단계 M3에서는 비순환적인 준매끄러운 차수
입력 클래스에 대한 제한 정리를 탐색합니다.
