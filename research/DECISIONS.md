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

## ADR-018 - Separate standard leaf materialization from general circuits

- Date: 2026-07-27.
- Decision: define the first implicit-batch milestone as a standard binary
  product tree that enumerates, evaluates, stores, and charges every selected
  residue leaf, while leaving specialized circuits without leaf
  materialization outside the theorem.
- Rationale: selector syntax can be compact while its selected output family
  is exponential. The smallest auditable model must say whether those leaves
  exist as charged objects before using the familiar product-tree count.
  This yields exact aggregate valuation and extraction semantics without
  pretending to prove a general arithmetic-circuit lower bound.
- Consequence: BAR-010 proves that a compact selector does not hide the
  linear leaf cost in DEF-015, and that a root GCD can mask but not create a
  leaf success. Its BAR-008 transfer separately requires a common
  factorization-independent leaf list and \(O(k\log k)\)-bit exponents.
  The next milestone may study a genuinely non-materializing circuit only
  after defining its formal output, cost, and extraction semantics.

## ADR-019 - Distinguish DAG sharing from distinct atom synthesis

- Date: 2026-07-27.
- Decision: define M16's smallest non-materializing model as explicit
  same-base atoms followed by a multiplication DAG whose earlier subproducts
  may be reused without unfolding, and charge atom construction, gates,
  outputs, GCDs, and optional formal multiplicity output separately.
- Rationale: DAG sharing genuinely represents exponentially many repeated
  formal occurrences at polynomial gate cost, so it leaves DEF-015's
  materialized-tree model. At the same time, it has an exact elementary
  multiplicity semantics that permits falsification without assuming a
  lower bound for arbitrary arithmetic circuits.
- Consequence: BAR-011 can prove that sharing exposes no distinct exponent
  beyond the explicit atom table and no proper product-node factor absent
  from those atoms. Addition, subtraction, division, composition, closed-form
  atom synthesis, modulus-specific identities, and adaptive branches remain
  open modeling axes rather than being silently ruled out.

## ADR-020 - Give exact division a total branch and keep the quotient path explicit

- Date: 2026-07-27.
- Decision: study the first richer M17 circuit through the dyadic identity
  \((X^{2^t}-1)/(X-1)=\prod_{j<t}(X^{2^j}+1)\), classify every denominator
  GCD as unit, proper factor, or full collision, and retain the
  division-free factor product in all three branches.
- Rationale: this circuit combines repeated composition, subtraction,
  addition, multiplication, and exact formal division while remaining
  completely auditable. It distinguishes an exponentially large formal
  monomial list from separately extractable GCD tests and prevents failed
  inversion from being silently discarded.
- Consequence: BAR-012 applies only to this dyadic telescope. Its compact
  evaluation has \(t+1\) explicit extraction components, while an expanded
  coefficient output costs \(2^t\). Arbitrary rational circuits,
  cancellation-obscured exact divisions, general composition, adaptive
  behavior, other groups, and general arithmetic-circuit lower bounds remain
  outside the theorem and must be modeled separately.

## ADR-021 - Reduce one arbitrary geometric sum by denominator status

- Date: 2026-07-27.
- Decision: generalize the dyadic telescope to the exact left-to-right binary
  pair grammar for \((X^M,S_M(X))\), and retain the division-free sum residue
  in all denominator branches.
- Rationale: the even and odd identities evaluate an exponentially long
  all-one coefficient vector in \(O(\log M)\) modular operations, so M18 must
  distinguish compact evaluation from extraction power. Total denominator
  semantics exposes the exact reduction: unit denominators preserve the
  endpoint GCD, proper denominators already factor \(N\), and full
  denominators reduce the sum GCD to the public \(\gcd(M,N)\).
- Input accounting: charge the encoded base length \(b\), base reduction and
  GCD precheck, exponent length \(\ell\), circuit operations, requested
  outputs, GCDs, and extraction. The post-reduction residue circuit is
  \(O(\ell\operatorname{poly}(k))\), while total work is polynomial in
  \(b+k+\ell\).
- Consequence: BAR-013 closes one arbitrary-exponent geometric sum, not
  cancellation-obscured multi-denominator programs or general rational,
  compositional, or arithmetic circuits. In the proper-denominator branch it
  preserves success existence, not the exact divisor value.

## ADR-022 - Audit a nested quotient through two independent total denominators

- Date: 2026-07-27.
- Decision: model M19 with the exact certificate
  \(S_{AB}(X)=S_A(X)S_B(X^A)\), retain \(Q=S_B(g^A)\) independently of
  division, and classify both the intermediate rational denominator
  \(L=S_A(g)\) and the composed denominator \(C=g^A-1\) as unit, proper, or
  full.
- Rationale: cancellation by \(S_A(g)\) is the smallest concrete extension
  not covered by BAR-013. Keeping the direct \(S_{AB}\), rational quotient,
  and composed endpoint paths separate prevents a failed inversion from
  being discarded and makes every extraction comparison explicit.
- Output accounting: the compact certificate uses the encoded pair
  \((A,B)\). The quotient has degree \(A(B-1)\), \(B\) nonzero monomials, and
  \(A(B-1)+1\) dense positions. Dense and sparse expanded outputs are charged
  by these exact sizes.
- Consequence: BAR-014 closes this two-stage identity only. It does not prove
  a lower bound for arbitrary rational straight-line programs, iterated
  quotient chains, unrelated denominators, adaptive computation, other
  groups, or general arithmetic circuits. M20 may study an explicitly
  charged iterated chain only after defining all intermediate exits and
  certificate/output costs.

## ADR-023 - Iterate certificates while retaining every stage exit

- Date: 2026-07-27.
- Decision: model M20 as a nonempty public factor list with prefix products
  \(M_i=\prod_{j\le i}A_j\), keep every quotient
  \(Q_i=S_{A_i}(g^{M_{i-1}})\) explicit, and classify both its rational prefix
  denominator and composed denominator before forming the final product.
- Rationale: finite iteration is the nearest extension of BAR-014, but
  telescoping can mask an earlier proper stage success in a later full
  collision. Retaining all stage outputs makes the extraction semantics
  total and permits a zero-safe implication from a proper aggregate GCD to a
  proper explicit stage GCD.
- Cost accounting: charge the public factor encodings, every prefix product,
  three binary geometric evaluators per stage, all requested GCDs and
  outputs, the compact product certificate, and any dense or sparse formal
  expansion. A quotient has \(A_i\) nonzero monomials and
  \(M_i-M_{i-1}+1\) dense positions; an expanded prefix has \(M_i\) entries.
- Consequence: BAR-015 closes product-only aggregation of this exact public
  chain. Cross-stage addition or subtraction, arbitrary subset interfaces,
  unrelated denominators, adaptive behavior, other groups, and general
  arithmetic-circuit lower bounds remain open; M21 isolates the smallest
  factorization-independent linear-combination extension.

## ADR-024 - Treat signed aggregation as a new extraction mechanism

- Date: 2026-07-27.
- Decision: extend DEF-020 by one aligned public signed coefficient per
  explicit quotient stage, retain every component output and GCD, and expose
  exactly one charged linear aggregate.
- Rationale: multiplication preserves the unit/full component implication,
  but addition does not. The exact \(N=9\) witness creates a proper aggregate
  from unit components, so folding signed aggregation into BAR-015 would be
  mathematically false.
- Cost accounting: charge coefficient encodings and reductions, \(r\) scalar
  multiplications, \(r-1\) additions, all coefficient and weighted-stage
  GCDs, aggregate extraction, and any requested sparse or dense polynomial
  output. The uncollected polynomial has \(\sum_iA_i\) term records and
  degree at most \(\max_i(M_i-M_{i-1})\).
- Consequence: M21 records a positive separation in extraction power, not a
  factoring algorithm. M22 must characterize when these cancellations occur
  and whether a factorization-independent family yields a restricted theorem
  or only sparse isolated witnesses.

## ADR-025 - Factor the symmetric difference before proposing schedules

- Date: 2026-07-27.
- Decision: isolate the repeated-factor, coefficients \((-1,1)\) family and
  retain both the endpoint \(g^{A-1}-1\) and the exact cofactor \(H_A(g)\)
  before studying larger signed schedules.
- Rationale: the M21 witness is explained by the endpoint, but a separate
  unit-endpoint cofactor path exists. Treating every signed success as an
  undifferentiated aggregate would hide this algebraic split and encourage
  unsupported schedule claims.
- Cost accounting: compute the two geometric sums and endpoint in
  \(O(\log A)\) modular operations, and compute the cofactor by a fixed
  \(3\times3\) matrix recurrence in \(O(\log A)\) modular operations. Charge
  every GCD, the unit-branch inversion, and requested sparse or dense output.
