# EXP-0034: M35 next-envelope audit

## Status

`EMPIRICAL` for the registered eight-cap computation. The complete collision
and construction certificates promoted to BAR-029 and THM-008 are finite
proof objects.

## Deterministic commands

```powershell
python scripts/run_m35_next_envelope_audit.py
python scripts/generate_m35_next_envelope_schema.py
python scripts/check_m35_next_envelope_differential.py
```

No random seed is used.

## Registered result

At \(m=23\), both \(m+17\) and \(\lceil173m/100\rceil\) give cap 40 and
retain ten colliding pairs in one complete bucket. Caps 41 through 46 remain
noninjective; cap 47 is injective on all 109 balanced primes. The audit
checked:

- eight complete cap profiles and 109 balanced primes;
- 53,712 descriptor instances and 5,854,608 local exit profiles;
- 429,696 raw and 1,365 normalized coordinates;
- 41,202 monotonicity pair checks;
- 47,088 raw-versus-normalized pair equivalences;
- 5,886 construction-certificate pairs;
- 16 selected Rust/C# command comparisons;
- 5,886 independent dense construction pairs;
- 5,148 dense failed-schedule collision-descriptor checks;
- 7,470 dense predecessor collision-descriptor checks.

Canonical summary SHA-256:

```text
e797c329c0935dbed73a810723764755eacc117527394e1d82ab0b792a69d06d
```

Registered schema SHA-256:

```text
65f97c06c59b60bbf649fdb7146a59c51ab33f7002445344a168be88a3ad459e
```

## Interpretation

The result proves recurrence of the two fixed M34 schedules and the exact
cap-47 repair at one new length. It does not establish a growth rate for
\(L_m^\star\), behavior at \(m>23\), a promise recognizer, density, or a
general factoring algorithm or lower bound.
