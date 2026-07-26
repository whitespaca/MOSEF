# Research Status

## M20 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m20-iterated-quotient`.
- Completed milestone: M20, the public iterated geometric-quotient chain with
  \(M_0=1\), \(M_i=\prod_{j\le i}A_j\), and exact certificates
  \[
  S_{M_i}(X)=S_{M_{i-1}}(X)S_{A_i}(X^{M_{i-1}}).
  \]
- `DEF-020` charges every public factor and prefix, three binary evaluators
  per stage, both total denominator paths, all retained outputs and GCDs, the
  product aggregate, extraction, and requested dense, sparse, or expanded
  prefix output.
- `BAR-015` is `PROVED`: every stage follows BAR-014; a unit prefix preserves
  the quotient/numerator GCD, a proper prefix already factors \(N\), and a
  full prefix reduces the quotient GCD to public \(\gcd(A_i,N)\). Every
  composed denominator independently follows BAR-013. A proper final-product
  GCD implies a proper explicit stage-quotient GCD by a zero-safe unit/full
  dichotomy.
- For \(L=\sum_i\operatorname{bitlength}(A_i)\), every prefix has at most
  \(L\) bits, so compact evaluation uses \(O(rL)\) modular operations and
  \(r\le L\). Stage \(i\) has \(A_i\) sparse monomials,
  \(M_i-M_{i-1}+1\) dense positions, and a requested expanded prefix has
  \(M_i\) entries.
- Two independent reviews passed after repairs to a residue-level congruence,
  the zero-safe aggregate argument, expanded-prefix charging, and literal
  multiplication accounting. The adversarial review additionally passed
  58,680 small chains and a 256-bit prefix stress case.
- `REF-016` is `REFUTED`; NR-017 records that product-only iteration creates
  no success outside the charged stage and prefix exits. It may mask an
  earlier proper stage as a later full aggregate collision. This is not a
  lower bound for cross-stage addition, general rational programs, or
  arithmetic circuits.
- EXP-0019 checked 155 symbolic chains, 430 exact stage identities, 5,190
  coefficients, 190,805 modular chains, 529,330 stages, 338,525 prefix
  linkages, and 1,249,465 residue identities. All 68,260 proper final
  products had a proper stage quotient; there were zero unexplained cases and
  all 12 selected Python/Rust/C# comparisons agreed. Canonical summary
  SHA-256:
  `06cbbb13eca00655d33da9858117de6920d1e63f6bbfe95794ec18642000f9da`.
- Full gates passed: foundation and publication consistency (84 claims and 18
  experiment hashes), 147 Python tests and bytecode compilation, Rust
  formatting/Clippy/26 tests, C# Release restore/build with zero warnings or
  errors, 58 baseline comparisons, EXP-0019, and the 12-check M20
  differential validator.
- XeLaTeX converged with no warnings, undefined references or citations, or
  overfull/underfull boxes. All 50 pages were rendered and visually
  inspected. Stable PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `6cd6eaef92fda55c6eec886c65340a5a9150d4b3c09add6d281ef60cbb37fbe7`.
- Next action: M21 should define the smallest factorization-independent
  signed linear-combination grammar over explicit certified quotient stages
  and test whether cross-stage cancellation invalidates component-to-
  aggregate GCD implications.

## Korean summary

M20을 완료했습니다. 공개 인수 사슬의 각 기하급수 몫 단계를
unit/proper/full로 분기하면 새 인수 추출 경로가 생기지 않으며, 최종
곱의 GCD가 proper이면 명시된 단계 몫 중 하나도 proper임을
증명했습니다. 결정적 탐색, Python/Rust/C# 교차 검증, 독립 검토 두 건,
전체 출판 검사, 50쪽 PDF 시각 검증이 모두 통과했습니다. 다음 M21은
단계 값 사이의 덧셈과 뺄셈이 이 결론을 벗어나는지 조사합니다.

## M19 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m19-nested-quotient`.
- Completed milestone: M19, the cancellation-obscured two-stage identity
  \[
  S_{AB}(X)/S_A(X)=S_B(X^A).
  \]
- `DEF-019` and `BAR-014` distinguish the rational denominator \(S_A(g)\)
  from the composed denominator \(g^A-1\), give both paths total
  unit/proper/full semantics, and charge construction, residue, GCD,
  certificate, and expanded-output costs.
