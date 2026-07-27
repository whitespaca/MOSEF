# EXP-0021 - M22 symmetric quotient-difference audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

For the symmetric depth-two difference
\[
D_A(X)=S_A(X^A)-S_A(X),
\]
does the exact factorization
\[
D_A(X)=X(X^{A-1}-1)H_A(X)
\]
ever fail, does compact cofactor evaluation disagree with explicit
evaluation, or can a proper difference GCD escape both a proper endpoint and
the unit-endpoint cofactor branch? Any such case is the null outcome.

## Registered commands

```text
python scripts/run_m22_symmetric_quotient_difference_search.py \
  --exponent-max 24 --modulus-max 128 --base-max 16
python scripts/check_m22_symmetric_quotient_difference_differential.py
```

The symbolic audit uses every \(2\le A\le24\). The modular audit uses every
modulus from 4 through 128, every unit base from 0 through 16, and the same
exponent range. There is no random seed.

## Checks

- Exact sparse coefficient dictionaries agree on both sides of BAR-017.
- Binary matrix powering agrees with explicit cofactor monomial evaluation.
- Every prime-power component of every modulus satisfies the capped valuation
  sum.
- Unit endpoints preserve the difference/cofactor GCD; full endpoints force a
  full difference.
- Every proper difference is classified through a proper endpoint or a
  proper cofactor under a unit endpoint.
- Six canonical vectors agree in Python, Rust, and C#.

## Result

The registered audit completed with no unexplained case:

- 23 symbolic exponents, 2,300 cofactor monomials, and 552 collected
  nonzero difference terms;
- 27,209 modular evaluations and 27,209 expanded-cofactor comparisons;
- 43,148 exact prime-power valuation checks;
- 11,553 unit, 10,477 proper, and 5,179 full endpoint cases;
- 10,238 proper differences: 9,758 through an already proper endpoint and
  480 through a proper cofactor under a unit endpoint;
- 4,770 proper differences with both original stage quotients units: 4,739
  endpoint paths and 31 cofactor paths;
- 6,042 full difference collisions;
- zero unexplained failures;
- 12 selected Python/Rust/C# comparisons.

The first unit-stage cofactor path is
\[
N=55,\quad g=2,\quad A=3.
\]
The stage quotients are \(7,18\), the endpoint \(3\) is a unit, and
\[
H_3(2)=1+2+2^3=11,
\]
so the difference has proper GCD \(11\). The named M21 witness
\((N,g,A)=(9,2,5)\) instead reduces through endpoint
\(2^4-1\equiv6\pmod9\), whose GCD is \(3\).

Canonical summary SHA-256:

```text
637cfa34b777126206b269d16c5a3afb027b9d893a2bea00881e85efea8d4fe6
```

## Interpretation boundary

The experiment supports the exact DEF-022 implementation and demonstrates
both branches. It does not prove a universal exponent family, an asymptotic
success rate, recognition of successful inputs, or a result for unequal
factors, arbitrary signed chains, or general arithmetic circuits.
