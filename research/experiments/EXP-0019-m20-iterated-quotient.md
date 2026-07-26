# EXP-0019 - M20 iterated geometric-quotient-chain audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

For public positive factors \(A_1,\ldots,A_r\) and prefix products
\(M_i=\prod_{j\le i}A_j\), can an exact stage identity
\[
S_{M_i}(X)=S_{M_{i-1}}(X)S_{A_i}(X^{M_{i-1}})
\]
fail, can a stage escape the charged prefix/composed denominator
trichotomies, or can a proper final quotient-product GCD occur without a
proper stage quotient GCD? Any such case is the null outcome.

## Registered commands

```text
python scripts/run_m20_iterated_quotient_search.py \
  --factor-max 5 --depth-max 3 --modulus-max 128 --base-max 16
python scripts/check_m20_iterated_quotient_differential.py
```

The exact audit materializes every factor tuple of depths one through three
with entries in \([1,5]\). The modular audit uses every modulus from 4
through 128 and every base from 0 through 16.

## Checks

- Exact coefficient multiplication verifies every stage certificate and the
  fully telescoped product certificate.
- Binary geometric-sum evaluators agree with direct modular evaluation at
  every prefix and stage.
- Consecutive stages link the previous prefix numerator to the next
  intermediate denominator.
- Rational and composed denominators independently take exactly one of the
  unit, proper-factor, or full-collision branches.
- A full rational prefix makes the stage quotient congruent to its public
  multiplier.
- A proper final quotient-product GCD implies a proper GCD at some explicit
  stage quotient.
- Six selected vectors, including factor one, repeated prefixes, proper and
  full collisions, and a unit final result, agree in Python, Rust, and C#.

## Result

The registered audit completed with no counterexample:

- 155 factor chains, 430 exact stage identities, 155 telescoped chain
  identities, and 5,190 coefficient checks;
- 190,805 modular chains, 529,330 stages, 338,525 prefix linkages, and
  1,249,465 residue identities;
- 419,780 unit, 93,455 proper, and 16,095 full rational-prefix cases;
- 238,240 unit, 202,600 proper, and 88,490 full composed-denominator cases;
- 68,260 proper final quotient products, all with a proper stage quotient;
- 12,203 cases where later multiplication masked an earlier proper stage
  success;
- 22,119 proper-prefix cases where the prefix and stage quotient exposed
  different proper divisor values;
- zero unexplained reductions;
- 1,231 unit and 894 nonunit base prechecks;
- 12 selected Python/Rust/C# comparisons.

Canonical summary SHA-256:

```text
06cbbb13eca00655d33da9858117de6920d1e63f6bbfe95794ec18642000f9da
```

## Interpretation boundary

This finite audit does not prove the asymptotic theorem or a lower bound for
general rational or arithmetic circuits. BAR-015 remains restricted to a
public geometric factor chain with explicit stage quotient outputs and
charged prefix/composed denominator exits. It does not cover addition or
subtraction between stages, arbitrary subset extraction, unrelated
denominators, adaptive factor-dependent computation, or other groups.
