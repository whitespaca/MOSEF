# EXP-0055: M57 endpoint zero-slack audit

## Status

`EMPIRICAL` finite validation of BAR-050 arithmetic. The asymptotic theorem
is proved independently and does not follow by extrapolating these profiles.

## Commands

```powershell
python scripts/run_m57_endpoint_zero_slack_audit.py
python scripts/generate_m57_endpoint_zero_slack_schema.py
python scripts/check_m57_endpoint_zero_slack_differential.py
```

No random seed is used.

## Profiles and results

For every \(6\le\lambda\le22\), the audit constructs
\[
r=2^\lambda-1,\quad
\Delta=2^\lambda-2,\quad
m=\lceil\sqrt{2\lambda\Delta}\rceil
\]
and checks both sides of
\(H=\lfloor2\Delta/m\rfloor\):

- 17 scale exponents;
- 34 exact endpoint profiles;
- 17 switch dichotomies;
- 47 reduced rational coefficient profiles with denominator at most 12;
- 102 independently reconstructed exact-integer hashes.

At \(h=H\), the lower bound on the exact prefix-LCM charge already exceeds
the registered balanced-population lower bound. At \(h=H+1\), the exact
low-weight Hamming capacity already exceeds it. Every rational profile
confirms
\(\max\{1/(2x),x/2\}\ge1/2\), with equality only at \(x=1\).

Canonical summary SHA-256:

```text
c5f4a07e514e9307c66b3868a954925bd15ece3b48a2375ed834d8d7db37052f
```

Registered schema file SHA-256:

```text
da399a83a6152ced97e66a1cd747f803b912973f169927f328cf87b7ab22bc1b
```

The independent checker reconstructs all parameters, capacities, LCM
lower bounds, rational coefficients, and hashes without importing the
reference implementation. The finite pass does not establish endpoint
injectivity or balanced-prime occurrence.
