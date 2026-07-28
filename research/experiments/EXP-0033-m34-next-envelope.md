# EXP-0033: M34 next-envelope audit

## Status

`EMPIRICAL` for the registered six-cap computation. The complete collision
and construction certificates promoted to BAR-028 and THM-007 are finite
proof objects.

## Deterministic commands

```powershell
python scripts/run_m34_next_envelope_audit.py
python scripts/generate_m34_next_envelope_schema.py
python scripts/check_m34_next_envelope_differential.py
```

No random seed is used.

## Registered result

At \(m=22\), both \(m+12\) and \(\lceil153m/100\rceil\) give cap 34 and
retain 37 colliding pairs in two complete buckets. Caps 35 through 38 remain
noninjective; cap 39 is injective on all 80 balanced primes. The audit
checked:

- six complete cap profiles and 80 balanced primes;
- 23,190 descriptor instances and 1,855,200 local exit profiles;
- 185,520 raw and 578 normalized coordinates;
- 15,800 monotonicity pair checks;
- 18,960 raw-versus-normalized pair equivalences;
- 3,160 construction-certificate pairs;
- 16 selected Rust/C# command comparisons;
- 3,160 independent dense construction pairs;
- 5,676 dense failed-schedule descriptor-bucket checks;
- 3,996 dense predecessor collision-descriptor checks.

Canonical summary SHA-256:

```text
5f60b3e2d688697ce30a6b40b39d6adbd8fe365cca4dc8e36994090aa2a54b39
```

Registered schema SHA-256:

```text
36bd038cd325dc4bb151ffd366b1d47ed670f4ef4b7871343e14624d52fc2968
```

## Interpretation

The result proves recurrence of the two fixed M33 linear schedules and the
exact cap-39 repair at one new length. It does not establish a growth rate for
\(L_m^\star\), behavior at \(m>22\), a promise recognizer, density, or a
general factoring algorithm or lower bound.