- `BAR-014` is `PROVED`: a unit intermediate denominator makes rational
  numerator and quotient GCDs identical; a proper denominator is already a
  factor; and a full denominator forces \(g^A\equiv1\pmod N\), so the
  quotient GCD is the public \(\gcd(B,N)\). The composed denominator
  independently follows BAR-013.
- Two independent adversarial reviews passed after repairing the
  residue-versus-GCD wording and the sparse/dense formal-output accounting.
  The quotient has degree \(A(B-1)\), \(B\) nonzero monomials, and
  \(A(B-1)+1\) dense coefficient positions.
- `REF-015` is `REFUTED`; NR-016 records that cancellation in this exact
  two-stage identity does not create a proper quotient success outside the
  rational numerator, proper intermediate denominator, public multiplier,
  and composed-denominator paths. This is not a general rational-circuit
  lower bound.
- EXP-0018 checked 144 symbolic identities, 6,084 coefficients, 177,264
  modular circuits, and 354,528 residue identities. The rational-denominator
  split was 120,444 unit, 46,932 proper, and 9,888 full cases; the composed
  split was 74,028 unit, 66,936 proper, and 36,300 full cases. There were zero
  unexplained reductions and all 12 selected Python/Rust/C# comparisons
  agreed. Canonical summary SHA-256:
  `a6d1bd1344b439901f3d40b9dc226fbcedcaba6886d07363461b0814db6aa2aa`.
- Full gates passed: foundation and publication consistency (80 claims and 17
  experiment hashes), 141 Python tests and bytecode compilation, Rust
  formatting/Clippy/25 tests, C# Release restore/build with zero warnings or
  errors, 58 baseline comparisons, EXP-0018, and the 12-check M19
  differential validator. Optional third-party pytest, Ruff, and mypy remain
  unavailable under BLK-003.
- XeLaTeX converged with no warnings, undefined references or citations, or
  overfull/underfull boxes. All 47 pages, including the revised title and
  abstract, Section 20, results table, limitations, conclusion, complete
  proof, and reproduction appendix, were rendered and visually inspected.
  Stable PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `783ccf5f60de1cad688c638f4ef59a3f69f5dfffcd3a596ace4637ac8867db8f`.
- The implementation/proof checkpoint is
  `557731c0feefe1c58b65ab24c6b7b6552cd392bc`; the validated completion
  commit is `5d15540d372642dd4ca61f5ecf324026dbd55adf`.
- The completion push was rejected before execution under BLK-021 because
  publishing this specific repository payload was not explicitly authorized.
  The remote branch remains at the checkpoint commit, GitHub CLI is
  unauthenticated, and no pull request was created or verified.
- Next action: M20 should formalize an iterated public factor chain
  \(M=\prod_i A_i\), give every prefix denominator a total branch, and test
  whether induction reduces every quotient success to a charged prefix exit
  or public multiplier.

## Korean summary

M19를 완료했습니다. 두 단계 기하급수 몫의 중간 분모와 합성 분모를
각각 unit/proper/full로 분기하면, 상쇄가 새로운 숨은 인수 추출 경로를
만들지 않음을 증명했습니다. 두 독립 검토와 세 언어 구현, 결정적
탐색, 전체 출판 검사, 47쪽 PDF 시각 검증이 통과했습니다. 다음 M20은
이 구조를 공개 인수 사슬의 여러 단계로 확장할 수 있는지 조사합니다.

## M18 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m18-geometric-sum`.
- Completed milestone: M18, the charged left-to-right binary circuit for
  \[
  S_M(X)=\sum_{i=0}^{M-1}X^i=\frac{X^M-1}{X-1}
  \]
  at an arbitrary public positive exponent \(M\).
- `DEF-018` gives the exact even/odd pair grammar for
  \((P_M,S_M)=(X^M,\sum_{i<M}X^i)\), total unit, proper-factor, or
  full-collision denominator semantics, and explicit charges for the encoded
  base and exponent, preprocessing, construction, operations, outputs, GCDs,
  extraction, and any expanded coefficient output.
