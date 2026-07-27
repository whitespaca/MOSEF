# EXP-0026 - M27 exceptional-cofactor schedule audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

Do the closed cyclotomic remainders, resultants, local root/valuation
profiles, or stage-overlap implications fail anywhere in the registered
box? Does a fixed public prefix for the smallest \(\Phi_4\) or \(\Phi_6\)
parameter pair cover every tested square-free semiprime once the new public
resultant precheck is included? Every disagreement or missing registered
avoidance witness is a failure.

## Registered commands

```text
python scripts/run_m27_exceptional_cofactor_schedule_audit.py \
  --factor-max 19 --prime-max 97 --valuation-exponent-max 3 \
  --prefix-max 16 --schedule-prime-max 400
python scripts/check_m27_exceptional_cofactor_schedule_differential.py
```

There is no random seed.

## Checks

- Dense division reduced modulo \(\Phi_4,\Phi_6\) agrees with the closed
  linear remainders.
- The corresponding quadratic norms equal the claimed positive resultants.
- Explicit unit-root enumeration respects the monic degree bound.
- If a stage and cofactor vanish at the same residue, the prime belongs to
  the exact public support \(B\) or \(2B\).
- If the direct cyclotomic and cofactor vanish together, the prime divides
  the public cyclotomic/cofactor resultant.
- Compact cofactor values agree with dense Horner values modulo every
  enumerated prime power, and capped valuations agree.
- Prefixes of lengths \(1,2,4,8,16\) have minimized tested square-free
  avoidance witnesses after every charged precheck.
- Twelve canonical overlap descriptors agree in Python, Rust, and C#.

## Result

The audit covered 29 exceptional ordered parameter pairs and completed:

- 29 exact quadratic-remainder checks;
- 29 exact positive-resultant checks;
- 725 prime/root enumerations;
- 30,015 unit-residue root trials, finding 561 cofactor roots;
- 60,030 stage-overlap implication checks;
- 30,015 cyclotomic/cofactor overlap implication checks;
- 34,104 compact-versus-dense prime-power checks;
- 34,104 capped valuation checks;
- 10 fixed-prefix searches over 27,474 square-free semiprime candidates;
- zero failures;
- 24 selected Python/Rust/C# comparisons.

For prefix length 16, with bases \(2,\ldots,17\), the minimized tested
avoidance witnesses are

\[
 N=2491=47\cdot53,\quad (A,B)=(3,7),\quad \Phi_4,
\]

and

\[
 N=1537=29\cdot53,\quad (A,B)=(5,3),\quad \Phi_6.
\]

Every base GCD, both stage GCDs, both public stage bounds, the direct
cyclotomic, the compact cofactor, and the new public resultant precheck are
nonproper on these registered prefixes.

Canonical summary SHA-256:

```text
3ef554db904681c3e6764bf3aba3561b1075ee4372735ce06b7f15dcbc39b6f5
```

## Interpretation boundary

The finite search does not prove the avoidance theorem, a density statement,
or failure of a length-dependent or adaptive schedule. BAR-021 proves only
the fixed finite joint-schedule obstruction by a separate finite-product
argument. The experiment supplies exact regressions and minimized witnesses
inside the registered box; it makes no general classical polynomial-time
factoring or lower-bound claim.
