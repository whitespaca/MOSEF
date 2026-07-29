"""Deterministic M47 audit of the DEF-032 exact-output support budget."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "python")]

from mosef_reference import (
    balanced_prime_population,
    descriptor_bit_budget_upper_bound,
    descriptor_output_budget,
    diversified_exceptional_selector,
    selector_output_bit_budget_upper_bound,
)

CAPS = (9, 12, 16, 20)
POPULATION_LENGTHS = tuple(range(10, 35))
ROSSER_SCHOENFELD_NUMERATOR = 62753
ROSSER_SCHOENFELD_DENOMINATOR = 50000
RATIONAL_MAJORANT_NUMERATOR = 8
RATIONAL_MAJORANT_DENOMINATOR = 9


def _source_constant_margin() -> int:
    """Certify ``1.25506 / sqrt(2) < 8/9`` using integer arithmetic."""
    return (
        2
        * RATIONAL_MAJORANT_NUMERATOR**2
        * ROSSER_SCHOENFELD_DENOMINATOR**2
        - RATIONAL_MAJORANT_DENOMINATOR**2
        * ROSSER_SCHOENFELD_NUMERATOR**2
    )


def _balanced_lower_floor(input_length: int) -> int:
    upper = 2.0 ** (input_length / 2)
    return math.floor(upper / (81 * math.log(upper)))


def build_summary() -> dict[str, object]:
    """Materialize bounded lifts and register the source-inequality audit."""
    source_margin = _source_constant_margin()
    if source_margin != 1026940271:
        raise AssertionError("M47 source-constant arithmetic changed")

    cap_profiles: list[dict[str, int]] = []
    exact_value_checks = 0
    for cap in CAPS:
        descriptors = diversified_exceptional_selector(9, cap)
        budgets = tuple(
            descriptor_output_budget(descriptor, cap)
            for descriptor in descriptors
        )
        exact_budget = sum(record.bit_budget for record in budgets)
        upper_bound = selector_output_bit_budget_upper_bound(cap)
        if exact_budget > upper_bound:
            raise AssertionError("M47 selector output-bit bound failed")
        exact_value_checks += 8 * len(descriptors)
        cap_profiles.append(
            {
                "selector_cap": cap,
                "descriptor_count": len(descriptors),
                "raw_coordinate_count": 8 * len(descriptors),
                "exact_output_bit_budget": exact_budget,
                "maximum_descriptor_bit_budget": max(
                    record.bit_budget for record in budgets
                ),
                "per_descriptor_bit_upper_bound": (
                    descriptor_bit_budget_upper_bound(cap)
                ),
                "selector_output_bit_upper_bound": upper_bound,
                "selector_bound_slack": upper_bound - exact_budget,
            }
        )

    population_checks: list[dict[str, int]] = []
    for input_length in POPULATION_LENGTHS:
        population_size = len(balanced_prime_population(input_length))
        lower_floor = _balanced_lower_floor(input_length)
        if population_size <= lower_floor:
            raise AssertionError("M47 Rosser-Schoenfeld consequence failed")
        population_checks.append(
            {
                "input_length": input_length,
                "balanced_prime_count": population_size,
                "strict_lower_bound_floor": lower_floor,
            }
        )

    summary: dict[str, object] = {
        "schema_version": "1.0.0",
        "experiment_id": "EXP-0046",
        "caps": CAPS,
        "cap_profiles": cap_profiles,
        "source_inequality": {
            "citation": (
                "Rosser-Schoenfeld 1962, Corollary 1, "
                "equations (3.5) and (3.6)"
            ),
            "pi_lower_hypothesis": "x>=17",
            "pi_upper_hypothesis": "x>1",
            "upper_constant": "1.25506",
            "proved_rational_majorant": "(1.25506/sqrt(2))<8/9",
            "integer_square_margin": source_margin,
            "balanced_consequence": (
                "|P_m|>2^(m/2)/(81*ln(2^(m/2))) for m>=10"
            ),
        },
        "uniform_bounds": {
            "per_descriptor": "2*L^2*b+L*b+9*b+5",
            "descriptor_count": "2*(L-1)^3",
            "total_exact_output_bits": (
                "2*(L-1)^3*(2*L^2*b+L*b+9*b+5)"
            ),
            "width_definition": "b=bit_length(L)",
            "asymptotic": "O(L^5*log(L))",
        },
        "population_checks": population_checks,
        "counts": {
            "cap_profiles": len(cap_profiles),
            "descriptors_materialized": sum(
                int(profile["descriptor_count"]) for profile in cap_profiles
            ),
            "exact_primitive_value_checks": exact_value_checks,
            "population_lengths": len(population_checks),
            "source_integer_inequality_checks": 1,
        },
        "status": "PASS",
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":"))
    summary["summary_sha256"] = hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()
    return summary


def main() -> int:
    summary = build_summary()
    counts = summary["counts"]
    if not isinstance(counts, dict):
        raise AssertionError("M47 counts have the wrong shape")
    print(
        "M47 polynomial-cap support audit: PASS "
        f"(summary_sha256={summary['summary_sha256']}, "
        f"exact_values={counts['exact_primitive_value_checks']}, "
        f"population_lengths={counts['population_lengths']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
