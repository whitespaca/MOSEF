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

## ADR-007 - Separate divisor coverage from order-signature injectivity

- Date: 2026-07-26
- Status: accepted
- Context: M4 reconstructed a recent structured difference-set conjecture
  whose premise covers each divisor, but a MOSEF exponent must distinguish
  order supports rather than merely hit them.
- Alternatives: treat an \(n\)-divisor set as an order separator; reject all
  difference-cover ideas because one cover collides; state the exact
  divisibility-signature condition and preserve the source algorithm's
  different collision-resolution mechanism.
- Decision: define \(\Sigma_\Delta(r)=\{d\in\Delta:r\mid d\}\). Treat
  nonempty signatures as divisor coverage and injective signatures as the
  exact universal distinct-order separator condition. Record
  \(S=\{3\},T=\{1\}\) as the minimal coverage counterexample and the interval
  difference family as a sufficient but exponential control construction.
- Consequences: BAR-001 blocks only the unsupported implication from coverage
  to support-POSF separation. It does not refute Umans--Wang, does not supply a
  general factoring lower bound, and does not exclude compact batch
  representations. M5 must state and measure each channel's actual signature
  rather than use coverage as a proxy.
- Rollback condition: revise the abstraction only if a stronger candidate
  evaluation mechanism is defined with exact collision semantics and survives
  the same proof and source-scope audit.

## ADR-008 - Separate conjugate correlation from arbitrary Lucas parameters

- Date: 2026-07-26
- Status: accepted
- Context: M5 sought a factorization-independent pairing between the
  multiplicative \(a^d-1\) channel and the Lucas \(V_d(P,1)-2\) channel. The
  natural map \(P=a+a^{-1}\) looked like a two-group construction but exact
  algebra and the Williams source audit showed that it remains in the split
  \(p-1\) branch.
- Alternatives: treat the outcomes as independent; discard Lucas parameters
  entirely; prove the exact correlation for the conjugate map while keeping
  independently selected nonsplit parameters outside its scope.
- Decision: define every discriminant and sequence-GCD branch explicitly,
  including three outcomes when the discriminant GCD is all of \(N\). Record
  the conjugate identity as BAR-002 and keep arbitrary \(P\) as a distinct
  channel that may complement a multiplicative miss.
- Consequences: adding the conjugately derived Lucas family cannot enlarge a
  multiplicative exponent family's success domain when exponent \(2\) is
  retained, and it can degrade prime-power splits. This is not a lower bound
  for independently sampled parameters or other algebraic groups. A full
  discriminant GCD is not assumed to determine the later sequence GCD.
- Rollback condition: revise the separation only if a proposed parameter map
  is proved not to satisfy the conjugate identity and its exact failure
  distribution survives source, proof, and bounded counterexample review.

## ADR-009 - Make publication consistency executable

- Date: 2026-07-26
- Status: accepted
- Context: M6 must synthesize one restricted theorem, two barriers, imported
  results, and four experiment records without silently changing a status,
  hypothesis, count, or reproduction anchor.
- Alternatives: preserve the incremental manuscript unchanged; summarize only
  the positive theorem; make every ledger claim explicit in one self-contained
  paper and enforce the mapping mechanically.
- Decision: center the first publishable manuscript on THM-001, BAR-001, and
  BAR-002; include full proofs and explicit limitations; maintain
  `research/PUBLICATION_CLAIMS.md`; and gate the paper with
  `scripts/check_publication.py`. The release gate requires every claim exactly
  once with its ledger status, every registered experiment hash, all five full
  proofs, and a real 40-hex M6 core commit.
- Consequences: the paper remains honest about the factor-dependent promise,
  the map-specific nature of BAR-002, and OPEN-002/OPEN-003. A bootstrap-only
  `--allow-placeholder` mode exists solely to create the core commit; the
  normal publication check rejects the placeholder. Exact PowerShell
  reproduction commands use a repository-scoped .NET application-data path.
- Rollback condition: replace the checker or matrix only with a stricter
  mechanism that preserves claim, proof, experiment-hash, and commit
  traceability.

## ADR-010 - Sample independent Lucas parameters on an explicit promise

- Date: 2026-07-26
- Status: accepted
- Context: BAR-002 shows that the conjugate map \(P=a+a^{-1}\) cannot create
  an independent nonsplit channel. M7 asks whether a factorization-independent
  fresh uniform \(P\bmod K\) admits an exact success analysis without treating
  finite observations as independence evidence.
