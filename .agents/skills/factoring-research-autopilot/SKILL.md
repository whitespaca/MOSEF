---
name: factoring-research-autopilot
description: Use when independently conducting the classical integer-factorization research program in this repository, including literature review, theorem or proof work, counterexample search, algorithm implementation, reproducible experiments, Git updates, or LaTeX paper drafting. Do not use for unrelated coding tasks or for a purely explanatory answer that does not modify this research repository.
---

# Factoring Research Autopilot

## Objective

Advance the repository by one or more bounded, validated research milestones while preserving mathematical integrity, reproducibility, and Git traceability.

Treat general classical polynomial-time factoring as an open target. Never assume the universal POSF/MOSEF conjecture. Prefer falsification, exact statements, and independently checkable artifacts.

## Required context

Read in this order:

1. repository `AGENTS.md`;
2. repository `CODEX.md`;
3. `research/ROADMAP.md`;
4. `research/STATUS.md`;
5. `research/CLAIMS.md`;
6. `research/DECISIONS.md`;
7. `research/BLOCKERS.md` and `research/NEGATIVE_RESULTS.md`;
8. relevant source, proof, experiment, and paper files;
9. current Git status and recent history.

If state files are missing, initialize the minimum viable research state before starting a novel task.

## Operating loop

Repeat the following loop while the execution environment remains available and no stop condition is reached.

### 1. Preflight

- Confirm repository root, branch, worktree, remotes, and uncommitted changes.
- Preserve user changes and avoid unrelated formatting churn.
- Determine available compilers, package managers, LaTeX engine, GitHub CLI, and web/literature access.
- Read the active milestone and select the highest-priority unblocked acceptance criterion.
- Write or update a short executable plan in `research/STATUS.md` or the active roadmap entry.

### 2. Establish the evidence target

State the intended output before editing:

- claim ID or research question;
- expected artifact;
- acceptance criteria;
- falsification test;
- validation commands;
- paper section affected.

Do not begin an open-ended implementation without a concrete research question.

### 3. Choose the appropriate workflow

Use one or more of the workflows below. Keep independent tasks isolated when subagents or worktrees are available.

## Literature workflow

1. Search primary and authoritative sources.
2. Prefer final papers, official proceedings, author manuscripts, arXiv versions, and official software documentation.
3. Verify title, authors, date, version, identifier, theorem hypotheses, and complexity model.
4. Create or update a source note under `research/literature/`.
5. Add a validated BibTeX entry only after inspecting the source.
6. Map each imported result to a claim ID and exact use in the repository.
7. Record unresolved discrepancies between versions.
8. Update the state-of-the-art section of the paper only after comparison across sources.

When web access is unavailable, do not invent missing metadata. Mark the item `UNVERIFIED_SOURCE`, continue with offline work, and add an explicit blocker.

## Theorem and proof workflow

1. Allocate a stable claim ID.
2. Write the exact quantified statement and classify it provisionally.
3. List all assumptions and imported lemmas.
4. Check for circular access to unknown factors.
5. Expand all input-size and bit-complexity calculations.
6. Build an independent small-case search for counterexamples.
7. Test adversarial and boundary cases.
8. Write the proof attempt under `research/proofs/<claim-id>.md`.
9. Run an independent adversarial review. When subagents are available, assign a separate reviewer whose prompt is to refute the claim and who does not rely on the author's summary.
10. Resolve every review item or downgrade the claim.
11. Update `research/CLAIMS.md`.
12. Incorporate the result into the paper only after status and evidence agree.

Never promote a claim directly from `CONJECTURE` or `EMPIRICAL` to `PROVED` without an adversarial review pass.

## Counterexample workflow

1. Define the candidate statement precisely.
2. Identify the smallest parameter space likely to expose failure.
3. Implement at least one simple exact search oracle, preferably in Python.
4. Validate the oracle against hand-computed vectors and an independent language implementation when practical.
5. Use deterministic enumeration before random search when feasible.
6. Record seeds, bounds, pruning, environment, and commit.
7. Minimize any counterexample.
8. Add a regression test.
9. Reclassify the claim as `REFUTED` or restrict it precisely.
10. Document the result in `research/NEGATIVE_RESULTS.md` and the paper if scientifically material.

## Algorithm implementation workflow

