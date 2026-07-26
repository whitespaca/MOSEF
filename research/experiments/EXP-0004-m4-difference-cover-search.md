# EXP-0004 - M4 divisor-cover separation falsification search

## Registration

- Research question: does divisor coverage imply order separation for any
  bounded explicit candidate family, does the signature characterization or
  counting bound fail, and are the registered simultaneous collisions exact?
- Core implementation commit:
  `89cc44a6823ef223f36b37ad1cc268fe8fbd9697`.
- Host and toolchains: `research/toolchains/windows-amd64-20260725.json`.
- Seed: none; the registered search exhaustively enumerates candidate subsets,
  two-order profiles, and deterministic construction bounds.
- Bounds: orders \(1\le r\le8\), explicit candidates \(1\le d\le12\),
  collision moduli \(4\le N\le200\), and square constructions
  \(1\le n\le200\).
- Pruning: the empty candidate family is excluded by definition. No nonempty
  subset of \([12]\), order pair in \([8]\), or square-construction bound is
  pruned.
- Command:

```powershell
python scripts/run_m4_difference_cover_search.py --order-bound 8 `
  --candidate-max 12 --modulus-max 200 --construction-bound 200
```

## Result

- Status: `PASS`.
- Candidate families: 4,095.
- Two-order profile checks: 114,660.
- Divisor covers of \([8]\): 576, consisting of 240 noninjective and 336
  injective signature families.
- Smallest registered difference-family failure:
  \(S=\{3\}\), \(T=\{1\}\), \(\Delta^+(S,T)=\{2\}\), at \(n=2\).
- Within the fixed \([8]\) search, the first noninjective divisor cover is
  \(\{5,6,7,8\}\), whose orders 3 and 6 have equal signatures.
- Smallest exact multiplicative collision: \((N,g,d)=(6,5,2)\).
- Smallest odd exact collision: \((N,g,d)=(15,4,2)\).
- The signature characterization, explicit-candidate counting lower bound,
  and square difference construction through \(n=200\) passed.
- Canonical summary SHA-256:
  `4c046ae8694070b59f5e328f94038fe32cb84b5ab716bb86a62e79636077e55f`.

Selected cover/profile outcomes were independently evaluated by Python, Rust,
and C#:

```powershell
python scripts/check_m4_difference_cover_differential.py
```

This passed 12 cross-language comparisons.

## Interpretation and limitations

The finite search audits the implementation and attempts to falsify BAR-001;
the proof, not this experiment, supplies universal validity. The search does
not estimate how often useful structured covers occur, construct unknown
factor orders, prove a lower bound for compressed batch evaluation, or imply a
general factoring lower bound. The Umans--Wang integer mechanism factors the
actual registered integers and is not refuted by these order-profile
collisions.
