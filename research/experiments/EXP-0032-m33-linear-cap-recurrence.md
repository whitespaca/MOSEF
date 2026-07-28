# EXP-0032: M33 linear-cap recurrence audit

## Status

`EMPIRICAL` for the registered two-cap computation. The collision and
construction certificates promoted to BAR-027 and THM-006 are complete
finite proof objects.

## Deterministic commands

```powershell
python scripts/run_m33_linear_cap_recurrence_audit.py
python scripts/generate_m33_linear_cap_recurrence_schema.py
python scripts/check_m33_linear_cap_recurrence_differential.py
```

No random seed is used.

## Registered result

At \(m=21\), both \(m+11\) and \(\lceil151m/100\rceil\) give cap 32 and
retain the collision bucket \(\{1031,1231,1319,1433\}\). Cap 33 is injective
on all 57 balanced primes. The audit checked:

- two complete cap profiles and 57 balanced primes;
- 5,263 descriptor instances and 299,991 local exit profiles;
- 42,104 raw and 143 normalized coordinates;
- 1,596 monotonicity pair checks;
- 3,192 raw-versus-normalized pair equivalences;
- 1,596 construction-certificate pairs;
- 28 selected Rust/C# command comparisons;
- 1,596 independent dense construction pairs;
- 2,511 independent dense collision-descriptor cases.

Canonical summary SHA-256:

```text
3b6536eaf343951ca0efb50aae08f1b32f36f89e896a9f5a9f2cc6286f1ffa88
```

Registered schema SHA-256:

```text
5947cc85d8664fcb1433d7d748a7d7be0be81098c49ddd433cc0645313c77b80
```

## Interpretation

The result proves a first recurrence collision for the two fixed M32 linear
schedules and the exact cap-33 repair at one new length. It does not
establish a growth rate for \(L_m^\star\), behavior at \(m>21\), a promise
recognizer, density, or a general factoring algorithm or lower bound.
