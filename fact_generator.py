"""Pure, deterministic functions: no LLM and no network calls."""
from dataclasses import dataclass

YEAR = 2024
SOURCE = "U.S. Census Bureau, American Community Survey (ACS) 2024 5-year estimates"
SOURCE_URL = "https://www.census.gov/programs-surveys/acs"
# Census uses large negative sentinel values for unavailable estimates.


@dataclass(frozen=True)
class Fact:
    statement: str
    source: str
    variable: str
    geography: str
    year: int = YEAR


def valid_nonnegative_int(raw):
    try:
        n = int(raw)
    except (TypeError, ValueError):
        return None
    return n if n >= 0 else None


def generate_facts(record: dict) -> list[Fact]:
    name = record.get("NAME", "").strip()
    if not name:
        raise ValueError("A geographic name is required.")
    facts = []
    income = valid_nonnegative_int(record.get("B19013_001E"))
    if income is not None:
        facts.append(Fact(
            f"In {name}, estimated median household income was ${income:,.0f} "
            f"(ACS {YEAR} 5-year estimates).",
            SOURCE, "B19013_001E", name,
        ))
    occupied = valid_nonnegative_int(record.get("B25003_001E"))
    owner = valid_nonnegative_int(record.get("B25003_002E"))
    if occupied and owner is not None and owner <= occupied:
        rate = owner / occupied * 100
        facts.append(Fact(
            f"In {name}, approximately {rate:.1f}% of occupied housing units "
            f"were owner-occupied (ACS {YEAR} 5-year estimates).",
            SOURCE, "B25003_001E, B25003_002E", name,
        ))
    return facts


SAMPLE_RECORD = {
    "NAME": "Example County, Example State",
    "B19013_001E": "92500",
    "B25003_001E": "10000",
    "B25003_002E": "6200",
}
