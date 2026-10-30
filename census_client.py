
import requests
import streamlit as st


class CensusDataError(Exception):
    """Raised when Census data cannot be retrieved or validated."""
    pass


def fetch_county(state: str, county: str, year: int = 2024):
    """Retrieve county-level ACS statistics."""

    if not (state.isdigit() and len(state) == 2):
        raise ValueError("State FIPS must contain exactly 2 digits.")

    if not (county.isdigit() and len(county) == 3):
        raise ValueError("County FIPS must contain exactly 3 digits.")

    url = f"https://api.census.gov/data/{year}/acs/acs5"

    params = {
        "get": "NAME,B19013_001E,B25003_001E,B25003_002E",
        "for": f"county:{county}",
        "in": f"state:{state}",
        "key": st.secrets["CENSUS_API_KEY"],
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        if "json" not in response.headers.get(
            "Content-Type", ""
        ).lower():
            raise CensusDataError(
                "Census API returned a non-JSON response. "
                f"HTTP status: {response.status_code}"
            )

        rows = response.json()

    except requests.RequestException as exc:
        raise CensusDataError(
            f"Census API request failed: {exc}"
        ) from exc

    except ValueError as exc:
        raise CensusDataError(
            f"Invalid Census API response: {exc}"
        ) from exc

    if len(rows) < 2:
        raise CensusDataError(
            "Census API returned no county data."
        )

    if len(rows[0]) != len(rows[1]):
        raise CensusDataError(
            "Census API returned mismatched columns."
        )

    record = dict(zip(rows[0], rows[1]))

    # Preserve the original field names expected by fact_generator.py
    return record
