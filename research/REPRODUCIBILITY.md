# Reproducibility Guide

## Reproduction levels

The repository exposes three review levels. They answer different questions
and must not be conflated.

### Level A: publication and artifact integrity

This level is fast. It checks that the claims ledger, English manuscript,
Korean manuscript, registered source hashes, consolidated finite table, and
generated table fragments agree.

```powershell
python scripts/validate_foundation.py
python scripts/generate_korean_claim_appendix.py --check
python scripts/generate_m50_finite_threshold_summary.py --check
python scripts/check_m50_finite_threshold_summary.py
python scripts/check_m84_promise_wrappers.py
python scripts/check_m87_focused_papers.py
python scripts/check_m88_reader_labels.py
python scripts/check_m89_appendix_boundaries.py
python scripts/check_m90_finite_chronology.py
python scripts/check_publication.py
```

Passing Level A does not recompute the large finite certificates.

### Level B: selected semantic reconstruction

Run the differential checker for the result under review. The final
finite-threshold row and the current asymptotic barriers are checked with:

```powershell
python scripts/check_m46_length_34_cap_differential.py
python scripts/check_m47_polynomial_cap_support_differential.py
python scripts/check_m48_compact_gap_overlap_differential.py
python scripts/check_m49_wide_span_compact_gap_differential.py
python scripts/check_m51_subquadratic_span_differential.py
python scripts/check_m52_boundary_constant_differential.py
python scripts/check_m53_distinct_gap_differential.py
python scripts/check_m54_realizable_gap_differential.py
python scripts/check_m55_overlap_gcd_differential.py
python scripts/check_m56_dense_prefix_differential.py
python scripts/check_m57_endpoint_zero_slack_differential.py
python scripts/check_m58_overlap_prime_order_differential.py
python scripts/check_m59_half_order_size_differential.py
python scripts/check_m60_m80_synthesis_differential.py
python scripts/check_m84_promise_wrappers.py
python scripts/check_m85_m41_semantic_certificate.py
python scripts/check_m86_m46_streaming_certificate.py
python scripts/check_m87_focused_papers.py
python scripts/check_m88_reader_labels.py
python scripts/check_m89_appendix_boundaries.py
python scripts/check_m90_finite_chronology.py
python -m unittest discover -s tests -p test_promise_wrappers.py
python -m pytest tests/test_m85_semantic_certificate.py -q
python -m pytest tests/test_m86_streaming_semantic_certificate.py -q
pytest -p no:cacheprovider tests/test_m87_focused_papers.py -q
pytest -p no:cacheprovider tests/test_m88_reader_labels.py -q
pytest -p no:cacheprovider tests/test_m89_appendix_boundaries.py -q
pytest -p no:cacheprovider tests/test_m90_finite_chronology.py -q
```

These commands recompute registered masks, identities, collision or
construction certificates, and selected Rust/C# protocol vectors. Each
matching experiment record under `research/experiments/` states its exact
finite bounds and canonical hash.

The M85 command is the clean-room option for the M41 row. It uses only the
standard library, reconstructs all 685 balanced primes and 1,528 certificate
coordinates, verifies the exact cap-102 collision and cap-103 injectivity,
and imports no generator or project number-theory module. Its mutation suite
rehashes altered artifacts before selected negative checks, so passing is not
equivalent to trusting the legacy SHA-256.

The M86 command is the streaming clean-room option for the final M46 row. It
reconstructs all 3,299 balanced primes and streams 10,880,102 certificate
evaluations into 3,299 packed signatures, verifies the exact cap-200 collision
and cap-201 unique repair, and imports no project code. It does not retain a
prime-by-coordinate matrix or either complete descriptor set.

The M87 commands are editorial integrity checks rather than semantic
certificate reconstruction. They enforce one four-row cost ledger before
section 1 of each focused manuscript, a reproducible 200--300 lexical-token
abstract interval, and exact bilingual parity for the 21 representative claim
IDs and statuses.

The M88 commands validate the reader-facing layer over those same claims.
They require one compact heading per claim, exactly five localized label
families in each language, stable claim order, visible `PROVED` metadata, and
the exact 21-ID bilingual map. Passing does not promote a claim or create a
second numbering authority.

