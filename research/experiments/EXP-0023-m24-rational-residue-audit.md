# EXP-0023 - M24 rational-residue, resultant, and cyclotomic audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

Do coefficient-content normalization, either public stage-overlap bound, the
cleared root-of-unity identity, or exact cyclotomic divisibility fail? Is
every primitive cyclotomic factor explained only by the value-at-one
boundary or the opposite-coefficient common-step factor? Any failed identity
is the null outcome; an exceptional exact factor is retained as a scoped
counterexample rather than discarded.

## Registered commands

```text
python scripts/run_m24_rational_residue_audit.py \
  --factor-max 8 --coefficient-max 3 --cyclotomic-order-max 128 \
  --modulus-max 128 --base-max 16
python scripts/check_m24_rational_residue_audit_differential.py
```

There is no random seed. The symbolic audit uses every ordered unequal pair
\(2\le A,B\le8\), all nonzero coefficient pairs in \([-3,3]^2\), and exact
cyclotomic division through order 128 for primitive pairs. The modular audit
uses every modulus from 4 through 128 and every unit base from 0 through 16.

## Checks

- Every coefficient pair normalizes to a primitive pair.
- The exact first-stage Bezout identity and cleared root-of-unity identity
  hold coefficient by coefficient.
- Exact monic division classifies every requested cyclotomic order.
- Every content-unit aggregate has the primitive aggregate GCD.
- Every unit prefix has the same aggregate and rational-residue GCD.
- Both stage-overlap GCDs divide their public coefficient--multiplier bounds.
- Six canonical vectors agree in Python, Rust, and C#.

## Result

The registered audit completed with:

- 42 ordered unequal factor pairs and 1,512 coefficient pairs, of which
  1,176 are primitive;
- 1,512 content, Bezout, and cleared-root identities each;
- 150,528 exact cyclotomic divisibility checks, finding 46 factors:
  24 value-at-one factors, 16 difference common-step factors, and 6
  exceptional factors;
- 1,788,696 modular evaluations, including 1,675,464 unit-content checks;
- 1,176,552 unit-prefix rational reductions;
- 1,788,696 checks of each public stage-overlap bound;
- 56,586 proper aggregate GCDs with content, both stages, and both public
  overlap bounds all units;
- zero unexplained failures;
- 12 selected Python/Rust/C# comparisons.

The named exceptional witness is
\((N,g,A,B,c_1,c_2)=(55,2,3,7,1,1)\). Exact division finds only
\(\Phi_4\) through order 20; the stages are 7 and 8, while the aggregate is
15 and has GCD 5.

Canonical summary SHA-256:

```text
01953fe34732449aa6a0ec6ba9bc8c0487027a359eb1fc96f9765ce189ec39e8
```

## Interpretation boundary

The audit supports DEF-024 and the exact identities in BAR-019, and it
refutes the simple cyclotomic classification. It does not prove that the
finite exceptional list is complete beyond the registered bound, a
distribution or success rate, an order recognizer, a universal schedule,
novelty, a general factoring theorem, or a broader circuit lower bound.
