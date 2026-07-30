# EXP-0053: M55 overlap GCD and prefix LCM audit

## Status

`EMPIRICAL` exact arithmetic verification. BAR-048 is a symbolic theorem;
the finite profiles are not extrapolated.

## Commands

```powershell
python scripts/run_m55_overlap_gcd_audit.py
python scripts/generate_m55_overlap_gcd_schema.py
python scripts/check_m55_overlap_gcd_differential.py
```

No random seed is used.

## Profiles and results

For all ordered pairs \(1\le a,b\le12\), the audit checks
\[
\gcd(R_a,R_b)=R_{\gcd(a,b)}
\]
and
\[
R_a\mid R_b\Longleftrightarrow a\mid b.
\]
It also constructs all 12 exact prefix LCMs
\(\operatorname{lcm}(R_1,\ldots,R_D)\), verifies the largest-term lower
bound and product-bit upper bound, and hashes the large integers.

The registered counts are:

- 144 pair-GCD identities;
- 144 divisibility equivalences;
- 12 prefix-LCM profiles;
- 168 exact-integer SHA-256 checks;
- 12 largest-value lower-bound checks.

Canonical summary SHA-256:

```text
b82926a482dd133d94a3e89f041d23ec225ea2d9d30061d25f6e75c017b01534
```

Registered schema file SHA-256:

```text
d9dd97ea9f29b3b9fb3042992b01a181b39d5c8a8a8ebe7d57d296c3745faeb3
```

The independent checker reconstructs powers, pair GCDs, prefix LCMs, bit
bounds, and hashes without importing the reference implementation. These
finite identities do not prove the presence of balanced prime divisors.