- Consequence: BAR-017 classifies the symmetric family but does not close
  unequal factors or arbitrary coefficients. M23 should test whether those
  next cases admit any comparably compact factorization.

## ADR-026 - Separate total prefix reduction from residual unequal extraction

- Date: 2026-07-27.
- Decision: for unequal depth-two factors, retain the general signed form's
  total first-prefix trichotomy and analyze the normalized difference through
  the exact common factor \(XS_{\gcd(A-1,B-1)}\).
- Rationale: the general coefficient form always reduces to a proper prefix,
  a public full-prefix value, or one unit-prefix rational residue. The
  normalized difference has a provable natural factor, but the \(N=25\)
  witness shows that its residual cofactor can still extract a factor.
  Conflating these statements would falsely claim that the natural factor is
  complete.
- Cost accounting: charge two binary geometric-sum evaluators, signed
  coefficient reductions, every GCD, any unit inversion, extraction, and
  requested expanded coefficients. Compact residue evaluation is logarithmic
  in the public factors; formal cofactor output is charged by its actual
  degree and coefficient count.
- Consequence: BAR-018 closes the total first-prefix semantics and exact
  endpoint/common-step classification but leaves the surviving unit-prefix
  rational residue open. M24 should classify that residue or produce a
  sharper restricted obstruction.

## ADR-027 - Isolate public stage overlap before classifying exceptional roots

- Date: 2026-07-27.
- Decision: normalize coefficient content first, retain both exact stage
  resultants as compact descriptors, and separate their public overlap bounds
  from the standalone primitive numerator. Treat cyclotomic order searches
  as explicitly bounded exact divisions.
- Rationale: the resultants prove that aggregate overlap with either charged
  stage is controlled by a public coefficient--multiplier GCD, but the
  \(\Phi_4\) witness produces a proper aggregate GCD after every such bound
  is a unit. Folding that witness into a stage explanation would erase the
  mechanism M24 was intended to isolate.
- Cost accounting: compact base--exponent resultant descriptors are
  polynomial-size, while expanded resultants can have bit length linear in
  the numerical factor \(A\) or \(B\). Charge expansion, coefficient lists,
  and cyclotomic order enumeration by actual output size or explicit bound;
  charge all content, stage, aggregate, and rational-residue GCDs.
- Consequence: BAR-019 closes coefficient content and stage overlap and gives
  an exact root-of-unity equation, while REF-020 prevents a false
  boundary-only classification. M25 should study the rational
  root-of-unity ratio and its Galois-orbit restrictions before proposing any
  schedule-level theorem.

## ADR-028 - Normalize the Galois orbit before enumerating orders

- Date: 2026-07-27.
- Decision: classify a requested primitive order through conjugation,
  normalize \(A\) by its inverse modulo \(n\), and apply the norm of
  \((1-\zeta^k)/(1-\zeta)\). Retain the complete order set as the compact
  common-step divisor descriptor plus fixed exceptional orders four and six.
- Rationale: the necessary phase congruence has many irrational solutions;
  \((A,B,n)=(2,4,5)\) is the first. Exact norms turn the rational value into
  a nonnegative integer and eliminate every apparent wider family without
  extrapolating from finite enumeration.
- Cost accounting: requested-order recognition uses only GCDs and modular
  reductions in the binary inputs. Listing divisors of
  \(\gcd(A-1,B-1)\), factoring that integer, or expanding cyclotomic and
  numerator polynomials is charged separately by actual work and output.
- Consequence: THM-003 completely classifies rational orders in the M25
  model. M26 should test whether the two fixed exceptional polynomials add
  any algorithmic content beyond direct small-cyclotomic GCDs.

## ADR-029 - Evaluate exceptional cofactors independently on every branch

- Date: 2026-07-27.
- Decision: retain the exact quotients \(C_4=F_4/\Phi_4\) and
  \(C_6=F_6/\Phi_6\) as first-class extraction components. Evaluate them by
  fixed periodic and binary geometric-sum formulas, not only by multiplying
  the aggregate by a cyclotomic inverse.
- Rationale: inverse recovery is valid only when \(\Phi_i(g)\) is a unit.
  A full direct cyclotomic collision makes the aggregate full but does not
  determine or suppress the cofactor GCD. Moreover, the clean residual
  witnesses show that unit direct cyclotomic GCDs can coexist with proper
  cofactor GCDs after all earlier stage and public-bound checks.
- Cost accounting: compact evaluation uses a constant number of exponentiations
  and binary geometric sums whose counts have bit length
  \(O(\log A+\log B)\). A dense quotient request still emits
  \(A(B-1)-1\) coefficients and is charged by that output size. Every base,
  stage, public-bound, cyclotomic, cofactor, and extraction GCD remains
  explicit.
- Consequence: BAR-020 gives a total factorization-independent evaluator and
  REF-022 blocks the direct-cyclotomic-only interpretation. M27 may study a
  public schedule only after isolating local cofactor roots and overlaps; M26
  provides no coverage or density theorem.

## ADR-030 - Close the fixed finite schedule model before length-indexed claims

- Date: 2026-07-28.
- Decision: compute compact stage/cofactor and cyclotomic/cofactor resultants
  before treating any cofactor root as a new schedule event. Define the first
  schedule model as one fixed finite set of public family, parameter, and base
  tuples chosen before the input.
- Rationale: exact resultants remove every hidden overlap with already charged
  exits. In the resulting model, a finite product of all nonzero charged
  integer values has only finitely many prime divisors, so infinitely many
  square-free semiprimes avoid the whole schedule. This is a rigorous barrier
  and requires no empirical density extrapolation.
- Cost accounting: the direct/cofactor resultants have
  \(O(\log A+\log B)\)-bit closed forms. Stage resultants remain compact
  base/exponent descriptors. Explicit root enumeration costs \(p-1\) trials
  and is not called polynomial in \(\log p\).
- Consequence: BAR-021 refutes a universal fixed finite joint schedule while
  preserving the local cofactor extraction mechanism. M28 may study schedules
  indexed by input length only after stating their quantifier order and total
  construction/evaluation budget; BAR-021 does not transfer automatically.

## ADR-031 - Separate compact modular cost from exact-lift support cost

- Date: 2026-07-28.
- Decision: define a length-indexed schedule before the particular input
  \(N\), but maintain two ledgers. The compact ledger charges binary
  parameters and modular evaluation. The materialized ledger additionally
  charges the actual bit length of every nonzero exact integer or an
  equivalent explicit support certificate.
- Rationale: a same-length finite-support diagonalization must control how
  many balanced primes divide the charged values. BAR-022 provides that
  control exactly under materialization. The valid family
  \(A=3,B=2^m+3,g=2\) shows that compact evaluation alone can represent an
  exponentially long cofactor, so using its exact bit length as compact
  running time would be false.
- Cost accounting: for a balanced prime population, \(h\) hit primes each
  contribute at least \(b=\lfloor(m-1)/2\rfloor\) bits to the product of
  materialized values, giving \(bh\le W\). Compact geometric-sum evaluation
  is instead charged by the binary count lengths and modular operands.
  Touched pairs are only an upper bound because one value can collide on both
  factors.
- Consequence: M28 proves a scoped materialized-support barrier and refutes
  the naive compact-to-exact cost transfer. M29 should examine the distinct
  balanced-prime support of compact exceptional cofactors directly; neither
  large magnitude nor finite-box root counts may be treated as support
  density.

## ADR-032 - Treat one compact cofactor as one support-signature bit

- Date: 2026-07-28.
- Decision: analyze the M29 family through the exact local predicate
  \(p\mid C_m\), but evaluate it publicly only as one compact residue modulo
  \(N\). Count square-free pair outcomes as the cut induced by that predicate,
  including both unit and full-collision failures.
- Rationale: exact magnitude says nothing about the distribution of distinct
  prime divisors, and broad support alone can worsen extraction by placing
  both factors on the hit side. The cut model captures success exactly and
  requires neither factorization nor materialization in the public
  evaluator.
- Cost accounting: the public \(B_m=2^m+3\) and the local exponent
  \(E_m=3\cdot2^m+5\) have \(O(m)\) bits. Compact evaluation uses the M26
  binary formulas. Listing the support, factoring the exact cofactor, or
  supplying local primes remains outside and is charged if requested.
- Consequence: BAR-023 closes the single-tuple family and refutes a
  magnitude-as-coverage interpretation. M30 should study multi-candidate
  signature vectors, where universal pair separation requires distinct
  signatures rather than merely a large union of supports.

## ADR-033 - Maintain synchronized English and Korean manuscripts

- Date: 2026-07-28.
- Decision: retain `paper/main.tex` as the full English publication manuscript
  and add `paper/main-ko.tex` as a Korean companion manuscript. Every
  milestone must update both where its result affects the paper. Automated
  publication checks must verify claim-ID/status parity, the current
  experiment hash, required limitations, and reproduction commands across
  both manuscripts.
