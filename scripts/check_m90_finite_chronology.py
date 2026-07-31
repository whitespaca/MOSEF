"""Check the M90 finite-paper narrative/chronology split."""

from __future__ import annotations

import json
import re
from fractions import Fraction
from pathlib import Path
from typing import NamedTuple, cast

ROOT = Path(__file__).resolve().parents[1]
FOCUSED = ROOT / "paper" / "focused"
TABLES = ROOT / "paper" / "tables"
ARTIFACT = ROOT / "schemas" / "m50-finite-threshold-summary-v1.json"


class ThresholdRow(NamedTuple):
    """Semantic fields preserved in every rendered threshold row."""

    input_length: int
    population_size: int
    cap: int
    offset: int
    collision_buckets: tuple[tuple[int, ...], ...] | None
    repair_coordinates: int | None
    evidence_ids: tuple[str, ...]


EXPECTED_ROWS = (
    ThresholdRow(9, 2, 9, 0, None, None, ("THM-004", "EMP-030")),
    ThresholdRow(10, 3, 10, 0, None, None, ("THM-004", "EMP-030")),
    ThresholdRow(11, 3, 11, 0, None, None, ("THM-004", "EMP-030")),
    ThresholdRow(12, 4, 12, 0, None, None, ("THM-004", "EMP-030")),
    ThresholdRow(13, 6, 13, 0, None, None, ("THM-004", "EMP-030")),
    ThresholdRow(14, 7, 14, 0, None, None, ("THM-004", "EMP-030")),
    ThresholdRow(15, 11, 15, 0, None, None, ("THM-004", "EMP-030")),
    ThresholdRow(
        16,
        12,
        19,
        3,
        ((191, 227, 233),),
        None,
        ("THM-005", "BAR-026", "EMP-031"),
    ),
    ThresholdRow(
        17,
        18,
        19,
        2,
        ((277, 317), (263, 349)),
        None,
        ("THM-005", "BAR-026", "EMP-031"),
    ),
    ThresholdRow(
        18,
        25,
        27,
        9,
        ((503, 509),),
        None,
        ("THM-005", "BAR-026", "EMP-031"),
    ),
    ThresholdRow(
        19,
        31,
        27,
        8,
        ((569, 719),),
        None,
        ("THM-005", "BAR-026", "EMP-031"),
    ),
    ThresholdRow(
        20,
        44,
        31,
        11,
        ((809, 827),),
        None,
        ("THM-005", "BAR-026", "EMP-031"),
    ),
    ThresholdRow(
        21,
        57,
        33,
        12,
        ((1031, 1231, 1319, 1433),),
        None,
        ("THM-006", "BAR-027", "EMP-032"),
    ),
    ThresholdRow(
        22,
        80,
        39,
        17,
        ((1481, 1571),),
        None,
        ("THM-007", "BAR-028", "EMP-033"),
    ),
    ThresholdRow(
        23,
        109,
        47,
        24,
        ((2411, 2777),),
        None,
        ("THM-008", "BAR-029", "EMP-034"),
    ),
    ThresholdRow(
        24,
        146,
        51,
        27,
        ((3049, 3643, 3863, 4057),),
        None,
        ("THM-009", "BAR-030", "EMP-035"),
    ),
    ThresholdRow(
        25,
        196,
        65,
        40,
        ((5011, 5179),),
        None,
        ("THM-010", "BAR-031", "EMP-036"),
    ),
    ThresholdRow(
        26,
        268,
        71,
        45,
        ((7187, 7229, 7649),),
        2,
        ("THM-011", "BAR-032", "EMP-037"),
    ),
    ThresholdRow(
        27,
        365,
        87,
        60,
        ((10607, 10939),),
        5,
        ("THM-012", "BAR-033", "EMP-038"),
    ),
    ThresholdRow(
        28,
        507,
        104,
        76,
        ((11867, 12791),),
        5,
        ("THM-013", "BAR-034", "EMP-039"),
    ),
    ThresholdRow(
        29,
        685,
        103,
        74,
        ((18979, 21031),),
        1,
        ("THM-014", "BAR-035", "EMP-040"),
    ),
    ThresholdRow(
        30,
        927,
        123,
        93,
        ((28591, 29209, 29387),),
        2,
        ("THM-015", "BAR-036", "EMP-041"),
    ),
    ThresholdRow(
        31,
        1280,
        144,
        113,
        ((37483, 44963),),
        1,
        ("THM-016", "BAR-037", "EMP-042"),
    ),
    ThresholdRow(
        32,
        1750,
        167,
        135,
        ((59699, 63463),),
        1,
        ("THM-017", "BAR-038", "EMP-043"),
    ),
    ThresholdRow(
        33,
        2410,
        195,
        162,
        ((80309, 92671),),
        1,
        ("THM-018", "BAR-039", "EMP-044"),
    ),
    ThresholdRow(
        34,
        3299,
        201,
        167,
        ((97927, 99527),),
        1,
        ("THM-019", "BAR-040", "EMP-045"),
    ),
)

