# EXP-0029: M30 compact support-signature audit

## Status

`EMPIRICAL`.

## Purpose

Falsify overly weak multi-candidate criteria, exhaustively validate the exact
signature collision formulas in a bounded box, and measure the canonical
compact prefix \(C_2,\ldots,C_m\) without treating finite evidence as an
asymptotic theorem.

## Deterministic command

```powershell
python scripts/run_m30_compact_support_signature_audit.py `
  --assignment-candidate-max 3 --assignment-population-max 5 `
  --input-length-min 9 --input-length-max 40 --pair-check-max 20
python scripts/check_m30_compact_support_signature_differential.py
```

No random seed is used.

## Registered result

The audit completed with zero failures and checked:

- 38,860 complete binary-signature assignments;
- 366,284 direct pair comparisons;
- 38,860 injectivity equivalences;
- 38,860 collision lower bounds and 38,860 coverage lower bounds;
- 12 exact tight collision-minimum instances;
- the materialized coverage counterexample
  \((z_1,z_2)=(15,7)\) on \(\{3,5,7\}\);
- 82,019 balanced primes at 32 input lengths;
- 2,978,644 M29-prefix signature coordinates;
- 2,034 explicitly enumerated balanced pairs;
- 530,378,607 total prefix pairs, of which 84,734 were separated and
  530,293,873 collided;
- 17 selected signatures and 34 Python/Rust/C# comparisons.

No canonical prefix \(C_2,\ldots,C_m\) was injective for any registered
\(9\le m\le40\). Sixteen lengths had only zero signatures:
\[
9,10,11,12,13,16,17,19,23,25,31,32,33,34,38,40.
\]
At \(m=40\), all 22,394 balanced primes had zero signature, so all
250,734,421 prime pairs collided. The best observed separation fraction
occurred at \(m=15\): 19 of 55 pairs.

Canonical summary SHA-256:

```text
74db38bf2f8ebeb088b3773fc1d94207cca0c1a73f7efb7a58a82f387dac5212
```

## Independent implementation

Python provides arbitrary-width signature accounting and the bounded audit.
Rust independently packs up to 64 compact \(\Phi_4\) coordinates in `u64`.
C# independently recomputes the same coordinates with `BigInteger`.
The registered JSON vectors include small-prime exceptions, generic hits and
misses, sparse level selections, long prefixes, and the endpoints of the
40-bit balanced population.

## Interpretation

The exhaustive abstract box supports BAR-024's exact combinatorial formulas;
it is not proof of the theorem, whose proof is in
`research/proofs/BAR-024-compact-support-signatures.md`.

The prefix result is a reproducible negative result for one specified
polynomial compact schedule only. It does not imply:

- noninjectivity beyond input length 40;
- noninjectivity for other bases, exceptional families, or parameter lists;
- an asymptotic density statement;
- a factorization-free injectivity recognizer;
- impossibility of all polynomial compact schedules;
- impossibility of general classical polynomial-time factoring.
