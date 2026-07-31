# M87 focused-paper cost-model editorial audit

Date: 2026-07-31

## Question

Can the three focused bilingual paper pairs satisfy the supplied feedback by
putting one explicit online/offline cost model before the first section and
keeping every abstract between 200 and 300 words without changing a
mathematical claim?

## Counting convention

`scripts/check_m87_focused_papers.py` uses a language-neutral lexical-token
count. It strips LaTeX commands and comments, counts each inline or display
mathematical expression as one token, and counts the remaining Unicode
letter-or-number runs. This is deliberately reproducible for both English and
Korean; it is an editorial gate, not a linguistic claim about Korean eojeol.

The frozen counts are:

| Focused paper | English | Korean |
|---|---:|---:|
| promise factorization | 226 | 204 |
| cyclotomic extraction | 231 | 200 |
| finite certificates | 235 | 203 |

All six values lie in the inclusive 200--300 interval.

## Front-loaded cost ledgers

Each manuscript contains exactly one four-row `costmodel` environment after
the abstract and before the first numbered section. The 24 synchronized rows
make these boundaries explicit:

- Promise factorization charges public schedule construction, exact
  preprocessing, fresh sampling, modular or Lucas evaluation, every GCD,
  recursion, output verification, and output. Witness factors, promise
  membership, and factor-dependent schedules are not inputs. Group counts,
  tail bounds, counterexample searches, and reproducibility records are
  offline proof work. Expected polynomial bit complexity is asserted only on
  the stated hereditary promises; the total wrapper may return `UNRESOLVED`.
- Cyclotomic extraction charges public-parameter construction and encoding,
  compact stage and cofactor evaluation, coefficient reduction, every GCD and
  failed inversion, factor extraction, and requested output. Root-of-unity
  classification, polynomial identities, resultant derivation,
  counterexample search, and reproducibility records are offline. Dense or
  sparse exact materialization is charged by actual output size. The theorem
  applies only to the stated signed depth-two grammar.
- Finite certificates charge public descriptor construction and encoding,
  compact modular exits, every GCD and failed inversion, factor extraction,
  and verified output. Population enumeration, cap search, support-signature
  normalization, collision refinement, certificate generation, hashing, and
  rendering are offline proof costs. Prime factors, population membership,
  support signatures, selected certificate columns, and threshold-search
  results are not online inputs. The generator may be expensive and is not
  claimed polynomial; the proved online statement is finite and
  family-relative.

Repeated opening prose was condensed only after these ledgers were present.
No cost was moved from an evaluator into an offline certificate generator.

## Claim and projection audit

The checker fixes exactly seven representative claim IDs for each paper and
requires their `PROVED` status in both languages. It found 21 bilingual claim
IDs with exact status parity and no duplicate or missing cost ledger. The M82
projection still accounts for 270 ledger claims: 21 focused and 249
archive-only. The M83 matrix still contains six inspected sources and seven
synchronized `NO_PRIORITY_CLAIM` rows.

The M82 canonical portfolio SHA-256 is
`3a88d6c71bef8d438c3e660722626360e3282bb63b8c8b481b9fbe55efcffbce`.
The M83 canonical audit SHA-256 is
`756eea8cdeb733ef78ed6c82f3abe6ef07938d048be47c4d840013dc614c11c8`.

## Validation and rendered review

- The 292-line checker passed on all six manuscripts.
- Nine targeted tests cover the frozen counts, math-token convention,
  short/long rejection, label drift, an empty cost row, a late cost box, and
  claim-ID/status drift.
- Targeted Ruff and strict mypy checks passed.
- All six XeLaTeX builds converged. Final logs contain no selected undefined
  reference, undefined citation, missing-character, overfull, underfull,
  LaTeX, package, or rerun warning.
- Page-1 renders were inspected for all six manuscripts. Each abstract and
  complete cost ledger is visible before section 1, Korean glyphs render, and
  no clipping or overlap is visible.

PDF records:

| Focused paper | Pages | SHA-256 |
|---|---:|---|
| promise factorization, English | 6 | `1aa0b7bb79f4adee90b4a558128683cdd8f0d43a4a3c3ea952ed784fea80a35b` |
| promise factorization, Korean | 5 | `b83f2d9da9618273816a51c089184c167474f075ccca15238808701c0b7d1b17` |
| cyclotomic extraction, English | 5 | `fb15247d74dc3bcb5eb3c2eb4168cf2971050c219e7b4921aeeaf158bcd06635` |
| cyclotomic extraction, Korean | 5 | `f9dc3f4daff4425c1634d9d926dc0ec26a9233fb0afa618d24642a9c53729c74` |
| finite certificates, English | 6 | `c5df795c47ad0789abb4a27a7212963e57caafe466563d634c830f3e8ebbe60a` |
| finite certificates, Korean | 6 | `84afe41cabe3b0cf5ea293a0892407451af17e4ea311b6c2d8d410a1e7d081ac` |

## Scope

M87 is an editorial milestone. It changes no authoritative claim status,
proof, experiment, certificate, or source assessment. In particular, the
finite certificates remain bounded through \(m=34\), the hereditary promises
remain unrecognized, and general classical polynomial-time integer factoring
remains open.