EXPECTED_CLAIMS = (
    "BAR-024",
    "THM-021",
    "THM-022",
    "THM-023",
    "THM-024",
    "THM-004",
    "THM-005",
    "THM-014",
    "THM-019",
    "BAR-041",
    "BAR-046",
)

PAPER_CONFIG = {
    "en": {
        "initial_section": r"\section{Initial and widened finite theorems}",
        "synthesis_section": r"\section{Exact finite threshold synthesis}",
        "barrier_section": (
            r"\section{Asymptotic barriers inside the same grammar}"
        ),
        "subsections": (
            r"\subsection{Complete 26-row threshold chronology}",
            r"\subsection{Artifact and semantic reproduction}",
        ),
        "table_input": (
            r"\input{paper/tables/finite-threshold-summary-en.tex}"
        ),
        "initial_cases": (
            (
                r"For every \(9\le m\le15\), the base selector",
                r"1,2,2,3,4,6,10",
            ),
            (
                r"At \(m=16\), the three primes \(191,227,233\)",
                "identical complete masks",
            ),
        ),
        "synthesis_cases": (
            (
                r"\(L_{27}^\star=87\)",
                r"\(L_{28}^\star=104\)",
                r"\(\{11867,12791\}\)",
                "five-coordinate subcertificate",
            ),
            (
                r"L_{29}^\star=103<L_{28}^\star=104",
                r"\{18979,21031\}",
                "phi4:87:95:103:cofactor",
            ),
            (
                r"L_{34}^\star=201",
                r"\{97927,99527\}",
                "phi6:149:201:45:cofactor",
            ),
        ),
    },
    "ko": {
        "initial_section": r"\section{초기 및 확장 유한 정리}",
        "synthesis_section": r"\section{정확한 유한 threshold 종합}",
        "barrier_section": r"\section{같은 문법 내부의 점근 장벽}",
        "subsections": (
            r"\subsection{26행 전체 threshold 연혁}",
            r"\subsection{Artifact 및 semantic 재현}",
        ),
        "table_input": (
            r"\input{paper/tables/finite-threshold-summary-ko.tex}"
        ),
        "initial_cases": (
            (
                r"모든 \(9\le m\le15\)에서 base selector",
                r"1,2,2,3,4,6,10",
            ),
            (
                r"\(m=16\)에서는 \(191,227,233\)",
                "완전 mask가 같아",
            ),
        ),
        "synthesis_cases": (
            (
                r"\(L_{27}^\star=87\)",
                r"\(L_{28}^\star=104\)",
                r"\(\{11867,12791\}\)",
                "다섯 좌표 subcertificate",
            ),
            (
                r"L_{29}^\star=103<L_{28}^\star=104",
                r"\{18979,21031\}",
                "phi4:87:95:103:cofactor",
            ),
            (
                r"L_{34}^\star=201",
                r"\{97927,99527\}",
                "phi6:149:201:45:cofactor",
            ),
        ),
    },
}

