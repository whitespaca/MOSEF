# SRC-013 - Odd-cycle-transversal iterative compression

- Retrieval date: 2026-07-31.
- Inspection level: `FULL_ARTICLE`.
- Citation: Daniel Lokshtanov, Saket Saurabh, and Somnath Sikdar,
  "Simpler Parameterized Algorithm for OCT," *Combinatorial Algorithms*,
  IWOCA 2009, Lecture Notes in Computer Science 5874, pages 380--384.
- DOI: `10.1007/978-3-642-10217-2_37`.
- Inspected artifact:
  `https://sites.cs.ucsb.edu/~daniello/papers/octIterComp.pdf`.
- Inspection extent: all five pages, including the iterative-compression
  reduction, separator construction, correctness argument, and running-time
  statement.

## Imported result

The inspected paper gives a parameterized algorithm for Odd Cycle
Transversal (OCT) with running time
\(O(3^k k|E||V|)\). Its proof uses iterative compression. For an
OCT \(S\) of size at most \(k+1\), it enumerates three states for each
vertex of \(S\): left color, right color, or deletion. Once a state is
fixed, the remaining obstruction is reduced to a vertex-separator problem
in the bipartite graph obtained by deleting \(S\).

This repository imports only the established existence and complexity of
that OCT algorithm. It does not claim novelty or priority for iterative
compression, the three-way partition, node splitting, or the source's
parameterized OCT theorem.

No novelty or priority conclusion is drawn from this bounded source audit.

## Local reconstruction

`THM-028` gives a self-contained reconstruction tailored to an explicit
coverer graph. The local presentation:

1. allows separator terminals themselves to be deleted and spells out the
   node-splitting network;
2. returns a minimum-cardinality OCT when one of size at most the public cap
   exists, not merely an arbitrary feasible set;
3. exposes a conservative local bound
   \(O(3^{k+1}(k+1)t(t+q))\) for \(t\) vertices and \(q\) edge
   occurrences;
4. composes the discovered OCT with `THM-027`;
5. distinguishes an FPT search from the naive XP subset enumeration and
   from polynomial time in the original integer bit length.

These are local proof and accounting choices, not a claim that the
underlying OCT method is new.

## Scope boundary

The paper solves OCT on an already explicit graph. It does not construct
the factor-dependent complete type system or coverer graph used in this
repository, prove that those graphs have logarithmic OCT number, recognize
a hidden-factor promise, or factor integers. Thus it removes the supplied
transversal advice only after an admissible explicit graph and cap have
already been provided. General classical polynomial-time integer factoring
remains open.
