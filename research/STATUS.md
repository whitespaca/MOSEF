# Research Status

## Execution snapshot

- Date: 2026-07-26.
- Branch: `research/20260726-m4-difference-cover`.
- Completed milestone: M4, divisor coverage versus order separation.
- Active milestone: M5, correlated failures across two rigorously defined
  group channels.
- Reviewed core commit:
  `89cc44a6823ef223f36b37ad1cc268fe8fbd9697`.
- General classical polynomial-time integer factoring remains open. M4 proves
  a transfer barrier, not a factoring algorithm or a general lower bound.

## M4 outcome

- `DEF-005` distinguishes nonempty divisibility signatures (coverage) from
  injective signatures (universal distinct-order separation).
- `BAR-001` is `PROVED`: an \(n\)-divisor family need not separate distinct
  orders. The exact profile criterion is that its signatures are not all
  equal; the universal criterion is injectivity on \([n]\).
- The minimal positive difference-family counterexample is
  \(S=\{3\}\), \(T=\{1\}\), and \(\Delta^+(S,T)=\{2\}\).
- The collision occurs in the intended multiplicative mechanism:
  \(\operatorname{ord}_2(5)=1\), \(\operatorname{ord}_3(5)=2\), but
  \(\gcd(5^2-1,6)=6\). The smallest odd example is \(N=15,g=4,d=2\).
- Any explicit family with coverage and injective signatures satisfies
  \(|\Delta|\ge\lceil\log_2(n+1)\rceil\); a positive difference realization
  also satisfies \(|S||T|\ge|\Delta|\).
- The interval difference construction covers and separates, but uses
  \(\Theta(n)\) pairs and supplies no polynomial-bit-complexity POSF.
- `EXT-003` remains conditional. The inspected Umans--Wang source uses divisor
  coverage of actual prefactored integers, not multiplicative orders, and its
  stated \(N^{\max(\alpha,\beta)/2+o(1)}\) time is exponential in
  \(m=\lceil\log_2N\rceil\). BAR-001 does not refute that mechanism.
- Independent literature and adversarial proof audits both approved the scope
  boundary. The proof reviewer reconstructed every argument after the helper
  semantics and sign wording were repaired.

## Reproducible evidence

- Proof:
  `research/proofs/BAR-001-divisor-cover-separation-gap.md`.
- Source audit:
  `research/literature/SRC-004-umans-wang-divisor-conjecture.md`.
- Experiment:
  `research/experiments/EXP-0004-m4-difference-cover-search.md`.
- Negative result: `research/NEGATIVE_RESULTS.md` NR-003.
- Python semantics: `python/mosef_reference/difference_cover.py`.
- Independent selected verifiers: Rust `u64` and C# `BigInteger`.
- Registered bounds: all 4,095 nonempty subsets of \([12]\), order pairs on
  \([8]\), collision moduli through 200, and square constructions through 200;
  deterministic exhaustive enumeration with no seed.
- Result: 114,660 pair-profile checks; 576 divisor covers, of which 240 were
  noninjective and 336 injective.
- Canonical summary SHA-256:
  `4c046ae8694070b59f5e328f94038fe32cb84b5ab716bb86a62e79636077e55f`.

## Validation

- `python scripts/validate_foundation.py`: PASS.
- `python -m unittest discover -s tests -v`: PASS (44 tests).
- `python -m compileall -q python scripts tests`: PASS.
- `python -m pytest`, Ruff, and mypy: unavailable under BLK-003; no dependency
  was added merely to hide the environment limitation.
- `cargo fmt --all --check`: PASS.
- `cargo clippy --workspace --all-targets --all-features -- -D warnings`:
  PASS.
- `cargo test --workspace --all-features`: PASS (14 Rust tests).
- Workspace-scoped `dotnet restore` and `dotnet build`: PASS with zero
  warnings and errors. A first unscoped restore was denied access to the user
  NuGet config; the explicit workspace `APPDATA` repair passed.
- Baseline differential validation: PASS (58 checks).
- M2 search and differential validation: PASS (78,860 candidates and 24
  cross-language checks).
- M3 search and differential validation: PASS (557 witnesses and 22
  cross-language checks).
- M4 search: PASS (4,095 families and 114,660 pair-profile checks).
- M4 Python/Rust/C# differential validation: PASS (12 checks).
- Independent M4 theorem review: PASS; no remaining promotion blocker.
- `latexmk -xelatex -outdir=tmp/pdfs -interaction=nonstopmode -halt-on-error
  paper/main.tex`: PASS; the converged log has no LaTeX warnings, undefined
  references, citations, or overfull/underfull boxes.
- Poppler render and page-by-page visual inspection: PASS (10 pages; no
  clipping, overlap, malformed mathematics, or broken claim labels).
- Final PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `d936b2fbdaf9b256b1ddc30dc14fd4c4cd86c6be09c317131f6134af315241f6`.

## Remote state, blockers, and next action

- M2 pull request `https://github.com/whitespaca/MOSEF/pull/2` is merged into
  `main`.
- M3 remote delivery still awaits explicit authorization under BLK-005.
- Optional pytest/Ruff/mypy tools remain unavailable under BLK-003.
- M4 local delivery is complete at `8c874d8`. The policy-required push attempt
  was rejected because this exact branch payload lacks explicit authorization;
  see BLK-006. No M4 pull request exists.
- Next action: M5 should define two exact group-channel signatures, preregister
  a bounded correlated-collision search, and try to falsify any independence
  assumption before measuring performance.

## 한국어 요약

M4에서는 “모든 수를 한 번 이상 나누는 차이 집합”과 “서로 다른 위수를
실제로 분리하는 지수 집합”이 같은 조건이 아님을 증명했습니다.
\(S=\{3\},T=\{1\}\)의 유일한 차이 2는 위수 1과 2를 모두 덮지만 둘을
구분하지 못하며, 실제로 \(N=6,g=5,d=2\)에서 GCD가 6 전체가 됩니다.
보편적인 분리를 위해서는 단순한 덮음이 아니라 각 위수의 나눗셈 서명이
서로 달라야 합니다. 이 결과는 일반 정수분해의 하한도 아니고
Umans--Wang의 조건부 알고리즘을 반박하지도 않습니다. 다음 M5에서는 두
그룹 채널의 실패가 실제로 얼마나 함께 발생하는지부터 엄밀하게
검증합니다.