- Rationale: the repository owner requested Korean papers in addition to the
  English publication. A separately compiled companion preserves readable
  Korean prose and typography while retaining stable mathematical claim IDs
  and evidence anchors.
- Build and typography: both manuscripts use XeLaTeX. The Korean companion
  uses `fontspec`, `xeCJK`, and the installed Malgun Gothic family. Both final
  PDFs are rendered and visually inspected; missing Korean glyphs or broken
  line layout are failures.
- Consequence: the stable outputs are `output/pdf/mosef-paper.pdf` and
  `output/pdf/mosef-paper-ko.pdf`. The Korean companion is self-contained for
  definitions, verified results, limitations, M29's complete proof, and
  reproduction, while the English manuscript remains the exhaustive proof
  archive for earlier milestones.

## ADR-034 - Require injectivity, not union coverage, from compact candidates

- Date: 2026-07-28.
- Decision: represent every public compact cofactor by one analytical support
  bit per population prime and evaluate a candidate list through the complete
  binary signature. Universal square-free pair extraction is accepted only
  when those signatures are injective.
- Rationale: a covered prime may share every support coordinate with another
  covered prime. Candidate count and union coverage alone therefore cannot
  rule out full/unit collisions. BAR-024 gives exact collision accounting and
  the information lower bound before any parameter schedule is proposed.
- Cost and recognition: the signature is a semantic proof object. The public
  algorithm evaluates compact residues and GCDs but receives neither the
  unknown factors nor support sets. Abstract bit-label constructions
  materialize factor-aware prime products and do not establish a compact
  exceptional schedule.
- Consequence: the canonical polynomial prefix \(C_2,\ldots,C_m\) may be
  audited fairly without overstating its finite failure. M31 may diversify
  families, bases, and parameters only through an explicit
  factorization-independent selector whose full compact cost is charged.

## ADR-035 - Normalize support columns without deleting charged exits

- Date: 2026-07-28.
- Decision: retain every base, stage, public bound, direct cyclotomic,
  cyclotomic/cofactor resultant, and independent cofactor GCD in the public
  algorithm. For analytical injectivity only, delete constant population
  columns, merge exact duplicate columns, and omit aggregate or overlap
  columns that are Boolean functions of the primitive columns.
- Rationale: suppressing a cofactor merely because a direct exit hits the same
  prime can destroy a legitimate later separation when both factors share the
  direct hit. Exact column equivalence preserves all pair outcomes, while
  marginal partition refinement counts only cofactor separations not already
  supplied by direct coordinates.
- Cost accounting: the selector contains at most \(2(m-1)^3\) descriptors.
  Every descriptor, compact evaluation, public precheck, GCD, output, and
  extraction remains charged. Population support enumeration and
  normalization are proof/audit operations, not a public recognizer.
- Consequence: THM-004 gives a complete finite construction for lengths 9
  through 15, while BAR-025 records the exact length-16 collision for the same
  selector. M32 must vary the public range or formula explicitly and charge
  the resulting polynomial degree before interpreting any repaired finite
  signature.

## ADR-036 - Separate the public cap from input length and certify thresholds

- Date: 2026-07-28.
- Decision: parameterize the exceptional selector by a public cap \(L(m)\)
  independent of the unknown factors. Search complete integer caps, prove
  monotonicity using raw selector inclusion, and certify each first injective
  cap with both a predecessor collision and an injective coordinate sublist.
- Rationale: normalized column counts can rise, fall, or merge as the cap
  changes, so normalized-count monotonicity is not a valid proof. Raw
  descriptors are nested, and DEF-031 normalization preserves pair separation
  at each fixed cap. A checked predecessor collision plus this inclusion
  proves threshold minimality without trusting an optimizer.
- Cost and branch semantics: at most \(2(L-1)^3\) descriptors are constructed,
  and all base, stage, bound, cyclotomic, resultant, cofactor, aggregate, GCD,
  output, and extraction costs remain charged. A nonunit base terminates at
  its public base GCD and does not enter the unit-only continuation.
- Consequence: \(m+11\) is the smallest common integer-offset schedule through
  \(m=20\), while multiplicative coefficients have infimum \(3/2\) but no
  smallest admissible endpoint. M33 must test whether a fixed public linear
  cap continues to work beyond the finite M32 range before any asymptotic
  interpretation.

## ADR-037 - Track finite linear envelopes without extrapolating a rate

- Date: 2026-07-28.
- Decision: record the least certified cap \(L_m^\star\), the common integer
  offset \(t_M^\star\), and the strict multiplier infimum \(c_M^\star\) only
  over an explicitly completed finite range.
- Rationale: the M32 formulas fail immediately at \(m=21\). Calling their
  earlier success a stable linear law would convert finite evidence into an
  asymptotic claim. A predecessor collision and repaired construction instead
  determine the next finite envelope exactly.
- Consequence: through length 21 the envelopes move from 11 to 12 and from
  \(3/2\) to \(32/21\). M34 must test the repaired formulas at \(m=22\)
  before inferring any further pattern.

## ADR-038 - Freeze the complete cap transition when the repair gap widens

- Date: 2026-07-28.
- Decision: for M34, register every complete cap profile from the failed
  public cap 34 through the first injective cap 39 rather than retaining only
  the two endpoints.
- Rationale: the collision count falls through
  \(37,15,10,6,1,0\). Preserving that ladder distinguishes a genuine exact
  threshold from an optimizer artifact and provides monotonicity checks at
  every widening step.
- Consequence: the finite envelopes through length 22 are now 17 and
  \(19/11\). They remain finite maxima, not evidence of an asymptotic growth
  law. M35 must test the repaired formulas at \(m=23\).

## ADR-039 - Treat the exact coefficient 2 as a strict failed endpoint

- Date: 2026-07-28.
- Decision: state the M35 multiplicative envelope as \(c>2\), not
  \(c\ge2\), and freeze the cap-46 predecessor collision proving the strict
  boundary.
- Rationale: \(\lceil2\cdot23\rceil=46\), where \(2411\) and \(2777\)
  still collide. The first injective cap is 47.
- Consequence: \(201/100\) is a concrete succeeding witness through length
  23, while the finite result remains silent about every later length. M36
  must test the now-distinct caps 48 and 49 at \(m=24\).

## ADR-040 - Audit the distinct caps separately and retain a strict endpoint

- Date: 2026-07-28.
- Decision: preserve separate cap-48 and cap-49 failure certificates before
  combining them into the new finite envelope, and state the M36
  multiplicative boundary as \(c>25/12\), not \(c\ge25/12\).
- Rationale: the two M35 formulas no longer coincide at \(m=24\). Cap 48 has
  a five-prime collision bucket, while caps 49 and 50 have a four-prime
  bucket. Since \(\lceil(25/12)\cdot24\rceil=50\), the endpoint fails and
  the first injective cap is 51.
- Consequence: \(209/100\) is a concrete succeeding witness through length
  24, while the finite result remains silent about every later length. M37
  must separately test additive cap 52 and multiplicative cap 53 at \(m=25\).

## ADR-041 - Track later collisions inside the first complete failed bucket

- Date: 2026-07-28.
- Decision: freeze complete population profiles at the two public caps 52
  and 53 and at the first injective cap 65, while auditing caps 54 through 64
  on the sole complete cap-52 collision bucket.
- Rationale: raw selector inclusion prevents any pair already separated at
  cap 52 from merging at a later cap. Therefore every later collision lies
  inside the registered nine-prime bucket, and an exact bucket-restricted
  audit is a complete transition certificate rather than sampling. This
  avoids repeatedly materializing eleven redundant 196-prime profiles.
- Consequence: the cap-64 pair \(\{5011,5179\}\) proves the lower endpoint,
  while the complete cap-65 profile proves the upper endpoint. The finite
  envelopes through length 25 become \(m+40\) and \(c>64/25\); no
  asymptotic rate is inferred. M38 must test the repaired caps 66 and 67 at
  \(m=26\).

## ADR-042 - Certify a repair incrementally from the last complete profile

- Date: 2026-07-28.
- Decision: for M38, freeze complete population profiles at the two public
  caps 66 and 67, then certify cap 71 by appending the two explicit new
  binary columns that separate the sole cap-67 collision triple.
- Rationale: raw selector inclusion guarantees that every pair separated at
  cap 67 remains separated. The complete cap-67 profile leaves only
  \(\{7187,7229,7649\}\); the two registered cap-71 cofactor patterns assign
  it signatures \(0,2,1\). Thus the 561 old normalized columns plus two new
  raw columns are a complete 268-prime construction certificate without
  materializing a redundant full cap-71 normalized profile.
