# EXP-0014 - M15 leaf-materialized implicit-batch audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

Do standard leaf-materialized product trees obey the exact capped
prime-power valuation formula, the implication from a proper root GCD to a
proper leaf GCD, and the exact \(n-1\) internal-multiplication count required
by BAR-010? The null outcome is any valuation mismatch, any proper aggregate
factor absent from all individual leaves, or any product-tree count other
than \(n-1\).

## Registered commands

```text
python scripts/run_m15_implicit_batch_search.py \
  --exponent-bound 10 --modulus-max 256 \
  --base-max 24 --tree-leaf-max 4096
python scripts/check_m15_implicit_batch_differential.py
```

The box and stopping rule were fixed before interpreting the full output.
For each unit base and modulus, the search enumerates every nonempty subset
of \(\{1,\ldots,10\}\). Nonunit bases are retained only as separate direct
precheck classifications.

## Checks

- Every root GCD agrees with the exact sum of capped prime-power leaf
  valuations, including zero leaves.
- Every proper root GCD has at least one proper leaf GCD.
- Batches with individual separators whose aggregate is the full collision
  are counted rather than discarded.
- The named \(N=21,g=2,\Delta=\{2,3\}\) witness has leaf GCDs \(3,7\) and
  root GCD \(21\).
- Every leaf count from 1 through 4,096 has exactly \(n-1\) binary
  multiplications.
- Five selected batches, including odd leaf counts and a prime power, are
  independently checked in Python, Rust, and C#.

## Result

The registered audit completed with no counterexample:

- 3,821,928 nonempty subset checks;
- 6,488,889 prime-power valuation-component checks;
- 1,333,349 proper-root implication checks;
- 1,192,443 unit-root batches, 1,333,349 proper-root batches, and 1,296,136
  full-root batches;
- 2,183,887 batches containing at least one proper leaf separator;
- 850,538 batches where aggregation masked a leaf separator as a full
  collision;
- 3,736 unit prechecks, 2,296 proper nonunit prechecks, and 293 full
  nonunit prechecks;
- 4,096 exact tree-count checks through 4,095 multiplications;
- 10 selected Python/Rust/C# comparisons.

Canonical summary SHA-256:

```text
c4c3f20cc193dc90728d19fa5809d794d9ee07474fe093f12439cf3d16508529
```

## Interpretation boundary

The experiment audits finite leaf-materialized semantics and implementation
agreement. It does not prove the asymptotic transfer, establish a lower bound
for specialized arithmetic circuits without leaf materialization, cover
adaptive selectors, construct a stipulated prime population, estimate
natural density, establish novelty, or imply a general factoring lower
bound.