TABLE_ROW_PATTERN = re.compile(
    r"^(\d+) & (\d+) & (\d+) & (-?\d+) & ([^&]+) & "
    r"([^&]+) & ([^&]+) & ([^\n]+) \\\\$",
    re.MULTILINE,
)
CLAIM_PATTERN = re.compile(
    r"\\claimstatus\{([A-Z]+-\d{3})\}\{([A-Z]+)\}"
)
SUBSECTION_PATTERN = re.compile(r"^\\subsection\{.*\}$", re.MULTILINE)


def normalize(text: str) -> str:
    """Normalize layout-only whitespace for exact prose anchors."""
    return " ".join(text.split())


def parse_collision_cell(cell: str) -> tuple[tuple[int, ...], ...] | None:
    """Parse one rendered predecessor-collision cell."""
    groups = re.findall(r"\\\{([^}]*)\\\}", cell)
    if not groups:
        return None
    return tuple(
        tuple(int(value.strip()) for value in group.split(","))
        for group in groups
    )


def parse_repair_cell(cell: str) -> int | None:
    """Parse a rendered repair-coordinate count."""
    stripped = cell.strip()
    if stripped in {"--", "n.c."}:
        return None
    return int(stripped)


def expected_repair_status(input_length: int) -> str:
    """Return the exact row-level repair certification status."""
    if input_length <= 15:
        return "NOT_APPLICABLE_DOMAIN_FLOOR"
    if input_length <= 25:
        return "NOT_SEPARATELY_CERTIFIED"
    return "CERTIFIED_MINIMUM"


def table_repair_status(cell: str) -> str:
    """Map one rendered repair cell to its exact status class."""
    stripped = cell.strip()
    if stripped == "--":
        return "NOT_APPLICABLE_DOMAIN_FLOOR"
    if stripped == "n.c.":
        return "NOT_SEPARATELY_CERTIFIED"
    int(stripped)
    return "CERTIFIED_MINIMUM"


def expected_endpoint_cell(input_length: int, cap: int) -> str:
    """Render the independently derived reduced strict endpoint."""
    endpoint = Fraction(cap - 1, input_length)
    if endpoint.denominator == 1:
        return str(endpoint.numerator)
    return (
        rf"\(\frac{{{endpoint.numerator}}}"
        rf"{{{endpoint.denominator}}}\)"
    )


def parse_table_rows(text: str) -> tuple[ThresholdRow, ...]:
    """Parse the semantic columns of a generated LaTeX table."""
    rows: list[ThresholdRow] = []
    for match in TABLE_ROW_PATTERN.finditer(text):
        (
            input_length,
            population_size,
            cap,
            offset,
            _endpoint,
            collision_cell,
            repair_cell,
            evidence_cell,
        ) = match.groups()
        parsed_input_length = int(input_length)
        parsed_cap = int(cap)
        if _endpoint.strip() != expected_endpoint_cell(
            parsed_input_length,
            parsed_cap,
        ):
            raise AssertionError(
                f"length {input_length} strict endpoint drifted"
            )
        if table_repair_status(repair_cell) != expected_repair_status(
            parsed_input_length
        ):
            raise AssertionError(
                f"length {input_length} repair status drifted"
            )
        rows.append(
            ThresholdRow(
                parsed_input_length,
                int(population_size),
                parsed_cap,
                int(offset),
                parse_collision_cell(collision_cell),
                parse_repair_cell(repair_cell),
                tuple(re.findall(r"\\texttt\{([^}]+)\}", evidence_cell)),
            )
        )
    return tuple(rows)


def require_int(mapping: dict[str, object], key: str) -> int:
    """Read one non-boolean integer from a decoded JSON object."""
    value = mapping.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise AssertionError(f"artifact field {key} is not an integer")
    return value