The M89 commands validate the boundary between mathematical narrative and
repository audit material. They fix the order of 34 main sections, require 12
labeled appendices, and preserve exact bilingual registries containing 32
commands, 38 repository paths, and 14 inspected-source anchors. They also
reject commands, paths, experiment IDs, hashes, and internal milestone tokens
in the main body. Passing is an editorial integrity result; it neither
recomputes a mathematical certificate nor changes a claim status.

The M90 commands validate the finite-paper chronology split. They require
five exact representative cases and seven focused `PROVED` claims in each
main narrative, place the generated full table only in the reproduction
appendix, and compare both 26-row rendered tables plus the frozen M50 JSON
against a hard-coded semantic registry. Passing preserves the finite evidence
but does not independently recompute every row's modular signatures.

### Level C: complete repository gate

Use the available Windows toolchains:

```powershell
python -m unittest discover -s tests
python -m compileall python scripts tests
ruff check python scripts tests
mypy python
cargo fmt --all --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
dotnet build verification/csharp/MosefVerifier.csproj --configuration Release --nologo
latexmk -xelatex -interaction=nonstopmode -halt-on-error paper/main.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error paper/main-ko.tex
```

The paper builds must also be checked for undefined citations/references,
missing Korean glyphs, and overfull content that hides text. Generated PDFs
are ignored build products; stable hashes are recorded only after successful
visual inspection.

## M50 finite-threshold artifact

The single machine-readable source for the integrated \(m=9,\ldots,34\)
publication table is:

```text
schemas/m50-finite-threshold-summary-v1.json
```

It is generated from 16 registered M31--M46 schemas and contains 26 rows.
Its canonical summary SHA-256 is:

```text
1fb6185f73b4bc2243dc2f339c1e823d7c849acd7bf33ef5f288af4baa9d00b3
```

The artifact records each source-file SHA-256 and the source snapshot commit.
Its `scope` field is normative: the rows are complete only for the finite
balanced populations and the exact `DEF-032` selector family. They do not
encode an asymptotic rate or a general factoring complexity.

Regenerate and verify with:

```powershell
python scripts/generate_m50_finite_threshold_summary.py
python scripts/check_m50_finite_threshold_summary.py
git diff --exit-code -- schemas/m50-finite-threshold-summary-v1.json paper/tables
```

The last command is optional after a clean checkout; it demonstrates that
regeneration did not change the registered artifact.

## Authoritative versus generated files

Authoritative mathematical sources:

- `research/CLAIMS.md`;
- `research/proofs/`;
- immutable registered schemas under `schemas/`;
- experiment records under `research/experiments/`.

Generated publication files:

- `paper/claim-status-ko.tex`, from
  `scripts/generate_korean_claim_appendix.py`;
- `paper/tables/finite-threshold-summary-en.tex`;
- `paper/tables/finite-threshold-summary-ko.tex`;
- `schemas/m50-finite-threshold-summary-v1.json`.

Modify generators or authoritative sources. Do not hand-edit generated
tables or the Korean claim appendix.

## Determinism and environment

The M31--M49 and M51--M58 searches are deterministic finite enumerations and
record no random seed. Source schemas use sorted JSON serialization and
canonical SHA-256 values. Wall time can vary; mathematical rows and hashes
must not.

The repository baseline is Windows/PowerShell, Python 3.12, Rust/Cargo,
.NET, and MiKTeX XeLaTeX. Exact tool versions and host details for the latest
validated run are recorded in `research/STATUS.md`. Tool availability is not
evidence of successful validation; only commands actually reported as passed
count.

## Failure interpretation

- A source-file hash mismatch means the consolidated artifact must be
  regenerated and reviewed; it does not by itself refute a theorem.
- A semantic mask, collision, or injectivity mismatch invalidates the
  affected finite certificate until resolved.
- A Rust/C# vector mismatch shows implementation disagreement on the selected
  overlap and blocks publication, even if the Python certificate still
  passes.
- A manuscript mismatch blocks publication but does not change claim status.
- No finite pass supports a conclusion for \(m>34\).

The detailed trust assumptions and the distinction between minimal and full
checking are in `research/CERTIFICATE_TRUST_MODEL.md`.
