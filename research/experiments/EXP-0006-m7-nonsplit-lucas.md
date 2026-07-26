# EXP-0006 - M7 nonsplit Lucas root and splitter search

## Registration

- Research question: for a fresh uniform Lucas parameter \(P\bmod K\), is
  \[
  \#\{P\bmod q:V_d(P,1)=2\}
  =\frac{\gcd(d,q-1)+\gcd(d,q+1)}2,
  \]
  and does the event used by THM-002 always expose a proper factor under a
  \(p+1\mid d,\ q+1\nmid d\) witness?
- Core implementation commit:
  `171a3058c8a26b7d2e25641e8c35a9373c19bc06`.
- Host and toolchains: `research/toolchains/windows-amd64-20260725.json`.
- Seed: none; the registered search is deterministic and exhaustive within
  each stated loop.
- Bounds: every odd prime \(3\le q\le43\), every exponent
  \(1\le d\le80\), and every ordered pair of distinct odd primes
  \(p,q\le43\) satisfying \(p+1\mid d\) and \(q+1\nmid d\).
- Pruning: primality is decided by the exact reference implementation.
  Witness checks exclude \(p=q\), require both divisibility predicates
  exactly, and enumerate every CRT parameter modulo \(pq\); no parameter is
  sampled or discarded.
- Command:

```powershell
python scripts/run_m7_nonsplit_search.py --prime-max 43 --exponent-max 80
```

## Result

- Status: `PASS`.
- Odd primes: 13.
- Root-formula checks: 1,040, comprising 22,320 direct prime-field parameter
  evaluations.
- Nonsplit-parameter count checks: 13.
- Ordered asymmetry witnesses: 714.
- Witness parameter evaluations: 194,996.
- Proved-event exact-split checks: 75,934.
- Every exact root count, nonsplit count, CRT event count, \(1/12\) lower
  bound, and proved-event split implication passed.
- The smallest witness in the registered ordering was
  \((p,q,d,N)=(3,5,4,15)\), with four parameters in the proved event and ten
  actual splitting parameters.
- The minimum proved-event probability was
  \(8/51\), at \((p,q,d)=(3,17,48)\).
- The minimum actual split probability was
  \(960/1763\), at \((p,q,d)=(41,43,42)\).
- Canonical summary SHA-256:
  `23ed0067d2ccb642c3676ff4ea3f5c34e1e622f6372626aa84377eac74b7d905`.

Selected exact root counts and composite splitter counts were independently
evaluated by Python, Rust, and C#:

```powershell
python scripts/check_m7_nonsplit_differential.py
```

This passed 26 cross-language comparisons.

## Interpretation and limitations

The search attempts to falsify LEM-003 and the per-witness success event in
THM-002; the finite-field proof, not bounded enumeration, supplies universal
validity. The observed probabilities are finite-box diagnostics and are not
used to strengthen the theorem's conservative \(1/12\) bound. The hereditary
\(p+1\)-asymmetry promise is factor-dependent and is not recognized by this
experiment or by the theorem's algorithm. The result neither covers inputs
outside that promise nor gives a general classical polynomial-time factoring
algorithm.
