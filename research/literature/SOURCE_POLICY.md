# Source Verification and Citation Policy

## Admission rule

Technical claims use primary sources: final journal or proceedings papers,
author manuscripts, or arXiv versions when no final version is accessible.
Official software documentation is primary evidence for software behavior.
Secondary material may guide discovery but cannot be the sole support for a
theorem statement or state-of-the-art claim.

## Inspection record

Each admitted source receives a stable `SRC-NNN` entry recording:

1. complete citation, version, DOI or other stable identifier;
2. authoritative retrieval URL and retrieval date;
3. exact pages, sections, theorem, or abstract language inspected;
4. computation model and result classification;
5. hypotheses and limitations relevant to this repository;
6. the claim IDs and paper locations that use it;
7. unresolved version or metadata discrepancies.

An abstract-only inspection is labeled as such. A bibliography entry is added
only after title, authors, venue, year, pages, and identifier are checked against
an authoritative record.

## Claim discipline

- A source proves only the theorem under its own hypotheses.
- A cited empirical or heuristic analysis remains `EMPIRICAL` or `HEURISTIC`.
- Average-case, randomized, conditional, and restricted-domain results cannot be
  restated as unconditional worst-case results.
- State-of-the-art claims require a fresh multi-source search and a recorded
  retrieval date; old baseline sources do not establish what is latest.
- If the full source needed for a claim cannot be inspected, record
  `UNVERIFIED_SOURCE` and a blocker rather than completing the claim from memory.

## Citation maintenance

`research/CLAIMS.md` maps claim IDs to source IDs. `paper/references.bib` stores
verified bibliographic data. The foundation validator checks that every manuscript
citation key exists in the bibliography, but mathematical source review remains a
human-readable evidence task.
