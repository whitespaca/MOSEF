# EXP-0020 - M21 signed quotient-stage combination audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

For a DEF-020 public factor chain and public signed coefficients, can
\[
R=\sum_i c_iS_{A_i}(g^{M_{i-1}})\pmod N
\]
have a proper GCD when every charged stage, prefix, denominator, multiplier,
coefficient, and weighted-stage GCD is a unit or full? Failure to find such a
case is the null outcome. A compact evaluation disagreeing with the expanded
integer polynomial is also a null outcome.

## Registered commands

```text
python scripts/run_m21_quotient_linear_combination_search.py \
  --factor-max 5 --coefficient-max 1 --depth-max 3 \
  --modulus-max 128 --base-max 16
python scripts/check_m21_quotient_linear_combination_differential.py
```

The symbolic audit uses every factor tuple of depths two and three with
entries in \([1,5]\) and every aligned coefficient tuple over
\(\{-1,1\}\). The modular audit uses every modulus from 4 through 128 and
every unit base from 0 through 16.

## Checks

- Compact stage evaluation agrees with direct evaluation of the collected
  sparse integer polynomial.
- Every coefficient, quotient, weighted stage, aggregate, and retained
  DEF-020 stage output has an explicit GCD.
- Proper aggregate GCDs are separated into those already accompanied by a
  proper charged component and genuinely new aggregate successes.
- Strict successes require every charged component GCD to equal one.
- The named BAR-016 witness is asserted exactly.
- Six selected vectors, including a full cancellation, a preexisting
  component factor, even moduli, repeated prime powers, and signed
  coefficients, agree in Python, Rust, and C#.

## Result

The registered audit completed without semantic disagreement:

- 1,100 symbolic descriptors, 9,600 uncollected terms, and 7,450 collected
  nonzero terms;
- 177,450 factor chains and 1,301,300 signed combinations;
- 340,640 proper aggregate GCDs, of which 326,840 had a proper charged
  component and 13,800 did not;
- 6,262 strict successes with every charged component GCD equal to one;
- 41,302 zero residues, exactly the 41,302 full aggregate collisions;
- zero unexplained compact-versus-expanded failures;
- 1,183 unit and 851 nonunit base prechecks;
- 12 selected Python/Rust/C# comparisons.

The first strict success in enumeration order is
\[
N=9,\quad g=2,\quad(A_1,A_2)=(1,5),\quad(c_1,c_2)=(-1,1),
\]
whose quotients are \(1,4\) and whose aggregate is \(3\). BAR-016 retains
the symmetric repeated-factor witness \((5,5)\), whose quotients are \(4,7\)
and whose aggregate is also \(3\).

Canonical summary SHA-256:

```text
34f0f120a1ef3ab08b08fb9c477ea03161f96c8857bcc143e91be51137c85f6f
```

## Interpretation boundary

The exact witness proves that BAR-015's product component implication does
not extend to signed addition. The finite counts do not imply an asymptotic
success rate, a universal factoring schedule, recognition of successful
inputs, or a lower bound for richer arithmetic circuits. They do establish
that cross-stage cancellation is a genuine extraction mechanism that the next
milestone must characterize rather than dismiss.
