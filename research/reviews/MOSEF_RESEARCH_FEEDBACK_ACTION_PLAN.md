# MOSEF Research Feedback Action Plan

## 1. Original problems

The supplied review identified six publication risks:

1. readers could mistake MOSEF for a completed general factoring algorithm;
2. the M29--M46 history repeated a collision/repair chronology without one
   integrated view;
3. family-relative finite thresholds could be misread as minima over all
   selectors or as an asymptotic growth law;
4. `O(m^3 log m)` compact modular steps were too easy to read as a complete
   standard bit-operation analysis;
5. the certificate generator, semantic verifier, and minimal external trust
   base were not documented in one place;
6. numerical theorem/barrier counts in the title did not define a stable
   counting rule for the heterogeneous `THM-*` and `BAR-*` ledgers.

## 2. Applied changes

- The English and Korean titles no longer aggregate claims by a numerical
  theorem/barrier count.
- Both manuscripts state at the abstract, synthesis table, complexity
  section, limitations, and conclusion that:
  - MOSEF is a research program;
  - the strongest current selector result is a computer-assisted finite
    promise theorem for `DEF-032`;
  - \(L_m^\star\) is minimal only inside
    \(\mathcal T_{m,L}\);
  - the window is exactly \(9\le m\le34\);
  - no asymptotic injectivity, all-selector lower bound, or general classical
    polynomial-time factorization result follows.
- The M29--M46 presentation is organized around support-signature theory,
  selector construction, one integrated table, representative case studies,
  and a supplementary per-length audit trail.
- `scripts/generate_m50_finite_threshold_summary.py` creates a 26-row
  machine-readable artifact and both manuscript tables from the 16 M31--M46
  source schemas.
- `scripts/check_m50_finite_threshold_summary.py` provides a stdlib-only
  minimal checker for hashes, source projections, arithmetic, scope, and
  bilingual table synchronization.
- The complexity section separates descriptor generation, compact modular
  steps, modular arithmetic, GCDs, outputs, online public work, and offline
  proof generation. It gives a conservative standard bit-operation upper
  bound instead of calling `O(m^3 log m)` a bit bound.
- `research/CERTIFICATE_TRUST_MODEL.md` records generator/verifier roles,
  population reconstruction, branch-mask checks, injectivity and predecessor
  checks, cross-language overlap, and residual trust.
- `research/REPRODUCIBILITY.md` records fast integrity, semantic
  reconstruction, and complete repository gates.
- The related-work discussion distinguishes the present formalization,
  barriers, and finite certificates from Pollard-style `p-1`, Williams
  `p+1`, and general factoring breakthroughs.

## 3. Items deliberately unchanged

- No existing claim status was promoted, downgraded, or renumbered. The
  source proofs and registered schemas remain the evidence for
  `THM-004`--`THM-019`, `BAR-025`--`BAR-040`,
  `REF-027`--`REF-042`, and `EMP-030`--`EMP-045`.
- The detailed length-by-length audits were not deleted. They remain as a
  supplementary manuscript trail and in their proof, experiment, and schema
  files.
- The complete source schemas were not compacted or rewritten. M50 freezes
  their file hashes and projects only the review-facing fields.
- No uninspected literature or priority claim was added.
- Early milestones that did not separately prove minimum incremental-repair
  coordinate counts are marked `n.c.` rather than assigned inferred minima.

## 4. Additional mathematical research required

- No theorem currently gives injectivity for \(m>34\) in `DEF-032`.
- `BAR-041` rules out polynomial numeric caps in that exact family
  asymptotically, but not every public selector.
- `BAR-043` closes fixed linear spans only for the exact compact-gap family
  \(A=3,B_t=2^t+3,g=2\). Superlinear spans and other compact grammars remain
  open.
- The finite thresholds do not establish an asymptotic law, and fitting a
  regression to them would not prove one.
- Promise recognition for the balanced factor-dependent semiprime class is
  not supplied.
- A formal proof assistant or a genuinely independent full-population
  reimplementation would reduce implementation trust further.

## 5. Artifact verification status

The M50 consolidated artifact has schema version `1.0.0`, 26 rows, and 16
frozen source schemas. Its canonical summary SHA-256 is:

```text
1fb6185f73b4bc2243dc2f339c1e823d7c849acd7bf33ef5f288af4baa9d00b3
```

The minimal checker verifies the source-file hashes, source summary hashes,
row projections, finite arithmetic, explicit scope warning, and both table
fragments. Full semantic confidence still depends on running the registered
M31--M46 differential checkers.

## 6. Remaining publication risks

- The English manuscript is intentionally exhaustive. Even after structural
  synthesis, its supplementary audit and proof appendices remain long.
- The finite theorem is computer-assisted; a reviewer must choose between the
  quick source-schema trust path and the more expensive semantic reruns.
- Rust and C# cover selected arithmetic vectors, not every late
  full-population pair.
- The local trial-division population oracle is exact for the registered
  bounds but is not a polynomial-time online recognizer.
- Any future source-schema change invalidates the frozen M50 source hashes and
  requires regeneration plus review.
- The paper's novelty claim remains deliberately narrow: formal
  order-separation semantics, scoped barriers, exact finite certificates, and
  reproducible falsification rather than a general factoring breakthrough.
