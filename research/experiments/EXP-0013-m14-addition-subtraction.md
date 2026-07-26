# EXP-0013 - M14 addition-subtraction program audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

Do charged same-base addition-subtraction programs obey the signed formal
exponent bound, direct modular semantics, and positive/negative GCD
equivalence required by BAR-009? The null outcome is any program node with
\(|z_i|>2^i\), any unit-residue mismatch, any non-inert zero exponent, or any
unit base and positive \(d\) for which the GCDs of \(g^d-1\) and
\(g^{-d}-1\) differ.

## Registered commands

```text
python scripts/run_m14_addition_subtraction_search.py \
  --step-max 6 --residue-step-max 5 \
  --modulus-max 512 --base-max 32 --exponent-max 64
python scripts/check_m14_addition_subtraction_differential.py
```

The box and stopping rule were fixed before interpreting the full output.
At each node the search includes every unordered product of earlier nodes and
every oriented ratio of distinct earlier nodes. It therefore retains positive,
negative, and zero formal exponents.

## Checks

- Every unique program prefix through six nodes satisfies
  \(|z_i|\le2^i\).
- Repeated squaring attains \(2^i\) at every tested depth.
- Every program prefix through five nodes agrees with direct signed modular
  exponentiation on four registered unit base/modulus pairs.
- Every zero output in the residue box evaluates to one.
- Every unit base through the registered modulus/base box gives equal GCDs
  for positive and negative exponents through 64.
- Nonunit prechecks are classified as proper-factor or invalid-full branches.
- Four signed programs and eight absolute-value lower-bound vectors are
  independently checked in Python, Rust, and C#.

## Result

The registered audit completed with no counterexample:

- 2,403,786 signed node-growth checks;
- 190,344 direct signed-residue checks;
- 646,400 positive/negative GCD-symmetry checks;
- 10,100 unit prechecks, 6,127 proper nonunit prechecks, and 570 full
  nonunit prechecks;
- 734,190 negative outputs and 251,685 zero outputs retained;
- 19,688 zero-output residue checks;
- 24 selected Python/Rust/C# comparisons.

The complete-program counts by depth were
\[
1,1,5,60,1320,46200,2356200,
\]
including the empty program at depth zero, and the observed maximum absolute
exponents were exactly
\[
1,2,4,8,16,32,64.
\]

Canonical summary SHA-256:

```text
7203d3fc6ee67d5af3984c2b5c1eefb1640275dccdecaf979fed645d2d0fbb7d
```

## Interpretation boundary

The experiment audits exact finite semantics and implementation agreement.
It does not prove BAR-009's asymptotic transfer, cover implicit exponential
batches or other algebraic models, construct a stipulated prime population,
estimate natural density, recognize a promise class, establish novelty, or
imply a general factoring lower bound.
