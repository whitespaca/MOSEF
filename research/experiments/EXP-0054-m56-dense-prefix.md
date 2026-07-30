# EXP-0054: M56 dense-interval full-prefix audit

## Status

`EMPIRICAL` finite verification. BAR-049 is proved constructively and does
not depend on extrapolating the experiment.

## Commands

```powershell
python scripts/run_m56_dense_prefix_audit.py
python scripts/generate_m56_dense_prefix_schema.py
python scripts/check_m56_dense_prefix_differential.py
```

No random seed is used.

## Profiles and results

The constructive audit covers \(1\le h\le8\) and 12 target prefix lengths,
including nonzero span remainders. It checks:

- 96 dense-interval profiles;
- 624 explicit arithmetic-progression subset witnesses;
- two sequence hashes per constructive profile.

The exhaustive audit independently enumerates every \((h+1)\)-subset for
all spans \(2\le\Delta\le14\) and \(1\le h\le\min\{4,\Delta\}\):

- 49 exhaustive profiles;
- 14,755 subset GCD enumerations;
- 241 total sequence-hash checks across both audit parts.

Every exact realized-gap set equals
\(\{1,\ldots,\lfloor\Delta/h\rfloor\}\).

Canonical summary SHA-256:

```text
7a15643f88dcb66825845e76b27fdbe174f5f0458c89cdc9a608e15a6abef27a
```

Registered schema file SHA-256:

```text
bc406d68888a9e649d945d9e8d942d48ec30588146b4487067212a5b363c164f
```

The independent checker reconstructs all witnesses and exhaustive
combinations without importing the reference implementation. No
balanced-prime occurrence is inferred.
