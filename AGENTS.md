# AGENTS.md — Classical Integer Factoring Research Repository

## Purpose

This repository is an autonomous, evidence-driven research program on classical algorithms for factoring an integer `N` in time polynomial in its input length `m = ceil(log2 N)`.

The goal is **not** to presume that a polynomial-time algorithm exists. The acceptable outcomes are:

1. a correct unconditional algorithm and proof;
2. a correct conditional theorem with every assumption explicit;
3. a rigorous algorithmic improvement for a restricted input class;
4. a lower bound, counterexample, or barrier result;
5. a reproducible negative result that eliminates a plausible approach.

## Mandatory instruction order

Before changing the repository:

1. Read this file completely.
2. Read `CODEX.md` completely. It is the project constitution and research specification.
3. Read `.agents/skills/factoring-research-autopilot/SKILL.md` and follow it for all research, proof, experiment, paper, and repository-maintenance work.
4. Read the current state files if present:
   - `research/ROADMAP.md`
   - `research/STATUS.md`
   - `research/CLAIMS.md`
   - `research/DECISIONS.md`
   - `research/BLOCKERS.md`
   - `research/NEGATIVE_RESULTS.md`
   - `paper/main.tex`
   - `paper/main-ko.tex` when present
5. Inspect `git status`, the current branch, recent commits, open worktrees, and available build tools.

If any required state file is absent, create it from the specifications in `CODEX.md` before substantive work.

## Autonomous operating policy

Work without requesting routine direction. Select the highest-priority unblocked item in `research/ROADMAP.md`, complete one bounded milestone, validate it, update the research record and paper, commit it, and then select the next milestone.

Ask for human action only when one of these conditions is unavoidable:

- credentials, repository permissions, or paid-service authorization are missing;
- a destructive or irreversible operation is required;
- a legal, licensing, privacy, or security decision cannot be resolved from repository policy;
- two repository instructions conflict materially;
- the requested action would require claiming an unproved theorem as proved.

Do not ask for preferences that can be resolved by the project constitution, existing code, literature, tests, or conservative defaults.

## Research integrity rules

These rules are absolute.

- Never describe the general classical polynomial-time factoring problem as solved unless a complete proof survives independent adversarial review and all dependencies are discharged.
- Never convert empirical success into a theorem.
- Never conceal a heuristic, conjecture, average-case assumption, GRH-type assumption, smoothness assumption, generic-group assumption, or unverified computational claim.
- Never fabricate a citation, DOI, arXiv identifier, theorem statement, quotation, benchmark, or experimental result.
- Never cite a source not actually inspected.
- Never use a theorem outside its hypotheses.
- Never silently weaken the definition of polynomial time. Complexity is measured in the bit length `m = ceil(log2 N)`, not in `N`.
- Track the bit length of exponents, generated objects, certificates, and intermediate values. A compact description is not sufficient if evaluation is superpolynomial.
- Treat proof search as falsification-first: search for counterexamples and hidden circularity before attempting polish.
- Preserve failed approaches in `research/NEGATIVE_RESULTS.md`; do not delete inconvenient evidence.

Every mathematical statement used in the paper must have one explicit status:

- `DEFINITION`
- `PROVED`
- `CONDITIONAL`
- `CONJECTURE`
- `HEURISTIC`
- `EMPIRICAL`
- `OPEN`
- `REFUTED`

Maintain the status and evidence link in `research/CLAIMS.md`.

## Repository update policy

At the start of each work cycle:

- preserve existing uncommitted user changes;
- do not overwrite files whose intent is unclear;
- create a dedicated branch named `research/YYYYMMDD-<short-topic>` when not already on a suitable research branch;
- never force-push, rewrite shared history, delete remote branches, or bypass protected-branch rules;
- keep commits small, coherent, and reproducible.

Commit prefixes:

- `research:` literature, claims, proofs, counterexamples
- `feat:` algorithm or tooling implementation
- `test:` validation and regression tests
- `exp:` experiment definitions or reproducible results
- `paper:` LaTeX manuscript changes
- `docs:` operational documentation
- `chore:` build and repository maintenance

After a validated milestone:

1. update `research/STATUS.md`;
2. update `research/CLAIMS.md` if any claim changed;
3. update `research/DECISIONS.md` for nontrivial design choices;
4. update `research/NEGATIVE_RESULTS.md` for failed hypotheses;
5. update the manuscript when the result affects the paper;
6. run the relevant quality gates;
7. commit with a precise message;
8. push if a configured remote, network access, and credentials permit;
9. create or update a draft pull request if `gh` is available and repository policy permits.

If push or PR creation is blocked, keep the local commit, record the exact blocker in `research/BLOCKERS.md`, and continue with work that does not require remote access.

## Expected repository layout

Create missing directories incrementally; do not scaffold unused code merely for appearance.