- `BAR-013` is `PROVED`: a unit denominator makes quotient and endpoint GCDs
  identical; a proper denominator is already a factor; and a full denominator
  gives \(S_M(g)\equiv M\pmod N\), so the quotient GCD is the public
  \(\gcd(M,N)\). The proper branch preserves success existence, not divisor
  value: \(N=15,g=4,M=2\) gives denominator GCD \(3\), quotient GCD \(5\),
  and a full endpoint collision.
- For \(\ell=\operatorname{bitlength}(M)\), the exact composition counts are
  \(2(\ell-1)+\operatorname{popcount}(M)-1\) multiplications and
  \((\ell-1)+\operatorname{popcount}(M)-1\) additions. The post-reduction
  residue circuit is \(O(\ell\operatorname{poly}(k))\), while total work is
  polynomial in the charged base, modulus, and exponent lengths. Compact
  formal metadata uses \(O(\ell)\) bits; expanded output has \(M\) entries.
- `REF-014` is `REFUTED`; NR-015 records that compact arbitrary-exponent
  evaluation still produces one quotient value, not a new extraction path
  beyond endpoint, denominator, and public-exponent GCDs.
- EXP-0017 checked 64 symbolic identities, 2,080 coefficients, 320,896
  modular circuits, 1,323,696 binary-prefix steps, and 320,896 residue
  identities. All 166,784 unit, 134,272 proper, and 19,840 full denominator
  reductions held with zero unexplained reductions. All 12 selected
  Python/Rust/C# comparisons agreed. Canonical summary SHA-256:
  `0f182c819374451a3fd8d9ddb7ffc75580ac363186e19bd804eb28fe1371d2bd`.
- Independent source/scope review required explicit accounting for the
  encoded base length and reduction; the repaired review passed. Independent
  adversarial review passed the proof, \(M=1\), even and repeated-prime
  moduli, exact counters, \(M=2^{64}-1\), a 129-bit exponent in the
  arbitrary-precision implementations, and the registered three-language
  checks.
- Full gates passed: foundation and publication consistency (76 claims and
  16 experiment hashes), 135 Python tests and bytecode compilation, Rust
  format/Clippy/24 tests, C# Release restore/build with zero warnings or
  errors, 58 baseline comparisons, EXP-0017, and the 12-check M18
  differential validator. Optional third-party pytest, Ruff, and mypy remain
  unavailable under BLK-003.
- XeLaTeX converged with no warnings, undefined references or citations, or
  overfull/underfull boxes. All 45 pages, including the revised title and
  abstract, Section 19, results table, limitations, conclusion, complete
  proof, and reproduction appendix, were rendered and visually inspected.
  Stable PDF: `output/pdf/mosef-paper.pdf`, SHA-256
  `85eb9b46fad3ebd5b336be49d56bdcadcc750d0c203bc58e1889a08ac858c31e`.
- Core implementation/proof/paper commit:
  `9f36ee9c75d8f13d2883301da63404747e358bcc`.
- The core commit is synchronized to
  `origin/research/20260727-m18-geometric-sum`. No pull request was created
  or verified because GitHub CLI remains unauthenticated. The local
  status/cleanup follow-up is commit `c6f4dc3`; its push is blocked under
  BLK-020 because this specific external payload was not explicitly
  authorized.
- Next action: M19 should formalize the cancellation-obscured two-stage
  identity \(S_{AB}(X)/S_A(X)=S_B(X^A)\), including total intermediate
  denominator semantics and a division-free composed path.

## Korean summary

M18은 임의의 공개 지수 \(M\)에 대한 geometric sum을 이진 합성으로
\(O(\log M)\) 단계에 계산하지만, 새로운 인수분해 경로를 만들지는
못함을 증명했습니다. 분모가 unit이면 endpoint GCD와 같고, proper이면
분모 자체가 이미 인수이며, full collision이면 결과가 공개된
\(\gcd(M,N)\)로 환원됩니다. 이는 일반 rational circuit 하한이 아니며,
다음 단계는 중간 분모가 nonunit일 수 있는 두 단계 quotient입니다.

## M17 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m17-rational-circuit`.
- Completed milestone: M17, the charged dyadic exact-division and repeated
  composition circuit
  \[
  (X^{2^t}-1)/(X-1)=\sum_{i<2^t}X^i
  =\prod_{j<t}(X^{2^j}+1).
  \]
