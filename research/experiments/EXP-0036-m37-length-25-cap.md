# EXP-0036: M37 length-25 cap audit

## Status

`EMPIRICAL` for the registered full-cap and transition computations. The
complete collision and construction certificates promoted to BAR-031 and
THM-010 are finite proof objects.

## Deterministic commands

```powershell
python scripts/run_m37_length_25_cap_audit.py
python scripts/generate_m37_length_25_cap_schema.py
python scripts/check_m37_length_25_cap_differential.py
```

No random seed is used.

## Registered result

At \(m=25\), \(m+27\) gives cap 52 and
\(\lceil209m/100\rceil\) gives cap 53. Both fail: cap 52 retains 36
colliding pairs in a nine-prime bucket, while cap 53 retains 28 pairs in an
eight-prime bucket. A monotone transition audit reduces that bucket through
caps 54 to 64; \(\{5011,5179\}\) still collides at cap 64. Cap 65 is
injective on all 196 balanced primes. The audit checked:

- three complete cap profiles and 196 balanced primes;
- 47,056 descriptor instances and 9,222,976 local exit profiles;
- 376,448 raw and 1,068 normalized coordinates;
- 38,220 monotonicity pair checks;
- 57,330 raw-versus-normalized pair equivalences;
- 189,494 transition descriptor checks and 1,705,446 tracked local exits;
- 19,110 construction-certificate pairs;
- 16 selected Rust/C# command comparisons;
- 19,110 independent dense construction pairs;
- 11,628 dense additive-cap collision-descriptor checks;
- 12,324 dense multiplicative-cap collision-descriptor checks;
- 22,050 dense predecessor collision-descriptor checks.

Canonical summary SHA-256:

```text
56e595f3096bebd46184f221d0a81844eeaa8d5b4c46b0f2ccbbecad3be6d5d7
```

Registered schema SHA-256:

```text
d85d081243f5ae32b38405e35e8921ff3378ccd5bbb19c63eb135b79c4b61524
```

## Interpretation

The result separately refutes the two fixed M36 schedules and proves the
exact cap-65 repair at one new length. It does not establish a growth rate
for \(L_m^\star\), behavior at \(m>25\), a promise recognizer, density, or a
general factoring algorithm or lower bound.
