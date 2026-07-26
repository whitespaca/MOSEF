# Publication Claim Matrix

This matrix is the executable bridge between `research/CLAIMS.md` and
`paper/main.tex`. It records every public claim exactly once. The executable
gate `python scripts/check_publication.py` verifies ID and status agreement;
the evidence and scope remain authoritative in the full claims ledger.

| ID | Status | Manuscript role | Evidence anchor |
|---|---|---|---|
| DEF-001 | DEFINITION | Binary input length | `CODEX.md` section 4 |
| DEF-002 | DEFINITION | Support separator | `research/proofs/M2-formal-specification.md` |
| DEF-003 | DEFINITION | Capped valuation profile | `research/proofs/M2-formal-specification.md` |
| DEF-004 | DEFINITION | Hereditary semismooth-asymmetry promise | `research/proofs/THM-001-semismooth-promise.md` |
| LEM-001 | PROVED | Support-separator sufficiency | `research/proofs/M2-formal-specification.md` |
| LEM-002 | PROVED | Exact prime-power GCD criterion | `research/proofs/M2-formal-specification.md` |
| THM-001 | PROVED | Las Vegas factoring on the hereditary promise class | `research/proofs/THM-001-semismooth-promise.md` |
| EXT-001 | PROVED | Imported polynomial-time primality theorem | `research/literature/BASELINE.md` SRC-001 |
| EXT-002 | PROVED | Imported rigorous randomized factoring bound | `research/literature/BASELINE.md` SRC-002 |
| OPEN-001 | REFUTED | All-composite support-only target | `research/NEGATIVE_RESULTS.md` NR-001 |
| OPEN-002 | OPEN | Residual-composite support-POSF constructor | `research/proofs/M2-formal-specification.md` |
| OPEN-003 | OPEN | Universal valuation-separating constructor | `research/proofs/M2-formal-specification.md` |
| REF-001 | REFUTED | Fixed-base divisibility-asymmetry shortcut | `research/NEGATIVE_RESULTS.md` NR-002 |
| EMP-001 | EMPIRICAL | Cross-language baseline agreement | `schemas/baseline-vectors-v1.json` |
| EMP-002 | EMPIRICAL | Bounded separator falsification | `research/experiments/EXP-0002-m2-separator-search.md` |
| EMP-003 | EMPIRICAL | Bounded semismooth theorem audit | `research/experiments/EXP-0003-m3-semismooth-search.md` |
| DEF-005 | DEFINITION | Divisibility signatures | `research/proofs/BAR-001-divisor-cover-separation-gap.md` |
| EXT-003 | CONDITIONAL | Imported Umans-Wang conditional theorem | `research/literature/SRC-004-umans-wang-divisor-conjecture.md` |
| BAR-001 | PROVED | Coverage-separation barrier | `research/proofs/BAR-001-divisor-cover-separation-gap.md` |
| REF-002 | REFUTED | Coverage-implies-separation transfer | `research/NEGATIVE_RESULTS.md` NR-003 |
| EMP-004 | EMPIRICAL | Bounded difference-cover audit | `research/experiments/EXP-0004-m4-difference-cover-search.md` |
| DEF-006 | DEFINITION | Exact multiplicative and Lucas channels | `research/proofs/BAR-002-conjugate-channel-correlation.md` |
| EXT-004 | PROVED | Imported Williams-Lucas congruences | `research/literature/SRC-005-williams-p-plus-one.md` |
| BAR-002 | PROVED | Conjugate-channel correlation barrier | `research/proofs/BAR-002-conjugate-channel-correlation.md` |
| REF-003 | REFUTED | Conjugate pairing as an independent channel | `research/NEGATIVE_RESULTS.md` NR-004 |
| EMP-005 | EMPIRICAL | Bounded conjugate-channel audit | `research/experiments/EXP-0005-m5-multigroup-correlation.md` |
| DEF-007 | DEFINITION | Hereditary nonsplit Lucas-asymmetry promise | `research/proofs/THM-002-nonsplit-lucas-promise.md` |
| LEM-003 | PROVED | Exact Lucas root and nonsplit-parameter counts | `research/proofs/THM-002-nonsplit-lucas-promise.md` |
| THM-002 | PROVED | Las Vegas factoring on the hereditary nonsplit promise class | `research/proofs/THM-002-nonsplit-lucas-promise.md` |
| EMP-006 | EMPIRICAL | Bounded nonsplit Lucas theorem audit | `research/experiments/EXP-0006-m7-nonsplit-lucas.md` |
| DEF-008 | DEFINITION | Combined \(p-1/p+1\) schedule signature | `research/proofs/BAR-003-combined-promise-density.md` |
| BAR-003 | PROVED | Common-schedule finite-distribution and magnitude barrier | `research/proofs/BAR-003-combined-promise-density.md` |
| REF-004 | REFUTED | Small-magnitude combined-promise coverage | `research/NEGATIVE_RESULTS.md` NR-005 |
| EMP-007 | EMPIRICAL | Bounded combined-promise density audit | `research/experiments/EXP-0007-m8-promise-density.md` |
| DEF-009 | DEFINITION | Exact exponent-bit-length divisor budget | `research/proofs/BAR-004-exponent-encoding-divisor-budget.md` |
| BAR-004 | PROVED | Explicit-schedule exponent-encoding divisor barrier | `research/proofs/BAR-004-exponent-encoding-divisor-budget.md` |
| REF-005 | REFUTED | Large exponent value as a coverage guarantee | `research/NEGATIVE_RESULTS.md` NR-006 |
| EMP-008 | EMPIRICAL | Bounded exponent-encoding divisor audit | `research/experiments/EXP-0008-m9-divisor-budget.md` |
| DEF-010 | DEFINITION | Factor-oblivious multiplication straight-line model | `research/proofs/BAR-005-multiplication-straight-line-compression.md` |
| BAR-005 | PROVED | Multiplication straight-line compression barrier | `research/proofs/BAR-005-multiplication-straight-line-compression.md` |
| REF-006 | REFUTED | Compact tower descriptor as compact evaluation | `research/NEGATIVE_RESULTS.md` NR-007 |
| EMP-009 | EMPIRICAL | Bounded multiplication-program audit | `research/experiments/EXP-0009-m10-compressed-exponents.md` |
| EXT-005 | PROVED | Imported explicit upper bound for the \(n\)-th prime | `research/literature/SRC-006-rosser-schoenfeld-primes.md` |
| DEF-011 | DEFINITION | Constant-sensitive exact divisor budget | `research/proofs/BAR-006-boundary-constant.md` |
| BAR-006 | PROVED | Exact-boundary hit-set coefficient barrier | `research/proofs/BAR-006-boundary-constant.md` |
| REF-007 | REFUTED | Boundary node count as a sufficient guarantee | `research/NEGATIVE_RESULTS.md` NR-008 |
| EMP-010 | EMPIRICAL | Bounded primorial-boundary audit | `research/experiments/EXP-0010-m11-boundary-schedule.md` |