- `DEF-017` gives every denominator a total unit, proper-factor, or
  full-collision branch and retains the division-free product in every case.
  It charges the public factorization-free constructor, \(t\) squarings,
  \(t\) explicit dyadic factors, \(\max(0,t-1)\) product multiplications,
  extended-GCD division attempt, requested outputs, GCDs, and extraction.
- `BAR-012` is `PROVED`: valid division equals the factor product; every
  proper quotient GCD implies a proper dyadic-factor GCD; and every proper
  numerator GCD implies a proper denominator or dyadic-factor GCD. The
  proper factor value need not be identical: \(N=8,g=1,t=2\) has component
  GCDs \(2,2\) but quotient GCD \(4\).
- The compact circuit uses \(O(t+1)\) modular operations and
  \(O((t+1)\operatorname{poly}(k))\) bit operations. Degree and monomial
  metadata use \(O(t+1)\) bits, but an expanded formal coefficient output
  has \(2^t\) entries. Those monomials are terms of one quotient value, not
  separately extracted exponent tests.
- `REF-013` is `REFUTED`; NR-014 records that dyadic geometric compression
  cannot create an exponential test family or a proper success when every
  explicit component GCD is trivial or full. At \(N=15,g=4,t=1\),
  denominator/factor GCDs \(3,5\) aggregate to full numerator GCD \(15\).
  At \(N=6,g=1,t=3\), division has a full denominator collision while the
  division-free quotient GCD is \(2\).
- EXP-0016 checked 11 symbolic identities, 2,047 coefficients, 55,154
  modular circuits, 275,770 repeated-squaring recurrences, 55,154 product
  identities, 22,757 proper quotient implications, and 25,430 proper
  numerator implications with zero unexplained proper successes. All 12
  selected Python/Rust/C# comparisons agreed. Canonical summary SHA-256:
  `1db5968e635901bc00eda0fdaa211aefe16af630741459eb9eb7f51ab50fc219`.
- Independent source/scope review required exact unreduced lifts and weakened
  exact factor-value wording. Independent adversarial review additionally
  required \(t=0\) cost repair and exact implementation of the reported
  product multiplication count. Both repaired re-reviews passed.
- Full gates passed: foundation and publication consistency (72 claims and
  15 experiment hashes), 127 Python tests and bytecode compilation, Rust
  format/Clippy/23 tests, C# Release restore/build with zero warnings or
  errors, EXP-0016, and the 12-check differential validator. Optional
  third-party pytest, Ruff, and mypy remain unavailable under BLK-003.
- XeLaTeX converged with no warnings, undefined references or citations, or
  overfull/underfull boxes. All 43 pages, including the revised title and
  abstract, theorem, results, limitations, full proof, and reproduction
  appendix, were rendered and visually inspected. Stable PDF:
  `output/pdf/mosef-paper.pdf`, SHA-256
  `48e9b77dbe4973bc9e9e8b9a66b2efb61d7d5f7ff45224f1b1530f031e35abc9`.
- Local milestone implementation/proof/paper commit:
  `8a09b70497451a23711d853f94af0eb8b9fbeea4`.
- Remote publication is blocked under BLK-019: the safety reviewer rejected
  the M17 branch push because this specific external payload has not been
  explicitly authorized. GitHub CLI is also unauthenticated, so no pull
  request was created.
- Next action: M18 should formalize the arbitrary-exponent binary geometric
  sum \(S_M(X)\), including its odd/even composition recurrences and the
  full-denominator reduction \(S_M(1)\equiv M\pmod N\).

## Korean summary

M17은 \(2^t\)개 단항식을 가진 dyadic geometric quotient를 압축 계산해도
그것이 \(2^t\)개의 독립 GCD 검사가 되지는 않음을 보였습니다. 분모가
비가역인 경우도 proper factor, full collision, unit으로 모두 분기하며,
어떤 proper quotient 또는 numerator 성공도 분모나 \(t\)개 dyadic factor
중 하나의 proper 성공을 동반합니다. 일반 rational/compositional circuit에
대한 하한은 아니며, 다음 단계는 임의 지수 \(M\)의 binary geometric sum
회로입니다.

## M16 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m16-product-dag`.
- Completed milestone: M16, the explicit-atom product-only DAG whose shared
  subproducts are evaluated once while formal leaf occurrences remain
  non-materialized.
