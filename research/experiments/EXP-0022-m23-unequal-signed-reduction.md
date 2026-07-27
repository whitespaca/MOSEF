# EXP-0022 - M23 unequal signed-reduction audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

For unequal \(A,B\), do the stage Bezout identity, total prefix reduction,
common-step difference factorization, endpoint polynomial GCDs, or
prime-power valuation formula fail? Can a proper normalized difference
escape both a proper common factor and the unit-common-factor cofactor path?
Any such case is the null outcome.

## Registered commands

```text
python scripts/run_m23_unequal_signed_reduction_search.py \
  --factor-max 8 --coefficient-max 2 --modulus-max 128 --base-max 16
python scripts/check_m23_unequal_signed_reduction_differential.py
```

The symbolic audit uses every ordered unequal pair \(2\le A,B\le8\) and
every nonzero coefficient pair in \([-2,2]^2\). The modular audit uses every
modulus from 4 through 128 and every unit base from 0 through 16. There is no
random seed.

## Checks

- Exact integer coefficients satisfy the Bezout and common-step identities.
- Fraction-based polynomial Euclid computation gives both endpoint GCDs.
- Boundary factors at zero and one agree with their coefficient conditions.
- Every signed evaluation follows the unit/proper/full prefix trichotomy.
- Every common stage divisor divides the public multiplier \(B\).
- Every prime-power component satisfies the capped valuation sum.
- Every proper difference follows a proper common factor or the unit-factor
  cofactor path.
- Six canonical vectors agree in Python, Rust, and C#.

## Result

The registered audit completed with no unexplained case:

- 42 ordered unequal factor pairs;
- 42 stage coprimality and Bezout checks, 42 common-step factorizations, and
  84 endpoint polynomial-GCD checks;
- 672 boundary-factor checks and 802 exact cofactor coefficients;
- 794,976 signed evaluations: 522,912 unit, 240,576 proper, and 31,488 full
  first-prefix branches;
- 49,686 difference and common-stage-divisor checks;
- 78,792 prime-power valuation checks;
- 11,256 proper differences: 3,408 through a proper common factor and 7,848
  through a cofactor under a unit common factor;
- 3,229 proper differences with both original stages units, split into 2,455
  common-factor and 774 cofactor paths;
- zero unexplained failures;
- 12 selected Python/Rust/C# comparisons.

Canonical summary SHA-256:

```text
88f103f7a18681abb357cccd4b77f0086f1a7bf165b5e31537c744a2c23d3e04
```

## Interpretation boundary

The experiment supports the exact DEF-023 implementation and demonstrates
both residual paths. It does not prove a distribution, success rate,
recognizer, universal schedule, classification of the surviving rational
residue, or a general classical factoring result.
