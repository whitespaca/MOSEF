# EXP-0016 - M17 dyadic telescope audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

Can the dyadic exact-division/composition circuit violate its symbolic
telescoping identity, disagree between its unit-division and division-free
product paths, produce a proper quotient or numerator GCD without a proper
explicit component GCD, or mishandle a nonunit denominator? Any such case is
the null outcome.

## Registered commands

```text
python scripts/run_m17_dyadic_telescope_search.py \
  --level-max 10 --modulus-max 256 --base-max 32
python scripts/check_m17_dyadic_telescope_differential.py
```

The box and stopping rule were fixed before interpreting the registered full
output. The symbolic audit materializes levels zero through ten. The modular
audit uses every modulus from 4 through 256, every base from 0 through 32,
and every level from zero through ten after classifying the base GCD.

## Checks

- The exact product
  \(\prod_{j<t}(X^{2^j}+1)\) has all-one coefficients and exactly \(2^t\)
  monomials.
- Every repeated-squaring residue follows \(x_{j+1}=x_j^2\bmod N\).
- Every numerator satisfies \(E=DQ\bmod N\).
- Every unit-denominator division agrees with the division-free product.
- Every proper denominator is returned as a direct factor.
- Every full denominator is classified without attempting inversion.
- Every proper quotient GCD has a proper explicit dyadic-factor GCD.
- Every proper numerator GCD has a proper denominator or dyadic-factor GCD.
- Named unit, proper-denominator, full-denominator, and full-aggregation
  cases are retained as regression vectors.
- Six selected circuits are independently checked in Python, Rust, and C#.

## Result

The registered audit completed with no counterexample:

- 11 exact symbolic identities;
- 2,047 exact coefficient checks, with 1,024 monomials at level ten;
- 55,154 modular circuits;
- 275,770 repeated-squaring recurrence checks;
- 55,154 product identities;
- 28,666 valid modular divisions;
- 23,078 proper denominator factor exits;
- 3,410 full denominator collisions;
- 22,757 proper quotient implications;
- 25,430 proper numerator implications;
- zero unexplained proper successes;
- 3,073 full quotient collisions masking an explicit proper factor;
- 5,014 unit base prechecks, 3,021 proper nonunit base prechecks, and 314
  full nonunit base prechecks;
- 12 selected Python/Rust/C# comparisons.

Canonical summary SHA-256:

```text
1db5968e635901bc00eda0fdaa211aefe16af630741459eb9eb7f51ab50fc219
```

## Interpretation boundary

The experiment audits finite dyadic telescopes only. It does not prove the
asymptotic theorem, establish a general rational/compositional circuit lower
bound, or support a population, density, recognition, novelty, or general
factoring inference. The \(2^t\) materialized coefficients belong to one
geometric quotient and are not counted as \(2^t\) separately extracted GCD
tests.