- `DEF-016` charges the public-input, factorization-free constructor, explicit
  exponent atoms, product gates, requested residue or formal outputs, GCDs,
  and extraction. `BAR-011` is `PROVED`: every node has an exact
  nonnegative atom-multiplicity product and positive-multiplicity
  prime-power valuation formula; every proper node GCD implies a proper used
  atom GCD; and gate \(s\) has at most \(2^s\) unfolded occurrences, tightly.
- Sharing therefore permits exponential repeated formal occurrences but does
  not synthesize exponentially many distinct exponent tests or a proper
  success absent from the explicit atom table. A complete optional formal
  table has \(O(a(a+t)(t+1))\) bits for \(a\) atoms and \(t\) gates.
  `REF-012` is `REFUTED`, and NR-013 records the scoped negative result.
- Aggregation can worsen extraction. The single atom at
  \(N=9,g=4,d=1\) has proper GCD \(3\), but its first self-product has full
  GCD \(9\). The complementary \(N=21,g=2,\Delta=(2,3)\) union collision
  also persists.
- The BAR-008 transfer remains separate: at each input length the explicit
  atom list must be common and factorization-independent, and its exponents
  must have \(O(k\log k)\) bits. Addition, subtraction, division,
  composition, closed-form atom synthesis, modulus-specific identities,
  adaptive factor dependence, other groups, and general arithmetic circuits
  remain outside BAR-011.
- EXP-0015 checked 611,572 exact product-DAG syntaxes, 3,033,586 gate
  occurrences, 517,020 residue circuits, 2,282,274 node semantics, and
  3,581,928 valuation components. All 856,512 proper-node implications held,
  84,013 product nodes masked a used atom success as a full collision, the
  exact occurrence maxima were \(2,4,8,16,32\), and the 10 selected
  Python/Rust/C# comparisons agreed. Canonical summary SHA-256:
  `431faf3c71fc0f13c3152bffd06faa5e7eb96382164e40611979c8573e41a12d`.
- Independent source-scope review required positive-multiplicity valuation
  sums to avoid \(0\cdot(+\infty)\) and removed unsupported minimality
  wording. Independent adversarial review required the \(t=0\) formal-table
  repair, a used-atom rather than global-atom audit predicate, the corrected
  84,013 reachable-mask count, and accurate all-moduli box wording. Both
  re-reviews passed.
- Full gates passed: foundation and publication consistency (68 claims and
  14 experiment hashes), 118 Python tests and bytecode compilation, Rust
  format/Clippy/22 tests, C# Release build with zero warnings or errors,
  EXP-0015, and the 10-check differential validator. Optional third-party
  pytest, Ruff, and mypy remain unavailable under BLK-003.
- XeLaTeX converged with no warnings, undefined references or citations, or
  overfull/underfull boxes. All 41 pages, including the revised abstract,
  theorem, results, limitations, full proof, and reproduction appendix, were
  rendered and visually inspected. Stable PDF:
  `output/pdf/mosef-paper.pdf`, SHA-256
  `6880cfc1740496123ea8aa9f8d8ad029de8adbfad4f29996b4750e9960989023`.
- Local milestone implementation/proof/paper commit:
  `0728628b5ffe5387b926080de8674f22d1c8dadf`.
- Remote publication is blocked under BLK-018: the safety reviewer rejected
  the M16 branch push because this specific external payload has not been
  explicitly authorized. GitHub CLI is also unauthenticated, so no pull
  request was created.
- Next action: M17 should formalize a richer rational or compositional
  circuit, beginning with the dyadic telescoping identity, and charge failed
  division, formal output, residue evaluation, and factor extraction.

## 한국어 요약

M16에서는 명시적으로 계산한 \(g^{d_i}-1\) 원자들을 곱셈 DAG에서
재사용하는 비물질화 모델을 검증했습니다. 공유를 통해 형식적 반복
횟수는 \(2^t\)까지 늘릴 수 있지만, 새로운 서로 다른 지수 검사를
만들거나 사용된 원자에 없던 인수를 얻을 수는 없습니다. 이 결과는
일반 산술 회로 하한이 아니며, 덧셈ㆍ나눗셈ㆍ합성ㆍ폐쇄형 원자 생성은
다음 연구 범위로 남습니다.

