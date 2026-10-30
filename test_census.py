import requests
import streamlit as st

url = "https://api.census.gov/data/2024/acs/acs5"

params = {
    "get": "NAME,B19013_001E,B25003_001E,B25003_002E",
    "for": "county:031",
    "in": "state:17",
    "key": st.secrets["CENSUS_API_KEY"],
}

response = requests.get(url, params=params, timeout=20)

print("STATUS:", response.status_code)
print("CONTENT TYPE:", response.headers.get("Content-Type"))
print("BODY:", repr(response.text[:500]))