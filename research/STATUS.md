# Research Status

## Execution snapshot

- Date: 2026-07-26
- Branch: `research/20260725-m3-semismooth-class`
- Starting commit: `a1861b4f19ca645e9f6b6553396976105764f7d3`
- M3 core commit: `93e97d96c544d5feddad208997834f47763cf31f`
- Completed milestone: M3 - hereditary semismooth-order restricted theorem
- Active milestone: M4 - divisor-cover separation analysis
- Working-tree policy: the run started from the validated M2 head; no
  pre-existing user changes were overwritten, and generated build/PDF
  intermediates remain ignored.

## M3 result

M3 proves one restricted theorem and records one deterministic obstruction:

- `DEF-004` defines a base-free hereditary semismooth asymmetry promise:
  every composite non-perfect-power divisor has distinct primes \(p,q\) and a
  polynomially bounded multiplier \(t\) with
  \(p-1\mid t\operatorname{lcm}(1,\ldots,B)\) but
  \(q-1\nmid t\operatorname{lcm}(1,\ldots,B)\).
- `THM-001` is `PROVED`: fresh uniform residues give a Las Vegas complete
  factorization algorithm on this promise class, with success probability at
  least \(5/12\) per witness trial, at most \(12/5\) cycles in expectation,
  almost-sure termination, and expected polynomial bit complexity.
- The promise is factor dependent but noncircular. The algorithm never uses
  the witness primes, and no polynomial-time membership recognizer or
  outside-promise termination guarantee is claimed.
- `REF-001`/NR-002 refutes a fixed-base shortcut. For
  \(N=51\), \(a=2\), and \(d=840\), the prime-divisor asymmetry holds but
  \(\operatorname{ord}_{17}(2)=8\mid840\), so the GCD is all of \(N\).
- Independent adversarial review approved promotion after schedule-cost,
  perfect-power-node, fresh-sample, and all-witness-enumeration repairs.

## Reproducible evidence

- Proof: `research/proofs/THM-001-semismooth-promise.md`.
- Experiment: `research/experiments/EXP-0003-m3-semismooth-search.md`.
- Negative result: `research/NEGATIVE_RESULTS.md` NR-002.
- Python semantics and oracle: `python/mosef_reference/semismooth.py`.
- Rust/C# selected verifiers: `crates/mosef-arithmetic` and
  `verification/csharp`.
- Registered bounds: \(4\le N\le500\), \(B=8\), \(R=3\); deterministic
  exhaustive enumeration with no seed.
- Result: 155 hereditary promised inputs all factored; all 557 ordered witness
  tuples met the \(5/12\) exact success bound.
- Minimum observed probability: \(268/493\), at \(N=493\) and \(d=840\).
- Canonical summary SHA-256:
  `0a1d2ca2fef29126b60f3a9377454200e33fce20c0b49c081ea527622f8c536d`.

## Validation

- `python scripts/validate_foundation.py`: PASS.
- `python -m unittest discover -s tests -v`: PASS (37 tests).
- `python -m compileall -q python scripts tests`: PASS.
- `python -m pytest`, Ruff, and mypy: unavailable under BLK-003; no dependency
  was added merely to hide the environment limitation.
- `cargo fmt --all --check`: PASS.
- `cargo clippy --workspace --all-targets --all-features -- -D warnings`: PASS.
- `cargo test --workspace --all-features`: PASS (13 Rust tests).
- `dotnet build verification/csharp/MosefVerifier.csproj --nologo
  --no-restore`: PASS with zero warnings and errors.
- `python scripts/run_m3_semismooth_search.py --n-max 500 --base-bound 5
  --smooth-bound 8 --cofactor-bound 3 --collision-bound-max 20`: PASS.
- `python scripts/check_m3_semismooth_differential.py`: PASS (22 comparisons).
- Independent theorem review: PASS; no remaining promotion blocker.
- `latexmk -xelatex -outdir=tmp/pdfs -interaction=nonstopmode -halt-on-error
  paper/main.tex`: PASS; final log has no LaTeX warnings, undefined references,
  or overfull/underfull boxes.
- Poppler render and page-by-page visual inspection: PASS (7 pages; no
  clipping, overlap, orphaned references, malformed mathematics, or broken
  claim labels).
- Final PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `5cc68afa7c2a67fb52ca850569579f9a625e873ada846da7ed748137819ee185`.

## Remote state, blockers, and next action

- M2 pull request `https://github.com/whitespaca/MOSEF/pull/2` is merged into
  `main`; BLK-004 is resolved.
- The M3 push was rejected by the environment safety reviewer because remote
  content egress requires explicit authorization for this branch payload. The
  commits remain local and no M3 pull request exists; see BLK-005.
- Unresolved blockers: optional pytest/Ruff/mypy tools are unavailable
  (BLK-003), and M3 remote delivery awaits explicit authorization (BLK-005).
  Neither blocks the local M3 correctness gates.
- Next action: M4 should formalize a factorization-independent natural
  difference-cover family, reconstruct its strongest primary-source support,
  and attempt to falsify the implication from divisor coverage to actual
  prime-factor separation.

## 한국어 요약

M3에서는 모든 입력에 대한 일반 인수분해 주장이 아니라, 명시적인
준매끄러운 차수 비대칭 약속 클래스에 대한 제한 정리를 증명했습니다.
무작위 밑을 정확히 균등 추출하면 각 증인 시행의 성공 확률이 최소
\(5/12\)이고, 재귀 전체의 기대 비트 복잡도가 다항식임을 보였습니다.
약속 클래스의 소속 판정은 제공하지 않으며, 약속 밖에서는 종료를
보장하지 않습니다. 고정 밑 \(2\)는 \(N=51\)에서 실패하므로 해당
지름길은 반례로 보존했습니다. 다음 단계 M4에서는 자연스러운
차이-커버 구성이 실제 소인수 분리를 보장하는지 검증합니다.