## M15 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m15-implicit-batch`.
- Completed milestone: M15, the selector-described standard product tree
  whose every selected residue leaf is enumerated, evaluated, stored, and
  charged.
- `DEF-015` fixes the leaf-materialized semantics. `BAR-010` is `PROVED`:
  the root GCD has the exact sum-of-prime-power-valuations formula, every
  proper root GCD implies a proper individual leaf GCD, aggregation may mask
  individual separators as a full collision, and an \(n\)-leaf binary tree
  has exactly \(n-1\) internal multiplications in addition to its \(n\)
  charged leaf evaluations and materializations.
- Polynomial charged work therefore permits only polynomially many
  materialized leaves. The BAR-008 transfer is separate: for each input
  length the complete leaf list must also be common and
  factorization-independent, and its ordinary exponent lengths must be
  \(O(k\log k)\). No result is claimed for specialized circuits without leaf
  materialization.
- `REF-011` is `REFUTED`; NR-012 records that compact selector syntax does
  not compress a standard materialized batch. The explicit witness
  \(N=21,g=2,\Delta=\{2,3\}\) has proper leaf GCDs \(3,7\) but root GCD
  \(21\).
- EXP-0014 checked 3,821,928 nonempty batches, 6,488,889 valuation
  components, 1,333,349 proper-root implications, and 4,096 exact tree
  counts. It recorded 850,538 masked separator batches. Its canonical summary
  SHA-256 is
  `c4c3f20cc193dc90728d19fa5809d794d9ee07474fe093f12439cf3d16508529`;
  the selected Python/Rust/C# differential validator passed 10 checks.
- Independent adversarial review initially rejected equality wording for a
  population upper bound and the missing common factorization-independent
  transfer hypothesis. Both were repaired, and re-review passed. Independent
  source-scope review found no external citation requirement and confirmed
  the non-general-circuit boundary.
- Full gates passed: foundation and publication consistency (64 claims and
  13 experiment hashes), 111 Python tests and bytecode compilation, Rust
  format/Clippy/21 tests, C# Release build with zero warnings or errors,
  EXP-0014, and the 10-check differential validator. XeLaTeX converged
  without final warnings to a 38-page PDF; all pages and the new theorem,
  proof, results, limitations, and reproduction pages were rendered and
  visually inspected. The stable PDF SHA-256 is
  `9ae325caaf98428d15443638e90063e4896b9fa191cb60c9d5b6145084280ca6`.
- Local milestone implementation/proof/paper commit:
  `21b6673898d672659412c0cb4300f6ed6c00a5f6`.
- The push was rejected before execution because this specific M15 payload
  lacks explicit authorization for external GitHub publication. BLK-017
  records the local-only branch, and no M15 pull request was created.
- Optional third-party Python `pytest`, Ruff, and mypy gates remain
  unavailable under BLK-003.
- Next selected milestone: M16, define the smallest uniform
  non-materializing product circuit and determine whether its formal output
  or proper-factor extraction can avoid DEF-015's leaf cost without assuming
  a general arithmetic-circuit lower bound.

## M14 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m14-addition-subtraction`.
- Completed milestone: M14, the explicitly charged same-base
  addition-subtraction representation beyond multiplication-only DEF-010.
- `DEF-014` charges every product, extended-GCD inversion, parent/sign/output
  table entry, and retained output after a base GCD precheck. `BAR-009` is
  `PROVED`: \(x_i=g^{z_i}\) and \(|z_i|\le2^i\); negative exponents give
  exactly the same raw GCD and capped valuations as their positive absolute
  values, while zero gives only the full collision. A common fixed-base
  schedule with \(T(k)=O(k\log k)\) therefore transfers to BAR-008 and has a
  \(2^{o(k)}\) factor-scale combined hit set and stipulated-population
  fraction \(2^{-\alpha k+o(k)}\).
- `REF-010` is `REFUTED`; NR-011 records that charged same-base ratios and
  inversions alone do not restore a nonvanishing exponent-mediated
  \(p-1/p+1\) promise fraction. Proper factors returned by the initial base
  GCD remain separate algorithmic exits.
