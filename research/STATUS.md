# Research Status

## M12 active

- Date: 2026-07-26.
- Branch: `research/20260726-m12-prime-yield`.
- Active milestone: M12, the critical/supercritical primorial prime-yield
  question after common-input-length population normalization.
- Baseline validation passed before edits: foundation and publication
  consistency (47 claims and nine experiment hashes), 86 Python tests and
  bytecode compilation, Rust format/Clippy/19 tests, and a clean converged
  28-page XeLaTeX build.
- Provisional claim target: `BAR-007`. For first-primes primorial indices
  \(r(k)=O(k)\), count only divisors \(d\le2^{\beta k}+1\), because a hit on
  an \(O(k)\)-bit target prime must have \(d=q\pm1\) in that range. The
  factorial lower bound on a square-free divisor's support should force
  \(\omega(d)=O(k/\log k)\), leaving only
  \(2^{O(k\log\log k/\log k)}=2^{o(k)}\) relevant divisors despite
  \(\tau(P_{r(k)})=2^{\Theta(k)}\) overall.
- Expected consequence: every stipulated exponentially large
  common-input-length population of \(O(k)\)-bit primes has vanishing
  primorial-schedule promised-pair fraction, for every fixed boundary
  coefficient. This would refute the transfer from total divisor capacity to
  factor-scale prime yield without making a primality-distribution claim.
- Falsification plan: exhaustively compare the exact factorial/binomial bound
  with all divisors of bounded primorials; independently test actual
  \(d\pm1\) prime hits and exact three-signature population fractions on
  balanced finite prime intervals.
- Literature plan: audit primary shifted-smooth-prime results only to delimit
  scope. No external distribution theorem will be used in the elementary
  barrier proof.
- Planned deliverables: proof and negative-result record, deterministic
  EXP-0011, selected Python/Rust/C# checks, claims and manuscript
  synchronization, independent adversarial/source review, full gates, and a
  local commit.

## M11 outcome

- Date: 2026-07-26.
- Branch: `research/20260726-m11-boundary-constant`.
- Completed milestone: M11, the exact \(\Theta(k\log k)\) multiplication
  straight-line boundary.
- `DEF-011` gives an exact integer divisor budget whose monotone envelope
  satisfies
  \(\log_2 R(L)\le(1+o(1))L/\log_2L\).
- `BAR-006` is `PROVED`: a polynomial-size common schedule with
  \(L(k)\le(c+o(1))k\log_2k\) hits at most \(2^{ck+o(k)}\) odd primes.
  On a supplied common-input-length population of size at least
  \(2^{\alpha k}\), its promised-pair fraction therefore vanishes when
  \(c<\alpha\). The \(c=0\) endpoint and the fixed-base DEF-010 transfer are
  included explicitly.
- The first-primes primorial \(P_r\) supplies an explicit boundary-capacity
  family: \(\ell(P_r)=\Theta(r\log r)\), \(\tau(P_r)=2^r\), and ordinary
  binary evaluation uses at most \(2\ell(P_r)-2\) multiplication nodes.
  This does not supply an asymptotic prime-yield lower bound.
- `REF-007` is `REFUTED`; NR-008 records that repeated squaring reaches the
  boundary while its exposed exponent divisors remain only powers of two.
- EXP-0010 checked all 262,143 positive exponents below \(2^{18}\), enumerated
  all divisors and \(d\pm1\) candidates for the first 12 primorials, and
  executed 1,777,936 exact trial divisions. At \(r=12\), the 43-bit exponent
  had 4,096 divisors, 67 binary nodes, and 897 disjoint-channel prime hits
  split 449/448. The canonical summary SHA-256 is
  `22699f23a1421805cb472ddca1723e8d580d601cd25ca72b8b2cd134743e4f83`.
- Independent adversarial review reproduced the seven focused tests,
  registered experiment, 32 differential comparisons, and publication gate,
  then added 10,000 exact-budget cases, 200,000 divisor-count cases,
  primorial accounting through \(r=50\), and 131,054 channel checks through
  \(r=16\). No mathematical defect was found, including in the \(c=0\)
  transfer or stipulated-population scope.
