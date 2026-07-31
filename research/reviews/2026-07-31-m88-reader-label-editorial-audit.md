# M88 reader-label editorial audit

Date: 2026-07-31

## Question

Can the six focused manuscripts replace code-first claim headings with
readable mathematical roles and subjects while keeping every stable ID,
status, evidence anchor, and bilingual ordering intact?

## Presentation rule

The shared preambles define a three-argument `readerclaim` wrapper. It renders
a compact bold reader label, then the existing `claimstatus` token, and lets
the statement continue in the same paragraph. The wrapper does not allocate a
new theorem number, infer status, or replace the authoritative ID.

Each language uses exactly five families:

| English | Korean | Purpose |
|---|---|---|
| Theorem | 정리 | Full restricted or classification theorem |
| Proposition | 명제 | Exact identity, count, criterion, or evaluator result |
| Counterexample and criterion | 반례와 판정 | Explicit failure plus exact replacement criterion |
| Barrier | 장벽 | Scoped impossibility, sparsity, or cost boundary |
| Finite certificate | 유한 인증서 | Complete bounded family-relative certificate |

## Exact bilingual map

| Stable ID | English reader heading | Korean reader heading |
|---|---|---|
| THM-001 | Theorem: Hereditary \(p-1\) complete factorization | 정리: 유전적 \(p-1\) 완전 인수분해 |
| BAR-001 | Counterexample and criterion: Coverage is not separation | 반례와 판정: 약수 포함은 차수 분리가 아니다 |
| BAR-002 | Proposition: Conjugate channels have identical support | 명제: 켤레 채널의 support는 동일하다 |
| LEM-003 | Proposition: Exact Lucas root count | 명제: 정확한 Lucas root 개수 |
| THM-002 | Theorem: Hereditary nonsplit \(p+1\) complete factorization | 정리: 유전적 비분할 \(p+1\) 완전 인수분해 |
| BAR-003 | Barrier: Common-schedule density ceiling | 장벽: 공통 schedule의 분포 상한 |
| BAR-004 | Barrier: Subcritical exponent-list sparsity | 장벽: 임계 미만 지수 목록의 희소성 |
| BAR-018 | Proposition: Stage coprimality and exact resultant | 명제: stage 서로소성과 정확한 resultant |
| BAR-019 | Proposition: Total content and resultant reduction | 명제: total content 및 resultant 축약 |
| THM-003 | Theorem: Rational root-of-unity ratios | 정리: 유리 root-of-unity 비율 |
| BAR-020 | Proposition: Division-free exceptional cofactors | 명제: 나눗셈 없는 예외 cofactor |
| BAR-021 | Proposition: Branch-total cofactor extraction | 명제: branch-total cofactor 추출 |
| BAR-022 | Barrier: Exponentially costly exact lifts | 장벽: 지수적으로 비싼 exact lift |
| BAR-023 | Barrier: One-bit cofactor support | 장벽: cofactor support 한 비트 |
| BAR-024 | Proposition: Signature separation | 명제: signature 분리 |
| THM-004 | Finite certificate: Base cap through length 15 | 유한 인증서: 길이 15까지의 base cap |
| THM-005 | Finite certificate: Offset 11 through length 20 | 유한 인증서: 길이 20까지의 offset 11 |
| THM-014 | Finite certificate: Length-29 nonmonotonicity | 유한 인증서: 길이 29 비단조성 |
| THM-019 | Finite certificate: Length-34 endpoint | 유한 인증서: 길이 34 endpoint |
| BAR-041 | Barrier: Polynomial numeric-cap failure | 장벽: 다항 numeric-cap 실패 |
| BAR-046 | Barrier: Compact-gap failure below \(1/2\) | 장벽: \(1/2\) 미만 compact-gap 실패 |

Presenting LEM-003 as a reader proposition does not rename it: `LEM-003` stays
visible and remains the stable ledger key. Likewise, `BAR` headings may be
propositions, a counterexample and criterion, or barriers according to the
mathematical statement rather than the repository chronology.

## Executable audit

`scripts/check_m88_reader_labels.py` is 307 lines and uses only the Python
standard library. It checks:

- exactly one three-argument reader-label macro in each preamble;
- exact English/Korean kind and title for every stable ID;
- seven claims in the fixed order in each focused paper;
- one reader wrapper around every raw `claimstatus` occurrence;
- `PROVED` on all 42 rendered headings;
- exact bilingual ID order for each paper pair; and
- no internal ID reused as a reader kind or title.

Nine targeted tests pass: one validates the current repository, and eight
mutation tests reject a missing macro, an unwrapped claim, kind drift, title
drift, ID drift, status drift, order drift, and Korean-map drift. The existing
M87 gate still reports the same abstract counts, 24 cost rows, and 21
bilingual claim IDs.

## Projection and rendered review

The regenerated M82 portfolio still covers 270 claims: 21 focused and 249
archive-only. Its canonical SHA-256 is
`29e50a466e5ba7e0d88f4fd6c8aa4450d5843887535452a74eb1bdadc4db9449`.
The regenerated M83 audit still contains six inspected sources, seven
synchronized rows, and no priority claim. Its canonical SHA-256 is
`6b3af11eae78bed03abf56a1bd96e938218aaed4e725f327369f96102bd69525`.

All six final XeLaTeX logs contain zero selected undefined-reference,
undefined-citation, missing-character, overfull, underfull, LaTeX, package,
or rerun warnings. Every page was rendered into a contact sheet and
inspected. All 42 headings are readable, IDs and statuses remain adjacent,
and there is no visible clipping, overlap, or missing Korean glyph. An
initial forced paragraph layout created almost-empty reference pages; compact
inline typography removed them. The finite-certificate English last page was
expanded by three baselines, then re-rendered to confirm safe bottom margin.

| Focused paper | Pages | SHA-256 |
|---|---:|---|
| promise factorization, English | 6 | `398fb90c933f1c55c7696eb3103016921b6eda302c31f3d6a704f766d41b50de` |
| promise factorization, Korean | 5 | `67a0c444eaa3346c812920ad91044e6fdbac6f7582839838530bac99d964d39b` |
| cyclotomic extraction, English | 5 | `8d9bbd9e4842b69b16cbf39bd72ac88ee7019f2f0986c4ab8850e8e3ce221ba5` |
| cyclotomic extraction, Korean | 5 | `16a87ad22607feb9ab184d4b6e777643174df432138dcdfae46c76ea5da37684` |
| finite certificates, English | 6 | `ffce87870effe8ed2fee6f6be86215381c294ccbe9704a55c28bb4db288963a4` |
| finite certificates, Korean | 6 | `f22cb270bb05c51286f2c7268876a652c0e3bc4fc36dec059b43c4a2c8748501` |

## Scope

M88 is editorial. It changes no authoritative statement, status, proof,
experiment, source assessment, complexity model, or finite certificate.
General classical polynomial-time integer factoring remains open.
