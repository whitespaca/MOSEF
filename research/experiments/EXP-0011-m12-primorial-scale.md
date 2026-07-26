# EXP-0011 - M12 factor-scale primorial audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question

Do bounded first-primes primorials satisfy the exact support/binomial premises
of BAR-007, and does the three-signature population formula agree with direct
pair enumeration?

## Registered command

```text
python scripts/run_m12_primorial_scale_search.py --primorial-count-max 18 --target-bit-max 20
python scripts/check_m12_primorial_scale_differential.py
```

The parameter box was fixed before interpreting the output. Primorials
through \(r=18\) are exhaustively enumerated. Target caps range through
\(2^{20}-1\). Balanced finite populations use primes in
\([\lceil2^{n-1/2}\rceil,2^n)\), so every product of two distinct members has
the common input length \(2n\); their schedule is \(P_{2n}\).

## Checks

- Every enumerated divisor below the target cap obeys the exact factorial
  support threshold.
- The number of such divisors obeys the registered binomial bound.
- Actual prime candidates \(d\pm1\) obey the twice-divisor candidate bound.
- All nonzero one-primorial signatures are disjoint channel signatures.
- The exact formula \(ab+z(a+b)\) agrees with direct pair enumeration in the
  registered direct-check range.
- Selected divisor counts, signatures, asymmetries, and hit counts agree
  across Python, Rust, and C#; four exact scale-bound records are checked in
  Python.

## Result

The exhaustive audit completed:

- 9,961,434 divisor-membership checks;
- 145,413 factor-support checks;
- 290,826 \(d\pm1\) prime-candidate checks;
- 16 balanced-population formula checks;
- 32 selected cross-language comparisons and four Python-only scale-bound
  checks.

At the largest divisor instance, \(r=18\) has \(2^{18}=262{,}144\) total
divisors, but only 7,074 divisors at most \(2^{20}\); the deliberately coarse
support/binomial upper bound is 106,762. In the largest balanced population,
22,394 primes produced 461 minus-channel hits, 447 plus-channel hits, 21,486
zero signatures, and 19,715,355 promised pairs out of 250,734,421 pairs.

Canonical summary SHA-256:

```text
bad46ee8f6638d98d19bc4479da998ea55af4d1617fef10cfc2c3ea973f39751
```

## Interpretation boundary

The experiment validates finite combinatorial premises and implementation
agreement. It does not prove the asymptotic bound, estimate natural prime
density, show a uniform prime-yield lower bound, construct or recognize the
stipulated populations, establish novelty, or imply a general factoring lower
bound.
