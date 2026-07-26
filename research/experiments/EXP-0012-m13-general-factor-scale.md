# EXP-0012 - M13 general factor-scale divisor audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

Does the exact DEF-013 small/large-prime split bound every divisor of an
arbitrary bounded exponent that is small enough to equal \(q-1\) or \(q+1\)?
The null outcome is any exponent, target cap, or threshold for which exact
divisor enumeration exceeds the registered bound.

## Registered commands

```text
python scripts/run_m13_general_factor_scale_search.py \
  --exponent-max 65536 --target-bit-max 14
python scripts/check_m13_general_factor_scale_differential.py
```

The box and stopping rule were fixed before interpreting the full output.
Every \(2\le d<2^{16}\) is factored exactly and all divisors are enumerated.
Target caps are \(2^b-1\) for even \(b=4,\ldots,14\), and the split thresholds
are \(2,3,5,11\).

## Checks

- Exact factor-scale divisor counts do not exceed DEF-013.
- Actual \(d\pm1\) prime hits do not exceed twice the divisor bound.
- Prime-power, squareful smooth, noninitial square-free, and mixed
  noninitial squareful exponents are recorded separately.
- Four exact split-bound vectors are checked in Python.
- Selected divisor counts, signatures, asymmetries, and hit counts are
  independently evaluated in Python, Rust, and C#.

## Result

The registered audit completed with no counterexample:

- 1,572,816 exact split-bound checks;
- 4,421,736 divisor-membership checks;
- 5,344,372 \(d\pm1\) prime-candidate checks;
- 32 selected cross-language comparisons;
- four Python-only exact split-bound records.

The smallest observed slack was zero at \(d=2\), target cap 15, and threshold
2, where the exact count and bound were both 2. The deliberately adversarial
family records also passed:

- \(2^{48}\): 15 relevant divisors, bound 49;
- \(2^{12}3^8 5^5 7^3\): 391 relevant divisors, bound 509,639;
- \(17\cdot19\cdot23\cdot29\cdot31\cdot37\): 33 relevant divisors, bound 64;
- \(2^4 11^5 17^3 43^2\): 67 relevant divisors, bound 5,065.

Canonical summary SHA-256:

```text
a564c00c8eaafad6f5be31d8705147578e6c86d9e6f42c6a9bacf3b0d93591d3
```

## Interpretation boundary

The experiment tests exact finite combinatorial premises and implementation
agreement. It does not prove BAR-008's asymptotic, construct a stipulated
prime population, estimate natural prime density, recognize a promise class,
establish novelty, or imply a general factoring lower bound.
