# EXP-0050: M52 boundary-constant entropy-ledger audit

## Status

`EMPIRICAL` for the exact finite integer ledgers and independent
reconstruction. The asymptotic constant theorem is `BAR-045`; it is not an
extrapolation from these records.

## Deterministic commands

```powershell
python scripts/run_m52_boundary_constant_audit.py
python scripts/generate_m52_boundary_constant_schema.py
python scripts/check_m52_boundary_constant_differential.py
```

No random seed is used.

## Registered profiles

The audit uses
\[
m\in\{1024,4096,16384,65536\}
\]
and five boundary constants
\[
c\in
\left\{\frac1{32},\frac1{16},\frac3{32},\frac18,\frac5{32}\right\}.
\]
For each pair, it constructs a near-quadratic packed count
\[
r_m=
\left\lfloor\frac{c m^2}{4\log_2m}\right\rfloor
\]
and the exact span
\[
\Delta_m=
\left\lfloor\frac{c m^2}
{\lceil\log_2(r_m+1)\rceil}\right\rfloor.
\]
Every record checks \(r_m\le\Delta_m+1\).

The rational overlap multipliers are respectively
\[
x\in
\left\{\frac14,\frac38,\frac7{16},\frac12,\frac9{16}\right\}.
\]
Their exact uniform leading coefficients
\[
\frac{x}{2}+\frac{c}{x}
\]
are \(1/4,17/48,97/224,1/2,161/288\). Thus the first three
constants are theorem-eligible, the fourth is the open endpoint, and the
fifth is above the present ledger's range.

## Registered results

Across 20 profiles, the audit records:

- 20 exact packing checks;
- 20 rational overlap-order and leading-coefficient checks;
- 12 exact finite collision certificates below \(c=1/8\);
- eight endpoint-or-above profiles without a certificate;
- 60 SHA-256 checks over independently reconstructed high-weight bounds,
  low-weight capacities, and conservative population lower bounds;
- five growth-rate thresholds, including \(1/4,3/16,5/32,1/8\).

Large exact integers are not serialized in decimal. The schema stores their
bit lengths and SHA-256 hashes of unsigned big-endian encodings; the
independent checker reconstructs the integers before comparing both fields.

Canonical summary SHA-256:

```text
89e5465e4f1bf4d577d77d3c7624682405ecf7b8aa208432916cab2e90a8d3aa
```

Registered schema SHA-256:

```text
8265f5d4839f892640fe3c3530229bf08d584228850d9c07c35ce9208ac79f52
```

## Interpretation

The finite records test exact ceiling arithmetic, list packing, subset
multiplicity, overlap-bit charges, Hamming capacities, and the conservative
population lower bound. Their clean split at the registered constants is
implementation evidence only.

The open \(c=1/8\) endpoint is not a positive construction. It states that
the current packing-aware leading upper coefficient loses strict exponential
slack there. M53 will test whether repeated-subset or shared-divisor charging
can reduce that overcount.
