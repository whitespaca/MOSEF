# EXP-0009 - M10 multiplication straight-line compression search

## Registration

- Research question: in DEF-010's factor-oblivious multiplication
  straight-line model, can any node exceed exponent \(2^t\) after \(t\)
  charged multiplications, can the formal exponent semantics disagree with
  direct modular exponentiation, or can the compact tower descriptor
  \(2^{2^s}\) be evaluated below its generic multiplication lower bound?
- Core implementation commit:
  `5501d2d1d2a6a5c584fdc03f905e9a36a6054733`.
- Host and toolchains: `research/toolchains/windows-amd64-20260725.json`.
- Seed: none; every registered loop is deterministic.
- Bounds: every multiplication program through seven nodes, with commutative
  parent pairs enumerated once in nondecreasing order; every constructed node
  checked at base 7 modulo 1009; and every tower descriptor level
  \(0\le s\le16\).
- Pruning: multiplication is commutative, so parent pairs \((a,b)\) and
  \((b,a)\) are identified. No resulting program, node, or descriptor level
  inside the registered bounds is sampled or omitted.
- Stopping rule: complete the finite loops above or stop immediately at the
  first exponent-growth, direct-residue, maximum-tightness, tower-lower-bound,
  or repeated-squaring disagreement.
- Command:

```powershell
python scripts/run_m10_compressed_exponent_search.py --step-max 7 --descriptor-level-max 16
```

## Result

- Status: `PASS`.
- Exact program counts at depths zero through seven:
  \(1,1,3,18,180,2700,56700,1587600\).
- Constructed-node exponent-growth checks: 1,647,202.
- Direct modular-residue comparisons: 1,647,202.
- Maximum formal exponents at depths zero through seven:
  \(1,2,4,8,16,32,64,128\), attaining the BAR-005 bound at every depth.
- Distinct final-node exponent counts:
  \(1,1,3,6,11,20,35,61\).
- Tower descriptor checks: 17. At level 16 the exact exponent has 65,537
  bits and both the lower bound and repeated-squaring construction use
  65,536 generic modular multiplications.
- Canonical summary SHA-256:
  `67508cf957fa356350a707a58f1079aebcea4f02481ff826cd5ed09727d210fa`.

Selected complete programs and lower bounds were independently evaluated by
Python, Rust, and C#:

```powershell
python scripts/check_m10_compressed_exponent_differential.py
```

This passed 24 cross-language comparisons.

## Interpretation and limitations

The experiment tries to falsify BAR-005's exact induction and implementation
semantics. Universal validity comes from the proof, not from the seven-node
enumeration. The counts describe syntactic commutative programs; they are not
counts of inequivalent addition chains or residue functions.

The tower result is an exact obstruction only in DEF-010's generic
multiplication model. The experiment does not cover inversion, special field
maps, elliptic-curve operations, adaptive factor-revealing GCD branches, or a
different rigorously costed algebraic representation. It makes no claim about
the sufficiency of \(\Theta(k\log k)\)-step schedules, natural input density,
general factoring complexity, or novelty.