- Independent source review checked the official Rosser--Schoenfeld scan at
  printed page 69 and confirmed equation (3.13), its strict inequality,
  natural-log convention, and \(r\ge6\) hypothesis. The imported result is
  used only for the primorial construction range; no prime-yield or novelty
  statement is attributed to it.
- Full validation passed: foundation and publication consistency (47 claims
  and nine experiment hashes), 86 Python tests and bytecode compilation, Rust
  format/Clippy/19 tests, C# Release build with zero warnings or errors, all
  registered M1--M11 searches and differential suites, and a clean converged
  28-page XeLaTeX build. Every page was rendered and visually inspected; the
  stable PDF SHA-256 is
  `bfd6a0f165c20dd5db0f7822d6b9decd253a96da26d295a157f799b6cdeba812`.
- Optional third-party Python `pytest`, Ruff, and mypy gates remain unavailable
  under BLK-003; dependency-free unit tests and compilation are the validated
  Python substitutes in this environment.
- Scope: BAR-006 is a hit-set upper bound for common
  factorization-independent schedules on a supplied finite population. It
  constructs no exponentially large common-input-length population, proves no
  natural-density or prime-yield theorem, recognizes no promise class, and is
  not a general algebraic or factoring lower bound.
- Next selected milestone: M12, isolate whether an explicit critical or
  supercritical boundary family admits a rigorously supported uniform
  \(d\pm1\) prime-yield statement after population normalization.

## M11 execution snapshot

- Date: 2026-07-26.
- Branch: `research/20260726-m11-boundary-constant`.
- Core implementation/proof commit:
  `cd391e5cf64207ea7dc2f6e4dd55cf469af45424`.
- Registered experiment commit:
  `de290aea906d0a868fafa958c789227e94904d37`.
- Reviewed manuscript and milestone completion commit:
  `a681071f73a22f02e0007923fa03d9e1c4b30d98`.
- Remote delivery: blocked by BLK-013. The policy-reviewed push attempt was
  rejected because the user has not explicitly authorized external GitHub
  egress for the new M11 payload; the local GitHub CLI is also unauthenticated.
- Next selected milestone: M12, an explicit critical/supercritical
  boundary-family prime-yield theorem or obstruction.

## M10 outcome

- Date: 2026-07-26.
- Branch: `research/20260726-m10-straight-line-compression`.
- Completed milestone: M10, a restricted multiplication straight-line
  compression barrier.
- `DEF-010` defines a factor-oblivious multiplication-only DAG with explicit
  parent/output indices, exact formal exponents, charged construction, and
  charged node-by-node modular evaluation.
- `BAR-005` is `PROVED`: node \(i\) represents \(g^{e_i}\) with
  \(e_i\le2^i\). Exact formal realization of \(g^d\) therefore needs at least
  \(\lceil\log_2d\rceil\) multiplication nodes, tight for powers of two by
  repeated squaring.
- A common schedule with fixed initial-base count and total charged nodes
  \(T(k)=o(k\log k)\) has \(E(k)\le T(k)+O(1)\) and
  \(L(k)\le T(k)+1\), so BAR-004 still applies. Polynomial \(T(k)\) cannot
  hide a superpolynomial-bit formal exponent in this model.
- `REF-006` is `REFUTED`; NR-007 records that the compact descriptor
  \(2^{2^s}\) requires exactly \(2^s\) charged multiplications inside
  DEF-010.
- EXP-0009 enumerated all 1,587,600 commutative seven-node programs and
  checked 1,647,202 constructed nodes for exponent growth and direct residue
  agreement. Seventeen tower levels and 24 Python/Rust/C# comparisons passed.
  Its canonical summary SHA-256 is
  `67508cf957fa356350a707a58f1079aebcea4f02481ff826cd5ed09727d210fa`.
