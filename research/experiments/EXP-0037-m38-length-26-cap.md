# EXP-0037: M38 length-26 cap audit

## Status

`EMPIRICAL` for the registered full-cap and transition computations. The
complete collision and incremental construction certificates promoted to
BAR-032 and THM-011 are finite proof objects.

## Deterministic commands

```powershell
python scripts/run_m38_length_26_cap_audit.py
python scripts/generate_m38_length_26_cap_schema.py
python scripts/check_m38_length_26_cap_differential.py
```

No random seed is used.

## Registered result

At \(m=26\), \(m+40\) gives cap 66 and
\(\lceil257m/100\rceil\) gives cap 67. Both fail: cap 66 retains 21
colliding pairs in a seven-prime bucket, while cap 67 retains three pairs in
a three-prime bucket. A monotone transition audit preserves that triple
through cap 70. At cap 71, two new cofactor coordinates append the patterns
\((0,0,1)\) and \((0,1,0)\), completing a 563-coordinate injective
certificate on all 268 balanced primes. The audit checked:

- two complete cap profiles and 268 balanced primes;
- 49,403 descriptor instances and 13,240,004 local exit profiles;
- 395,224 raw and 1,101 normalized coordinates;
- 35,778 monotonicity pair checks;
- 71,556 raw-versus-normalized pair equivalences;
- 113,179 transition descriptor checks and 792,253 tracked local exits;
- two new repair coordinates and 35,778 construction-certificate pairs;
- 16 selected Rust/C# command comparisons;
- 35,778 independent dense construction pairs;
- 23,465 dense additive-cap collision-descriptor checks;
- 25,938 dense multiplicative-cap collision-descriptor checks;
- 27,876 dense predecessor collision-descriptor checks.

Canonical summary SHA-256:

```text
c3b758e046f9e6ae722352bd54be62521a32608c43a4fc95237f2e89229a094c
```

Registered schema SHA-256:

```text
68f7e9b710be7960b78c11e4bef06119f00d75a6df2074ed8976f211e6b32a97
```

## Interpretation

The result separately refutes the two fixed M37 schedules and proves the
exact cap-71 repair at one new length. It does not establish a growth rate
for \(L_m^\star\), behavior at \(m>26\), a promise recognizer, density, or a
general factoring algorithm or lower bound.
