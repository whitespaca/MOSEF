# EXP-0017 - M18 arbitrary geometric-sum audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

Can the binary circuit disagree with the exact odd/even recurrences, violate
\((g-1)S_M(g)=g^M-1\), or produce a quotient-GCD result that fails the
unit-endpoint, proper-denominator, or full-public-exponent reduction? Any
such case is the null outcome.

## Registered commands

```text
python scripts/run_m18_geometric_sum_search.py \
  --exponent-max 64 --modulus-max 256 --base-max 32
python scripts/check_m18_geometric_sum_differential.py
```

The box and stopping rule were fixed before interpreting the registered full
output. The symbolic audit materializes every exponent from one through 64.
The modular audit uses every modulus from 4 through 256, every base from 0
through 32, and every exponent from one through 64 after classifying the
base GCD.

## Checks

- The exact even identity \(S_{2r}=S_r(1+X^r)\) and odd identity
  \(S_{2r+1}=S_{2r}+X^{2r}\) produce all-one coefficient vectors.
- Binary power and sum residues agree with direct modular evaluation.
- Every circuit satisfies \(E=DQ\bmod N\).
- Every unit-denominator division returns \(Q\), and the quotient and
  endpoint GCDs agree exactly.
- Every proper denominator is a direct factor exit; quotient factor values
  are allowed to differ.
- Every full denominator satisfies \(Q\equiv M\bmod N\), including repeated
  prime-power moduli, and quotient and public-exponent GCDs agree exactly.
- Six selected circuits are independently checked in Python, Rust, and C#.

## Result

The registered audit completed with no counterexample:

- 64 exact symbolic identities and 2,080 coefficient checks;
- 32 even and 31 odd non-base identities;
- 320,896 modular circuits;
- 1,323,696 binary-prefix composition steps;
- 320,896 endpoint/geometric-sum residue identities;
- 166,784 unit-denominator endpoint reductions;
- 134,272 proper-denominator factor exits;
- 19,840 full-denominator public-exponent reductions;
- zero unexplained reductions;
- 36,730 proper-denominator cases whose proper quotient GCD had a different
  value;
- 5,014 unit base prechecks, 3,021 proper nonunit base prechecks, and 314
  full nonunit base prechecks;
- 12 selected Python/Rust/C# comparisons.

Canonical summary SHA-256:

```text
0f182c819374451a3fd8d9ddb7ffc75580ac363186e19bd804eb28fe1371d2bd
```

## Interpretation boundary

The experiment audits finite arbitrary-exponent geometric sums only. It does
not prove the asymptotic theorem, establish a general rational/compositional
circuit lower bound, or support a population, density, recognition, novelty,
or general factoring inference. The \(M\) formal monomials belong to one
geometric-sum value and are not counted as \(M\) separately extracted GCD
tests.