- Independent adversarial review reproduced the registered search, 5/5
  focused unit tests, and 24/24 differential checks, then added 645,350 node
  checks across 20,000 deterministic random programs, 200,000 arbitrary-\(d\)
  lower-bound edge checks, and tower levels 0--20. Independent source-scope
  review confirmed that the proof is elementary and needs no new citation.
- Full validation passed: foundation and publication consistency (42 claims,
  eight experiment hashes), 79 Python tests and bytecode compilation, Rust
  format/Clippy/19 tests, C# Release restore/build with zero warnings or
  errors, all registered M1--M10 searches and differential suites, and a clean
  converged 25-page XeLaTeX build. Every page was rendered and visually
  inspected; the stable PDF SHA-256 is
  `5b64504d4bf18f2646defdcd512f4e2bd96c6b34cca5a03d7f874050a8acd0e0`.
- Scope: BAR-005 concerns exact formal exponents in a factor-oblivious
  multiplication-only same-base DAG. It is not a fixed-modulus residue,
  generic-group, richer-algebraic, natural-density, recognizer, factoring, or
  general lower-bound result, and it leaves
  \(T(k)\not=o(k\log k)\) open.
- 한국어 요약: 짧은 지수 표기만으로 계산 비용을 숨길 수는 없다. 이
  곱셈 전용 모델에서는 곱셈 한 번마다 형식적 지수 길이가 최대 한
  비트만 증가하며, 정확한 \(k\log k\) 경계는 다음 과제로 남는다.
- Next selected milestone: M11, specify and test one divisor-rich
  \(\Theta(k\log k)\)-node schedule family.

## M10 execution snapshot

- Date: 2026-07-26.
- Branch: `research/20260726-m10-straight-line-compression`.
- Completed milestone: M10.
- Core implementation/proof commit:
  `5501d2d1d2a6a5c584fdc03f905e9a36a6054733`.
- Registered experiment commit:
  `18f104fdb69b8fd96f5776796047487ef211f03a`.
- Validated milestone completion commit:
  `bd822de928ff14fd6ee0e270d50862591ee36918`.
- Remote delivery: blocked by `BLK-012`; the policy-reviewed push attempt was
  rejected because the user has not explicitly authorized external GitHub
  egress for this new M10 payload.
- Next selected milestone: M11, the exact
  \(\Theta(k\log k)\) straight-line schedule boundary.

## M9 outcome

- Branch: `research/20260726-m9-divisor-rich-schedules`.
- Completed milestone: M9, an explicit-list exponent-encoding divisor barrier
  for the combined local \(p-1/p+1\) promises.
- `DEF-009` defines the exact integer one-length budget
  \[
  B(\ell)=(\ell+1)^{\lfloor\sqrt\ell\rfloor}2^{A_\ell}
  \]
  and its monotone envelope \(Q\), where \(A_\ell\) is the largest integer
  satisfying
  \((\lfloor\sqrt\ell\rfloor+1)^{A_\ell}<2^\ell\).
- `BAR-004` is `PROVED`: every exponent satisfies
  \(\tau(d)\le B(\ell(d))\), with
  \(\log_2Q(L)=O(L/\log L)\). A factorization-independent explicit schedule
  with polynomial list size and \(L(k)=o(k\log k)\) therefore hits at most
  \(2^{o(k)}\) odd primes.
- On every stipulated finite odd-prime population of size at least
  \(2^{\alpha k}\), whose distinct products all have common input length
  \(k\), the uniform combined-promised pair fraction is at most
  \(2^{-\alpha k+o(k)}\) and tends to zero. This is not a prime-distribution
  existence claim or a natural-density theorem.
- `REF-005` is `REFUTED`; NR-006 records the minimal bounded value-only
  counterexample \((d,p,q,N)=(7,3,5,15)\).
- EXP-0008 checked 262,143 exact divisor budgets and single-exponent hit
  bounds, 2,306,048 direct prime-oracle comparisons, 987 record-family bounds,
  and 46 selected Python/Rust/C# comparisons. Its canonical summary SHA-256
  is
  `b8357f9436ef4d31d072f62dab4f3c8dedad41d6f1787803bf5df2f485ca53ed`.
