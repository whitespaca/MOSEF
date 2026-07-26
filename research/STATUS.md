# Research Status

## M8 outcome

- Branch: `research/20260726-m8-promise-recognition`.
- Completed milestone: M8, a self-contained common-schedule
  finite-distribution and magnitude barrier for the union of the local
  \(p-1\) and \(p+1\) semiprime promises.
- `DEF-008` defines the combined prime signature
  \[
  \sigma_\Delta(p)=
  ((\mathbf1_{p-1\mid d},\mathbf1_{p+1\mid d}))_{d\in\Delta}.
  \]
  It is evaluated at an unknown factor for analysis and is not an
  \(N\)-only recognizer.
- `BAR-003` is `PROVED`: a distinct-prime semiprime is in the local, hence
  hereditary, promise union exactly when its two signatures differ. For a
  finite \(s\)-prime set with \(h\) nonzero signatures, the promised fraction
  is at most \(h(2s-h-1)/(s(s-1))\), with
  \(h\le2\sum_{d\in\Delta}\tau(d)\le4|\Delta|\sqrt{\max\Delta}\).
- Every prime above \(\max\Delta+1\) has zero signature. Thus the explicitly
  defined balanced-semiprime distribution has exact zero density under the
  stated strict magnitude hypothesis and an asymptotically vanishing upper
  bound under the stated sparsity hypothesis.
- `REF-004` is `REFUTED`; NR-005 records the smallest unrestricted witness
  \((\Delta,N)=(\{1\},15)\). This witness is not labeled as a member of the
  balanced interval.
- EXP-0007 checked 987 exponent families, 296,100 direct/signature pairs,
  184,994 magnitude-zero pairs, 2,443 balanced zero-density cases, and 28
  cross-language comparisons. Its summary SHA-256 is
  `fb2f861f1670c3e4f68a0e8b461f430e7e10eeb966d9f5bec48886c810dd6cd3`.
- Independent adversarial review reconstructed the proof and additionally
  checked 1,920,600 pairs, 1,940 finite bounds, 20,000 divisor bounds, and
  27,284 balanced bit-length pairs. Independent source-scope review found no
  external citation dependency and approved the no-novelty framing.
- General classical factoring remains open. M8 proves no recognizer, natural
  density theorem, universal schedule barrier, or general lower bound.

## M7 outcome

- Branch: `research/20260726-m7-nonsplit-lucas`.
- Completed milestone: M7, a factorization-independent random-parameter
  theorem on a hereditary nonsplit Lucas-asymmetry promise class.
- `LEM-003` is `PROVED`:
  \[
  \#\{P\bmod q:V_d(P,1)=2\}
  =\frac{\gcd(d,q-1)+\gcd(d,q+1)}2.
  \]
  Its proof also counts degenerate roots and the \((q-1)/2\) nonsplit
  parameters without importing an uninspected finite-field lemma.
- `DEF-007` records the hereditary factor-dependent promise
  \(p+1\mid d,\ q+1\nmid d\). It is nonempty but is not recognized by the
  algorithm.
- `THM-002` is `PROVED`: fresh exact uniform \(P\bmod K\), with every
  discriminant and sequence branch retained, gives a correct almost-sure
  complete factorer with expected polynomial bit complexity on DEF-007 and
  at least \(1/12\) success probability at each witness trial.
- EXP-0006 checked 1,040 root formulas, 714 ordered witnesses, and 75,934
  proved-event splits. The minimum proved-event probability was \(8/51\);
  the summary SHA-256 is
  `23ed0067d2ccb642c3676ff4ea3f5c34e1e622f6372626aa84377eac74b7d905`.
- Independent adversarial review checked 2,481,900 additional root parameters
  and 1,080 repeated-factor/multiprime event splits. Independent source review
  approved the Williams/Lehmer boundary after repairs; neither the root count
  nor THM-002 is attributed to Williams or claimed as a novelty result.
- General classical polynomial-time factoring remains open. THM-002 supplies
  no membership recognizer, density theorem, statistical independence claim,
  or outside-promise termination guarantee.

