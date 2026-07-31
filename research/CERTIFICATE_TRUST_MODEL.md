# Certificate Trust Model

## Scope

This document describes what a reviewer must trust to check the
computer-assisted finite promise theorem for the exact public selector family
\(\mathcal T_{m,L}\) (`DEF-032`) on the complete balanced-prime populations
for \(9\le m\le34\). It does not turn the finite certificate into an
asymptotic theorem, a promise recognizer, an all-selector lower bound, or a
general factoring result.

The authoritative mathematical statements and scopes remain
`research/CLAIMS.md` and the proof files for `THM-004`--`THM-019` and
`BAR-025`--`BAR-040`. The consolidated M50 artifact is a publication and
review index over those existing records, not a new proof.

## Artifact layers

### Layer 1: immutable registered source schemas

The M31--M46 schemas record:

- the schema version used by that milestone;
- the complete balanced population or its construction certificate;
- the public cap and descriptor family;
- primitive branch-total masks or selected primitive vectors;
- injective restricted signatures at the certified cap;
- collision buckets at the predecessor or inherited failed cap;
- transition or incremental-repair data where that quantity was separately
  certified;
- an embedded canonical summary SHA-256 when the milestone schema defines
  one.

The exact source paths and their file SHA-256 values are frozen in
`schemas/m50-finite-threshold-summary-v1.json`. The source snapshot is
commit `e286a0042ca2cda57fdc31e143ecc65605ea57fd`.

### Layer 2: generator and semantic verifier

For a typical later finite threshold, such as M46:

- `scripts/run_m46_length_34_cap_audit.py` constructs the complete population,
  public profiles, transition, predecessor collision, repair profile, and
  construction certificate;
- `scripts/generate_m46_length_34_cap_schema.py` serializes that deterministic
  result and selected primitive-exit vectors;
- `scripts/check_m46_length_34_cap_differential.py` recomputes the canonical
  summary hash, selected primitive masks, public-cap collisions, transition
  masks, construction signatures, predecessor bucket, and repair coordinate.

Earlier M31--M45 records use the corresponding numbered audit, generator, and
differential checker. The M50 consolidated generator does not replace these
semantic verifiers.

### Layer 3: publication projection

`scripts/generate_m50_finite_threshold_summary.py` reads the 16 registered
M31--M46 schemas and creates:

- `schemas/m50-finite-threshold-summary-v1.json`;
- `paper/tables/finite-threshold-summary-en.tex`;
- `paper/tables/finite-threshold-summary-ko.tex`.

The two manuscript tables therefore come from the same 26 machine-readable
rows. No threshold, population count, predecessor bucket, or incremental
repair minimum is copied into either paper by hand.

## Minimal checker path

An external reviewer who does not want to rerun the large population audits
can run:

```powershell
python scripts/check_m50_finite_threshold_summary.py
python scripts/generate_m50_finite_threshold_summary.py --check
python scripts/check_publication.py
```

The first command uses only the Python standard library. It verifies:

1. M50 schema version `1.0.0`;
2. the frozen source-snapshot commit;
3. the M50 canonical summary SHA-256;
4. exactly 16 distinct source schemas and all source-file SHA-256 values;
5. the embedded source summary hashes;
6. exact coverage of \(m=9,\ldots,34\);
7. projection of population size, family-relative cap, predecessor collision
   buckets, and separately certified incremental-repair minima from each
   source schema;
8. local-offset arithmetic and both unreduced and reduced strict endpoints;
9. presence of every row and evidence ID in both generated paper tables;
10. the explicit finite/family-relative scope warning.

This minimal path verifies integrity and projection. It trusts the registered
source schemas and does not independently prove primality, population
completeness, descriptor semantics, or signature injectivity.

## Independent M41 semantic path

M85 adds a smaller but deeper path for the representative \(m=29\) row:

```powershell
python scripts/check_m85_m41_semantic_certificate.py
python -m pytest tests/test_m85_semantic_certificate.py -q
```

The 548-line checker uses only the Python standard library and imports no
generator, reference implementation, or prior checker. It independently:

1. sieves the exact balanced interval and reconstructs all 685 primes;
2. parses and validates every registered source against the public
   order-four/order-six descriptor grammar;
3. reconstructs geometric stages and resultants from their formulas;
4. evaluates the cofactor by finite-field division away from a cyclotomic
   root, while a separate small exact-quotient test checks the differentiated
   polynomial identity at a simple root;
5. recomputes all 1,528 certificate coordinates and packed signatures;
6. checks injectivity on all 234,270 population pairs;
7. checks all 89,789 cap-102 descriptors on the predecessor pair;
8. checks all 47,912 newly admitted cap-103 primitive coordinates and the
   unique one-coordinate repair; and
9. reconstructs descriptor and raw-coordinate counts at caps 102, 103, 105,
   and 108.

