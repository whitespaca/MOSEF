# Research Status

## M6 execution plan

- Branch: `research/20260726-m6-publishable-manuscript`.
- Evidence target: produce a self-contained first manuscript whose title,
  abstract, contribution statement, theorem hypotheses, full proofs,
  experimental results, limitations, and reproduction appendix agree with the
  reviewed claims ledger.
- Center of contribution: one restricted positive result (`THM-001`) and two
  structural barriers (`BAR-001`, `BAR-002`), with `OPEN-002` and `OPEN-003`
  remaining explicit.
- Expected artifacts: a publication claim matrix, an executable manuscript
  consistency checker, full proof appendices, a reproduction appendix, a
  refreshed stable PDF, and an independent adversarial manuscript review.
- Falsification test: search the manuscript for untracked claim IDs, status
  mismatches, factor-dependent constructors presented as algorithms,
  polynomial-in-\(N\) language, missing theorem hypotheses, experiment counts
  without hashes, stale proof statuses, and conclusions broader than the
  reviewed proofs.
- Acceptance gate: every public theorem statement reconstructs from its proof,
  every imported statement maps to an inspected source, every empirical
  statement names its finite scope, the consistency checker and all existing
  software gates pass, XeLaTeX has no unresolved warnings, and every final PDF
  page passes visual inspection.

## Execution snapshot

- Date: 2026-07-26.
- Branch: `research/20260726-m5-multigroup-correlation`.
- Completed milestone: M5, exact correlation across multiplicative and Lucas
  channels.
- Active milestone: M6, strongest fully supported publishable contribution.
- Reviewed M5 core commit:
  `7ca79de49c404b10c1b1b355ff10b8a8d7d59635`.
- General classical polynomial-time integer factoring remains open. M5 proves
  a barrier for one natural parameter map, not a factoring algorithm or a
  general two-channel lower bound.

## M5 outcome

- `DEF-006` defines
  \(G_M(N,a,d)=\gcd(a^d-1,N)\),
  \(G_\Delta(N,P)=\gcd(P^2-4,N)\), and
  \(G_L(N,P,d)=\gcd(V_d(P,1)-2,N)\), including every miss, factor,
  collision, and full-discriminant sequence branch.
- `BAR-002` is `PROVED`: for the conjugate map
  \(P=a+a^{-1}\),
  \[
  V_d(P,1)-2=a^{-d}(a^d-1)^2,\qquad
  P^2-4=a^{-2}(a^2-1)^2.
  \]
  The residues have identical prime support, and their raw GCDs agree for
  square-free \(N\).
- If the exponent family contains \(2\), any proper derived Lucas or
  discriminant GCD implies a proper multiplicative-family GCD. Adding the
  conjugate Lucas family therefore cannot enlarge the multiplicative success
  domain.
- The map can degrade repeated-prime valuations:
  \((N,a,P,d)=(25,2,15,4)\) gives discriminant GCD \(1\),
  multiplicative GCD \(5\), and Lucas GCD \(25\).
- A full discriminant GCD is not a complete sequence outcome:
  \((N,P,d)=(15,8,1)\) has discriminant GCD \(15\) but sequence GCD \(3\).
- Arbitrary \(P\) remains outside the barrier. The exact witness
  \((N,a,P,d)=(15,2,9,3)\) has multiplicative GCD \(1\), discriminant
  GCD \(1\), and Lucas GCD \(5\).
- The Williams source audit confirms that the conjugate discriminant is a
  square and forces the split \(p-1\) branch, not the nonsplit \(p+1\)
  branch. Williams does not claim independence for this pairing.
- Independent literature and proof audits approved the algebra, exact failure
  semantics, source boundary, and map-specific theorem scope.

## Reproducible evidence

- Proof:
  `research/proofs/BAR-002-conjugate-channel-correlation.md`.
- Source audit:
  `research/literature/SRC-005-williams-p-plus-one.md`.
- Experiment:
  `research/experiments/EXP-0005-m5-multigroup-correlation.md`.