- Alternatives: abandon Lucas parameters after the conjugate barrier; assume
  independent channel failure heuristically; count exact prime-field roots and
  state the remaining factor-dependent structure as a hereditary promise.
- Decision: use fresh exact uniform parameters, retain both the discriminant
  and sequence GCD branches, prove the exact Lucas root count, and turn
  \(p+1\mid d,\ q+1\nmid d\) into the restricted THM-002 Las Vegas theorem.
- Consequences: one witness trial succeeds with probability at least \(1/12\),
  and complete factorization has expected polynomial bit complexity on the
  hereditary promise class. Membership is not recognized, no density theorem
  is supplied, and neither the root-count formula nor the theorem is claimed
  as a literature novelty.
- Rollback condition: revise the theorem if a counterexample breaks the root
  count, exact exceptional-branch analysis, CRT event, recursive promise, or
  polynomial representation/evaluation bound.

## ADR-011 - Choose an exact density barrier over an unsupported recognizer

- Date: 2026-07-26
- Status: accepted
- Context: M8 asks whether the union of the M3 \(p-1\) and M7 \(p+1\)
  hereditary promise classes can be recognized or assigned a rigorous density
  guarantee. Direct evaluation of the relevant divisibility predicates needs
  the unknown prime factors, and no independent \(N\)-only observable was
  found or proved equivalent.
- Alternatives: present factor signatures as a recognizer; assert a
  random-integer density heuristic; define an explicit common-schedule
  finite-pair distribution and prove the exact signature and magnitude
  obstruction.
- Decision: use the combined prime signature only as an analytical object and
  select the density/barrier branch. BAR-003 gives a self-contained
  finite-distribution upper bound and a magnitude-conditioned zero-density
  corollary for one common M3/M7 schedule.
- Consequences: M8 supplies no recognizer, natural-density theorem, general
  schedule lower bound, or factoring result. It leaves schedules with
  polynomial-bit-length but sufficiently large exponent values to M9.
- Rollback condition: revise the boundary only if a factorization-independent
  observable is proved equivalent to the combined promise or a schedule
  outside BAR-003's magnitude/sparsity hypotheses receives a rigorous
  construction or obstruction.

## ADR-012 - Charge explicit exponent encodings and divisor structure

- Date: 2026-07-26
- Status: accepted
- Context: BAR-003's magnitude argument does not constrain a
  polynomial-bit-length exponent whose numerical value exceeds the target
  primes. M9 asks whether large explicit values alone can give a nonvanishing
  common-schedule combined-promise guarantee.
- Alternatives: infer coverage from exponent magnitude; search for one
  favorable highly composite schedule without an asymptotic guarantee; or
  charge binary representation length and bound every possible \(p\pm1\) hit
  through the exponent's divisor count.
- Decision: define the exact integer budget DEF-009 and prove BAR-004 for
  factorization-independent explicit lists whose members are individually
  evaluated. Treat the prime population as a declared finite distribution,
  not as an implicit prime-number-theorem claim.
- Consequences: polynomial list size and
  \(L(k)=o(k\log k)\) imply only a subexponential hit set and a vanishing
  promised-pair fraction on every stipulated exponentially large
  common-input-length population. This is not a recognizer, natural-density
  theorem, factoring lower bound, or result about compressed, adaptive, or
  implicit exponent families. Exponent magnitude alone is refuted by
  REF-005.
- Rollback condition: revise the barrier if a counterexample violates the
  exact divisor budget, or if a rigorously specified compressed evaluation
  model invalidates the explicit-list accounting while preserving polynomial
  construction and evaluation cost.

## ADR-013 - Charge multiplication straight-line expansion

- Date: 2026-07-26
- Status: accepted
- Context: BAR-004 deliberately leaves compressed or batched implicit exponent
  families outside its explicit-list model. M10 needs one exact representation
  and evaluation semantics before deciding whether syntax compression evades
  the divisor barrier.
- Alternatives: treat a short symbolic exponent as automatically cheap;
  attempt a lower bound for every algebraic representation; or isolate the
  multiplication-only same-base DAG used by repeated squaring and shared
  addition chains.
- Decision: adopt DEF-010. Charge every multiplication node, parent index, and
  output index, track the exact formal exponent, and require the
  factor-oblivious table constructor itself to run in polynomial time. Prove
  only the elementary node-growth consequence and its internal transfer to
  BAR-004.