- Independent adversarial review reproduced the registered search and added
  200,000 divisor-budget checks, 128 small-length boundaries, 24 density caps,
  and 57 \(O(k)\)-bit large-value cases. It identified and verified repairs
  for upper-bound notation and oscillatory \(L(k)\). Independent source-scope
  review confirmed that the proof is elementary and requires no new citation,
  while prohibiting novelty, prime-distribution, recognizer, or general
  lower-bound framing.
- Full validation passed: foundation and publication consistency (38 claims,
  seven experiment hashes), 74 Python tests and bytecode compilation, Rust
  format/Clippy/17 tests, C# Release restore/build with zero warnings or
  errors, all registered M1--M9 searches and differential suites, and a clean
  converged 22-page XeLaTeX build. Every page was rendered and visually
  inspected; the stable PDF SHA-256 is
  `7bc17c4a48a02052b6bedc241cb9c81016542d701c920b652b383103276305fd`.
- Scope: the result does not cover compressed or batched implicit families,
  adaptive factor-dependent schedules, exponentially many explicit
  exponents, \(L(k)\not=o(k\log k)\), or other algebraic mechanisms. It is not
  a recognizer, natural-density theorem, factoring lower bound, or general
  classical factoring result.
- 한국어 요약: 명시적으로 나열하고 개별 평가하는 다항 개수의 지수는 각
  지수 길이가 \(o(k\log k)\)이면 전체 \(p\pm1\) 적중 소수 집합이
  준지수적 크기에 머문다. 지숫값이 인수보다 크다는 사실만으로는 약속
  포함을 보장하지 않는다.
- Next selected milestone: M10, specify one evaluable compressed or
  \(L(k)\not=o(k\log k)\) representation model before searching for an escape
  theorem or a stronger obstruction.

## M9 execution snapshot

- Date: 2026-07-26.
- Branch: `research/20260726-m9-divisor-rich-schedules`.
- Completed milestone: M9.
- Core implementation/proof commit:
  `1416d70a6bc39a4c7491e9ec86e4e67f96293962`.
- Registered experiment commit:
  `fcdb3eb76c942b6c8019ef3002b138385a7ec5b9`.
- Validated milestone completion commit:
  `12f2172aaaca8016baccca109d28e0e7cbb8db98`.
- Remote delivery: blocked by `BLK-011`; the policy-reviewed push attempt was
  rejected because the user has not explicitly authorized external GitHub
  egress for this new M9 payload.
- Next selected milestone: M10, a rigorously specified compressed or
  \(L(k)\not=o(k\log k)\) exponent representation with exact construction and
  evaluation accounting.

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
- Full validation passed: foundation and publication consistency (34 claims,
  six experiment hashes), 66 Python tests, Python bytecode compilation, Rust
  format/Clippy/16 tests, C# Release restore/build with zero warnings or
  errors, all registered M1--M8 searches and differential suites, and a clean
  converged 19-page XeLaTeX build. Every PDF page was rendered and visually
  inspected; the stable PDF SHA-256 is
  `70c926a864636f11206936ba13887f5847f5742f93a3f9e54d4ba4a1174e57a9`.
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

## M8 execution snapshot

- Date: 2026-07-26.
- Branch: `research/20260726-m8-promise-recognition`.
- Completed milestone: M8.
- Core implementation/proof commit:
  `bc8b25222823e06830530eac3962271c6d14a7ca`.
- Registered experiment commit:
  `a4895df3c0cf4de54b59932acf9f2e4ecbef2463`.
- Validated milestone completion commit:
  `3e2018616e6ac63e8f8632e42f65d34c22c00f90`.
- Remote delivery: blocked by `BLK-010`; the policy-reviewed push attempt was
  rejected because this new M8 payload lacks explicit authorization for
  external GitHub egress.
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
