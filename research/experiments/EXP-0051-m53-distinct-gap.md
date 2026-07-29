# EXP-0051: M53 distinct GCD-gap ledger audit

## Status

`EMPIRICAL` for the exact finite ledgers and independent reconstruction.
`BAR-046` is the asymptotic proof; it does not extrapolate these profiles.

## Commands

```powershell
python scripts/run_m53_distinct_gap_audit.py
python scripts/generate_m53_distinct_gap_schema.py
python scripts/check_m53_distinct_gap_differential.py
```

No random seed is used.

## Registered profiles

The audit uses
\[
m\in\{1024,4096,16384,65536\}
\]
and
\[
c\in\left\{\frac18,\frac14,\frac38,\frac12,\frac58\right\}.
\]
It tests two candidate-count regimes:

- a near-quadratic packed limit
  \(r_m=\lfloor c m^2/(4\log_2m)\rfloor\);
- linear growth \(r_m=m+1\).

Each exact span is
\[
\Delta_m=
\left\lfloor\frac{c m^2}
{\lceil\log_2(r_m+1)\rceil}\right\rfloor.
\]
The rational \(x\) values are registered per regime. The packed profiles
test the uniform \(c<1/2\) boundary; the linear profiles test the refined
result that every fixed \(c\) is excluded when
\(\ell_m/\log_2m\to1\).

## Results

Across 40 profiles, the audit records:

- 40 list-packing checks;
- 40 strict reductions from subset charging to distinct-gap charging;
- 120 SHA-256 checks over independently reconstructed distinct-gap bounds,
  low-weight capacities, and conservative population lower bounds;
- 32 theorem-eligible asymptotic classifications;
- 25 exact finite collision certificates and 15 finite noncertificates.

Some theorem-eligible packed \(c=3/8\) records are finite noncertificates:
their second-order Hamming terms still exceed the finite population lower
bound. Conversely, the linear profiles eventually certify \(c=1/2\) and
\(c=5/8\), consistent with the growth-refined theorem. These observations
are implementation checks, not asymptotic evidence.

Canonical summary SHA-256:

```text
7b066fc90a8925934886c5e6ee9b819a4dda95bb00c32732430eda3b5d58376b
```

Registered schema SHA-256:

```text
2828e1c7fcc2deb9e4bc182b5fad74f831626d1728e9376103d56d5e35ce5ac5
```

## Independent implementation

The verifier independently reconstructs:

- the candidate count, span, rational order, and packing slack;
- the old subset-based high-weight upper bound;
- the prefix sum of every overlap bit budget for
  \(1\le q\le\lfloor\Delta_m/h_m\rfloor\);
- the exact low-weight Hamming capacity and conservative population bound;
- all integer bit lengths and unsigned big-endian SHA-256 values.

The schema stores hashes rather than decimal expansions of large exact
integers. The endpoint noncertificates do not establish injectivity.
