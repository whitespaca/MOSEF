# CODEX.md — Research Constitution and Technical Specification

## 1. Mission

Conduct a rigorous, autonomous research program on classical integer factorization. The central question is whether an arbitrary positive integer `N`, represented in binary with input length

```text
m = ceil(log2 N),
```

can be factored on a classical computation model in time `poly(m)`.

The repository begins from a proposed research direction called **MOSEF** (Multi-Group Order-Separating Exponent Factoring) and its central combinatorial object, a **POSF** (Polynomial Order-Separating Family). These names identify a research program, not an established theorem.

The system must actively attempt to refute, repair, restrict, or replace these ideas. A rigorous barrier theorem is as valuable as a positive algorithm.

## 2. Scientific scope

### 2.1 In scope

- deterministic and Las Vegas classical integer-factorization algorithms;
- bit-complexity analysis with input length `m = ceil(log2 N)`;
- order-finding surrogates in multiplicative groups, Lucas/Pell-type groups, norm-one groups, and elliptic-curve groups over composite moduli;
- difference covers and structured exponent families;
- smooth and semismooth integers, smooth exponents, and explicit smooth-object generation;
- product trees, remainder trees, batch GCD, multipoint evaluation, and fast arithmetic;
- exact counterexample search and adversarial input construction;
- restricted input classes and density-one results;
- lower bounds and impossibility results for explicitly defined algorithm families;
- reproducible implementation and publication-quality empirical analysis;
- continuously maintained English and Korean LaTeX research papers.

### 2.2 Out of scope unless explicitly used as comparison

- claiming Shor's quantum algorithm as a classical solution;
- implementation-only speedups without a precise complexity or empirical research question;
- cryptanalytic targeting of real private keys or unauthorized systems;
- proprietary or inaccessible evidence that cannot be inspected or reproduced;
- machine-learning predictions presented as mathematical proof;
- experiments whose raw generation procedure, seed, or environment cannot be reconstructed.

## 3. Baseline research position

At the start of any literature phase, re-verify the current state of the art from primary sources. Do not treat the following as permanently current:

- primality testing is known to be in deterministic polynomial time;
- general classical factoring is not presently known to be in polynomial time;
- practical general factoring is dominated by number-field-sieve methods whose standard performance analysis includes smoothness heuristics;
- rigorous randomized and deterministic factoring bounds remain superpolynomial in `m`;
- recent work may improve deterministic exponents conditionally or shift identified bottlenecks.

For every state-of-the-art statement:

1. identify the exact computation model;
2. identify whether the result is deterministic, Las Vegas, Monte Carlo, heuristic, conditional, average-case, or worst-case;
3. record the theorem statement and hypotheses rather than only the abstract claim;
4. verify publication metadata from an authoritative source;
5. record the retrieval date;
6. compare event/publication dates when evaluating “latest” results.

Store literature notes under `research/literature/` and validated BibTeX entries in `paper/references.bib`.

## 4. Core mathematical definitions

Let `P(N)` denote the set of distinct prime divisors of `N`. For `g` coprime to `N` and positive integer `d`, define

```text
D_N(g, d) = { p in P(N) : ord_p(g) divides d }.
```

A pair `(g, d)` is an **order separator** for `N` when

```text
D_N(g, d) is nonempty and D_N(g, d) != P(N).
```

Then `gcd(g^d - 1, N)` is a nontrivial factor. This elementary implication may be used only after all domain conditions are checked, including repeated prime factors and failed inversions in generalized group channels.

A candidate **Polynomial Order-Separating Family** consists of constructible sets `G_m(N)` and `Delta_m(N)` satisfying all of the following:

1. `|G_m(N)| <= poly(m)`;
2. `|Delta_m(N)| <= poly(m)`;
3. every exponent has bit length `log2 d <= poly(m)`;
4. the sets are constructed in `poly(m)` bit operations without access to the unknown factorization;
5. for every composite input in the claimed domain, some `(g, d)` is an order separator;
6. the separator can be evaluated and the factor extracted in `poly(m)` bit operations.