- Negative result: `research/NEGATIVE_RESULTS.md` NR-004.
- Python semantics: `python/mosef_reference/multigroup.py`.
- Independent selected verifiers: Rust `u64` and C# `BigInteger`.
- Registered bounds: composite moduli through 700, unit bases through 32,
  Lucas parameters through 32, and exponents through 12; deterministic
  exhaustive enumeration with no seed.
- Result: 9,773 conjugate families, 117,276 identities, 36,048 pointwise
  success implications, 69,192 square-free GCD equalities, and zero
  derived-Lucas-only family successes.
- Multiplicative and combined success counts were both 9,037. Independently
  parameterized same-exponent complements were counted separately and not
  interpreted probabilistically.
- Canonical summary SHA-256:
  `98f2be052a315231292c73319fa98066cf4d8fc4cd66740f207b2d99c7f616f5`.

## Validation

- `python scripts/validate_foundation.py`: PASS.
- `python -m unittest discover -s tests -v`: PASS (51 tests).
- `python -m compileall -q python scripts tests`: PASS.
- `python -m pytest`, Ruff, and mypy: unavailable under BLK-003; no dependency
  was added merely to hide the environment limitation.
- `cargo fmt --all --check`: PASS.
- `cargo clippy --workspace --all-targets --all-features -- -D warnings`:
  PASS.
- `cargo test --workspace --all-features`: PASS (15 Rust tests).
- Workspace-scoped `dotnet restore` and `dotnet build`: PASS with zero
  warnings and errors.
- Baseline differential validation: PASS (58 checks).
- M2 search and differential validation: PASS (78,860 candidates and 24
  cross-language checks).
- M3 search and differential validation: PASS (557 witnesses and 22
  cross-language checks).
- M4 search and differential validation: PASS (4,095 families, 114,660
  pair-profile checks, and 12 cross-language checks).
- M5 registered search: PASS (9,773 families and 117,276 identity checks).
- M5 Python/Rust/C# differential validation: PASS (18 checks).
- Independent M5 theorem review: PASS; no remaining promotion blocker.
- `latexmk -xelatex -outdir=tmp/pdfs -interaction=nonstopmode -halt-on-error
  paper/main.tex`: PASS; the converged log has no LaTeX warnings, undefined
  references, citations, or overfull/underfull boxes.
- Poppler render and page-by-page visual inspection: PASS (12 pages; no
  clipping, overlap, malformed mathematics, or broken claim labels).
- Final PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `0fc846829ae080cc60cd7052936392f438ec15a75fa3c554b3214a06ede62369`.

## Remote state, blockers, and next action

- M2 pull request `https://github.com/whitespaca/MOSEF/pull/2` is merged into
  `main`.
- M3 and M4 remote delivery remain blocked by explicit content-egress
  authorization requirements under BLK-005 and BLK-006.
- Optional pytest/Ruff/mypy tools remain unavailable under BLK-003.
- M5 local delivery is complete at `22e213b`. The policy-required push attempt
  was rejected because this exact branch payload lacks explicit authorization;
  see BLK-007. No M5 pull request exists.
- Next action: M6 should synthesize the restricted theorem and two barrier
  results into the strongest claim-complete manuscript, without enlarging any
  theorem beyond its reviewed hypotheses.

## 한국어 요약

M5에서는 곱셈 채널 \(a^d-1\)과 Lucas 채널 \(V_d(P,1)-2\)를 정확히
비교했습니다. 자연스러운 결합 \(P=a+a^{-1}\)을 사용하면 Lucas 잔여식은
곱셈 잔여식의 제곱에 단위원을 곱한 형태가 되므로 새로운 소인수 지지집합을
만들지 못합니다. 지수 집합에 2가 포함되면 두 채널을 합쳐도 곱셈 채널보다
성공 범위가 넓어지지 않으며, \(N=25\)에서는 오히려 유용한 GCD 5가 전체
충돌 25로 악화됩니다. 다만 독립적으로 선택한 Lucas 매개변수는 이 장벽의
대상이 아니며, 작은 범위에서는 곱셈 실패를 보완하는 정확한 예도
확인했습니다. 이 결과는 일반 정수분해 알고리즘이나 모든 다중 그룹
구성에 대한 하한을 뜻하지 않습니다.