- Consequence: two new coordinates are minimal for the final triple, although
  the full 563-coordinate certificate is not claimed minimum. The finite
  envelopes through length 26 become \(m+45\) and \(c>35/13\); no
  asymptotic rate is inferred. M39 must test the repaired caps 72 and 73 at
  \(m=27\).

## ADR-043 - Use one complete profile and an incremental raw transition

- Date: 2026-07-29.
- Decision: for M39, materialize the complete cap-72 population profile
  once, then evaluate each descriptor added through cap 87 exactly once on
  the sole six-prime collision bucket.
- Rationale: raw selector inclusion guarantees that cap widening cannot
  merge a pair already separated at cap 72. The incremental transition is
  therefore complete for every later collision while avoiding redundant
  full-profile normalization at fifteen larger caps.
- Consequence: 235 nonconstant new raw coordinates collapse to five unit
  patterns on the bucket. Appending one representative of each pattern to
  the 625 cap-72 normalized columns gives a 630-coordinate construction
  certificate. All five new coordinates are minimum for this incremental
  repair, although the full certificate is not claimed minimum. The finite
  envelopes through length 27 become \(m+60\) and \(c>86/27\); no
  asymptotic rate is inferred. M40 must test caps 88 and 90 at \(m=28\).

## ADR-044 - Stream primitive masks without caching audit objects

- Date: 2026-07-29.
- Decision: retain the public cached `primitive_exit_mask` interface, but
  construct complete selector profiles through an allocation-free evaluator
  that returns the same eight support bits and stores only the resulting
  population masks.
- Rationale: a cap-88, length-28 profile contains 58,464 descriptors and
  507 balanced primes, hence 29,641,248 local evaluations. Retaining one full
  audit object or cache entry per pair is not needed to normalize support
  columns. The direct evaluator computes both geometric sums, the public
  bounds, the exceptional resultant, and the cyclotomic bit exactly. It uses
  the integral identity \(F=\Phi_k C\) when the cyclotomic residue is a unit
  and evaluates the compact cofactor explicitly when that residue vanishes.
- Consequence: column ordering and profile semantics remain unchanged while
  peak retained state is proportional to the raw coordinate masks rather
  than the descriptor-population product. Exhaustive selector comparisons
  against the original full audit-object path, all historical M33--M39
  collision regressions, and the frozen M39 audit pass. This is an
  implementation optimization, not a new complexity or factoring claim.

## ADR-045 - Audit several caps with lossless raw-signature prefixes

- Date: 2026-07-29.
- Decision: for M41, order descriptors by their exact first public cap and
  store the eight primitive charged exits for each descriptor as one byte per
  population prime. Compare complete byte prefixes at caps 102, 103, 105,
  and 108, then independently materialize the normalized cap-103 profile.
- Rationale: equality of packed bytes is exactly equality of all eight raw
  coordinates; no probabilistic hash is used. One pass through the cap-108
  selector therefore compares both pre-registered schedules and the adjacent
  threshold profiles without four redundant full normalizations.
- Consequence: the audit proves cap 102 has one collision and caps 103, 105,
  and 108 are injective. The separate normalized cap-103 profile and
  independently reconstructed 1,528-coordinate certificate provide a second
  representation. This is a finite certificate strategy, not an asymptotic
  algorithm or a public promise recognizer.

## ADR-046 - Combine public raw prefixes with complete bucket transitions

- Date: 2026-07-29.
- Decision: for M42, compute lossless full-population raw prefixes only at
  the two pre-registered public caps 106 and 112. After cap 112, use raw
  selector inclusion to evaluate each newly admitted descriptor only on the
  complete nine-prime collision bucket through cap 123. Independently
  materialize and normalize the complete cap-123 profile.
- Rationale: the public-cap profiles must independently falsify both inherited
  formulas on all 927 primes. Once a complete cap-112 equivalence class is
  known, widening cannot merge any already separated pair, so the exact
  bucket transition is complete without eleven redundant full-population
  profiles.
- Consequence: the audit proves both public caps fail, tracks the exact
  \(36,36,36,21,21,21,15,10,10,3,3,0\) collision ladder, and constructs a
  2,403-coordinate cap-123 certificate from 2,401 cap-122 representatives
  plus two minimum repair coordinates. The finite envelopes become \(m+93\)
  and \(c>61/15\). This is a finite certificate strategy, not an asymptotic
  algorithm or a public promise recognizer.

## ADR-047 - Reuse lossless prefixes and normalize only the repair cap

- Date: 2026-07-29.
- Decision: for M43, compute lossless full-population raw prefixes only at
  the two pre-registered public caps 124 and 127. After cap 127, use raw
  selector inclusion to evaluate each newly admitted descriptor only on the
  complete 12-prime collision bucket through cap 144. Independently
  materialize and normalize the complete cap-144 profile.
- Rationale: the public-cap profiles must independently falsify both inherited
  formulas on all 1,280 primes. Once a complete cap-127 equivalence class is
  known, widening cannot merge any already separated pair, so the exact
  bucket transition is complete without seventeen redundant full-population
  profiles.
- Consequence: the audit proves both public caps fail, tracks the exact
  \(66,66,66,66,21,21,21,21,10,10,6,6,1,1,1,1,1,0\) collision ladder,
  and constructs a 3,362-coordinate cap-144 certificate from 3,361 cap-143
  representatives plus one minimum repair coordinate. The finite envelopes
  become \(m+113\) and \(c>143/31\). This is a finite certificate strategy,
  not an asymptotic algorithm or a public promise recognizer.

## ADR-048 - Replace full raw prefixes with exact partition refinement

- Date: 2026-07-29.
- Decision: for M44, retain only the non-singleton raw-signature
  equivalence classes after each descriptor and record every primitive bit
  that changes a class. Use those recorded coordinates as the positive
  construction certificate.
- Rationale: the length-32 cap-148 selector has 284,004 descriptors and
  1,750 population primes. Materializing every byte prefix would retain
  roughly half a billion entries even though almost all primes become
  singletons early. Appending coordinates can refine an equality partition
  but cannot merge distinct prefixes, so a discarded singleton can never
  re-enter a collision. Recording every varying primitive bit reproduces
  each exact descriptor-mask split and converts the same pass into an
  explicit binary-coordinate certificate.
- Consequence: the exact audit performs 82,518,653 optimized local-exit
  evaluations, proves the complete cap-145 and cap-148 failures, and tracks
  all later collisions through the adjacent cap-166/cap-167 boundary. The
  1,748 recorded cap-166 coordinates leave only
  \(\{59699,63463\}\); one cap-167 coordinate repairs it. Independent
  closed-form, dense, Rust, and C# paths verify the certificate. This is a
  lossless finite proof strategy, not a sampling method, an asymptotic
  improvement to DEF-032, or a general factoring result.

## ADR-049 - Reuse exact partition refinement at length 33

- Date: 2026-07-29.
- Decision: retain the M44 exact non-singleton equivalence-partition
  algorithm for M45, but register both inherited public caps before
  restricting the transition to the complete cap-172 collision class.
  Record every varying primitive bit as a construction coordinate and audit
  every newly admitted cap-195 primitive coordinate on the last pair.
- Rationale: the complete cap-172 profile proves that all primes outside its
  eight-prime bucket are already singletons and cannot merge after coordinate
  appending. Evaluating subsequent descriptors only on live classes is
  therefore exact, while avoiding a full \(2{,}410\times661{,}152\) byte
  prefix. The separate repair census prevents a first-found witness from
  being mistaken for uniqueness.
- Consequence: the audit proves both public-cap failures, the complete
  cap-172--195 collision ladder, the adjacent cap-194/cap-195 threshold, and
  uniqueness of the final nonconstant primitive coordinate. The resulting
  2,410-coordinate certificate is explicit and independently checkable. This
  remains a finite certificate method, not an asymptotic selector
  construction, a public promise recognizer, or a general factoring result.

## ADR-050 - Register both length-34 public caps before adjacent repair

- Date: 2026-07-29.
- Decision: retain exact non-singleton equivalence-partition refinement for
  M46, record the distinct cap-196 and cap-200 public profiles, then restrict
  the transition to the complete cap-200 collision pair. Audit every newly
  admitted cap-201 primitive coordinate rather than stopping at the first
  separating witness.
- Rationale: the cap-200 partition proves that every prime outside
  \(\{97927,99527\}\) is already a singleton and cannot merge after
  coordinate appending. The restricted transition is therefore exact.
  Separately enumerating all 81,112 new primitive coordinates establishes
  uniqueness of the repair source instead of silently promoting a
  first-found witness.
- Consequence: the audit proves both public-cap failures, the adjacent
  cap-200/cap-201 threshold, and the unique one-coordinate incremental
  repair. The 3,298-coordinate certificate is explicit and independently
  checkable. This remains a finite certificate method, not an asymptotic
  selector construction, a public promise recognizer, or a general factoring
  result.

