# EXP-0038: M39 length-27 cap audit

## Status

`EMPIRICAL` for the registered full-cap and incremental transition
computations. The complete collision and construction certificates promoted
to BAR-033 and THM-012 are finite proof objects.

## Deterministic commands

```powershell
python scripts/run_m39_length_27_cap_audit.py
python scripts/generate_m39_length_27_cap_schema.py
python scripts/check_m39_length_27_cap_differential.py
```

No random seed is used.

## Registered result

At \(m=27\), \(m+45\) gives cap 72 and
\(\lceil27m/10\rceil\) gives cap 73. Both fail: cap 72 retains 15
colliding pairs in a six-prime bucket, while cap 73 retains ten pairs in a
five-prime bucket. Raw selector inclusion and exact incremental evaluation
preserve \(\{10607,10939\}\) through cap 86. At cap 87, five new primitive
coordinates append the signatures \(4,1,0,2,8,16\) to the original bucket,
completing a 630-coordinate injective certificate on all 365 balanced
primes. The audit checked:

- one complete cap profile and 365 balanced primes;
- 31,950 descriptors and 11,661,750 full-profile local exits;
- 255,600 raw and 625 normalized coordinates;
- 66,430 raw-versus-normalized pair equivalences;
- sixteen exact transition profiles;
- 25,842 newly added descriptors and 155,052 tracked local exits;
- 206,736 new raw-coordinate pattern checks and 240 tracked pair checks;
- 235 nonconstant raw coordinates inducing five distinct patterns;
- five new repair coordinates and 66,430 construction-certificate pairs;
- 16 selected Rust/C# command comparisons;
- 66,430 independent dense construction pairs;
- 31,950 dense additive-cap collision-descriptor checks;
- 32,400 dense multiplicative-cap collision-descriptor checks;
- 52,360 dense predecessor collision-descriptor checks.

Canonical summary SHA-256:

```text
4de3a4d7f8474e91ee2e488807149b73e67c1a541018434383db8ede79ce0208
```

Registered schema SHA-256:

```text
252126eeb4de40e6c8940d23516419e8f6f4b11dbebe8a84bd8d2cdcf59757cd
```

## Interpretation

The result separately refutes the two fixed M38 schedules and proves the
exact cap-87 repair at one new length. It does not establish a growth rate
for \(L_m^\star\), behavior at \(m>27\), a promise recognizer, density, or a
general factoring algorithm or lower bound.
