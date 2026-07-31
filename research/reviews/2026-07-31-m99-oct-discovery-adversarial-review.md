# M99 adversarial review - iterative-compression OCT discovery

Date: 2026-07-31

## Review target

- `research/literature/M99-odd-cycle-transversal-iterative-compression.md`
- `research/proofs/THM-028-iterative-compression-oct-discovery.md`
- `schemas/m99-oct-discovery-v1.json`
- `scripts/run_m99_oct_discovery_profile.py`
- `scripts/check_m99_oct_discovery.py`
- `tests/test_m99_oct_discovery.py`

## Falsification checks

1. **Imported versus local result.** The inspected five-page primary paper
   is credited for iterative compression and its
   \(O(3^k k|E||V|)\) bound. M99 claims only a self-contained local
   reconstruction and conservative accounting.
2. **Compression advice.** At prefix \(i\), the previous OCT plus the new
   vertex is always an OCT and has size at most \(k+1\).
3. **Three-way completeness.** Any OCT \(Z\) of size at most \(k\), together
   with a two-coloring of \(G-Z\), induces one enumerated
   left/right/deleted partition of the compression set.
4. **Internal edges.** A same-color edge inside the nondeleted compression
   vertices invalidates exactly that partition.
5. **Separator orientation.** The two terminal sets encode incompatible
   orientations of a base bipartite component. Separating them is necessary
   and sufficient to extend the partial coloring.
6. **Terminal deletion.** Node splitting places unit capacity on every
   vertex, including source and sink terminals. The shared-terminal
   regression confirms that terminal deletion is not silently forbidden.
7. **Large capacities.** Capacity \(k+1\) prevents a within-budget minimum
   cut from using an original-edge or super-terminal arc.
8. **Early flow stop.** Reaching flow \(k+1\) proves that no separator within
   the remaining budget exists; it does not approximate a feasible cut.
9. **Exact cardinality.** Every returned candidate is an OCT and every
   within-cap OCT induces a candidate no larger than itself. The theorem
   asserts minimum size, not globally lexicographically first witness.
10. **Early prefix rejection.** OCT number cannot decrease when vertices
    and their incident edges are added, so an above-cap prefix makes the
    full graph above cap.
11. **Runtime.** At most \(t3^{k+1}\) partitions and \(k+1\) augmentations
    per separator call are charged. Neither the \(3^k\) nor \(2^k\)
    composition term is hidden.
12. **XP boundary.** Naive subset enumeration costs \(t^{\Theta(k)}\).
    With \(t=\operatorname{poly}(m)\) and \(k=\Theta(\log m)\), this is
    quasi-polynomial, unlike the FPT construction.
13. **Polynomial consequence.** The logarithmic-cap consequence separately
    assumes polynomial explicit graph parameters. It does not construct the
    graph from an integer.
14. **Composition.** M98 receives only a discovered valid OCT. Vertex-cover
    exactness still comes from `THM-027`; OCT discovery alone is not an
    arbitrary vertex-cover algorithm.
15. **Finite differential.** All 4,096 five-vertex graph/cap pairs compare
    validity and exact cardinality with an independent enumerator.
16. **Source binding.** The checker pins M98 file/content and constructor
    hashes before extracting graph cases.
17. **Synthetic scope.** Deleted-column targets remain synthetic and do not
    establish selector occurrence or factor-independent complete types.

## Mutation review

Twenty tests cover deterministic generation, checker independence, exact
registry values, the \(K_5\) cap boundary, all 4,096 five-vertex graph/cap
pairs, parallel edges, an isolate, shared-terminal deletion, a zero-budget
path, and rehashed mutations of source, literature, graph, cap, status,
witness, metrics, payload, composed cover, rejection, and scope fields.

## Severity result

- P0 findings: none.
- P1 finding (corrected): the first exhaustive differential required the
  lexicographically first optimum. Maximum-flow tie choices guarantee an
  optimum cardinality but not that global lexicographic property. The test,
  theorem, and experiment now require exact size and OCT validity.
- P1 finding (corrected): a naive subset-search draft called the
  \(k=O(\log m)\) regime polynomial. Substitution gives
  \(2^{O((\log m)^2)}\); the paper now distinguishes XP,
  quasi-polynomial, FPT, and polynomial regimes.
- P2 boundary: the production profile imports the M98 constructor for
  composition, while the 367-line M99 checker imports neither constructor.

The result is suitable for `THM-028` as an unconditional FPT theorem on an
explicit graph and `EMP-070` as an eight-system synthetic application.
General classical polynomial-time factoring remains open.
