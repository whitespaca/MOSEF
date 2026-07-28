# EXP-0030: M31 diversified compact-signature audit

## Status

`EMPIRICAL` for the complete registered range. The explicit certificates
used by THM-004 and BAR-025 are separately checked finite proof objects.

## Purpose

Construct the public selector containing both exceptional families with all
valid \(2\le A,B,g\le m\), normalize every charged primitive support
coordinate, find a finite restricted construction if present, and search
first for duplicate all-unit or nonzero signatures.

## Deterministic commands

```powershell
python scripts/run_m31_diversified_compact_signature_audit.py `
  --input-length-min 9 --input-length-max 20
python scripts/check_m31_diversified_compact_signature_differential.py
```

No random seed is used.

## Registered result

The audit completed with zero failures and checked:

- 12 input lengths and 166 balanced primes;
- 2,816 public descriptors;
- 63,953 local descriptor/prime exit profiles;
- 22,528 raw primitive coordinates;
- 152 distinct nonconstant normalized coordinates;
- 2,034 complete pair-normalization equivalences;
- 104 pairs in the seven injective construction certificates;
- 705 marginal pair separations attributable to genuinely new cofactor
  columns after direct exits;
- 72 selected Rust/C# command comparisons;
- 12 registered profile comparisons;
- 104 independent dense-certificate pair checks.

The selector is injective at every registered length \(9\le m\le15\). It is
noninjective at every registered length \(16\le m\le20\), with collision
counts \(3,2,10,55,105\), respectively. At \(m=16\), the exact collision
bucket is \(\{191,227,233\}\). At \(m=20\), one bucket contains 15 primes.

Canonical summary SHA-256:

```text
423a86409f38a4be1382e611ca94d3e2b08abfe7c1923133ab195db9c3716ae8
```

Certificate-vector SHA-256:

```text
f27e1681525d9c71f488c07457ed998cd43a8ea85ccac5b6e8e1b1e7227e93d0
```

## Independent implementations

Python constructs and normalizes the complete selector. Rust and C#
independently evaluate selected stage, bound, cyclotomic, cofactor, aggregate,
and resultant records; the differential checker reconstructs the eight-bit
primitive mask from each implementation. A separate dense verifier expands
the exact cofactor polynomial instead of using the compact recurrence, checks
all finite construction certificates, and verifies the complete \(m=16\)
collision descriptor by descriptor.

## Interpretation

The exact certificates prove a bounded promise-class construction for
\(9\le m\le15\) and a counterexample to this selector at \(m=16\). The
larger registered profile table remains finite evidence. Nothing here
establishes:

- injectivity or noninjectivity at untested lengths;
- a barrier for selectors with different polynomial ranges or formulas;
- a factorization-free recognizer for the balanced promise;
- an asymptotic density theorem;
- a lower bound for adaptive or \(N\)-dependent schedules;
- a general classical polynomial-time factoring algorithm or impossibility
  theorem.
