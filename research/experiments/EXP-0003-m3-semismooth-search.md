# EXP-0003 - M3 semismooth promise falsification search

## Registration

- Research question: does the exact \(5/12\) success bound or recursive
  completeness fail on any bounded hereditary semismooth-asymmetric input, and
  can the invalid fixed-base replacement be minimized?
- Core implementation commit:
  `93e97d96c544d5feddad208997834f47763cf31f`.
- Host and toolchains: `research/toolchains/windows-amd64-20260725.json`.
- Seed: none; the registered search exhaustively enumerates inputs, witnesses,
  and residues.
- Bounds: \(4\le N\le500\), \(B=8\), \(R=3\). The separate fixed-base
  diagnostic uses \(A=5\), and its collision minimizer searches
  \(1\le B\le20\).
- Pruning: prime inputs are skipped. Perfect-power nodes are handled exactly.
  No hereditary promised input or ordered asymmetry witness in the box is
  pruned.
- Command:

```powershell
python scripts/run_m3_semismooth_search.py --n-max 500 --base-bound 5 `
  --smooth-bound 8 --cofactor-bound 3 --collision-bound-max 20
```

## Result

- Status: `PASS`.
- Hereditary promised inputs: 155; all 155 were completely factored by the
  exhaustive residue oracle.
- Ordered asymmetry witnesses: 557; every exact successful-residue count met
  the proved \(5/12\) lower bound.
- Minimum observed exact success probability: \(268/493\), at
  \(N=493=17\cdot29\), \(t=1\), and \(d=840\).
- The fixed-base diagnostic completely factored all 153 inputs satisfying its
  stronger hereditary base-order promise.
- The smallest base-\(2\) collision against the invalid deterministic
  \(q-1\nmid d\) shortcut was
  \(N=51=3\cdot17\), \(B=8\), \(d=840\), with
  \(\operatorname{ord}_{17}(2)=8\mid840\).
- Canonical summary SHA-256:
  `0a1d2ca2fef29126b60f3a9377454200e33fce20c0b49c081ea527622f8c536d`.

Selected fixed-base outcomes and exact randomized-trial success counts were
independently evaluated by Python, Rust, and C#:

```powershell
python scripts/check_m3_semismooth_differential.py
```

This passed 22 cross-language comparisons.

## Interpretation and limitations

The finite oracle and independent implementations audit the proof boundary and
executable semantics; they do not prove THM-001. The proof supplies the
universal \(5/12\) bound. The search does not estimate promise-class density,
recognize membership without factoring, justify behavior beyond the declared
box, or imply a general polynomial-time factoring algorithm.
