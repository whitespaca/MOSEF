# EXP-0015 - M16 non-materializing product-DAG audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

Can sharing in an explicit-atom product DAG create a proper node GCD absent
from every explicit atom, exceed the tight \(2^s\) unfolded-occurrence bound
at gate \(s\), or violate the formal residue and capped-valuation formulas of
BAR-011? The null outcome is any such counterexample.

## Registered commands

```text
python scripts/run_m16_product_dag_search.py \
  --exponent-bound 4 --program-step-max 5 \
  --residue-step-max 2 --modulus-max 128 --base-max 16
python scripts/check_m16_product_dag_differential.py
```

The box and stopping rule were fixed before interpreting the full output.
Syntax enumeration uses one to three explicit atoms and every commutative
parent pair, including self-products. Residue enumeration uses every nonempty
exponent subset of \([4]\) of size at most three, every circuit through two
gates, every modulus from 4 through 128, and bases through 16. Nonunit bases are
retained only as separate precheck classifications.

## Checks

- Every product node agrees with its formal atom-multiplicity product.
- Every node GCD agrees with the exact sum of multiplicity-weighted
  prime-power valuations.
- Every proper product-node GCD has a proper explicit atom GCD.
- Every gate-\(s\) unfolded occurrence count is at most \(2^s\), and repeated
  self-product attains equality through five gates.
- The \(N=21,g=2,\Delta=(2,3)\) union collision has atom GCDs \(3,7\) and
  product GCD \(21\).
- The \(N=9,g=4,\Delta=(1)\) repeated collision has atom GCD \(3\), but its
  first self-product has GCD \(9\).
- Five selected DAGs are independently checked in Python, Rust, and C#.

## Result

The registered audit completed with no counterexample:

- 611,572 exact product-DAG syntax checks;
- 3,033,586 gate occurrence and formal-multiplicity checks;
- exact maximum unfolded occurrences \(2,4,8,16,32\);
- 517,020 bounded residue-circuit checks;
- 2,282,274 node residue-semantics checks;
- 3,581,928 prime-power valuation-component checks;
- 856,512 proper-node-to-proper-atom implication checks;
- 84,013 product nodes where aggregation masked a used explicit atom success as
  a full collision;
- 1,231 unit prechecks, 748 proper nonunit prechecks, and 146 full nonunit
  prechecks;
- 10 selected Python/Rust/C# comparisons.

Canonical summary SHA-256:

```text
431faf3c71fc0f13c3152bffd06faa5e7eb96382164e40611979c8573e41a12d
```

## Interpretation boundary

The experiment audits finite explicit-atom product-DAG semantics and
implementation agreement. It demonstrates exponential repeated formal
occurrences, not exponentially many distinct exponent tests. It does not
prove the asymptotic theorem or establish a lower bound for richer arithmetic
circuits, closed-form atom synthesis, adaptive selectors, population,
density, recognition, novelty, factoring, or any general circuit model.
