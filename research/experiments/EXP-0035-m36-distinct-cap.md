# EXP-0035: M36 distinct-cap audit

## Status

`EMPIRICAL` for the registered four-cap computation. The complete collision
and construction certificates promoted to BAR-030 and THM-009 are finite
proof objects.

## Deterministic commands

```powershell
python scripts/run_m36_distinct_cap_audit.py
python scripts/generate_m36_distinct_cap_schema.py
python scripts/check_m36_distinct_cap_differential.py
```

No random seed is used.

## Registered result

At \(m=24\), \(m+24\) gives cap 48 and
\(\lceil201m/100\rceil\) gives cap 49. Both fail: cap 48 retains ten
colliding pairs in a five-prime bucket, while caps 49 and 50 retain six
colliding pairs in a four-prime bucket. Cap 51 is injective on all 146
balanced primes. The audit checked:

- four complete cap profiles and 146 balanced primes;
- 39,624 descriptor instances and 5,785,104 local exit profiles;
- 316,992 raw and 888 normalized coordinates;
- 31,755 monotonicity pair checks;
- 42,340 raw-versus-normalized pair equivalences;
- 10,585 construction-certificate pairs;
- 16 selected Rust/C# command comparisons;
- 10,585 independent dense construction pairs;
- 9,212 dense additive-cap collision-descriptor checks;
- 9,408 dense multiplicative-cap collision-descriptor checks;
- 9,604 dense predecessor collision-descriptor checks.

Canonical summary SHA-256:

```text
7e66da1e71bf93b7c18d614581197c40b42ab9bf1da787dd318f76b77a16bda5
```

Registered schema SHA-256:

```text
3709d2e2a35212103ad838f83a25152e996cb33b9b5786d9642935a8d2ccfbcb
```

## Interpretation

The result separately refutes the two fixed M35 schedules and proves the
exact cap-51 repair at one new length. It does not establish a growth rate
for \(L_m^\star\), behavior at \(m>24\), a promise recognizer, density, or a
general factoring algorithm or lower bound.
