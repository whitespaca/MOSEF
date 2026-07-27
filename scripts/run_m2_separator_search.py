"""Exhaustively check the M2 separator criteria on a finite parameter box."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from mosef_reference import (
    CandidateKind,
    capped_valuation_profile,
    evaluate_separator_candidate,
    order_support,
    prime_factorization,
    support_is_separator,
    valuation_predicts_factor,
)


def canonical_json(value: Any) -> bytes:
    """Serialize a value deterministically for hashing."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def search(n_max: int, base_max: int, exponent_max: int) -> dict[str, Any]:
    """Run the bounded falsification search and return its exact summary."""
    if n_max < 4 or base_max < 2 or exponent_max < 1:
        raise ValueError("require n_max >= 4, base_max >= 2, exponent_max >= 1")

    evaluated = 0
    square_free_evaluated = 0
    support_false_negatives: list[dict[str, Any]] = []
    outcome_counts: Counter[str] = Counter()

    for n in range(4, n_max + 1):
        factorization = prime_factorization(n)
        if len(factorization) == 1 and factorization[0][1] == 1:
            continue
        square_free = all(exponent == 1 for _, exponent in factorization)
        for g in range(2, base_max + 1):
            if math.gcd(g, n) != 1:
                continue
            for d in range(1, exponent_max + 1):
                evaluated += 1
                square_free_evaluated += int(square_free)
                outcome = evaluate_separator_candidate(n, g, d)
                outcome_counts[outcome.kind.value] += 1
                actual = outcome.kind == CandidateKind.FACTOR
                support = support_is_separator(n, g, d)
                valuation = valuation_predicts_factor(n, g, d)

                if support and not actual:
                    raise AssertionError(f"support sufficiency failed at {(n, g, d)}")
                if valuation != actual:
                    raise AssertionError(f"valuation criterion failed at {(n, g, d)}")
                if square_free and support != actual:
                    raise AssertionError(f"square-free equivalence failed at {(n, g, d)}")
                if actual and not support:
                    support_false_negatives.append(
                        {
                            "n": n,
                            "g": g,
                            "d": d,
                            "gcd": outcome.factor,
                            "factorization": [list(item) for item in factorization],
                            "support": list(order_support(n, g, d)),
                            "valuation_profile": [
                                list(item) for item in capped_valuation_profile(n, g, d)
                            ],
                        }
                    )

    smallest_odd = next(
        (case for case in support_false_negatives if case["n"] % 2 == 1),
        None,
    )
    summary: dict[str, Any] = {
        "bounds": {
            "n": [4, n_max],
            "g": [2, base_max],
            "d": [1, exponent_max],
        },
        "seed": None,
        "candidate_evaluations": evaluated,
        "square_free_candidate_evaluations": square_free_evaluated,
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "checked": {
            "support_separator_sufficient_in_search_box": True,
            "support_separator_equivalent_for_square_free_inputs_in_search_box": True,
            "valuation_criterion_equivalent_in_search_box": True,
        },
        "support_only_equivalence_refuted": bool(support_false_negatives),
        "support_false_negative_count": len(support_false_negatives),
        "smallest_support_false_negative": (
            support_false_negatives[0] if support_false_negatives else None
        ),
        "smallest_odd_support_false_negative": smallest_odd,
    }
    summary["summary_sha256"] = hashlib.sha256(canonical_json(summary)).hexdigest()
    return summary


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-max", type=int, default=500)
    parser.add_argument("--base-max", type=int, default=20)
    parser.add_argument("--exponent-max", type=int, default=20)
    args = parser.parse_args()
    print(
        json.dumps(
            search(args.n_max, args.base_max, args.exponent_max),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
