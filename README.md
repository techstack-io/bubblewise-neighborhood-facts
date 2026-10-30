# BubbleWise Neighborhood Facts Engine (Streamlit)

A small deterministic fact-generation prototype. It retrieves county-level ACS 2024 five-year statistics and generates fixed, sourced statements without an LLM.

## Run locally

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit (typically http://localhost:8501).

Select **Illustrative sample data** to test without internet. For live data, use **State FIPS = 17**, **County FIPS = 031** for Cook County, Illinois. The app requests the Census API; a network connection is required.

## Test

```bash
python -m pytest -q
```

## How it works

- `app.py`: Streamlit interface
- `census_client.py`: Census API request and basic response validation
- `fact_generator.py`: Pure functions that generate reproducible, source-labeled statements
- `tests/test_facts.py`: Determinism and missing-value tests

## Limits

- County-level data only. Do not call it neighborhood- or property-level data.
- ACS values are survey estimates, not precise current statistics. Margins of error are not displayed in v1.
- Sample values are fabricated and labeled as such.
- No LLM, AVM, renovation estimator, or user address lookup.
- Live Census API has not been tested from this offline environment.