The universal existence and constructibility of such families are **open research targets**, not assumptions to hide.

## 5. Threat model for invalid proofs

Every proof attempt must be screened for the following failure modes.

### 5.1 Circular access to factors

Reject any construction that requires knowledge of `p`, `q`, `p - 1`, `q - 1`, a group order modulo an unknown prime factor, or a factor-dependent choice that is not itself computable without factoring.

### 5.2 Input-size confusion

Reject complexity statements polynomial in `N`, `sqrt(N)`, the smallest factor, or an enumerated group size when the claimed target is polynomial in `m = log2 N`.

### 5.3 Hidden exponent explosion

A polynomial number of exponents is insufficient. Their bit lengths and the cost of modular exponentiation, representation conversion, and generation must also be polynomial in `m`.

### 5.4 Unproved distribution transfer

Do not transfer random-integer smoothness probabilities to structured polynomial values, algebraic norms, group orders, or adversarial inputs without a theorem or an explicit heuristic label.

### 5.5 Average-to-worst-case leakage

Density-one, average-case, or random-semiprime success does not establish a worst-case algorithm. State the input distribution and exceptional set explicitly.

### 5.6 Generic-group or oracle mismatch

A lower bound in a generic-group, black-box, algebraic-decision-tree, or restricted-query model applies only to that model. Do not overstate it as an unconditional factoring lower bound.

### 5.7 Computational proof gaps

A finite search proves only the searched range unless paired with a mathematically complete reduction. Record exact search bounds and certificates.

### 5.8 Simultaneous collision failure

If `g^d = 1` modulo every prime factor, the GCD is `N`, not a factor. Any claimed family must separate at least one prime factor from at least one other factor.

## 6. Research strategy

Use a falsification-first portfolio rather than betting the project on one conjecture.

### Stream A — Literature and formalization

- Maintain an annotated map of deterministic, randomized, heuristic, and conditional factoring algorithms.
- Extract exact lemmas involving smoothness, element orders, difference covers, batch GCD, and fast multipoint techniques.
- Reproduce theorem dependencies and identify where unproved hypotheses enter.
- Maintain a glossary and notation file to prevent silent changes of definitions.

### Stream B — Barrier and counterexample research

- Construct adversarial pairs of prime factors with correlated order structures.
- Search for inputs on which candidate exponent families produce only `1` or `N` as GCDs.
- Prove counting, information-theoretic, combinatorial, or restricted-model lower bounds for narrowly defined POSF families.
- Analyze whether a proposed POSF constructor is computationally equivalent to factoring.
- Preserve all meaningful failed constructions.

### Stream C — Single-group positive results

Study the multiplicative group first. Seek exact theorems for restricted classes such as:

- `p - 1` having a smooth component and a polynomially bounded cofactor;
- a bounded number of large prime factors in `p - 1`;
- explicitly parameterized semismooth cases;
- input classes where difference covers can provably hit one order without hitting all orders.

Every class theorem must include a membership condition, algorithm, correctness proof, bit-complexity proof, and statement of whether class membership is known or merely promised.

### Stream D — Multi-group separation

Investigate whether several independently parameterized group channels reduce correlated failures:

- multiplicative groups;
- Lucas sequences or Pell conics;
- quadratic norm-one groups;
- elliptic curves over `Z/NZ`.

For each channel, define the group law over a composite modulus carefully. Failed inversions may expose factors and must be handled as algorithmic branches rather than errors.

The multi-group objective is not “different orders probably help.” It is a theorem quantifying the number of channels, construction cost, separator probability or guarantee, exceptional inputs, and total bit complexity.

### Stream E — Algorithm engineering

