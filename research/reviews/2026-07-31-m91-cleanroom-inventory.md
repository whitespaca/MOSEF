# M91 clean-room source and grammar inventory

Date: 2026-07-31

## Source generations

| Frozen source | M50 rows | Certificate shape | Predecessor path | Repair status |
|---|---:|---|---|---|
| M31 compact vectors | 9--15 | certificate list | domain floor | not applicable |
| M32 widened caps | 16--20 | certificate list | complete raw cap-1 refinement | not separately certified |
| M33 linear recurrence | 21 | single certificate; failed profile fallback | complete raw cap-1 refinement | not separately certified |
| M34 next envelope | 22 | single certificate | complete raw cap-1 refinement | not separately certified |
| M35 next envelope | 23 | single certificate | complete raw cap-1 refinement | not separately certified |
| M36 distinct cap | 24 | single certificate | complete raw cap-1 refinement | not separately certified |
| M37 length 25 | 25 | single certificate | complete raw cap-1 refinement | not separately certified |
| M38 length 26 | 26 | final-collision pattern field | subcertificate plus raw persistence | certified minimum 2 |
| M39 length 27 | 27 | plural repair patterns | cap-86 predecessor; cap-72 repair baseline | certified minimum 5 |
| M40 length 28 | 28 | plural repair patterns | cap-103 predecessor; cap-88 repair baseline | certified minimum 5 |
| M41 length 29 | 29 | singular repair pattern | subcertificate plus raw persistence | certified minimum 1 |
| M42 length 30 | 30 | explicit repair sources | subcertificate plus raw persistence | certified minimum 2 |
| M43 length 31 | 31 | explicit repair source | subcertificate plus raw persistence | certified minimum 1 |
| M44 length 32 | 32 | explicit predecessor column count | subcertificate plus raw persistence | certified minimum 1 |
| M45 length 33 | 33 | explicit predecessor column count | subcertificate plus raw persistence | certified minimum 1 |
| M46 length 34 | 34 | explicit predecessor column count | subcertificate plus raw persistence | certified minimum 1 |

## Shared grammar

All 17,515 selected sources across the 26 rows have exactly five colon-
separated fields:

```text
family:first_factor:second_factor:base:primitive_kind
```

Every source uses the same order-four/order-six congruence grammar and one of
the same eight primitive kinds. This makes a single semantic evaluator
possible despite the schema-generation differences.

The incompatible fields are metadata placement, not mathematical grammar:

- early sources store certificate and profile lists;
- M33 lacks `predecessor_profile` and uses `failed_profile`;
- M29--M34 move the repair minimum from `repair_profile` to
  `construction_certificate`;
- M38--M41 use three names for the repair-pattern registry; and
- only M44--M46 state `predecessor_column_count` explicitly.

The checker resolves each difference with an explicit bounded adapter. It
does not infer field names dynamically or import a generator.

## Falsification findings

Two initially tempting unifications are false.

1. Collision bucket order is not semantic. At \(m=17\), the complete raw
   refinement yields the same two equivalence classes as M50 in the opposite
   list order. The checker therefore compares canonicalized unordered
   classes.
2. Every repair is not relative to \(L_m^\star-1\). The five-coordinate
   claims at \(m=27\) and \(m=28\) start from cap 72 and cap 88 respectively,
   even though the adjacent failing caps are 86 and 103.

Both counterexamples are encoded in regression logic. No source generation
is silently coerced into a false common schema.

## Review conclusion

The inventory supports one 987-line standard-library checker under a
1,000-line reviewer limit. The complete measured path passed in 155.31
seconds and 29.15 MiB peak working set. The source-format differences are
bounded adapters; the shared mathematics is reconstructed once.