## ADR-051 - Charge exact lifts analytically without changing the compact path

- Date: 2026-07-29.
- Decision: define an analytical exact-output ledger for all eight DEF-032
  primitive integers, including continuation values skipped by nonunit-base
  branches, while leaving the public compact modular implementation
  unchanged. Use the complete union support only as an upper bound.
- Rationale: a polynomial numeric cap bounds \(A,B,g\) themselves, so the
  exact lifts have polynomial bit length even though the public evaluator
  need not materialize them. Overcharging skipped values and duplicates makes
  the support obstruction conservative and avoids confusing it with a public
  factoring or support-enumeration step.
- Consequence: the exact ledger proves BAR-041 for every polynomial numeric
  DEF-032 cap. The decision does not extend the result to the BAR-022 compact
  gap, where an exponentially large numeric parameter has only polynomial
  encoding length, or to other compact descriptor grammars.

## ADR-052 - Charge compact-gap pair overlaps by level span

- Date: 2026-07-29.
- Decision: for the exact \(A=3,B_t=2^t+3,g=2\) family, charge primes with
  signature Hamming weight at least two to the pair-overlap integer
  \(R_d=3^{2^d-1}+32^{2^d-1}\), where \(d\) is the public level gap. Keep
  descriptor/evaluation cost, exact cofactor magnitude, and analytical
  support as separate ledgers.
- Rationale: the individual compact cofactors are exponentially long, so
  BAR-041's exact-output budget is unavailable. Their common support still
  obeys an exact shift-invariant divisibility relation. After removing the
  conservatively bounded multi-hit set, only zero and one-hot signatures
  remain and can be counted without a support oracle.
- Consequence: BAR-042 rules out every polynomial-size level list with span
  \((1/2-\varepsilon)m\) and polynomial total evaluation work. Wide-span
  lists at the half-length boundary or beyond remain open and become the
  next falsification target.

## ADR-053 - Charge high-weight support to the GCD of public gaps

- Date: 2026-07-29.
- Decision: for each fixed \(h\), charge a prime hitting \(h+1\) compact-gap
  levels to the single overlap integer \(R_q\), where \(q\) is the GCD of
  the \(h\) offsets from the first selected level. Bound all such primes by
  a union over \((h+1)\)-subsets, then count the remaining signatures by the
  exact Hamming ball of radius \(h\).
- Rationale: pairwise overlap alone pays for the full public span and stops
  below the half-length boundary. The common-support relations preserve
  their negative sign under GCD reduction because every quotient
  \((2^d-1)/(2^q-1)\) is odd. Also \(h\) distinct positive multiples of
  \(q\) force \(q\le\Delta/h\), recovering an exponential gap while keeping
  all factors and support sets outside the public algorithm.
- Consequence: BAR-043 rules out every polynomial-size, polynomial-cost
  list from this exact family with any fixed linear span \(Cm\). The finite
  union bound remains deliberately conservative, and superlinear spans,
  adaptive schedules, other compact grammars, and general factoring remain
  unresolved. Work pauses after M49 by user instruction.

## ADR-054 - Separate finite theorem synthesis from source certificates

- Date: 2026-07-30.
- Decision: preserve the 16 M31--M46 source schemas unchanged and generate one
  26-row M50 publication artifact plus English and Korean table fragments
  from them. Freeze every source file by SHA-256 and provide a separate
  stdlib-only projection checker. Keep full semantic recomputation in the
  original per-milestone differential checkers.
- Rationale: a hand-maintained table would duplicate thresholds, populations,
  predecessor buckets, and evidence IDs across two papers. Re-running every
  late population audit is too expensive for the minimum reviewer path, while
  trusting only prose is too weak. A layered trust model makes the cheap
  integrity check and the expensive semantic check explicit.
- Consequence: the integrated table is a review index, not a new experiment
  or mathematical claim. `n.c.` is used where early milestones did not
  separately prove a minimum incremental-repair coordinate count. Compact
  modular steps, standard bit operations, online evaluation, and offline
  certificate generation are reported in separate ledgers. The paper title
  no longer uses an unstable numerical theorem/barrier aggregate.
- Rollback condition: if any frozen source schema changes, regenerate the M50
  artifact and both tables, rerun the minimal and semantic checks, and review
  every affected manuscript statement before publication.

## ADR-055 - Balance overlap depth against public span

- Date: 2026-07-30.
- Decision: replace BAR-043's fixed analytical overlap order by the public
  variable order
  \(h_m=\min\{r_m,\lceil\sqrt{\Delta_m/
  \lceil\log_2(r_m+1)\rceil}\rceil\}\). Apply the exact existing high-weight
  union bound when \(h_m<r_m\), and count the full signature space when the
  order reaches \(r_m\).
- Rationale: the logarithms of the high-weight union and low-weight Hamming
  ledgers are respectively controlled by
  \(h_m\log r_m+\Delta_m/h_m\) and \(h_m\log r_m\). Balancing the terms makes
  both \(o(m)\) whenever
  \(\Delta_m\log_2(r_m+1)=o(m^2)\), without deleting the growing subset
  multiplicity or introducing factor data.
- Consequence: BAR-044 closes every polynomial subquadratic span
  \(O(m^{2-\varepsilon})\) in the exact compact-gap family. The full
  \(\Theta(m^2/\log m)\) constant boundary, quadratic spans, other compact
  grammars, adaptive schedules, and general factoring remain open.

## ADR-056 - Charge distinct-level packing before optimizing boundary entropy

- Date: 2026-07-30.
- Decision: at the M51 boundary, retain the exact high/low ledgers but choose
  \(h_m=\lceil xm/\ell_m\rceil\) and use the mandatory list-geometry
  inequality \(r_m\le\Delta_m+1\) before applying binomial entropy bounds.
- Rationale: packing forces
  \(\log_2(e r_m/h_m)\le(1/2+o(1))\ell_m\) uniformly. The resulting
  high-weight coefficient is \(x/2+c/x\), minimized at \(\sqrt{2c}\), so the
  exact-family range \(c<1/8\) closes without pretending that \(r_m\) and
  \(\Delta_m\) are independent.
- Consequence: BAR-045 reaches explicit boundary constants while leaving
  \(c=1/8\) honestly open. M53 will test whether the remaining subset
  overcount can be reduced; no injective endpoint construction is inferred.

## ADR-057 - Deduplicate high-weight charges by their GCD gap

- Date: 2026-07-30.
- Decision: replace the M52 high-weight sum over every
  \((h_m+1)\)-subset by one charge for each possible GCD gap
  \(1\le q\le\lfloor\Delta_m/h_m\rfloor\).
- Rationale: BAR-043 maps every high-weight prime to an overlap integer
  \(R_q\), and subsets with the same \(q\) do not create distinct support
  integers. The prefix bit budget is
  \(5\cdot2^{D_m+1}-10-4D_m\), eliminating the binomial subset exponent.
- Consequence: BAR-046 expands the uniform closed range from \(c<1/8\) to
  \(c<1/2\). The endpoint remains open because the high and low coefficient
  requirements meet without slack; M54 will audit which gaps are realizable.

## ADR-058 - Treat realizable-gap pruning as a sharpness test

- Date: 2026-07-30.
- Decision: define the exact set of GCD gaps realized by
  \((h+1)\)-subsets and test the maximum before attempting a smaller union
  ledger.
- Rationale: the largest overlap integer controls the exponential scale.
  The arithmetic progression \(\{s,s+q,\ldots,s+hq\}\) realizes
  \(q=\Delta/h\) exactly; its full containing interval has
  \(r=\Delta+1\) and retains that witness. Thus no universal constant-factor
  or little-o reduction follows from realizability alone, even under maximum
  level packing.
- Consequence: M54 records a method barrier rather than promoting a failed
  endpoint proof. M55 will audit shared divisors and primitive parts of the
  overlap integers \(R_q\).

## ADR-059 - Replace product charging by the exact prefix LCM

- Date: 2026-07-30.
- Decision: compute shared prime support through
  \(L_D=\operatorname{lcm}(R_1,\ldots,R_D)\), after first proving the exact
  pair identity \(\gcd(R_a,R_b)=R_{\gcd(a,b)}\).
- Rationale: an LCM is the smallest exact integer whose prime support covers
  the union, so it removes all duplicate prime powers without heuristic
  independence assumptions.
- Consequence: \(R_D\mid L_D\) keeps
  \(\log_2L_D=\Theta(2^D)\). Shared-divisor accounting improves finite
  constants but cannot by itself change the BAR-046 leading exponent.

## ADR-060 - Separate gap realizability from prime occurrence

- Date: 2026-07-30.
- Decision: characterize the full realizable-gap set for the
  maximum-density interval before making any statement about overlap prime
  divisors.
