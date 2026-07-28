# EXP-0039: M40 length-28 cap audit

## Status

`EMPIRICAL` for the registered full-cap and incremental transition
computations. The complete collision and construction certificates promoted
to BAR-034 and THM-013 are finite proof objects.

## Deterministic commands

```powershell
python scripts/run_m40_length_28_cap_audit.py
python scripts/generate_m40_length_28_cap_schema.py
python scripts/check_m40_length_28_cap_differential.py
```

No random seed is used.

## Registered result

At \(m=28\), \(m+60\) gives cap 88 and
\(\lceil16m/5\rceil\) gives cap 90. Both fail with the same 15
colliding pairs in a six-prime bucket. Raw selector inclusion and exact
incremental evaluation preserve \(\{11867,12791\}\) through cap 103. At
cap 104, five new primitive coordinates append the signatures
\(0,16,8,4,2,1\) to the original bucket, completing a 913-coordinate
injective certificate on all 507 balanced primes. The audit checked:

- one complete cap profile and 507 balanced primes;
- 58,464 descriptors and 29,641,248 full-profile local exits;
- 467,712 raw and 908 normalized coordinates;
- 128,271 raw-versus-normalized pair equivalences;
- seventeen exact transition profiles;
- 38,253 newly added descriptors and 229,518 tracked local exits;
- 306,024 new raw-coordinate pattern checks and 255 tracked pair checks;
- 14 nonconstant raw coordinates inducing five distinct patterns;
- five new repair coordinates and 128,271 construction-certificate pairs;
- 16 selected Rust/C# command comparisons and four dense vector checks;
- 128,271 independent construction-certificate pair checks;
- 58,464 independent additive-cap collision-descriptor checks;
- 61,143 independent multiplicative-cap collision-descriptor checks;
- 95,778 independent predecessor collision-descriptor checks.

Canonical summary SHA-256:

```text
2059fbfc2eff0bfe710427cea5de920362f5dfa6bbf34e3f2143e1513633f0c6
```

Registered schema SHA-256:

```text
7f45ad32c1abb3d09d0b47c4659b2e3555af7126fa534b786b5a0d0504ed4414
```

## Interpretation

The result separately refutes the two fixed M39 schedules and proves the
exact cap-104 repair at one new length. It does not establish a growth rate
for \(L_m^\star\), behavior at \(m>28\), a promise recognizer, density, or a
general factoring algorithm or lower bound.
