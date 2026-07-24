# Inspected Baseline Literature

Retrieval date for all entries: 2026-07-25.

These entries orient later milestones. They do not establish that the set is a
complete or current state-of-the-art survey.

## SRC-001 — Agrawal, Kayal, and Saxena (2004)

- Citation: Manindra Agrawal, Neeraj Kayal, and Nitin Saxena, “PRIMES is in P,”
  *Annals of Mathematics* 160(2), 781-793 (2004).
- DOI: `10.4007/annals.2004.160.781`.
- Authoritative record:
  `https://annals.math.princeton.edu/2004/160-2/p12`.
- Inspected artifact: official Annals PDF, especially abstract and pages 781-782
  for the deterministic polynomial-time claim and page 790 for the stated
  soft-O complexity analysis.
- Classification: unconditional deterministic primality decision.
- Computation/input model: polynomial time in binary input length; the paper
  defines P using deterministic Turing machines.
- Imported use: `EXT-001`; paper baseline section.
- Limitation for MOSEF: primality decision does not supply a polynomial-time
  algorithm for finding a nontrivial factor.
- Discrepancy note: the 2019 published erratum exists; no corrected item inspected
  here changes the high-level imported statement. Later algorithm reuse must
  inspect the erratum in detail.

## SRC-002 — Lenstra and Pomerance (1992)

- Citation: H. W. Lenstra, Jr. and Carl Pomerance, “A rigorous time bound for
  factoring integers,” *Journal of the American Mathematical Society* 5(3),
  483-516 (1992).
- DOI: `10.1090/S0894-0347-1992-1137100-0`.
- Authoritative record:
  `https://www.ams.org/journals/jams/1992-05-03/S0894-0347-1992-1137100-0/`.
- Inspected artifact: official AMS journal record and the paper's opening theorem
  in the official PDF.
- Classification: unconditional probabilistic algorithm with a rigorous expected
  subexponential bound \(L_n[1/2,1+o(1)]\).
- Computation/input model: probabilistic complete factorization; expected running
  time with model details deferred by the paper to its section 12.
- Imported use: `EXT-002`; paper baseline section.
- Limitation for MOSEF: the bound is superpolynomial in \(\log n\), so it does not
  prove the target worst-case polynomial-time classical factorization result.
- Discrepancy note: none found between the official metadata and paper header.

## SRC-003 — Lenstra (1987)

- Citation: Hendrik W. Lenstra, Jr., “Factoring integers with elliptic curves,”
  *Annals of Mathematics* 126(3), 649-673 (1987).
- DOI: `10.2307/1971363`.
- Authoritative record:
  `https://annals.math.princeton.edu/1987/126-3/p09`.
- Inspected artifact: official Annals article record and abstract.
- Classification: elliptic-curve factoring algorithm; the specific expected-time
  expression in the abstract is explicitly described there as conjectural.
- Computation/input model: positive integer \(n\); performance parameterized by
  the least prime divisor \(p\).
- Imported use: background motivation only; no theorem claim in the ledger depends
  on the conjectural bound.
- Limitation for MOSEF: changing group orders motivates multi-group research but
  does not itself prove deterministic separation or a polynomial worst-case bound.
- Discrepancy note: none found in the inspected official record.
