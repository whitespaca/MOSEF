# EXP-0057: balanced half-order size and residue audit

Status: `EMPIRICAL`

## Scope

This deterministic audit enumerates every balanced-population prime for
input lengths \(9\) through \(28\). For each prime it independently computes
\(\operatorname{ord}_p(3/32)\), the possible odd half-order, its first
occurrence gap, the exact integer size threshold, and the residue condition.

## Reproduction

```powershell
python scripts/run_m59_half_order_size_audit.py
python scripts/generate_m59_half_order_size_schema.py
python scripts/check_m59_half_order_size_differential.py
```

Canonical schema: `schemas/m59-half-order-size-v1.json`.

## Result

- 20 complete balanced input-length windows;
- 1,894 prime profiles;
- 622 primes with an eligible odd half-order;
- 622 strict size-inequality and residue-class checks;
- 1,894 independently reconstructed profile hashes.

All checks pass. The canonical summary SHA-256 is
`b3ebb32c0d59bae938475391af569ee9b166972d03cb106c1c6085f6d2dd625e`.
The schema file SHA-256 is
`0e40a80364951c2bfda5f4d09769e71d7d6686bb826899f0a7e7e3bf05d60599`.

## Limits

The windows are finite. They validate the exact arithmetic implementation,
not an asymptotic distribution of orders or primes in residue classes.
