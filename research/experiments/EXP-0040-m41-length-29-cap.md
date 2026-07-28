# EXP-0040: M41 length-29 cap audit

## Status

`EMPIRICAL` for the registered raw-prefix and full normalized computations.
The complete collision and construction certificates promoted to BAR-035
and THM-014 are finite proof objects.

## Deterministic commands

```powershell
python scripts/run_m41_length_29_cap_audit.py
python scripts/generate_m41_length_29_cap_schema.py
python scripts/check_m41_length_29_cap_differential.py
```

No random seed is used.

## Registered result

At \(m=29\), \(m+76\) gives cap 105 and
\(\lceil26m/7\rceil\) gives cap 108. Both are injective on all 685
balanced primes. Exact adjacent profiles show that cap 102 has the sole
collision \(\{18979,21031\}\), while cap 103 is injective. The exact
threshold is therefore \(L_{29}^{\star}=103\). Among all coordinates added
at cap 103, only `phi4:87:95:103:cofactor` distinguishes the predecessor
pair. It appends the pattern \((0,1)\) to 1,527 old representative columns,
completing a 1,528-coordinate injective certificate. The audit checked:

- four complete lossless raw-prefix profiles at caps 102, 103, 105, and 108;
- 685 balanced primes and 234,270 unordered pairs;
- 109,782 maximum-cap descriptors and 75,200,670 raw-prefix local exits;
- one cap-103 normalized profile with 95,778 descriptors and 65,607,930
  local exits;
- 766,224 raw and 1,555 normalized cap-103 coordinates;
- 234,270 raw-versus-normalized pair equivalences;
- 5,989 new cap-103 descriptors and 11,978 tracked-pair local exits;
- 47,912 new primitive-coordinate checks and one distinguishing coordinate;
- 1,528 construction coordinates and 234,270 certificate pairs;
- 16 selected Rust/C# command comparisons and four dense vector checks;
- 234,270 independent construction-certificate pair checks;
- 89,789 independent predecessor descriptor checks;
- 47,912 independent repair-coordinate checks; and
- 191,556 independent successful-schedule inclusion checks.

Canonical summary SHA-256:

```text
a9d61b984cf77c3c875ddbcdfaa2d6c6d1cd9bd6939d4c35ba4e1433a91d1589
```

Registered schema SHA-256:

```text
5be568844cbf1cbf766d32d20d1aee1c6c2708c92ec71db33a5e12e7c6547566
```

## Interpretation

The result proves that both M40 schedules survive one new complete
population and fixes the exact lower threshold at cap 103. The common
finite additive and multiplicative envelopes remain controlled by length
28, not length 29. The decrease from \(L_{28}^{\star}=104\) to
\(L_{29}^{\star}=103\) refutes threshold monotonicity across these two
different populations. It establishes no asymptotic rate, behavior at
\(m>29\), promise recognizer, density, or general factoring algorithm or
lower bound.
