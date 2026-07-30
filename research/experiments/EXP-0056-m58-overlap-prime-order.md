# EXP-0056: M58 overlap-prime order audit

## Status

`EMPIRICAL` finite verification of BAR-051 arithmetic. The universal order
equivalence is proved independently and does not follow from the search.

## Commands

```powershell
python scripts/run_m58_overlap_prime_order_audit.py
python scripts/generate_m58_overlap_prime_order_schema.py
python scripts/check_m58_overlap_prime_order_differential.py
```

No random seed is used.

## Profiles and results

The audit covers every prime \(11\le p\le50{,}000\) and every
\(1\le q\le16\):

- 5,129 prime profiles;
- 82,064 direct modular divisibility checks;
- 44 primes with at least one occurrence in the finite gap window;
- 74 periodic hit positions;
- 5,129 occurrence-sequence hashes.

For every prime, the direct condition
\[
3^{2^q-1}+32^{2^q-1}\equiv0\pmod p
\]
agrees with the order prediction. Every nonempty occurrence set in the
window consists exactly of multiples of
\(\operatorname{ord}_{d_p}(2)\).

Canonical summary SHA-256:

```text
41eb014eb5071fae4c7a33a98f66e5b7d0529c47cab832dd89fc8b493ed9b485
```

Registered schema file SHA-256:

```text
6ed0636dd95d3ab5a677cedc9859eebcf0148d4628b4ded61a1226f64edca0c8
```

The independent checker uses its own trial factorization, Euler-totient
order reduction, and modular divisibility path. The observed finite hit
fraction is not an asymptotic density theorem.