- Implement exact reference versions before optimized versions.
- Use product/remainder trees and batch GCD only after validating asymptotic and constant-factor relevance.
- Measure exponent generation, modular arithmetic, memory, GCD, and orchestration separately.
- Compare against appropriate baselines without implying practical superiority from toy sizes.

### Stream F — Publication

Maintain synchronized English and Korean papers whose claims never outrun
the evidence. A useful paper may report:

- a new restricted-class factoring theorem;
- a conditional exponent improvement;
- a barrier or lower bound for a natural POSF subclass;
- a systematic negative result plus a corrected research direction;
- a reproducible framework for evaluating order-separating algorithms.

## 7. Initial milestone sequence

Codex may revise this sequence with a documented reason, but must not skip foundational validation.

### M0 — Repository and evidence foundation

Acceptance criteria:

- initialize only the directories needed immediately;
- create `ROADMAP`, `STATUS`, `CLAIMS`, `DECISIONS`, `BLOCKERS`, and `NEGATIVE_RESULTS`;
- establish reproducible toolchain manifests;
- compile a minimal LaTeX paper;
- define a cross-language experiment-result schema;
- record verified baseline literature and a source-quality policy.

### M1 — Baseline algorithm suite

Implement and test:

- trial division for small factors;
- perfect-power detection;
- deterministic primality verification suitable for test validation;
- Pollard rho;
- Pollard `p - 1`;
- Williams-style `p + 1` or a clearly scoped equivalent;
- a batch-GCD utility;
- exact modular exponentiation and test-vector generation.

The objective is not novelty. It is a trusted oracle and regression suite.

### M2 — Formal MOSEF/POSF specification

Acceptance criteria:

- precise definitions for square-free and non-square-free inputs;
- proof of the basic separator lemma;
- pseudocode with all failure branches;
- bit-complexity accounting for construction, exponent size, evaluation, GCD, and recursion;
- explicit list of unresolved universal claims;
- counterexample search harness for finite parameter ranges.

### M3 — Restricted-family theorem

Seek the strongest theorem supported by complete proof, beginning with semismooth-order cases. A result is not complete until class conditions and recognition/promise assumptions are explicit.

### M4 — Difference-cover analysis

- reproduce relevant constructions from primary sources;
- formulate the exact separator-cover property needed here;
- identify the gap between divisor coverage and prime-factor separation;
- prove a positive construction or a lower bound for a defined family.

### M5 — Multi-group experiment and theorem search

Implement at least two independent group channels with exact failure handling. Use experiments to generate conjectures and counterexamples, never as proof.

### M6 — First publishable manuscript

Produce a self-contained paper centered on the strongest verified contribution, even if that contribution is a barrier or negative result rather than general polynomial-time factoring.

## 8. Repository artifacts and schemas

### 8.1 `research/ROADMAP.md`

Maintain a table with:

- milestone ID;
- research question;
- status;
- prerequisites;
- acceptance criteria;
- validation command;
- expected artifact;
- priority;
- next action.

Only one milestone should be marked `ACTIVE` per agent/worktree unless tasks are explicitly independent.

### 8.2 `research/STATUS.md`

Update after each milestone or execution. Include:

- current branch and commit;
- completed work;
- validated claims;
- refuted or weakened claims;
- tests and paper compilation state;
- remote push/PR state;
- current blockers;
- next task.

### 8.3 `research/CLAIMS.md`

Use stable IDs such as:

```text
DEF-001
LEM-001
THM-001
CONJ-001
HEUR-001
EMP-001
BAR-001
```

For each claim record:

- exact statement;
- status;
- hypotheses;
- proof or evidence path;
- source IDs;
- code/experiment IDs where applicable;
- adversarial review state;
- last verification date.

A claim may move from `CONJECTURE` to `PROVED` only after a separate adversarial review pass. A proof author and proof reviewer may be separate Codex subagents when available, but the reviewer must independently reconstruct the argument.

### 8.4 `research/DECISIONS.md`

Use architecture-decision-record style entries:

- context;
- alternatives;
- decision;
- mathematical and engineering consequences;
- rollback condition.

### 8.5 `research/NEGATIVE_RESULTS.md`

For each failed approach record:

- hypothesis;
- motivation;
- smallest counterexample or proof of failure;
- exact parameter range searched;
- code and command;
- whether a restricted repair remains possible.

### 8.6 Experiment records

Each experiment must produce a machine-readable record conforming to a versioned schema under `schemas/`. At minimum include:

```json
{
  "schema_version": "1.0.0",
  "experiment_id": "EXP-0001",
  "git_commit": "<full hash>",
  "timestamp_utc": "<RFC3339>",
  "host": {
    "os": "...",
    "arch": "...",
    "cpu": "...",
    "logical_cores": 0,
    "memory_bytes": 0
  },
  "toolchains": {},
  "algorithm": "...",
  "parameters": {},
  "seed": "...",
  "input_manifest_sha256": "...",
  "result": {},
  "timing": {},
  "peak_memory_bytes": null,
  "stdout_sha256": "...",
  "status": "PASS"
}
```

Never edit raw experiment records after creation. Correct them by creating a superseding record and documenting why.

## 9. Language and implementation architecture

### 9.1 Rust workspace

Suggested crates, created only when justified:

- `mosef-arithmetic`: exact modular arithmetic abstractions and batch GCD;
- `mosef-groups`: group-channel interfaces and implementations;
- `mosef-families`: exponent-family constructors;
- `mosef-search`: counterexample and parameter search;
- `mosef-cli`: deterministic command-line interface;
- `mosef-schema`: serialization types matching `schemas/`.

Requirements:

- avoid `unsafe` unless a measured FFI or low-level requirement justifies it;
- document all `unsafe` invariants;
- use checked conversions;
- make random seeds explicit;
- separate research prototypes from claimed algorithms;
- benchmark only release builds with environment metadata.

### 9.2 C/C++ native layer

Use only for:

- GMP/FLINT/NTL comparisons;
- kernels demonstrably material to performance;
- independent verification of Rust arithmetic.

Expose a narrow C ABI. Add sanitizer tests where available. Never allow an FFI optimization to become the only implementation of a mathematically essential step without a reference test.

### 9.3 Python reference layer

Use Python for clarity and exactness:

- executable pseudocode;
- brute-force counterexample search;
- Hypothesis/property tests where available;
- SymPy or Sage-compatible scripts when licenses and environments permit;
- generation of canonical test vectors.

Python is the primary semantic oracle for small inputs, not the primary performance claim.

### 9.4 TypeScript / Node.js 22 orchestration

Provide:

- experiment manifests and validation;
- subprocess execution with timeouts and captured logs;
- resumable queues;
- deterministic configuration expansion;
- report generation from immutable JSONL records;
- optional GitHub issue/PR automation when authenticated.

Use strict TypeScript. Validate all external process outputs against schemas.

### 9.5 R analysis

Use scripts, not manual console history. Produce figures from checked-in manifests. Report:

- sample sizes and sampling method;
- confidence intervals;
- multiple-comparison corrections where relevant;
- residual diagnostics for regressions;
- sensitivity to finite-size ranges;
- clear warnings that observed scaling is not an asymptotic proof.

### 9.6 Java and C# verification

Implement compact independent verifiers for selected algorithms and certificates. Avoid copying the same implementation structure line-for-line from Rust; independence is the point.

## 10. Proof-development protocol

For every nontrivial theorem candidate:

1. Write the exact statement with quantified variables and computation model.
2. List all imported lemmas and verify their hypotheses.
3. Search for small counterexamples using an independent implementation.
4. Search boundary cases: repeated primes, prime powers, `2`-adic behavior, equal orders, order `1` or `2`, failed inversions, and maximal simultaneous collisions.
5. Write a proof sketch in `research/proofs/<claim-id>.md`.
6. Expand every complexity step, including representation size and preprocessing.
7. Run an adversarial review whose task is to refute the theorem.
8. Repair, weaken, reclassify, or refute the claim based on review.
9. Only then incorporate the result into the paper as proved.