- Consequences: syntactic compression alone cannot hide a
  superpolynomial-bit formal exponent at polynomial multiplication cost in
  this model. If the total node count is \(o(k\log k)\), BAR-004 still applies.
  The result says nothing at the \(\Theta(k\log k)\) boundary and is not a
  modulus-specific modular-exponentiation, generic-group, general algebraic,
  or factoring lower bound.
- Rollback condition: revise the model or theorem if an exact earlier-parent
  multiplication program violates \(e_i\le2^i\), or evaluate a separately
  specified richer representation under its own explicit construction and
  operation costs.

## ADR-014 - Separate boundary capacity, coefficient, and prime yield

- Date: 2026-07-26
- Status: accepted
- Context: BAR-005 leaves the exact \(\Theta(k\log k)\) node boundary open.
  A schedule at that scale can have either very sparse or exponentially rich
  divisor structure, so node count alone cannot answer the combined-promise
  question.
- Alternatives: treat reaching the boundary as sufficient; search only for a
  favorable finite exponent; import a sharp maximal-order theorem without
  needing its lower-order terms; or optimize BAR-004's elementary split,
  expose the leading coefficient, and audit one explicit divisor-rich family.
- Decision: adopt DEF-011 and BAR-006. Keep the prime population stipulated,
  transfer the exponent-bit coefficient to the hit-set exponent, use the
  first-primes primorial as the explicit boundary-capacity witness, and keep
  actual \(d\pm1\) prime yield as a separate empirical/open quantity.
- Consequences: schedules below population coefficient \(\alpha\) still have
  vanishing promise fraction, and repeated squaring refutes boundary node
  count as a sufficient condition. Primorials establish exponential divisor
  capacity at \(\Theta(k\log k)\) cost but not a population guarantee.
- Rollback condition: revise the exact integer budget if a divisor-count
  counterexample is found; revise the primorial accounting if its constructor
  or binary evaluation exceeds the charged bounds; strengthen the outcome
  only if a proved asymptotic prime-yield lower bound is supplied.
## ADR-015 - Separate total divisor capacity from factor-scale capacity

- Date: 2026-07-27.
- Decision: for boundary schedules, count only divisors capable of equaling
  \(q-1\) or \(q+1\) at the stipulated target-factor scale before asking
  whether those candidates are prime.
- Rationale: M11's total divisor count is exponentially large but includes
  overwhelmingly many divisors too large to hit an \(O(k)\)-bit factor.
  DEF-012 exposes this scale mismatch, and BAR-007 resolves the first-primes
  primorial family without importing a shifted-prime distribution theorem.
- Consequence: prime-yield literature remains contextual; M13 must leave the
  nested first-primes primorial model or identify a genuinely different
  factor-scale divisor mechanism.

## ADR-016 - Use prime-occurrence splitting instead of support-specific arguments

- Date: 2026-07-27.
- Decision: replace M12's square-free support count by a threshold split that
  counts small-prime exponent choices and large-prime labeled occurrences
  separately.
- Rationale: this single exact budget handles prime powers, mixed
  multiplicities, arbitrary skipped primes, and square-free primorials without
  assuming a support shape. At the \(O(k\log k)\) boundary it remains
  subexponential at \(O(k)\)-bit factor scale.
- Consequence: BAR-008 subsumes the M12 asymptotic conclusion inside the
  broader common explicit-schedule model. M14 must leave at least one of the
  explicit-list, \(O(k\log k)\)-length, fixed target-scale, or existing
  \(p\pm1\)-channel hypotheses.

## ADR-017 - Charge inversion and normalize signed formal exponents

- Date: 2026-07-27.
- Decision: extend DEF-010 only to explicit same-base product/ratio nodes,
  charge every extended-GCD inversion and table/output entry, and represent
  the resulting candidate family by its distinct positive nonzero absolute
  formal exponents.
- Rationale: this is the smallest auditable representation change that tests
  cancellation and negative powers without hiding an exponential batch.
  Unit prechecks make inversion semantics total; negative exponents multiply
  the positive residue difference by a unit and zero gives a full collision.
- Consequence: BAR-009 transfers every \(O(k\log k)\)-node DEF-014 schedule
  to BAR-008. Direct proper-factor exits from the base precheck stay separate
  from the exponent-mediated hit-set theorem. The next milestone must change
  a stronger modeling axis, such as explicitly costed implicit batch
  evaluation, rather than merely add same-base inversion.