- Rationale: the explicit subset
  \(\{s,s+q,\ldots,s+hq\}\) realizes every
  \(q\le\lfloor\Delta/h\rfloor\). Hence the BAR-046 all-gap prefix is exact
  geometry for dense intervals, but this alone supplies no common prime.
- Consequence: M56 closes the realizability-pruning route without converting
  geometric witnesses into unsupported balanced-prime claims.

## ADR-061 - Test endpoint slack on an exact dense witness family

- Date: 2026-07-30.
- Decision: define
  \(r_\lambda=2^\lambda-1\),
  \(\Delta_\lambda=2^\lambda-2\), and
  \(m_\lambda=\lceil\sqrt{2\lambda\Delta_\lambda}\rceil\), then compare the
  exact prefix-LCM charge and exact low-weight Hamming capacity on the two
  sides of \(h=\lfloor2\Delta_\lambda/m_\lambda\rfloor\).
- Rationale: the family has exact logarithmic scale \(\lambda\), saturates
  the \(c=1/2\) boundary, and permits a threshold-uniform dichotomy. Below
  the switch the largest LCM term already consumes the population ledger;
  above it the Hamming ball does.
- Consequence: BAR-050 rules out lower-order rescue inside this exact
  sufficient certificate without claiming endpoint injectivity. M58 will
  examine which primes can actually occur in the overlap integers, the main
  information discarded by the LCM ledger.

## ADR-062 - Classify overlap-prime occurrence by exact ratio order

- Date: 2026-07-30.
- Decision: for each prime \(p>7\), replace direct factorization of growing
  \(R_q\) by the exact order of \(3\cdot32^{-1}\pmod p\), and derive the
  full occurrence-level set from the half-order \(d_p\).
- Rationale: \(p\mid R_q\) is equivalent to
  \((3/32)^{2^q-1}=-1\pmod p\). This holds exactly when the ratio order is
  \(2d_p\) with odd \(d_p\mid2^q-1\), making all occurrence levels multiples
  of \(\operatorname{ord}_{d_p}(2)\).
- Consequence: BAR-051 exposes exact periodic structure without a
  factorization heuristic. The periodic repeats are already removed by the
  prefix LCM, so M59 must quantify possible first-occurrence half-orders
  rather than count inherited hits again.

## ADR-063 - Separate half-order size pruning from residue counting

- Date: 2026-07-30.
- Decision: derive \(p<33^{d_p}\) and \(2d_p\mid p-1\), but assess
  first-gap pruning from the unconditional size inequality before applying
  any prime-distribution estimate.
- Rationale: summing residue classes over \(d\mid2^q-1\) is a distinct
  counting problem and must not be hidden inside the size theorem.
- Consequence: BAR-052 gives linear half-order and logarithmic first-gap
  floors; M60 will audit the residue-class union bound.

## ADR-064 - End with a status-separated separator synthesis

- Date: 2026-07-30.
- Decision: close M60--M80 as one dependency chain: exact residue barriers,
  a formal UCSS premise, conditional reductions, and an unconditional
  restricted-input theorem.
- Rationale: treating UCSS existence as proved would be the precise
  unsupported step. Keeping it as DEF-046 makes the conditional and
  unconditional branches independently reviewable.
- Consequence: M80 pauses with general factoring still open, while preserving
  THM-020 as a genuine restricted-class algorithm and COND-004 as a complete
  conditional reduction.

## ADR-065 - Migrate every live length parameter to standard bit length

- Date: 2026-07-31.
- Decision: define input length only as
  \(\operatorname{bitlength}(N)=\lfloor\log_2N\rfloor+1\), retain
  \(\lceil\log_2N\rceil\) only under the explicit legacy symbol used in the
  M81 refutation, and audit exact artifacts before changing any frozen data.
- Rationale: the former expression is one too small exactly at powers of two.
  The error does not justify discarding valid odd-semiprime results, but exact
  public schedules, perfect-power handling, and random-bit endpoints cannot
  rely on asymptotic equivalence.
- Consequence: powers \(2^e\) receive the correct length \(e+1\). The
  M31--M46 populations and hashes remain frozen because every certified input
  is odd and the implementations already use standard bit-length operations.
  M82 will normalize notation while splitting the manuscript; no general
  factoring claim changes status.

## ADR-066 - Keep one archival authority and three focused projections

- Date: 2026-07-31.
- Decision: retain `paper/main.tex`, `paper/main-ko.tex`, and
  `research/CLAIMS.md` as the complete authoritative record, while publishing
  three focused bilingual paper pairs for promise factorization, cyclotomic
  extraction, and finite certificates.
- Rationale: copying all 268 claim statements and the full milestone
  chronology into every submission would recreate the readability problem
  identified by the external review. A checked projection gives each paper
  seven representative results without silently deleting supporting proofs,
  barriers, refutations, or experiment anchors.
- Consequence: `schemas/m82-paper-portfolio-v1.json` records all 21 focused
  claim placements and all 247 archival-only claims with source hashes.
  `scripts/check_m82_paper_portfolio.py` independently enforces bilingual
  status parity, exclusive front-facing placement, exhaustive ledger
  coverage, reproduction anchors, the finite endpoint, and the OPEN general
  factoring scope. M83 may change positioning only after inspecting primary
  sources; it may not infer novelty from this editorial split.

## ADR-067 - Use a three-layer related-work classification without priority promotion

- Date: 2026-07-31.
- Decision: separate established mechanisms, the repository's exact scoped
  synthesis, and any independent priority conclusion. All seven M83 rows are
  marked `SCOPED_SYNTHESIS` and `NO_PRIORITY_CLAIM`; an unmatched bounded
  search cannot change either label.
- Rationale: Pollard \(p-1\), Williams \(p+1\), separating systems,
  addition-chain evaluation, root-of-unity methods, and product/remainder
  trees are established background, while the repository's exact promise,
  branch, family, and constant scopes require separate comparison.
- Consequence: M83 improves positioning without promoting a claim. A future
  positive novelty or priority label would require a broader independent
  literature review and direct technical comparison beyond the admitted
  source set.

## ADR-068 - Normalize text line endings before source hashing

- Date: 2026-07-31.
- Decision: M82 and M83 hash decoded UTF-8 text after universal-newline
  normalization instead of hashing checkout-specific raw bytes.
- Rationale: Git may materialize the same text blob with CRLF on Windows and
  LF on another platform. Raw-byte hashing made a fresh checkout appear stale
  even when its mathematical and publication content was unchanged.
- Consequence: content mutations remain detectable, while CRLF/LF conversion
  alone no longer changes the registered source hash. Both independent
  checkers and regression suites enforce the normalized convention.

## ADR-069 - Make bounded promise results all-or-nothing

- Date: 2026-07-31.
- Decision: expose only `FACTORED` with a complete verified prime multiset or
  `UNRESOLVED` from the bounded \(p-1\) and nonsplit \(p+1\) wrappers. Use a
  positive finite budget \(s\) at every randomized composite node, discard
  partial child results, and state local and complete-recursion probability
  bounds separately.
- Rationale: hereditary promise membership is not recognized online, so an
  exhausted budget cannot certify primality, nonmembership, or absence of a
  separator. Returning a partial list would invite callers to treat an
  incomplete result as a factorization. The complete recursion needs a
  conditional union bound over fewer than \(4m\) invocations, not an
  independence assumption between nodes.
- Consequence: both wrappers terminate on every positive input and never
  report a false factorization. The tails \((7/12)^s\) and \((11/12)^s\), and
  their capped \(4m\)-multiple bounds, apply only on the corresponding
  hereditary promises with valid schedules and fresh total sampling. The
  Python implementation remains an exact small-input reference; its
  trial-division primality routine is not the polynomial-time implementation
  assumed by THM-001 and THM-002.

## ADR-070 - Use M41 as the minimal clean-room semantic certificate

- Date: 2026-07-31.
- Decision: validate the M41 \(m=29\) row with a standard-library-only
  checker that reconstructs population, descriptor grammar, primitive
  residues, certificate signatures, predecessor collision, and unique repair
  without importing generator or reference code.
- Rationale: M41 retains every trust-boundary feature requested by the
  feedback, including a nonmonotone exact threshold and a unique incremental
  repair, with about 1.05 million certificate evaluations. The initially
  considered M46 row needs roughly 10.88 million construction evaluations
  before its predecessor audit, making it a poor first target for a small
  external-review checker.
- Consequence: one representative finite theorem now has an independent
  semantic path in 548 lines. Other M31--M46 rows retain their existing
  semantic checkers and M50 integrity path; no table-wide clean-room claim is
  made. M86 will test whether the same trust boundary can be extended to the
  final M46 row with streaming and bounded-memory evaluation.

## ADR-071 - Stream the M46 certificate by coordinate

