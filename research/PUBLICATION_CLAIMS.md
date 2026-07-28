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
| EXT-006 | PROVED | Imported power-scale shifted-prime smoothness theorem | `research/literature/SRC-007-lichtman-shifted-smooth-primes.md` |
| DEF-012 | DEFINITION | Factor-scale primorial support and divisor bound | `research/proofs/BAR-007-primorial-factor-scale.md` |
| BAR-007 | PROVED | Factor-scale first-primes primorial scarcity barrier | `research/proofs/BAR-007-primorial-factor-scale.md` |
| REF-008 | REFUTED | Total primorial divisor capacity as factor-scale yield | `research/NEGATIVE_RESULTS.md` NR-009 |
| EMP-011 | EMPIRICAL | Bounded factor-scale primorial audit | `research/experiments/EXP-0011-m12-primorial-scale.md` |
| DEF-013 | DEFINITION | General small/large-prime factor-scale divisor budget | `research/proofs/BAR-008-general-factor-scale.md` |
| BAR-008 | PROVED | General explicit-schedule exact-boundary factor-scale barrier | `research/proofs/BAR-008-general-factor-scale.md` |
| REF-009 | REFUTED | Squareful or noninitial support as a boundary escape | `research/NEGATIVE_RESULTS.md` NR-010 |
| EMP-012 | EMPIRICAL | Bounded arbitrary-exponent factor-scale audit | `research/experiments/EXP-0012-m13-general-factor-scale.md` |
| DEF-014 | DEFINITION | Charged same-base addition-subtraction program model | `research/proofs/BAR-009-addition-subtraction.md` |
| BAR-009 | PROVED | Addition-subtraction factor-scale transfer barrier | `research/proofs/BAR-009-addition-subtraction.md` |
| REF-010 | REFUTED | Charged inversion alone as a factor-scale escape | `research/NEGATIVE_RESULTS.md` NR-011 |
| EMP-013 | EMPIRICAL | Bounded addition-subtraction program audit | `research/experiments/EXP-0013-m14-addition-subtraction.md` |
| DEF-015 | DEFINITION | Charged leaf-materialized standard product-tree model | `research/proofs/BAR-010-implicit-batch.md` |
| BAR-010 | PROVED | Leaf-materialized implicit-batch barrier | `research/proofs/BAR-010-implicit-batch.md` |
| REF-011 | REFUTED | Compact selector as polynomial-cost materialized batch | `research/NEGATIVE_RESULTS.md` NR-012 |
| EMP-014 | EMPIRICAL | Bounded leaf-materialized batch audit | `research/experiments/EXP-0014-m15-implicit-batch.md` |
| DEF-016 | DEFINITION | Charged explicit-atom non-materializing product-DAG model | `research/proofs/BAR-011-product-dag.md` |
| BAR-011 | PROVED | Explicit-atom product-DAG sharing barrier | `research/proofs/BAR-011-product-dag.md` |
| REF-012 | REFUTED | DAG sharing as distinct exponential exponent coverage | `research/NEGATIVE_RESULTS.md` NR-013 |
| EMP-015 | EMPIRICAL | Bounded non-materializing product-DAG audit | `research/experiments/EXP-0015-m16-product-dag.md` |
| DEF-017 | DEFINITION | Charged dyadic exact-division/composition model | `research/proofs/BAR-012-dyadic-telescope.md` |
| BAR-012 | PROVED | Dyadic telescope extraction barrier | `research/proofs/BAR-012-dyadic-telescope.md` |
| REF-013 | REFUTED | Dyadic monomial compression as an exponential test family | `research/NEGATIVE_RESULTS.md` NR-014 |
| EMP-016 | EMPIRICAL | Bounded dyadic telescope audit | `research/experiments/EXP-0016-m17-dyadic-telescope.md` |
| DEF-018 | DEFINITION | Charged arbitrary-exponent binary geometric-sum model | `research/proofs/BAR-013-arbitrary-geometric-sum.md` |
| BAR-013 | PROVED | Endpoint-denominator-public-exponent extraction trichotomy | `research/proofs/BAR-013-arbitrary-geometric-sum.md` |
| REF-014 | REFUTED | Arbitrary geometric sum as an unaccounted extraction path | `research/NEGATIVE_RESULTS.md` NR-015 |
| EMP-017 | EMPIRICAL | Bounded arbitrary geometric-sum audit | `research/experiments/EXP-0017-m18-geometric-sum.md` |
| DEF-019 | DEFINITION | Charged nested geometric-quotient model with two total denominator paths | `research/proofs/BAR-014-nested-geometric-quotient.md` |
| BAR-014 | PROVED | Nested geometric-quotient extraction trichotomy | `research/proofs/BAR-014-nested-geometric-quotient.md` |
| REF-015 | REFUTED | Intermediate cancellation as an unaccounted extraction path | `research/NEGATIVE_RESULTS.md` NR-016 |
| EMP-018 | EMPIRICAL | Bounded nested geometric-quotient audit | `research/experiments/EXP-0018-m19-nested-quotient.md` |
| DEF-020 | DEFINITION | Charged iterated geometric-quotient-chain model with explicit stage exits | `research/proofs/BAR-015-iterated-geometric-quotient.md` |
| BAR-015 | PROVED | Stagewise and aggregate iterated-quotient extraction barrier | `research/proofs/BAR-015-iterated-geometric-quotient.md` |
| REF-016 | REFUTED | Public quotient-chain iteration as an unaccounted extraction path | `research/NEGATIVE_RESULTS.md` NR-017 |
| EMP-019 | EMPIRICAL | Bounded iterated geometric-quotient-chain audit | `research/experiments/EXP-0019-m20-iterated-quotient.md` |
| DEF-021 | DEFINITION | Charged signed linear combination of explicit quotient stages | `research/proofs/BAR-016-quotient-linear-combination.md` |
| BAR-016 | PROVED | Signed aggregation separates from the product component implication | `research/proofs/BAR-016-quotient-linear-combination.md` |
| REF-017 | REFUTED | Proper signed aggregates require proper charged components | `research/NEGATIVE_RESULTS.md` NR-018 |
| EMP-020 | EMPIRICAL | Bounded signed quotient-stage combination audit | `research/experiments/EXP-0020-m21-quotient-linear-combination.md` |
| DEF-022 | DEFINITION | Charged symmetric quotient-difference endpoint/cofactor model | `research/proofs/BAR-017-symmetric-quotient-difference.md` |
| BAR-017 | PROVED | Exact symmetric quotient-difference valuation reduction | `research/proofs/BAR-017-symmetric-quotient-difference.md` |
| REF-018 | REFUTED | Symmetric difference as an unclassified extraction mechanism | `research/NEGATIVE_RESULTS.md` NR-019 |
| EMP-021 | EMPIRICAL | Bounded symmetric quotient-difference audit | `research/experiments/EXP-0021-m22-symmetric-quotient-difference.md` |
| DEF-023 | DEFINITION | Charged unequal depth-two signed-reduction model | `research/proofs/BAR-018-unequal-signed-reduction.md` |
| BAR-018 | PROVED | Exact unequal signed prefix and common-step reduction | `research/proofs/BAR-018-unequal-signed-reduction.md` |
| REF-019 | REFUTED | Natural common factor as a complete unequal-difference explanation | `research/NEGATIVE_RESULTS.md` NR-020 |
| EMP-022 | EMPIRICAL | Bounded unequal signed-reduction audit | `research/experiments/EXP-0022-m23-unequal-signed-reduction.md` |
| DEF-024 | DEFINITION | Charged primitive rational-residue and stage-resultant audit | `research/proofs/BAR-019-rational-residue-resultants.md` |
| BAR-019 | PROVED | Exact content, stage-resultant, and root-of-unity reduction | `research/proofs/BAR-019-rational-residue-resultants.md` |
| REF-020 | REFUTED | Boundary and common-step factors as a complete cyclotomic classification | `research/NEGATIVE_RESULTS.md` NR-021 |
| EMP-023 | EMPIRICAL | Bounded rational-residue and cyclotomic audit | `research/experiments/EXP-0023-m24-rational-residue-audit.md` |
| DEF-025 | DEFINITION | Charged Galois-orbit rational root ratio model | `research/proofs/THM-003-rational-root-orbits.md` |
| THM-003 | PROVED | Complete rational root-of-unity ratio classification | `research/proofs/THM-003-rational-root-orbits.md` |
| REF-021 | REFUTED | Conjugation phase congruence as a sufficient condition | `research/NEGATIVE_RESULTS.md` NR-022 |
| EMP-024 | EMPIRICAL | Bounded rational root-orbit and norm audit | `research/experiments/EXP-0024-m25-rational-root-orbits.md` |
| DEF-026 | DEFINITION | Charged exceptional cyclotomic/cofactor extraction model | `research/proofs/BAR-020-exceptional-cyclotomic-extraction.md` |
| BAR-020 | PROVED | Exact compact exceptional cofactor and valuation theorem | `research/proofs/BAR-020-exceptional-cyclotomic-extraction.md` |
| REF-022 | REFUTED | Direct fixed-cyclotomic GCDs as an exhaustive explanation | `research/NEGATIVE_RESULTS.md` NR-023 |
| EMP-025 | EMPIRICAL | Bounded exceptional cofactor and prime-power audit | `research/experiments/EXP-0025-m26-exceptional-cyclotomic.md` |
| DEF-027 | DEFINITION | Charged exceptional-cofactor local profile and fixed joint schedule model | `research/proofs/BAR-021-exceptional-cofactor-schedule-barrier.md` |
| BAR-021 | PROVED | Exact overlap resultants and fixed finite schedule barrier | `research/proofs/BAR-021-exceptional-cofactor-schedule-barrier.md` |
| REF-023 | REFUTED | Fixed finite exceptional-cofactor schedule as universal | `research/NEGATIVE_RESULTS.md` NR-024 |
| EMP-026 | EMPIRICAL | Bounded local-root, overlap, valuation, and prefix audit | `research/experiments/EXP-0026-m27-exceptional-cofactor-schedule.md` |
| DEF-028 | DEFINITION | Length-indexed compact and materialized-lift schedule ledgers | `research/proofs/BAR-022-length-indexed-materialized-support.md` |
| BAR-022 | PROVED | Exact balanced-pair support and materialized-bit barrier | `research/proofs/BAR-022-length-indexed-materialized-support.md` |
| REF-024 | REFUTED | Compact modular cost as a bound on exact-lift bit length | `research/NEGATIVE_RESULTS.md` NR-025 |
| EMP-027 | EMPIRICAL | Bounded length-indexed support and compact-gap audit | `research/experiments/EXP-0027-m28-length-indexed-support.md` |
| DEF-029 | DEFINITION | Compact Phi4 cofactor prime-support signature | `research/proofs/BAR-023-compact-cofactor-prime-support.md` |
| BAR-023 | PROVED | Exact prime criterion, consecutive-support, and signature-cut barrier | `research/proofs/BAR-023-compact-cofactor-prime-support.md` |
| REF-025 | REFUTED | Exact magnitude or accumulated support as a universal single-candidate certificate | `research/NEGATIVE_RESULTS.md` NR-026 |
| EMP-028 | EMPIRICAL | Bounded compact cofactor prime-support audit | `research/experiments/EXP-0028-m29-compact-cofactor-prime-support.md` |
| DEF-030 | DEFINITION | Compact multi-candidate analytical support-signature model | `research/proofs/BAR-024-compact-support-signatures.md` |
| BAR-024 | PROVED | Exact injectivity criterion, candidate lower bounds, and collision minimum | `research/proofs/BAR-024-compact-support-signatures.md` |
| REF-026 | REFUTED | Union coverage and candidate count as sufficient for pair separation | `research/NEGATIVE_RESULTS.md` NR-027 |
| EMP-029 | EMPIRICAL | Bounded abstract-signature and canonical compact-prefix audit | `research/experiments/EXP-0029-m30-compact-support-signatures.md` |
| DEF-031 | DEFINITION | Diversified exceptional selector and overlap-normalized primitive coordinates | `research/proofs/THM-004-BAR-025-diversified-selector.md` |
| THM-004 | PROVED | Finite balanced-semiprime construction for input lengths 9 through 15 | `research/proofs/THM-004-BAR-025-diversified-selector.md` |
| BAR-025 | PROVED | Exact normalization equivalence and length-16 collision | `research/proofs/THM-004-BAR-025-diversified-selector.md` |
| REF-027 | REFUTED | The parameter-and-base box through m as universally injective | `research/NEGATIVE_RESULTS.md` NR-028 |
| EMP-030 | EMPIRICAL | Bounded diversified-selector and certificate audit | `research/experiments/EXP-0030-m31-diversified-compact-signatures.md` |
| DEF-032 | DEFINITION | Widened public exceptional-selector cap and branch-total exits | `research/proofs/THM-005-BAR-026-widened-selector-cap.md` |
| THM-005 | PROVED | Finite balanced-semiprime construction for input lengths 9 through 20 | `research/proofs/THM-005-BAR-026-widened-selector-cap.md` |
| BAR-026 | PROVED | Exact finite cap thresholds, monotonicity, and multiplicative endpoint | `research/proofs/THM-005-BAR-026-widened-selector-cap.md` |
| REF-028 | REFUTED | The additive cap m plus 10 as sufficient through length 20 | `research/NEGATIVE_RESULTS.md` NR-029 |
| EMP-031 | EMPIRICAL | Bounded widened-cap threshold and certificate audit | `research/experiments/EXP-0031-m32-widened-selector-cap.md` |
