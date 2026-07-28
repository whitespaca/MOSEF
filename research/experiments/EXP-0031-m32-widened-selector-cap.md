# EXP-0031: M32 widened-selector cap audit

## Status

`EMPIRICAL` for the complete registered cap box. The explicit threshold,
collision, and construction certificates used by THM-005 and BAR-026 are
separately checked finite proof objects.

## Purpose

Separate the balanced-population input length \(m\) from the public selector
cap \(L(m)\), find the exact first injective cap for every M31 collision
length \(16\le m\le20\), and audit additive and multiplicative public cap
formulas without factor-dependent support recognition.

## Deterministic commands

```powershell
python scripts/run_m32_widened_selector_cap_audit.py
python scripts/generate_m32_widened_selector_schema.py
python scripts/check_m32_widened_selector_cap_differential.py
```

No random seed is used.

## Registered result

The exact minimal caps for \(m=16,17,18,19,20\) are respectively
\(19,19,27,27,31\). The audit checked:

- 38 complete cap profiles;
- 35,421 public descriptor instances across those profiles;
- 1,206,359 descriptor-prime local exit profiles;
- 283,368 raw and 1,289 normalized coordinates;
- 17,330 pair checks for monotone collision refinement;
- 3,860 raw-versus-normalized pair equivalences at each threshold and
  predecessor;
- 1,930 pairs in five complete construction certificates;
- 64 selected Rust/C# command comparisons;
- one explicit nonunit-base total-branch check;
- five registered threshold profile comparisons;
- 1,930 independent dense construction-certificate pair checks;
- 5,314 independent dense predecessor collision-descriptor checks.

The common additive schedule \(L=m+11\) works throughout \(9\le m\le20\),
and 11 is the smallest integer offset because \(m=20,L=30\) retains the
collision \(\{809,827\}\). For \(L=\lceil cm\rceil\), the exact admissible
finite-range coefficients are \(c>3/2\); the endpoint fails at the same
collision, while \(c=151/100\) is a fixed public witness.

Canonical summary SHA-256:

```text
5cdc44356ae8ed81d395b033e86403691205c6552bc8da3bf4414b47842463d8
```

Registered schema SHA-256:

```text
24f506ce7cb7ad9b10f8150f064441dbc1450f7402c72a6d228a363834eb9203
```

## Independent implementations

The compact Python implementation constructs and normalizes every cap
profile. The independent dense evaluator expands each selected cofactor
polynomial coefficient by coefficient, rechecks every construction
certificate, and evaluates every descriptor at each predecessor collision.
Rust and C# independently evaluate selected stage, public-bound,
cyclotomic, resultant, and cofactor records. The public base-GCD exit is
checked separately because the lower-level exceptional evaluator interface
is deliberately unit-base only.

## Interpretation

The exact certificates prove a bounded promise-class construction and a sharp
finite cap threshold. They do not establish:

- injectivity or failure at \(m>20\);
- an asymptotic upper bound on the minimal repairing cap;
- a factorization-free recognizer for the balanced promise;
- density for the promised inputs;
- a universal adaptive or \(N\)-dependent schedule;
- a general classical polynomial-time factoring algorithm or impossibility
  theorem.