- EXP-0013 completed 2,403,786 node-growth checks, 190,344 direct residue
  checks, 646,400 sign-symmetry checks, 10,100 unit prechecks, 6,127 proper
  nonunit prechecks, and 570 full-nonunit prechecks. It observed 734,190
  negative and 251,685 zero outputs and exact maxima
  \(1,2,4,8,16,32,64\). Its canonical summary SHA-256 is
  `7203d3fc6ee67d5af3984c2b5c1eefb1640275dccdecaf979fed645d2d0fbb7d`;
  the selected Python/Rust/C# differential validator passed 24 checks.
- Independent adversarial review reproduced the focused tests, registered
  experiment, and differential validator, then separately enumerated
  self-ratios and checked prime powers and 20,000 lower-bound boundary cases
  without finding a defect. Independent source-scope review found no new
  citation requirement and confirmed the theorem's charged, factor-oblivious,
  same-base, unit-branch scope.
- Full gates passed: foundation and publication consistency (60 claims and
  12 experiment hashes), 106 Python tests and bytecode compilation, Rust
  format/Clippy/20 tests, C# Release build with zero warnings or errors,
  EXP-0013, and the 24-check differential validator. XeLaTeX converged
  without final warnings to a 36-page PDF; all pages and the new theorem,
  proof, results, and reproduction pages were rendered and visually
  inspected. The stable PDF SHA-256 is
  `6ccdff994d04783b3a05170c28a1b6ccab9f1dca8c46dd8bbb64498655479f28`.
- Local milestone implementation/proof/paper commit:
  `e80115bd27200c0ec0f37a388cd4e9a4bbac9769`.
- Follow-up status commit: `4f92cbe`. The push failed because Windows Git
  had no credentials (`SEC_E_NO_CREDENTIALS`); BLK-016 records the
  unpublished branch, and no M14 pull request was created.
- The result excludes implicit exponential batches, fixed-modulus
  equal-residue shortcuts, factor-dependent adaptation, special
  endomorphisms, unrelated multi-base expressions, other groups/channels,
  population existence or natural density, and general factoring.
- Optional third-party Python `pytest`, Ruff, and mypy gates remain
  unavailable under BLK-003.
- Next selected milestone: M15, formalize the smallest explicitly charged
  implicit product/remainder-tree or arithmetic-circuit batch and determine
  whether it can test exponentially many factor-scale exponents without
  paying for output extraction.

## M13 outcome

- Date: 2026-07-27.
- Branch: `research/20260727-m13-general-factor-scale`.
- Completed milestone: M13, the general explicit factor-scale divisor
  question at the exact \(O(k\log k)\) exponent-length boundary.
- `DEF-013` gives the exact small/large-prime split budget. `BAR-008` is
  `PROVED`: every common polynomial-size explicit schedule whose exponents
  have bit length \(O(k\log k)\) hits only
  \(2^{O(k\log\log k/\log k)}=2^{o(k)}\) primes at any fixed
  \(O(k)\)-bit factor scale. BAR-003 therefore gives promised-pair fraction
  \(2^{-\alpha k+o(k)}\) on every stipulated common-input-length population
  of size at least \(2^{\alpha k}\), and BAR-005 transfers the conclusion to
  fixed-base DEF-010 schedules with \(O(k\log k)\) charged nodes.
- `REF-009` is `REFUTED`; NR-010 records that squareful multiplicities,
  prime powers, mixed exponents, and noninitial prime supports do not evade
  the boundary. The result excludes longer exponents, exponentially many
  explicit exponents, adaptive factor-dependent schedules, richer compressed
  representations, other group channels, population existence or natural
  density, and general factoring.
- EXP-0012 completed 1,572,816 split-bound checks, 4,421,736 exact
  divisor-membership checks, and 5,344,372 prime-candidate checks. Its
  canonical summary SHA-256 is
  `a564c00c8eaafad6f5be31d8705147578e6c86d9e6f42c6a9bacf3b0d93591d3`.
  The focused Python/Rust/C# validator passed 36 checks.
- Independent adversarial review reproduced the focused tests, registered
  experiment, differential validator, and publication gate, then added
  209,958 exact divisor-bound cases and 467,958 canonical
  labeled-occurrence mappings. It explicitly exercised 53,454 \(A=0\),
  37,864 \(J=0,A>0\), 97,702 \(A<2J\), and 20,938
  \(A\ge2J,J>0\) cases without finding a defect.
