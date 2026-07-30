# EXP-0058: M60--M80 residue and separator synthesis audit

Status: `EMPIRICAL`

## Reproduction

```powershell
python scripts/run_m60_m80_synthesis_audit.py
python scripts/generate_m60_m80_synthesis_schema.py
python scripts/check_m60_m80_synthesis_differential.py
```

Canonical schema: `schemas/m60-m80-synthesis-v1.json`.

## Result

- 32 exact endpoint residue profiles for input lengths 9 through 40;
- 271 admissible-divisor profiles;
- 85,812 exact integer residue candidates;
- 10 restricted-separator profiles;
- 94 separated-pair checks and 94 verified proper factors;
- 42 independently reconstructed row hashes.

The summary SHA-256 is
`98c64e889c9554562f1c934cbbb123fa9e91e8e0fc8a906e4bb7807352670e37`.
The schema file SHA-256 is
`fedb065411473ae130f4360b16318df21979d30875675a14c9cf7da4d7f31603`.

## Limits

The residue rows count necessary integer classes, not primes or actual
divisors of \(R_q\). The separator rows validate only finite members of the
restricted class. Neither is evidence for the UCSS premise or a universal
factoring theorem.
