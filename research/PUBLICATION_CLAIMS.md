# Publication Claim Matrix

This matrix is the M6 bridge between `research/CLAIMS.md` and
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
