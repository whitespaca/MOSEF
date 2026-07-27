# EXP-0027 - M28 length-indexed support audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

Does the exact materialized-support bound, the forced-miss pair formula, or
the balanced input-length construction fail in the registered range? Can a
valid exceptional \(\Phi_4\) tuple with a linear-size public description
already have an exponentially long exact cofactor while preserving compact
modular evaluation? Every arithmetic disagreement, pair-count mismatch, or
cross-language difference is a failure.

## Registered commands

```text
python scripts/run_m28_length_indexed_support_audit.py \
  --input-length-min 9 --input-length-max 18 \
  --subset-prime-max 8 --gap-level-max 14
python scripts/check_m28_length_indexed_support_differential.py
```

There is no random seed.

## Checks

- Every prime returned for length \(m\) satisfies
  \(2^{m-1}\le p^2<2^m\), and every distinct pair product has exactly \(m\)
  bits.
- For every enumerated support subset, both a single product and a list of
  signed prime values are audited where applicable.
- Direct divisibility agrees with the reported hit and missed prime sets.
- Every pair outside the hit set has only unit GCDs.
- The number of forced unit pairs is
  \(\binom{s-h}{2}\), and the number of proper GCD pairs never exceeds the
  touched-pair upper bound.
- The exact inequality \(h b\le W\) holds for every materialized schedule.
- For \(A=3,B=2^t+3,g=2\), exact division by \(\Phi_4(2)=5\), the exponential
  cofactor bit-length lower bound, and compact residues modulo
  \(35,77,101,125\) all agree.
- Twelve canonical support profiles agree in Python, Rust, and C#.

## Result

The audit covered input lengths 9 through 18 and completed:

- 91 balanced primes and 623 pair-length checks;
- 2,494 schedule profiles and materialized-support inequalities;
- 751,072 exact pair/value GCD checks;
- 182,523 forced-unit pair checks;
- 2,494 proper-GCD upper-bound checks;
- 13 exact exceptional-cofactor divisions and bit-length lower bounds;
- 52 compact-versus-exact cofactor residue checks;
- 24 selected Python/Rust/C# comparisons;
- zero failures.

The largest registered balanced population had 25 primes at input length 18.
At gap level 14, the public integer encodings used 19 bits and the binary
recurrence counts used 17 bits, while the exact cofactor had 49,156 bits.
Its proved lower bound and dense degree were also 49,156.

Canonical summary SHA-256:

```text
e0744fdd20d09b103e6e5e237b2e1375290d32d3991951913086965321e29d52
```

## Interpretation boundary

The bounded population counts do not establish an asymptotic prime-density
theorem. The compact-gap family establishes exponential exact magnitude, not
many distinct prime divisors or population coverage. BAR-022 is proved by a
separate divisibility argument and applies only when exact lifts or
equivalent explicit support certificates are charged. The experiment makes
no claim about \(N\)-dependent or adaptive schedules, universal factoring,
or general circuit lower bounds.
