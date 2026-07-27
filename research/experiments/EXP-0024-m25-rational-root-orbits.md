# EXP-0024 - M25 rational root-of-unity orbit audit

## Status

`EMPIRICAL`, deterministic and reproducible.

## Question and null outcome

Does the exact cyclotomic remainder ratio disagree with THM-003 anywhere in
the registered box? Does Galois phase divisibility fail for a rational
ratio, does the norm identity fail, or do the square-free and repeated-prime
modular witnesses collapse into a charged stage or public overlap bound?
Any disagreement is the null outcome and is reported rather than discarded.

## Registered commands

```text
python scripts/run_m25_rational_root_orbit_audit.py \
  --factor-max 32 --order-max 256
python scripts/check_m25_rational_root_orbit_differential.py
```

There is no random seed. The exact audit uses every ordered unequal pair
\(2\le A,B\le32\) and every order \(2\le n\le256\). For each order outside
the stage zero sets, it reduces both geometric-sum polynomials modulo
\(\Phi_n\) and tests exact rational proportionality.

## Checks

- Every requested order receives the theorem classification and compact
  fixed-\((A,B)\) descriptor.
- Exact cyclotomic remainders agree with the predicted rational value or
  irrational status.
- Every nonzero rational ratio satisfies
  \(n\mid A(B-2)+1\).
- Every positive \(T=R+1\) rational hit satisfies the exact cyclotomic norm
  identity used in THM-003.
- The phase-only obstruction \((A,B,n)=(2,4,5)\) remains irrational.
- Square-free \(\Phi_4\), repeated-prime \(\Phi_4\), and square-free
  \(\Phi_6\) modular witnesses retain unit stage and public overlap bounds.
- Twelve canonical vectors agree in Python, Rust, and C#.

## Result

The registered audit completed with:

- 930 ordered unequal factor pairs and 930 compact descriptors;
- 237,150 order checks, including 228,338 orders outside both stage zero
  sets;
- 228,338 exact Galois-orbit/cyclotomic remainder checks;
- 2,426 phase candidates, of which 1,913 were phase-only irrational orders;
- 513 rational orders: 432 common-step, 56 \(\Phi_4\), and 25 \(\Phi_6\)
  cases;
- 81 positive-ratio cyclotomic norm checks;
- zero classification failures;
- 24 selected Python/Rust/C# comparisons.

The named modular witnesses are \((55,2,3,7,1,1)\) with GCD \(5\),
\((75,2,3,7,1,1)\) with GCD \(25\), and
\((35,12,5,3,2,1)\) with GCD \(7\). Both stages and both M24 public overlap
bounds are units in every case.

Canonical summary SHA-256:

```text
7e498c64b848973c95501e5e043e2187ab21772c5d7edbbf62f737d36cf9bb13
```

## Interpretation boundary

The audit supports but does not prove THM-003; the proof is independent.
The finite box establishes no distribution, success rate, density, schedule,
novelty, general factoring theorem, or general arithmetic-circuit lower
bound. Enumerating every divisor of the compact common-step descriptor is
not treated as polynomial-time without charging factorization and output.