def parse_artifact_collisions(
    value: object,
) -> tuple[tuple[int, ...], ...] | None:
    """Parse the frozen artifact's nested collision buckets."""
    if value is None:
        return None
    if not isinstance(value, list):
        raise AssertionError("artifact collision buckets are not a list")
    buckets: list[tuple[int, ...]] = []
    for raw_bucket in value:
        if not isinstance(raw_bucket, list):
            raise AssertionError("artifact collision bucket is not a list")
        bucket: list[int] = []
        for raw_prime in raw_bucket:
            if not isinstance(raw_prime, int) or isinstance(raw_prime, bool):
                raise AssertionError("artifact collision prime is not an integer")
            bucket.append(raw_prime)
        buckets.append(tuple(bucket))
    return tuple(buckets)


def parse_artifact_rows(text: str) -> tuple[ThresholdRow, ...]:
    """Decode the semantic row registry from the frozen M50 artifact."""
    decoded = json.loads(text)
    if not isinstance(decoded, dict):
        raise AssertionError("artifact root is not an object")
    root = cast(dict[str, object], decoded)
    raw_rows = root.get("rows")
    if not isinstance(raw_rows, list):
        raise AssertionError("artifact rows are not a list")

    rows: list[ThresholdRow] = []
    for raw_row in raw_rows:
        if not isinstance(raw_row, dict):
            raise AssertionError("artifact row is not an object")
        row = cast(dict[str, object], raw_row)
        raw_repair = row.get("repair_coordinate_count")
        if raw_repair is not None and (
            not isinstance(raw_repair, int) or isinstance(raw_repair, bool)
        ):
            raise AssertionError("artifact repair count is not an integer")
        raw_evidence = row.get("evidence_ids")
        if not isinstance(raw_evidence, list) or not all(
            isinstance(item, str) for item in raw_evidence
        ):
            raise AssertionError("artifact evidence IDs are invalid")
        input_length = require_int(row, "input_length")
        cap = require_int(row, "family_relative_minimal_cap")
        raw_status = row.get("repair_coordinate_status")
        if raw_status != expected_repair_status(input_length):
            raise AssertionError(
                f"artifact length {input_length} repair status drifted"
            )
        raw_endpoint = row.get("strict_endpoint")
        if not isinstance(raw_endpoint, dict):
            raise AssertionError("artifact strict endpoint is not an object")
        endpoint = cast(dict[str, object], raw_endpoint)
        reduced = Fraction(cap - 1, input_length)
        expected_endpoint = {
            "numerator": cap - 1,
            "denominator": input_length,
            "reduced_numerator": reduced.numerator,
            "reduced_denominator": reduced.denominator,
        }
        if endpoint != expected_endpoint:
            raise AssertionError(
                f"artifact length {input_length} strict endpoint drifted"
            )
        rows.append(
            ThresholdRow(
                input_length,
                require_int(row, "population_size"),
                cap,
                require_int(row, "local_offset"),
                parse_artifact_collisions(
                    row.get("predecessor_collision_buckets")
                ),
                raw_repair,
                tuple(cast(list[str], raw_evidence)),
            )
        )
    return tuple(rows)


def validate_table_text(language: str, text: str) -> tuple[ThresholdRow, ...]:
    """Validate one complete rendered 26-row chronology."""
    if language not in PAPER_CONFIG:
        raise AssertionError(f"unknown language: {language}")
    rows = parse_table_rows(text)
    if rows != EXPECTED_ROWS:
        raise AssertionError(f"{language} threshold table rows drifted")
    return rows


def validate_artifact_text(text: str) -> tuple[ThresholdRow, ...]:
    """Validate the frozen artifact against the independent row registry."""
    rows = parse_artifact_rows(text)
    if rows != EXPECTED_ROWS:
        raise AssertionError("frozen M50 threshold rows drifted")
    return rows


def section_between(text: str, start: str, end: str) -> str:
    """Return a section slice between two exact headings."""
    start_index = text.find(start)
    end_index = text.find(end, start_index + len(start))
    if start_index < 0 or end_index < 0:
        raise AssertionError("required finite-paper section boundary missing")
    return text[start_index:end_index]


