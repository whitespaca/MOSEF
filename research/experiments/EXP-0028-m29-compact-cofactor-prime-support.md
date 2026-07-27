# EXP-0028 - M29 compact cofactor prime-support audit

## Status

`PASS` (`EMPIRICAL`)

## Question and stopping rule

For the length-indexed exceptional family

\[
A=3,\qquad B=2^m+3,\qquad g=2,
\]

does the compact evaluator agree with the exact prime-divisibility criterion,
the exceptional quotient rules at 5 and 7, the consecutive-support theorem,
and the exact signature-cut outcome counts?

The run is deterministic. It stops after exhausting all configured levels,
primes, balanced populations, and pair checks. Any arithmetic, identity,
cross-language, or outcome-count disagreement is a failure.

## Registered command

```powershell
python scripts/run_m29_compact_cofactor_prime_support_audit.py `
  --level-min 2 --level-max 24 --prime-max 20000 `
  --input-length-min 9 --input-length-max 40 `
  --pair-check-max 20 --exact-level-max 14
python scripts/check_m29_compact_cofactor_prime_support_differential.py
```

## Deterministic result

- 23 compact levels;
- 52,026 prime/level profiles through prime 20,000;
- 51,934 generic congruence checks;
- 92 exceptional quotient checks at \(2,3,5,7\);
- 49,742 consecutive odd-support checks;
- 13 exact closed-form identities;
- 13 exact consecutive GCD checks;
- 32 balanced input lengths from 9 through 40;
- 82,019 balanced primes;
- 32 exact signature-cut formula checks;
- 2,034 explicitly enumerated balanced pair outcomes through input length 20;
- 3 registered proper/full/unit outcome witnesses;
- 34 selected Python/Rust/C# differential comparisons;
- zero failures.

No balanced prime in the registered input-length range divided its
same-index compact cofactor. At input length 40 the balanced population had
22,394 primes and 250,734,421 possible pairs, all classified as unit outcomes
for this one candidate. This is a finite observation, not an asymptotic
zero-support theorem.

The largest support below prime 20,000 occurred at level 8 and contained

\[
\{2,7,11,1109,14143\}.
\]

The three registered pair outcomes at level 2 are:

- \(107\cdot109\): proper factor 107;
- \(5\cdot107\): full collision;
- \(109\cdot113\): unit.

## Canonical summary

The canonical JSON object is the printed summary before its final
`summary_sha256` field. Its SHA-256 is:

```text
8ca6c6310b64e56d37cfbc98caba9deddd02d5c35ea909870341aae8f23efb7a
```

## Implementations and vectors

- Python:
  `python/mosef_reference/compact_cofactor_prime_support.py`
- Rust:
  `compact_phi4_prime_profile` and CLI operation
  `compact-phi4-prime-profile`
- C#:
  independent `BigInteger` operation `compact-phi4-prime-profile`
- vectors:
  `schemas/m29-compact-cofactor-prime-support-vectors-v1.json`

## Environment

- Windows 11, AMD64;
- deterministic enumeration, no random seed;
- Python 3.12;
- Rust/Cargo workspace toolchain recorded in
  `research/toolchains/windows-amd64-20260725.json`;
- .NET SDK 8 verifier.

## Interpretation boundary

The run validates bounded arithmetic and independent implementations. It
does not prove that later balanced populations have zero support, estimate a
support density, provide a factorization-independent support recognizer, or
establish a general factoring lower bound. BAR-023's closed form,
consecutive GCD, and signature-cut counts are proved separately.