The adversarial reviewer must answer:

- Is there circular dependence on the unknown factorization?
- Does construction cost satisfy the claimed bound?
- Are exponent bit lengths bounded?
- Does the separator distinguish prime factors rather than merely hit an order?
- Are average-case assumptions hidden?
- Does recursion preserve the complexity bound?
- Are all composite and prime-power cases covered?
- Can the argument be reduced to an already open conjecture?

## 11. Literature protocol

Use primary sources for technical claims:

- peer-reviewed papers;
- authors' accepted manuscripts;
- official proceedings;
- arXiv preprints when no final version exists;
- official documentation for software behavior.

Secondary sources may guide discovery but cannot be the sole support for a theorem statement or state-of-the-art claim.

For each source create a note with:

- stable source ID;
- complete citation;
- version and date;
- result classification;
- exact theorem or algorithm used;
- assumptions;
- relevance to MOSEF/POSF;
- unresolved questions;
- inspected page/section references.

Do not quote more than necessary. Paraphrase accurately and keep verbatim excerpts short.

## 12. Experiment protocol

### 12.1 Input families

Include clearly labeled sets:

- random balanced semiprimes;
- semiprimes with smooth or semismooth `p - 1`;
- semiprimes with smooth or semismooth `p + 1`;
- adversarial pairs with large `gcd(p - 1, q - 1)`;
- intentionally correlated order structures;
- close-prime semiprimes;
- products of three or more primes;
- prime powers and perfect powers;
- Carmichael numbers and pseudoprimes where relevant.

Never mix generated distributions in one aggregate result without stratification.

### 12.2 Metrics

Record at least:

- input bit length;
- factor-size profile;
- number and maximum bit length of candidate exponents;
- modular multiplications;
- GCD count;
- product-tree and remainder-tree sizes;
- wall and CPU time;
- peak memory where available;
- outcomes `1`, nontrivial factor, or `N`;
- separator channel and parameter;
- generation time separate from evaluation time.

### 12.3 Statistical interpretation

Experiments may:

- reject candidate conjectures;
- identify finite-size behavior;
- estimate practical constants;
- compare implementations;
- motivate theorem statements.

Experiments may not establish worst-case polynomial time, smoothness density for a structured family, or universal POSF existence.

## 13. Paper specification

The exhaustive English manuscript is `paper/main.tex`. The synchronized
Korean companion is `paper/main-ko.tex`. Both use the same stable claim IDs,
statuses, theorem hypotheses, limitations, experiment hashes, and
reproduction commands. The Korean companion may summarize earlier proof
history by evidence anchor, but it must be self-contained for the current
milestone's definitions, theorem or obstruction, proof, limitations, and
reproduction procedure.

### 13.1 Provisional title

Choose the title that matches the strongest verified result. Do not retain a title claiming polynomial-time factoring unless that result is actually proved.

A conservative initial title is:

> Order-Separating Exponent Families for Classical Integer Factorization: Algorithms, Barriers, and Reproducible Evaluation

### 13.2 Required structure

1. Abstract
2. Introduction and contribution statement
3. Related work and precise complexity landscape
4. Models, notation, and definitions
5. Order-separator lemma and algorithmic framework
6. Positive theorem(s), if any
7. Barrier, counterexample, or negative-result theorem(s)
8. Algorithms and bit-complexity analysis
9. Reproducible experimental methodology
10. Results
11. Limitations and open problems
12. Conclusion
13. Appendices with full proofs, schemas, and reproduction commands

### 13.3 Claim language

Use disciplined wording:

- `We prove ...` only for `PROVED` claims.
- `Assuming ..., we prove ...` for `CONDITIONAL` claims.
- `We conjecture ...` for `CONJECTURE` claims.
- `A heuristic model suggests ...` for `HEURISTIC` claims.
- `In experiments over ..., we observed ...` for `EMPIRICAL` claims.
- `The following question remains open ...` for `OPEN` claims.

### 13.4 Reproducibility appendix

Include:

- repository commit;
- toolchain versions;
- hardware summary;
- exact commands;
- experiment IDs;
- data hashes;
- figure-generation commands;
- known nondeterminism;
- license and artifact availability.

## 14. Quality gates

### Gate Q0 — Repository hygiene

- clean or intentionally documented working tree;
- no secrets;
- no unexplained binaries;
- generated files are reproducible or ignored.

### Gate Q1 — Mathematical validity

- claim status correct;
- hypotheses explicit;
- independent counterexample search completed;
- adversarial review completed for theorem promotion.

### Gate Q2 — Software correctness

- formatting, lint, type checking, unit tests, property tests, and integration tests pass for changed components;
- independent implementation agrees on test vectors;
- undefined behavior and overflow risks reviewed.

### Gate Q3 — Experimental reproducibility

- immutable result record;
- seed and environment captured;
- command reruns from a clean checkout;
- output hashes match or nondeterminism is explained.

### Gate Q4 — Paper integrity

- both English and Korean PDFs compile without undefined
  citations/references or missing glyphs;
- claims ledger and both manuscripts agree on IDs and statuses;
- figures and tables trace to experiment IDs;
- abstract and title do not overclaim.

### Gate Q5 — Git delivery

- coherent commit;
- status documentation updated;
- push/PR completed when permitted, otherwise blocker recorded.

## 15. Autonomous decision rules

When several tasks are possible, prioritize in this order:

1. repair a false, ambiguous, or overclaimed result;
2. preserve and reproduce existing work;
3. resolve a proof gap or find a counterexample;
4. complete the active milestone's acceptance criteria;
5. improve tests and reproducibility;
6. update the paper to match verified evidence;
7. optimize performance only after correctness and measurement are stable;
8. explore a new direction only when higher-priority work is unblocked or exhausted.

Do not pursue a line merely because it produces more code. Prefer a smaller theorem with a complete proof over a broad conjecture with impressive experiments.

## 16. Stop, downgrade, and pivot rules

### Stop and record a blocker when

- required credentials or permissions are unavailable;
- external literature cannot be accessed and the next claim depends on it;
- a command would incur cost or interact with an unauthorized system;
- repository corruption or unresolved merge conflict makes further edits unsafe.

### Downgrade a claim when

- a proof uses an unproved lemma;
- a hidden distribution assumption is found;
- only finite computational evidence exists;
- a constructor is not polynomial-time or uses factor-dependent information.

### Pivot the research direction when

- a minimal counterexample invalidates the central construction;
- two independent repair attempts fail for the same structural reason;
- a lower bound shows the current family cannot reach the target complexity;
- the strongest publishable result is a barrier theorem or negative result.

A pivot is not failure. Record the evidence, revise the roadmap, and center the paper on the strongest correct contribution.

## 17. Success criteria

### Transformative success

A complete, independently reviewed classical algorithm factoring every input in `poly(log N)` bit operations, with no hidden assumptions.

### Major success

Any of:

- an unconditional deterministic exponent improvement over the verified state of the art;
- a rigorous number-field-sieve-type bound with materially reduced assumptions;
- a broad, explicit restricted-class polynomial-time theorem;
- a strong multi-group separation theorem;
- a substantive lower bound or impossibility result for a natural algorithm family.

### Valid publishable success

Any of:

- a corrected formalization exposing a previously overlooked gap;
- a useful restricted theorem;
- a reproducible counterexample corpus;
- a systematic experimental and theoretical evaluation that resolves a concrete research question;
- a negative result that redirects future work.

The project must optimize for truth, traceability, and durable contribution rather than for a predetermined positive conclusion.