def validate_case_fragments(
    section: str,
    cases: tuple[tuple[str, ...], ...],
    label: str,
) -> None:
    """Require every semantic fragment for each representative case."""
    normalized = normalize(section)
    for index, fragments in enumerate(cases, start=1):
        for fragment in fragments:
            if fragment not in normalized:
                raise AssertionError(
                    f"{label} representative case {index} drifted"
                )


def validate_paper_text(language: str, text: str) -> int:
    """Validate one finite paper's main/appendix chronology boundary."""
    if language not in PAPER_CONFIG:
        raise AssertionError(f"unknown language: {language}")
    config = PAPER_CONFIG[language]
    marker = r"\appendix"
    if text.count(marker) != 1:
        raise AssertionError(f"{language} appendix boundary count changed")
    main, appendix = text.split(marker, 1)
    table_input = config["table_input"]
    if not isinstance(table_input, str):
        raise AssertionError("table input configuration is invalid")
    if table_input in main:
        raise AssertionError(f"{language} full chronology remains in main")
    if appendix.count(table_input) != 1:
        raise AssertionError(f"{language} appendix chronology input drifted")

    subsections = tuple(SUBSECTION_PATTERN.findall(appendix))
    if subsections != config["subsections"]:
        raise AssertionError(f"{language} chronology subsection order drifted")
    if appendix.find(subsections[0]) > appendix.find(table_input):
        raise AssertionError(f"{language} chronology precedes its heading")
    if appendix.find(table_input) > appendix.find(subsections[1]):
        raise AssertionError(f"{language} chronology follows reproduction")

    initial_section = cast(str, config["initial_section"])
    synthesis_section = cast(str, config["synthesis_section"])
    barrier_section = cast(str, config["barrier_section"])
    if not all(
        isinstance(value, str)
        for value in (initial_section, synthesis_section, barrier_section)
    ):
        raise AssertionError("section configuration is invalid")
    initial = section_between(main, initial_section, synthesis_section)
    synthesis = section_between(main, synthesis_section, barrier_section)
    initial_cases = cast(
        tuple[tuple[str, ...], ...],
        config["initial_cases"],
    )
    synthesis_cases = cast(
        tuple[tuple[str, ...], ...],
        config["synthesis_cases"],
    )
    if not isinstance(initial_cases, tuple) or not isinstance(
        synthesis_cases, tuple
    ):
        raise AssertionError("case configuration is invalid")
    validate_case_fragments(initial, initial_cases, f"{language} initial")
    validate_case_fragments(
        synthesis,
        synthesis_cases,
        f"{language} synthesis",
    )

    claims_main = tuple(
        claim_id
        for claim_id, status in CLAIM_PATTERN.findall(main)
        if status == "PROVED"
    )
    claims_all = tuple(
        claim_id for claim_id, _status in CLAIM_PATTERN.findall(text)
    )
    if claims_main != EXPECTED_CLAIMS or claims_all != claims_main:
        raise AssertionError(f"{language} claim placement or status drifted")
    return len(initial_cases) + len(synthesis_cases)


def validate_all() -> tuple[int, int]:
    """Validate both papers, both tables, and the frozen artifact."""
    validate_artifact_text(ARTIFACT.read_text(encoding="utf-8"))

    case_counts: list[int] = []
    table_counts: list[int] = []
    for language in ("en", "ko"):
        paper_text = (
            FOCUSED / f"finite-certificates-{language}.tex"
        ).read_text(encoding="utf-8")
        table_text = (
            TABLES / f"finite-threshold-summary-{language}.tex"
        ).read_text(encoding="utf-8")
        case_counts.append(validate_paper_text(language, paper_text))
        table_counts.append(len(validate_table_text(language, table_text)))
    if len(set(case_counts)) != 1 or len(set(table_counts)) != 1:
        raise AssertionError("bilingual chronology counts drifted")
    return case_counts[0], table_counts[0]


def main() -> int:
    """Run the complete M90 chronology-boundary gate."""
    cases, rows = validate_all()
    print(
        "M90 finite-chronology checker: PASS "
        f"(2 papers, {cases} main representative cases each, "
        f"{rows} appendix rows each, {len(EXPECTED_CLAIMS)} main claims each)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