1. Start with executable pseudocode and a Python reference implementation.
2. Define input/output and failure behavior, including prime powers and noninvertible group operations.
3. Create canonical test vectors.
4. Implement the authoritative version in Rust.
5. Add C/C++ only for justified kernels or comparison.
6. Add Java or C# verification for selected outputs or certificates.
7. Add deterministic CLI and machine-readable result output.
8. Run unit, property, differential, integration, and adversarial tests.
9. Profile only after correctness gates pass.
10. Record complexity-relevant operation counts separately from wall time.

## Experiment workflow

1. Create an experiment ID and immutable manifest.
2. Define the hypothesis, null outcome, input distribution, sample size, and stopping rule before running.
3. Pin seeds and toolchains.
4. Build release binaries and capture the Git commit.
5. Run a smoke test on tiny inputs.
6. Run the registered experiment through the TypeScript orchestrator when present.
7. Validate output against the versioned schema.
8. Store raw output outside Git when large; commit hashes and manifests.
9. Analyze with scripted R code and record confidence intervals and diagnostics.
10. Generate figures and tables from manifests, never by manual editing.
11. State the result as empirical only.
12. Update the paper's reproduction appendix.

Stop an experiment early only under the preregistered rule or for a documented technical failure. Do not discard inconvenient runs.

## Paper workflow

1. Compile the current paper before editing to establish a baseline.
2. Update only sections supported by changed evidence.
3. Keep title, abstract, contributions, theorem statements, limitations, tables, and claims ledger synchronized.
4. Trace every table and figure to an experiment ID.
5. Trace every external technical statement to a verified source.
6. Use complete proofs in the main text or appendices; do not replace proof gaps with “clearly” or “standard” without a valid citation.
7. Run spelling/style checks if configured.
8. Compile with `latexmk -xelatex -interaction=nonstopmode -halt-on-error paper/main.tex`.
9. Treat undefined references, undefined citations, and overfull content that hides text as failures.
10. Inspect the generated PDF for malformed mathematics, tables, and figures.

## Git workflow

1. Work on a dedicated research branch unless repository policy already provides an isolated worktree.
2. Make minimal, coherent changes.
3. Run relevant quality gates before committing.
4. Review `git diff --check` and the complete staged diff.
5. Update research state and paper before the commit.
6. Commit with the repository prefixes defined in `AGENTS.md`.
7. Push when remote access and credentials permit.
8. Create or update a draft PR with:
   - research question;
   - verified result;
   - claim-status changes;
   - reproduction commands;
   - known limitations;
   - review requests focused on proof and reproducibility.
9. Never force-push or bypass branch protection.

## Optional subagent roles

When supported, use separate contexts for independent work:

- **Literature auditor:** verifies primary sources and theorem hypotheses.
- **Proof author:** develops the candidate proof.
- **Adversarial mathematician:** attempts to refute the claim and finds hidden assumptions.
- **Systems implementer:** writes the reference and optimized algorithms.
- **Reproducibility reviewer:** reruns commands from a clean checkout and validates paper traceability.

Do not accept majority vote as proof. Resolve disagreements by explicit mathematics, tests, or source evidence.

## Task selection policy

Choose work by this priority:

1. correct an overclaim or false result;
2. unblock repository reproducibility;
3. resolve the active proof gap or counterexample search;
4. complete the current milestone;
5. strengthen tests and independent verification;
6. synchronize the paper;
7. optimize a measured bottleneck;
8. begin a new hypothesis.

## Stop conditions

Stop the autonomous loop, leave the repository safe, and record a blocker when:

- credentials or permissions are essential and unavailable;
- a destructive operation would be required;
- literature needed for a claim cannot be inspected;
- a merge conflict or repository corruption cannot be resolved conservatively;
- the next step would require paid resources or unauthorized external computation;
- the only way to proceed is to misclassify an unproved statement.

A failed conjecture is not a stop condition. Minimize the counterexample, update the paper, revise the roadmap, and continue with the strongest surviving question.

## Completion checklist

Before ending an execution:

- [ ] Active acceptance criterion is complete or precisely blocked.
- [ ] Claims ledger matches the evidence.
- [ ] Negative results and decisions are recorded.
- [ ] Relevant tests and builds pass.
- [ ] Paper compiles if changed.
- [ ] Reproduction commands are documented.
- [ ] Diff is reviewed and committed.
- [ ] Push/PR state is recorded.
- [ ] `research/STATUS.md` states the next action.

Return a concise factual report with milestone, claims, validation, commit, remote state, blockers, and next action.