```text
.
├── AGENTS.md
├── CODEX.md
├── .agents/skills/factoring-research-autopilot/SKILL.md
├── research/
│   ├── ROADMAP.md
│   ├── STATUS.md
│   ├── CLAIMS.md
│   ├── DECISIONS.md
│   ├── BLOCKERS.md
│   ├── NEGATIVE_RESULTS.md
│   ├── literature/
│   ├── proofs/
│   └── experiments/
├── paper/
│   ├── main.tex
│   ├── main-ko.tex
│   ├── sections/
│   ├── figures/
│   ├── tables/
│   └── references.bib
├── crates/                 # Rust core and CLI
├── native/                 # C/C++ high-performance kernels
├── python/                 # Python reference implementations and search
├── orchestrator/           # TypeScript / Node.js 22 experiment control
├── analysis/               # R statistical analysis
├── verification/
│   ├── java/
│   └── csharp/
├── schemas/                # Cross-language result schemas
├── scripts/
├── tests/
└── artifacts/              # Small generated manifests; no large raw data
```

## Language responsibilities

Use the user's available stack deliberately.

- **Rust:** authoritative implementation of MOSEF/POSF candidates, exact arithmetic orchestration, product/remainder trees, batch GCD, deterministic experiment executables, and performance-critical safe code.
- **C/C++:** optional GMP/FLINT/NTL-backed kernels and independent performance comparison. Keep the FFI boundary minimal and tested.
- **Python 3:** mathematical reference implementation, property tests, counterexample search, symbolic or Sage-compatible notebooks/scripts, dataset generation, and differential testing.
- **TypeScript / Node.js 22:** experiment scheduling, manifests, process supervision, JSONL collection, dashboards/reports, and repository automation. Do not implement core big-integer number theory here unless needed for a small verifier.
- **R:** statistical analysis, confidence intervals, regression diagnostics, finite-size effects, and publication figures. Never use regression extrapolation as proof of asymptotic complexity.
- **Java and C#:** independent `BigInteger` verification of selected algorithms, certificates, and cross-language test vectors.
- **LaTeX:** publication manuscript. Use XeLaTeX or LuaLaTeX when Korean text is included.

Prefer the smallest set of languages needed for a milestone. Cross-language duplication is for independent verification, not for multiplying maintenance cost.

## Build and validation commands

Discover and use repository wrappers first. When the corresponding component exists, the default gates are:

```bash
# Rust
cargo fmt --all --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features

# Python
python -m pytest
python -m ruff check python tests
python -m mypy python

# Node.js 22 / TypeScript
npm ci
npm run lint
npm run typecheck
npm test
npm run build

# C/C++
cmake -S native -B build/native -DCMAKE_BUILD_TYPE=Release
cmake --build build/native --parallel
ctest --test-dir build/native --output-on-failure

# Java
./verification/java/gradlew -p verification/java test

# C#
dotnet test verification/csharp

# R
Rscript scripts/check-r-analysis.R

# Paper
latexmk -xelatex -interaction=nonstopmode -halt-on-error paper/main.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error paper/main-ko.tex
```

Do not install or add a production dependency merely to satisfy a preference. First determine whether the standard library or an existing dependency is sufficient. Record any added dependency and its license in `research/DECISIONS.md`.

## Testing requirements

- Use deterministic seeds and record them.
- Every bug fix needs a regression test.
- Every algorithm needs small exact test vectors, adversarial cases, perfect powers, repeated-prime cases, Carmichael numbers where relevant, and randomized property tests.
- Differentially compare Rust/C++ outputs against Python and at least one of Java or C# for selected vectors.
- Record toolchain versions, OS/architecture, Git commit, parameters, wall time, CPU time where available, peak memory where available, and output checksums.
- Never commit secrets, machine-specific credentials, or large generated datasets.
- Store large artifacts outside Git and commit only manifests, hashes, generation scripts, and retrieval instructions.

## Paper requirements

The manuscript is a continuous deliverable, not an end-stage summary.

- Maintain the full publication manuscript in English at `paper/main.tex`
  and a synchronized Korean companion manuscript at `paper/main-ko.tex`.
- Update both manuscripts whenever a milestone changes the title, abstract,
  contribution statement, claim statuses, current theorem or proof,
  limitations, conclusions, or reproduction record.
- Keep concise Korean progress summaries in `research/STATUS.md`.
- Every theorem must point to a proof file or a complete proof in the manuscript.
- Every experimental table or figure must point to a reproducible command, manifest, commit, and data hash.
- Separate unconditional results, conditional results, heuristics, and empirical findings into visibly distinct statements.
- Include negative results and limitations when they materially constrain the contribution.
- Compile both PDFs after manuscript changes and treat warnings about
  undefined references, citations, missing Korean glyphs, or hidden overfull
  content as failures.

## Definition of done for a milestone

A milestone is done only when:

1. its acceptance criteria are satisfied;
2. the relevant proof or code is present;
3. counterexample and edge-case checks were attempted;
4. validation commands pass, or failures are precisely documented as external blockers;
5. claims and assumptions are updated;
6. the manuscript or negative-results record is updated when applicable;
7. the work is committed;
8. the working tree contains no unexplained generated files.

## End-of-run report

At the end of each Codex execution, report only facts supported by the repository:

- milestone completed;
- files and claims changed;
- validation commands and outcomes;
- commit hash and push/PR state;
- unresolved blockers;
- the next highest-priority milestone.