- Independent source review found no imported theorem or new citation
  requirement: BAR-008 is elementary and depends only on proved internal
  BAR-003 and BAR-005. The manuscript avoids novelty claims.
- Full gates passed: foundation and publication consistency (56 claims and
  11 experiment hashes), 99 Python tests and bytecode compilation, Rust
  format/Clippy/19 tests, C# Release build with zero warnings or errors, the
  registered experiment and focused differential validator, and a clean
  converged 33-page XeLaTeX build. All pages and the new theorem/proof pages
  were rendered and visually inspected. The stable PDF SHA-256 is
  `7d821784f7aabc1b8791101189ce7844a157f5299f6fa60d9b35b747316cec4d`.
- Local milestone commit:
  `6628ea8158458ba2b3c660ee9d70fc651fa0bbfa`. The sandboxed push lacked
  Windows credentials, and external publication was not authorized; BLK-015
  records the unpublished branch. GitHub CLI is unauthenticated, so no M13
  pull request was created.
- Optional third-party Python `pytest`, Ruff, and mypy gates remain
  unavailable under BLK-003.
- Next selected milestone: M14, formalize a minimal explicitly costed
  representation outside DEF-010 and test whether it can expose
  factor-scale divisor families beyond BAR-008 without hidden exponential
  expansion.

## M12 outcome

- Date: 2026-07-27.
- Branch: `research/20260726-m12-prime-yield`.
- Completed milestone: M12, the critical/supercritical first-primes
  primorial prime-yield question at target-factor scale.
- `DEF-012` defines the exact factorial support threshold and binomial
  divisor-candidate bound. `BAR-007` is `PROVED`: for \(r(k)=O(k)\), only
  \(2^{O(k\log\log k/\log k)}=2^{o(k)}\) divisors of \(P_{r(k)}\) are small
  enough to equal \(q\pm1\) for \(q\le2^{\beta k}\). Hence the promised-pair
  fraction is at most \(2^{-\alpha k+o(k)}\) on every stipulated
  \(2^{\alpha k}\)-size common-input-length population.
- `REF-008` is `REFUTED`; NR-009 records the scale mismatch between
  \(2^{\Theta(k)}\) total primorial divisors and the subexponential
  factor-scale subset. The result uses no prime-distribution hypothesis and
  does not extend to arbitrary boundary exponent families.
- EXP-0011 completed 9,961,434 divisor checks, 145,413 support checks,
  290,826 prime-candidate checks, 16 balanced-population formula checks, 32
  cross-language comparisons, and four Python-only scale-bound records. Its
  canonical summary SHA-256 is
  `bad46ee8f6638d98d19bc4479da998ea55af4d1617fef10cfc2c3ea973f39751`.
- Independent adversarial review found and then verified the repair of the
  omitted \(T\le r<2T\) binomial case. Its extra audit checked 139,986 exact
  thresholds/formulas, 20,010 divisor supports, 153,456 channel-disjointness
  cases, 9,352 nested-hit containments, and 500 factorial/node transfers.
- Independent source review confirmed Lichtman's exact power-scale
  shifted-prime theorem and that it supplies no polylogarithmic,
  square-free, primorial-supported, or simultaneous-channel yield statement.
- Full gates passed: foundation and publication consistency (52 claims and
  ten experiment hashes), 93 Python tests and bytecode compilation, Rust
  format/Clippy/19 tests, C# Release build with zero warnings or errors, the
  registered M12 experiment and 36-count focused validator, and a clean
  converged 30-page XeLaTeX build. The updated sections and full proof were
  rendered and visually inspected. The stable PDF SHA-256 is
  `8fbc253727c4f42bd1e1248f09ca9a67431692ea4faea189a3f0fce11bcf8ee5`.
- Local milestone commit:
  `53915509bc257f343f61a814b1ec90bcd0ed8aeb`. The sandboxed push lacked
  Windows credentials, and the external push was not authorized; BLK-014
  records that the local branch is ahead of its existing remote ref. No M12
  pull request exists.
- Optional third-party Python `pytest`, Ruff, and mypy gates remain
  unavailable under BLK-003.
- Next selected milestone: M13, classify non-primorial squareful and
  noninitial-support exact-boundary families by factor-scale divisor yield
  per charged construction node.

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
