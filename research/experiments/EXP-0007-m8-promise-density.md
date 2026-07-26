# EXP-0007 - M8 combined-promise density search

## Registration

- Research question: for a fixed finite exponent set \(\Delta\), does the
  combined \(p-1/p+1\) promise on an odd semiprime \(pq\) hold exactly when
  the factor signatures differ, and do the hit-set, divisor-count, and
  magnitude bounds in BAR-003 hold?
- Core implementation commit:
  `bc8b25222823e06830530eac3962271c6d14a7ca`.
- Host and toolchains: `research/toolchains/windows-amd64-20260725.json`.
- Seed: none; the registered search is deterministic and exhaustive within
  each stated loop.
- Bounds: every odd prime \(3\le p\le101\), every unordered pair of distinct
  such primes, and every nonempty exponent subset
  \(\Delta\subseteq\{1,\ldots,18\}\) of size at most three. The balanced
  zero-density check additionally uses \(2\le n\le6\).
- Pruning: exponent families are enumerated as increasing combinations, so
  duplicates and permutations are omitted. Every prime pair is checked for
  every retained family. The balanced check is performed exactly when its
  strict magnitude hypothesis holds; no qualifying family is sampled or
  discarded.
- Stopping rule: complete the finite loops above or stop immediately at the
  first counterexample.
- Command:

```powershell
python scripts/run_m8_promise_density_search.py --prime-max 101 --candidate-max 18 --family-size-max 3 --balanced-n-max 6
```

## Result

- Status: `PASS`.
- Odd primes: 25.
- Exponent families: 987.
- Prime pairs per family: 300.
- Signature/direct-promise comparisons: 296,100.
- Exact density and pair-intersection checks: 987 each.
- Exact divisor hit-bound checks: 987.
- Magnitude-zero signature checks: 19,567.
- Magnitude-zero pair checks: 184,994.
- Balanced zero-density family checks: 2,443.
- The largest hit set contained seven primes, for
  \(\Delta=\{12,18\}\).
- The largest promised-pair density was \(147/300=49/100\), also for
  \(\Delta=\{12,18\}\).
- The smallest nonzero promised-pair density was \(24/300=2/25\), for
  \(\Delta=\{2\}\).
- The smallest all-zero counterexample to unrestricted coverage was
  \((\Delta,p,q,N)=(\{1\},3,5,15)\).
- Canonical summary SHA-256:
  `fb2f861f1670c3e4f68a0e8b461f430e7e10eeb966d9f5bec48886c810dd6cd3`.

Selected signatures, pair predicates, and hit counts were independently
evaluated by Python, Rust, and C#:

```powershell
python scripts/check_m8_promise_density_differential.py
```

This passed 28 cross-language comparisons.

## Interpretation and limitations

The search attempts to falsify every finite combinatorial step used by
BAR-003; the proof, not bounded enumeration, supplies universal validity. The
prime signatures are analytical objects evaluated at the unknown factors and
are not a recognizer computable from \(N\) without factoring. The
square-root check uses the safe integer relaxation with
\(\lceil\sqrt D\rceil\); the proof states the sharper real-valued bound.

The observed densities concern the explicitly registered finite prime set and
the common exponent family used for all pairs. They do not estimate a natural
density of semiprimes, cover schedules outside the theorem's magnitude or
sparsity hypotheses, prove a recognition lower bound, or give a general
classical polynomial-time factoring algorithm.