The M41 subcertificate has exactly one duplicate bucket,
\(\{18979,21031\}\). The full raw predecessor check proves that this pair
really collides in every cap-102 coordinate. The final source
`phi4:87:95:103:cofactor` has pattern \((0,1)\), and the complete
1,528-coordinate sublist is injective.

The M41 certificate itself never reaches a cyclotomic root: its primes exceed
16,000, its bases are at most 103, and both positive cyclotomic values are
therefore strictly below the prime. Its cofactor evidence relies on the
unit-division reconstruction. The derivative branch is a separately tested
totality boundary, not registered M41 root-case evidence.

The checker recomputes the legacy embedded summary hash, but acceptance is not
hash-only: rehashed population, descriptor, and primitive-vector mutations
are rejected semantically, and a packed-signature mutation is rejected
against fresh residues. The legacy M41 hash excludes four primitive vectors
that were appended after the summary was hashed; those vectors are checked
directly instead.

M41 was selected over M46 for the minimal path. It exercises population
completeness, descriptor semantics, a predecessor collision, unique repair,
and a nonmonotone threshold with roughly 1.05 million certificate evaluations.
The M46 construction alone would require roughly 10.88 million. This is a
bounded review-engineering decision, not a mathematical preference for the
length-29 theorem.

## Full semantic path

To reduce trust in the registered schemas, run the corresponding M31--M46
generator and differential checker. For example, the final row is rebuilt
and checked by:

```powershell
python scripts/generate_m46_length_34_cap_schema.py
python scripts/check_m46_length_34_cap_differential.py
```

The generator reconstructs
\(\mathcal P_m=\{p\text{ prime}:2^{m-1}\le p^2<2^m\}\) using the exact
bounded validation oracle in
`python/mosef_reference/length_indexed_cofactor_schedule.py`. That oracle
uses trial division and is intentionally a finite proof tool, not a
polynomial-time population recognizer.

The full per-milestone checker verifies the public descriptor data and
recomputes:

- population membership through the deterministic generator;
- public parameter enumeration;
- branch-total primitive masks;
- the injective construction signature;
- the predecessor collision partition or bucket;
- transition and incremental-repair claims when registered;
- selected dense and cross-language vectors.

The exact commands for every source row are listed in the matching
`research/experiments/EXP-0030`--`EXP-0045` record.

M85 does not replace those paths for the other 25 rows. It supplies a
clean-room semantic reconstruction for M41 and an executable template for
reducing the trusted computing base of additional rows.

## What the language implementations share

The implementation evidence is deliberately layered, but it is not described
as three fully clean-room proofs.

- Python is the arbitrary-precision semantic implementation and produces the
  complete finite certificates.
- The later Python differential checkers contain a separately written direct
  mask formula and reuse selected descriptor/protocol helpers from earlier
  milestones. They independently recompute masks and signatures but share the
  public descriptor specification and some serialization code.
- Rust implements the selected bounded integer protocol and modular
  operations independently for registered vectors.
- C# uses `BigInteger` and independently evaluates the same selected protocol
  vectors.
- Rust and C# do not enumerate every M44--M46 population pair. Their role is
  selected arithmetic and branch reconstruction; the complete pair audit is
  performed by the Python certificate checker.

Agreement on selected vectors detects implementation drift. It is not an
independent formal proof of the entire finite theorem.

## Online and offline boundary

The online public evaluator receives \(m\), \(N\), and the public cap formula.
It constructs descriptors without knowing \(p\), \(q\), their orders, or any
support signature; evaluates compact residues modulo \(N\); computes every
charged GCD; and extracts a factor when a GCD is proper.

The offline certificate procedure enumerates the finite prime population,
normalizes analytical support columns, expands dense values where requested,
searches caps, selects certificate columns, counts every pair, and serializes
hashes. None of these offline objects is an online input or a promise
recognizer.

## Residual trust and review limits

The minimal path still trusts:

- Python and its standard JSON/SHA-256 implementations;
- the small M50 checker itself;
- the 16 source schemas and their source snapshot;
- the mathematical interpretation connecting support-signature injectivity to
  semiprime separation (`BAR-024`).

The independent M41 path instead trusts:

- Python's standard integer, sieve, JSON, and SHA-256 operations;
- the 548-line checker and the public polynomial identities it implements;
- the registered list of certificate source strings as a candidate
  subcertificate, whose legality and semantics are recomputed; and
- `BAR-024` for the final support-signature-to-GCD implication.

It does not reconstruct the generator's greedy source-selection process or
the complete 1,555-column normalized basis. Neither is needed to validate a
legal separating sublist and the exact predecessor collision.

The full path additionally trusts the operating system and language
toolchains, and it remains a computer-assisted finite proof. A reviewer
seeking less implementation trust should reconstruct selected rows from the
proof definitions or port the complete population audit to an independently
designed implementation.
