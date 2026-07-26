# Research Decisions

## ADR-001 — Dependency-free M0 validation

- Date: 2026-07-25
- Status: accepted
- Context: the repository has no implementation baseline and Python package
  installation is unavailable in the current interpreter.
- Alternatives: add a JSON Schema package immediately; validate only by manual
  inspection; provide a small standard-library checker and tests.
- Decision: use Python 3.12 standard-library code for the M0 structural contract
  and negative-path tests. Keep the JSON Schema itself standards-oriented so
  later language implementations can use full validators.
- Consequences: M0 is reproducible offline with no dependency download. The
  checker intentionally implements only the repository's required contract, not
  the full JSON Schema specification.
- Rollback condition: replace or supplement the checker when M1 introduces an
  already-justified schema dependency and cross-language validation.

## ADR-002 — Conservative manuscript initialization

- Date: 2026-07-25
- Status: accepted
- Context: no novel theorem or experiment exists yet, and the sandboxed
  preflight could not see a TeX engine.
- Alternatives: postpone the paper; create an aspirational paper with unsupported
  claims; create a minimal claim-linked manuscript and record the compile blocker.
- Decision: initialize a conservative manuscript that states definitions, imported
  baseline results, the open POSF target, and limitations. Do not claim novelty.
- Consequences: source and bibliography integrity are checked structurally. The
  approved escalated environment later exposed MiKTeX, so the PDF also passed
  compilation, warning scanning, and visual inspection without changing the
  conservative claim policy.
- Rollback condition: revise the structure only when verified evidence supports a
  stronger contribution.

## ADR-003 — Primary-source evidence identifiers

- Date: 2026-07-25
- Status: accepted
- Context: claims need stable links to actually inspected sources.
- Alternatives: cite URLs directly from claims; use bibliography keys only; keep a
  separate source ledger with stable IDs.
- Decision: assign `SRC-NNN` identifiers in literature notes and map each imported
  claim to a source ID and BibTeX key.
- Consequences: claims can distinguish inspection evidence from bibliography
  formatting, and sources can be rechecked without changing claim IDs.
- Rollback condition: migrate identifiers only through an explicit mapping if a
  future reference manager becomes authoritative.

## ADR-004 — Three-layer M1 baseline scope

- Date: 2026-07-25
- Status: accepted
- Context: later counterexample searches need clear semantics, overflow-safe
  execution, and at least one independently implemented verifier.
- Alternatives: begin with external big-integer dependencies; use Python alone;
  use a small exact reference plus bounded authoritative and independent layers.
- Decision: Python supplies arbitrary-precision semantics; Rust is authoritative
  for documented `u64` inputs and uses `u128` modular products; C# `BigInteger`
  independently verifies selected canonical operations. All randomness-like rho
  choices are explicit deterministic inputs.
- Consequences: M1 is dependency-free and reproducible with installed toolchains.
  Rust stage-one exponent construction returns method failure if its `u64`
  exponent product overflows. Validation primality uses exact trial division and
  is not claimed polynomial in input length. The current batch-GCD routine is a
  per-item semantic baseline, not a product-tree optimization.
- Rollback condition: introduce arbitrary-precision Rust only when M2/M3 input
  ranges require it and the dependency, license, and differential plan are
  recorded.

## ADR-005 - Separate support-POSF and valuation-family domains

- Date: 2026-07-25
- Status: accepted
- Context: DEF-002 cannot hold on a prime power because its distinct-prime
  support is a singleton, while LEM-002 shows that partial prime-power
  valuations can still yield a nontrivial GCD.
- Alternatives: retain an impossible all-composite support-POSF target; redefine
  order support silently; preprocess perfect powers; introduce a separate exact
  valuation success condition.
- Decision: refute the original all-composite support-POSF target. Scope a
  repaired support-POSF to cofactors remaining after exact primality and
  perfect-power preprocessing, and track an all-input valuation-separating
  family as a second open target.
- Consequences: LEM-001 remains a general sufficient lemma, LEM-002 is the exact
  nonsquarefree criterion, and neither repaired open target is treated as an
  available constructor. Family semantics use the explicit Cartesian product
  \(G_m(N)\times\Delta_m(N)\) with canonical residue bases.
- Rollback condition: change this split only if a later definition preserves
  exact prime-power semantics and passes the same claim and proof review.

## ADR-006 - Randomize bases for the M3 restricted theorem

- Date: 2026-07-26
- Status: accepted
- Context: a deterministic M3 draft required its factor-aware promise to name a
  small base whose order already separates two unknown prime divisors. That
  condition was correct but scientifically close to restating LEM-001.
- Alternatives: retain the small-base order promise; assume only
  \(p-1\mid d\) and \(q-1\nmid d\) for a fixed base; sample a uniform residue
  for every bounded exponent.
- Decision: define a base-free hereditary divisibility-asymmetry promise and
  use fresh exact uniform residues. Preserve the fixed-base version only as a
  diagnostic and record its \(N=51\) proper-subgroup collision as NR-002.
- Consequences: THM-001 is a Las Vegas expected-polynomial restricted theorem.
  Its one-witness success probability is at least \(5/12\), membership remains
  promised rather than recognized, and no outside-promise termination claim is
  made. Exact rejection sampling and schedule-evaluation cost are charged.
- Rollback condition: replace the randomized step only if a deterministic,
  factorization-independent base construction survives the same subgroup and
  bit-complexity review.