## M6 outcome

- Branch: `research/20260726-m6-publishable-manuscript`.
- Completed milestone: M6, the first claim-complete publishable manuscript.
- Manuscript core commit:
  `9aac77921421fd69a4ab83e879cf50084f3024f3`.
- Validated milestone completion commit:
  `72f969df01555730cf2a27e96530444fdfa39b81`.
- The paper centers one restricted positive result (`THM-001`) and two
  structural barriers (`BAR-001`, `BAR-002`) without enlarging any hypothesis;
  `OPEN-002` and `OPEN-003` remain explicit.
- `research/PUBLICATION_CLAIMS.md` maps all 26 ledger claims into the paper.
  `scripts/check_publication.py` enforces unique claim IDs and matching
  statuses, all five full proofs, four registered experiment hashes, required
  sections, overclaim exclusions, and a real 40-hex M6 core commit.
- The reproduction appendix records exact PowerShell commands, workspace-local
  .NET state, experiment core commits, hashes, and the stable PDF path.
- Independent adversarial review reconstructed LEM-001, LEM-002, THM-001,
  BAR-001, and BAR-002; reproduced all experiment hashes and differential
  suites; and found no remaining theorem, source, hash, complexity, command, or
  publication-checker blocker after repairs.
- General classical polynomial-time integer factoring remains open. M6 is a
  restricted theorem plus two scoped barriers, not a universal algorithm or a
  general lower bound.

## Execution snapshot

- Date: 2026-07-26.
- Branch: `research/20260726-m8-promise-recognition`.
- Completed milestone: M8.
- Core implementation/proof commit:
  `bc8b25222823e06830530eac3962271c6d14a7ca`.
- Registered experiment commit:
  `a4895df3c0cf4de54b59932acf9f2e4ecbef2463`.
- Next selected milestone: M9, explicit divisor-rich schedules with
  polynomial-bit-length exponent values outside BAR-003's magnitude regime.

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
- `python -m unittest discover -s tests -v`: PASS (58 tests).
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
- M7 registered search: PASS (1,040 root formulas, 714 witnesses, and 75,934
  proved-event split checks).
- M7 Python/Rust/C# differential validation: PASS (26 checks).
- `python scripts/check_publication.py`: PASS (30 claims and 5 registered
  experiment hashes).
- Independent M7 proof and source-scope review: PASS after repairing the
  \(p=3\) non-strict inequality, Legendre notation, finite-field cyclicity
  proof, and Williams/Lehmer attribution.
- `latexmk -xelatex -outdir=tmp/pdfs -interaction=nonstopmode -halt-on-error
  paper/main.tex`: PASS; the clean converged log has no warnings, undefined
  references or citations, and no overfull or underfull boxes.
- Poppler render and page-by-page visual inspection: PASS (17 pages; no
  clipping, overlap, malformed mathematics, or broken claim labels).
- Final PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `c2d9f499fb1540468d54c192491e395ec710a65a1d59c6d36ba5b217c3b1b5a2`.

## Remote state, blockers, and next action

- M2 pull request `https://github.com/whitespaca/MOSEF/pull/2` is merged into
  `main`.
- M3 and M4 remote delivery remain blocked by explicit content-egress
  authorization requirements under BLK-005 and BLK-006.
- Optional pytest/Ruff/mypy tools remain unavailable under BLK-003.
- The M5 remote branch is now visible at
  `origin/research/20260726-m5-multigroup-correlation`; `gh` is not
  authenticated, so no M5 pull request was verified or created.
- M6 local delivery is complete. Its branch is now visible at
  `origin/research/20260726-m6-publishable-manuscript`; no M6 pull request was
  verified or created.
- M7 local research and publication validation are complete. The
  policy-required push attempt was rejected because this exact new branch
  payload lacks explicit authorization for external content egress; see
  BLK-009. No M7 pull request exists.
- Next action: M8 should define factorization-independent observables before
  proposing a recognizer or input-density claim for the combined \(p-1\) and
  \(p+1\) hereditary classes.

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
