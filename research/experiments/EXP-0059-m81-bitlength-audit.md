# EXP-0059: Standard-bit-length migration audit

Status: `EMPIRICAL`

## Purpose

Falsify the former identification of \(\lceil\log_2N\rceil\) with binary
bit length, locate its complete discrepancy set in a large deterministic
finite range, and verify that the frozen balanced odd-semiprime certificates
use the standard length already implemented in Python, Rust, and C#.

## Reproduction

```powershell
python scripts/run_m81_bitlength_audit.py
python scripts/generate_m81_bitlength_schema.py
python scripts/check_m81_bitlength_differential.py
```

Canonical schema: `schemas/m81-bitlength-audit-v1.json`.

## Result

- 1,048,576 positive integers through \(2^{20}\);
- exactly 21 discrepancies, the powers \(2^0,\ldots,2^{20}\);
- 1,048,555 non-power agreements;
- all 26 frozen M50 rows for input lengths 9 through 34;
- 12,245 balanced population primes and 11,628,152 distinct prime pairs;
- three standard implementation semantics and 47 row hashes.

The canonical summary SHA-256 is
`19435b38800bd75dec6fb628731eaa94a9fc5d0a9898cbf02e0edeec5d4ac709`.
The schema file SHA-256 is
`fd3ab80dfca08de5620db8f8d86b60ba2648a626d859579a8e4d5a8404150a46`.

## Limits

The finite enumeration is validation, not the proof of BAR-064. Preservation
of M31--M46 follows from the proved odd-product boundary and is checked against
the 26 frozen M50 rows; no claim is made about unregistered length-indexed
families or general factorization.
