# MOSEF

MOSEF is an evidence-driven research repository for classical integer
factorization. The universal existence of polynomial order-separating families
is an open research target, not an established result.

The project constitution is in `CODEX.md`. Current research state and claim
statuses are maintained under `research/`.

## Foundation validation

The M0 foundation has no third-party runtime dependencies:

```powershell
python scripts/validate_foundation.py
python -m unittest discover -s tests -v
```

When a TeX toolchain is available, compile the manuscript with:

```powershell
latexmk -xelatex -interaction=nonstopmode -halt-on-error paper/main.tex
```