- Date: 2026-07-31.
- Decision: validate the final M46 row with a standalone standard-library
  checker that iterates one certificate coordinate at a time and retains one
  packed signature per population prime. Stream the cap-200 and cap-201
  descriptor grammars instead of materializing descriptor sets.
- Rationale: the full construction has 10,880,102 coordinate/prime cells.
  Retaining a Python object for every cell would unnecessarily enlarge the
  reviewer memory and trust surface. The streaming invariant needs exactly
  3,299 mutable signature slots while preserving exact comparison with the
  registered certificate.
- Consequence: M46 now has a 624-line clean-room semantic path that completes
  in under one minute on the recorded host. M85 and M86 cover two endpoint
  rows only; the other 24 M50 rows retain their existing semantic and
  integrity paths. No asymptotic memory, selector-wide, or general-factoring
  claim is made.

## ADR-072 - Put a four-row cost ledger before every focused-paper section

- Date: 2026-07-31.
- Decision: every focused English/Korean manuscript places exactly one
  four-row cost ledger after its abstract and before section 1. The rows name
  charged online work, offline proof or excluded inputs, output semantics
  where needed, and the exact guarantee scope. Abstracts must contain
  200--300 Unicode lexical tokens after each LaTeX math expression is
  normalized to one token.
- Rationale: the supplied feedback correctly identified that repeated scope
  prose delayed the evaluator/generator trust boundary. A single early ledger
  makes hidden preprocessing and output expansion easier to audit, while one
  language-neutral counting rule gives the English and Korean papers the
  same executable editorial gate.
- Consequence: `scripts/check_m87_focused_papers.py` freezes six abstract
  counts, 24 labeled cost rows, and 21 bilingual claim IDs with unchanged
  `PROVED` status. The token count is only an editorial convention, not a
  Korean morphological analysis. No online operation is reclassified as
  offline, and no theorem or complexity claim changes.

## ADR-073 - Separate five reader-label families from stable claim metadata

- Date: 2026-07-31.
- Decision: render every focused-paper claim with one localized reader label
  from exactly five families: theorem, proposition, counterexample and
  criterion, barrier, or finite certificate. Keep the original
  `THM/BAR/LEM-###` ID and status visibly adjacent and unchanged. Use a compact
  inline heading rather than a new numbered theorem environment.
- Rationale: the internal codes are essential audit keys but are poor first
  descriptions for readers. More than five localized label kinds made the
  hierarchy harder to scan, while hiding or replacing the codes would break
  traceability. A small bold heading supplies mathematical role and subject
  without introducing a second authority for numbering or status.
- Consequence: `scripts/check_m88_reader_labels.py` fixes the one-to-one
  English/Korean presentation map over all 21 focused claims, requires all 42
  rendered headings to wrap existing `PROVED` metadata, and rejects missing,
  reordered, renamed, or unwrapped claims. Reader labels are editorial
  descriptions only; `research/CLAIMS.md` remains authoritative.

## ADR-074 - Make the focused-paper narrative boundary executable

- Date: 2026-07-31.
- Decision: every focused English/Korean manuscript has exactly one
  `\appendix` boundary followed by a primary-source-positioning appendix and
  a reproduction/limitations/archive appendix. Keep the mathematical section
  order and all representative claim IDs before that boundary. Require raw
  reproduction commands, repository paths, experiment IDs, file hashes, and
  internal milestone tokens to occur only after it.
- Rationale: the supplied review asked that repository chronology and
  reproducibility detail stop interrupting the mathematical narrative, but
  moving prose by editorial judgment alone could silently lose an audit
  anchor. A fixed bilingual registry makes both sides of the split
  independently testable: the main body is free of repository-internal
  mechanics, while the appendices remain complete enough to reproduce and
  audit every focused result.
- Consequence: `scripts/check_m89_appendix_boundaries.py` freezes 34 main
  sections, 12 appendices, 32 commands, 38 paths, 14 source anchors, and the
  21-ID bilingual claim map. It also requires a limitation statement in every
  paper and rejects main-body leakage or appendix anchor loss. The boundary
  is editorial only; it changes no claim status, proof, cost model, or
  experiment. M90 may move the complete finite threshold chronology within
  the finite-paper appendix, but may not alter its 26 registered rows.

## ADR-075 - Keep five finite cases in main and all 26 rows in appendix

- Date: 2026-07-31.
- Decision: remove the generated 26-row threshold table from the English and
  Korean finite-paper main narratives and place it in the existing
  certificate-reproduction appendix. Keep five reviewer-prioritized cases in
  main: the \(m=9\ldots15\) base range, the first base-cap failure at
  \(m=16\), the length-28 jump and five-coordinate repair, the length-29
  nonmonotonicity, and the length-34 endpoint. Preserve all seven focused
  claim IDs before the appendix boundary.
- Rationale: the full chronology is essential audit evidence but obscures the
  finite theorem's conceptual progression when rendered between the initial
  theorem and its two representative endpoint claims. The five cases expose
  onset, failure, jump, nonmonotonicity, and endpoint behavior, while a
  machine-checked appendix preserves every intermediate row.
- Consequence: `scripts/check_m90_finite_chronology.py` independently fixes
  the semantic fields of all 26 rows and checks them against both rendered
  table fragments and the frozen M50 artifact. It also requires exactly five
  representative cases and seven `PROVED` claims in each main narrative.
  The move changes no threshold, certificate, proof, population, or
  asymptotic statement. M91 will test whether the remaining 24 rows can
  receive a bounded no-project-import semantic path.

## ADR-076 - Use one grammar evaluator with explicit schema adapters

- Date: 2026-07-31.
- Decision: validate all 26 M50 finite rows with one standard-library-only
  semantic core and explicit adapters for the M31--M46 metadata generations.
  Fix the reviewer budget at 1,000 source lines, 300 seconds, and 128 MiB peak
  working set. Keep M85 and M86 as separately implemented endpoint checks.
- Rationale: all 17,515 selected certificate sources use the same public
  descriptor and primitive-exit grammar, while their JSON field placement
  differs. Duplicating 16 arithmetic evaluators would enlarge the trusted
  base without adding mathematical independence. Explicit adapters make the
  field differences reviewable and leave the arithmetic reconstruction
  singular.
- Consequence: M91 closes the 24-row semantic coverage gap under the stated
  resource budget. Collision buckets are compared as unordered equivalence
  classes. The \(m=27,28\) five-coordinate repairs retain their actual cap-72
  and cap-88 baselines rather than being coerced to adjacent predecessors.
  In-process `tracemalloc` is rejected by NR-059; external peak-working-set
  sampling is the recorded resource method. The outcome is `EMPIRICAL`
  finite evidence and does not change any theorem status.

## ADR-077 - Certify repair minima with coverage types and private pairs

- Date: 2026-07-31.
- Decision: quotient raw binary coordinates by identical pair-coverage masks,
  record one canonical pattern per nonzero type, and certify each exact
  minimum with both a covering upper witness and one private-pair lower
  witness per selected type. Bind the complete finite type lists to EMP-062
  and the exact M38--M46 source digests.
- Rationale: the nine repair instances have at most 15 unresolved pairs and
  five coverage types. Every selected type has a private pair, giving a
  polynomial certificate whose lower direction is directly reviewable. The
  generic cardinality bound is not exact at lengths 27 and 28.
- Consequence: the abstract portfolio is 745 bits and its core verifier
  ledger is 397 bit tests. The independent checker also exhausts 82 subsets
  as bounded defense in depth, but that exponential path is not part of the
  theorem's asymptotic verifier. Source hashing/parsing remains a separately
  charged 5,939,505-byte provenance layer.

## ADR-078 - Use a portfolio of lower witnesses for early repairs

- Date: 2026-07-31.
- Decision: retain private-pair lower witnesses where they exist, use the
  information-theoretic bucket-cardinality bound when it exactly matches the
  upper witness, and otherwise enumerate one uncovered pair for every
  \((k-1)\)-type subset. Require an independently reconstructed complete type
  list for private-pair and subset-obstruction claims.
- Rationale: the early length-16 and length-24 type systems have exact minimum
  covers but no private pair for any selected type. Cardinality is exact at
  length 16 but gives only two below the length-24 minimum three. The six
  two-type subsets at length 24 are small enough to expose directly without
  treating brute-force search as a proof object.
- Consequence: THM-022 gives a general finite subset-obstruction certificate,
  while REF-062 and NR-061 preserve the boundary of the private-pair
  criterion. The M93 production checker independently evaluates 154,920 raw
  primitive coordinates and checks a 483-bit abstract portfolio. The result
  remains finite and selector-specific and does not change the OPEN status of
  general classical polynomial-time factoring.

## ADR-079 - Treat two-coverer columns as a graph certificate

- Date: 2026-07-31.
- Decision: reconstruct the full coverer set of every universe element before
  selecting a lower argument. When every column has exactly two coverers,
  identify repair covers with vertex covers of the resulting coverer
  multigraph. For the two private-pair failures, verify every \(K_3\) or
  \(K_4\) edge rather than retaining an explicit undersized-subset list.
