# EXP-0046: M47 polynomial-cap support-budget audit

## Status

`EMPIRICAL` for the bounded materializations and independent implementation
checks. The asymptotic obstruction is the proof of `BAR-041`, not an
extrapolation from these finite records.

## Deterministic commands

```powershell
python scripts/run_m47_polynomial_cap_support_audit.py
python scripts/generate_m47_polynomial_cap_support_schema.py
python scripts/check_m47_polynomial_cap_support_differential.py
```

No random seed is used.

## Registered checks

The primary audit materializes all eight positive primitive integers for
every DEF-032 descriptor at caps 9, 12, 16, and 20. It checks the exact
cyclotomic division, per-descriptor bound, aggregate selector bound, and the
Rosser--Schoenfeld constant comparison. The four profiles contain 963
descriptor records and 7,704 exact primitive-value checks.

The independent verifier reconstructs the two geometric sums by direct
summation, evaluates the dense cofactor polynomial, independently computes
the resultant formulas, and compares every value. It then checks 25,346
branch-total support masks over every cap-20 descriptor and every prime at
most 199, including nonunit-base cases. An independent sieve verifies the
balanced-population lower inequality at all 31 lengths from 10 through 40.

The exact cap profiles are:

| cap | descriptors | exact output bits | uniform upper bound |
|---:|---:|---:|---:|
| 9 | 32 | 3,948 | 742,400 |
| 12 | 110 | 26,076 | 3,303,542 |
| 16 | 270 | 115,600 | 18,157,500 |
| 20 | 551 | 377,063 | 56,929,700 |

Canonical summary SHA-256:

```text
b9c97e8161d3470ad61d20fd9ee8834888e5f0139e1b3fd5b3fbe3b2a6463093
```

Registered schema SHA-256:

```text
a37f9d495de85943a69a6c3fbc122c9f09fbce0f78316c32163c380a782ef525
```

## Interpretation

The bounded checks validate the exact-lift mapping and conservative bit
formula used by the proof. They do not establish asymptotic noninjectivity
by regression or finite pattern continuation. BAR-041 instead combines the
proved symbolic \(O(L^5\log L)\) output budget with the inspected explicit
prime-counting inequalities. The result remains limited to polynomial
numeric caps in DEF-032.
