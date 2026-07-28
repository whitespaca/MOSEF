# EXP-0041: M42 length-30 cap audit

## Status

`EMPIRICAL` for the registered raw-prefix, transition, and full normalized
computations. The complete collision and construction certificates promoted
to BAR-036 and THM-015 are finite proof objects.

## Deterministic commands

```powershell
python scripts/run_m42_length_30_cap_audit.py
python scripts/generate_m42_length_30_cap_schema.py
python scripts/check_m42_length_30_cap_differential.py
```

No random seed is used.

## Registered result

At \(m=30\), \(m+76\) gives cap 106 and
\(\lceil26m/7\rceil\) gives cap 112. Cap 106 leaves one 14-prime bucket
and 91 failed pairs; cap 112 leaves one nine-prime bucket and 36 failed
pairs. Exact transition profiles through cap 123 give collision-pair counts
\[
36,36,36,21,21,21,15,10,10,3,3,0.
\]
The cap-122 predecessor is \(\{28591,29209,29387\}\). The only two new
nonconstant primitive patterns are \((0,0,1)\) and \((1,0,0)\), supplied by
`phi4:123:59:87:cofactor` and `phi4:79:123:54:cofactor`. They append to
2,401 old representative columns to give a 2,403-coordinate injective
certificate. Thus \(L_{30}^{\star}=123\), the minimum incremental repair
size is two, and the repaired finite envelopes are \(m+93\) and
\(c>61/15\), with \(\lceil49m/12\rceil\) as one fixed multiplicative
witness.

The registered audit checked:

- two complete lossless raw-prefix profiles at caps 106 and 112;
- 927 balanced primes and 429,201 unordered pairs;
- 121,878 public-maximum descriptors and 112,980,906 raw-prefix local exits;
- twelve transition profiles at caps 112 through 123;
- 42,822 transition descriptors, 385,398 tracked local exits, and 432
  tracked pair checks;
- one cap-123 normalized profile with 164,700 descriptors and 152,676,900
  local exits;
- 1,317,600 raw and 2,503 normalized cap-123 coordinates;
- 429,201 raw-versus-normalized pair equivalences;
- 11,030 new cap-123 descriptors and 88,240 primitive-coordinate checks;
- two distinct repair patterns, two minimum repair coordinates, 2,403
  construction coordinates, and 429,201 certificate pairs;
- 16 selected Rust/C# command comparisons and four dense vector checks;
- 222,258 independent public-cap descriptor checks;
- 385,398 independent transition local-exit checks;
- 88,240 independent repair-coordinate checks; and
- 429,201 independent construction-certificate pair checks.

Canonical summary SHA-256:

```text
37e7339ee919f6497857ac20c45f37c34aa03a2aef6d80bf0779b95db50f2c0d
```

Registered schema SHA-256:

```text
cd6ca83c68b901a8b9f9572724e33e71d847d0399192691c1868ebdf7982ea9a
```

## Interpretation

The result refutes both M41 schedules on one new complete population and
fixes the exact lower threshold at cap 123. The common finite additive and
multiplicative envelopes are repaired by the new length-30 row. It
establishes no asymptotic rate, behavior at \(m>30\), promise recognizer,
density, or general factoring algorithm or lower bound.
