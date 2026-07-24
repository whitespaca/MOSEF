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
- Context: no novel theorem or experiment exists yet, and no TeX engine is
  installed in the execution environment.
- Alternatives: postpone the paper; create an aspirational paper with unsupported
  claims; create a minimal claim-linked manuscript and record the compile blocker.
- Decision: initialize a conservative manuscript that states definitions, imported
  baseline results, the open POSF target, and limitations. Do not claim novelty.
- Consequences: source and bibliography integrity can be checked now; PDF
  compilation remains a documented external gate.
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