- Rationale: the length-16 and length-24 masks are vertex-edge incidence
  matrices of complete graphs. Complete-graph incidence makes the exact
  minimum \(t-1\), makes any fixed omitted type an implicit upper witness, and
  removes all stored upper/lower indices. The criterion is checked from the
  masks; the JSON coverer list is a redundant audit trace.
- Consequence: THM-023 supplies the finite structural theorem and EXP-0065
  records 130 payload bits instead of the incumbent 186, saving 56. The
  conservative verifier ledger is 75 rather than 70 tests, so REF-063 and
  NR-062 preserve that payload compression is not strict work compression.
  The applications inherit type-family completeness from EMP-064 and do not
  change any asymptotic or general-factoring claim.

## ADR-080 - Profile the entire repair portfolio as looped graphs

- Date: 2026-07-31.
- Decision: reconstruct every coverer column in both frozen M92/M93
  portfolios before selecting a certificate form. Treat singleton coverers as
  graph loops, two-element coverers as ordinary edges, and reject empty or
  higher-rank columns. Compare the full duplicate-sensitive slot list against
  one of three inferred templates rather than storing upper or lower witness
  indices.
- Rationale: all nineteen instances have coverer rank at most two and match
  exactly 12 loop-only, five looped-clique, or two loopless-clique templates.
  Loops force all types in seventeen instances; the two remaining cliques use
  THM-023. One graph grammar therefore verifies every registered minimum
  while reducing the combined abstract payload from 1,228 to 1,063 bits.
- Consequence: THM-024 records the general looped-graph reduction and the
  residual vertex-cover boundary; REF-064 and NR-063 prevent rank-two counts
  from being mistaken for a universal exact formula. EXP-0066 inherits
  completeness from EMP-062/EMP-064 and remains finite, source-bound, and
  unrelated to a general factoring solution.

## ADR-081 - Separate matching-certificate verification from discovery

- Date: 2026-07-31.
- Decision: define the M96 exactness witness as one residual vertex cover and
  one residual matching of the same declared size. Verify both objects
  directly after reconstructing forced loops, and use bounded enumeration
  only as an independent defense for the eight synthetic experiment cases.
- Rationale: equality gives both upper and lower bounds without storing one
  obstruction for every smaller subset. It extends the graph method to
  non-template systems such as \(P_3\) and \(K_4-e\), while the triangle
  preserves a clear boundary where matching is insufficient.
- Cost decision: charge one \(\lceil\log_2(t+1)\rceil\)-bit size field plus
  the cover and matching indices. The earlier 28-bit draft omitted five
  framing fields; the corrected registered aggregate is 43 bits.
- Consequence: THM-025 is a certificate-verification theorem, not an
  algorithm for finding equality witnesses or solving arbitrary vertex
  cover. EXP-0067 is synthetic and inherits only its seed slots from EMP-066.

## ADR-082 - Construct bipartite witnesses and charge the explicit input

- Date: 2026-07-31.
- Decision: on a two-colored residual coverer graph, repeatedly find and flip
  one augmenting path until none remains, then construct the minimum cover by
  alternating reachability. Emit the cover and matching as a checkable
  `THM-025` output rather than accepting either as advice.
- Rationale: the augmenting-path lemma and reachability construction give a
  complete restricted-class algorithm with a direct proof and no
  vertex-subset enumeration. The single-path implementation is simpler to
  audit than a faster batching implementation and already gives
  \(O(t(t+q))\) indexed operations.
- Input-model decision: state polynomiality only in the explicit
  graph/type-system representation and separately charge graph
  reconstruction and source binding. No step asserts that hidden-factor
  complete types can be constructed from the integer input.
- Boundary decision: retain triangle-plus-pendant as a non-bipartite equality
  case and \(C_5\) as a non-bipartite gap. Bipartiteness is sufficient for
  construction, not necessary for certificate existence.
- Consequence: THM-026 discharges M97 for the bipartite restricted class.
  EXP-0068 remains synthetic and source-bound; the next extension must expose
  any non-bipartite parameter dependence rather than hide it as polynomial.

## ADR-083 - Enumerate supplied transversal choices and expose advice

- Date: 2026-07-31.
- Decision: accept a proposed odd-cycle transversal \(X\) only after checking
  that the residual graph minus \(X\) is bipartite. Enumerate all
  \(2^{|X|}\) selected/unselected choices, reject uncovered internal edges,
  force neighbors of excluded transversal vertices, and invoke the M97
  constructor only on the remaining bipartite induced graph.
- Rationale: every vertex cover determines exactly one branch through its
  intersection with \(X\). This yields a short direct optimality proof and
  extends construction to matching-gap examples such as \(C_5\), \(K_4\),
  and \(K_5\) without claiming an arbitrary-graph polynomial solver.
- Cost decision: charge the transversal as supplied input using
  \(\ell_s+s\ell_t\) bits, the constructed cover separately using
  \(\ell_k+k\ell_t\) bits, and display \(2^s\) in indexed and bit-operation
  bounds. The experiment may retain all branches, but the theorem algorithm
  needs only the current branch and best candidate.
- Boundary decision: a conditional \(s=O(\log m)\) polynomial consequence
  also requires polynomial explicit graph parameters and an admissible way
  to obtain \(X\). M98 supplies neither a discovery algorithm nor a
  logarithmic bound.
- Consequence: THM-027 discharges M98 as a fixed-parameter exact-repair
  theorem. EXP-0069 remains synthetic and source-bound; M99 must separate
  polynomial transversal verification from factor-independent discovery.

## ADR-084 - Use iterative compression and retain the graph-construction boundary

- Date: 2026-07-31.
- Decision: reconstruct the inspected iterative-compression OCT algorithm
  for the explicit residual graph. Enumerate three states for each vertex
  of the compression set, reduce every surviving state to a
  terminal-deleting vertex separator by node splitting, and retain the
  smallest valid OCT.
- Literature decision: credit Lokshtanov, Saurabh, and Sikdar for the
  established \(O(3^k k|E||V|)\) OCT method. State the local
  \(O(3^{k+1}(k+1)t(t+q))\) implementation bound conservatively and do not
  claim novelty for iterative compression or the separator reduction.
- Tie decision: require deterministic output, exact OCT cardinality, and
  bipartite deletion. Do not require the globally lexicographically first
  optimum because a deterministic maximum-flow tie may choose another
  optimum separator.
- Cost decision: distinguish the FPT \(3^k\operatorname{poly}(t,q)\)
  discovery from naive XP subset enumeration
  \(\sum_{i\le k}\binom{t}{i}\). Only the former preserves polynomial time
  when \(k=O(\log m)\) and the explicit graph parameters are polynomial in
  \(m\).
- Boundary decision: discovery is factor-independent relative to the
  already explicit graph and public cap. M99 does not construct the
  factor-dependent complete type system or prove a logarithmic cap for
  graphs arising from unrestricted integer inputs.
- Consequence: THM-028 discharges M99 at the explicit-graph layer and
  composes with THM-027. M100 must confront public graph construction or a
  separately checkable substitute rather than silently treating the graph
  as available.

## ADR-085 - Separate factor independence from bit-polynomial construction

- Date: 2026-07-31.
- Decision: define a public collision-completeness certificate by selected
  coordinate confinement plus exhaustive raw-selector persistence. Rebuild
  every newly admitted coverage type and coverer edge from public modular
  evaluations instead of accepting prime labels, types, edges, or a row cap
  as advice.
- Cap decision: use the single public formula
  \(k(m)=\lceil\log_2m\rceil\) for every frozen row. Verify its finite
  success after graph construction, but retain its future asymptotic status
  as open.
- Cost decision: charge population enumeration \(P\), selected-coordinate
  work \(CnE\) for \(n=|X|\), baseline persistence \(D_0bE\), new-type
  enumeration \(D_1bE\), graph construction, and the full \(3^k\) OCT term
  separately.
  Polynomiality is in the expanded public artifacts, not automatically in
  \(m\).
- Oracle decision: derive blocks, labeled coverage types, coverer columns,
  forced loops, and residual edges before reading their M95 counterparts.
  Use M95 only as a post-construction semantic oracle modulo bucket and type
  ordering.
- Integrity decision: treat hashes only as byte bindings. The explicit
  omitted-type counterexample shows that a newly computed valid digest
  cannot establish semantic completeness.
- Consequence: the frozen M95 graphs are factor-independent offline
  constructions, correcting the earlier informal hidden-factor wording.
  The registered route nevertheless enumerates an exponentially large
  balanced population asymptotically, so M100 does not close the original
  general factoring goal. Per user instruction, research pauses after the
  merged M100 delivery.
