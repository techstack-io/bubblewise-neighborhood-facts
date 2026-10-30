import streamlit as st
from census_client import CensusDataError, fetch_county
from fact_generator import SAMPLE_RECORD, SOURCE_URL, generate_facts

st.set_page_config(page_title="BubbleWise | Neighborhood Facts", page_icon="🏠", layout="centered")
st.title("Neighborhood Facts Engine")
st.caption("BubbleWise technical prototype · Verified data + deterministic templates")
st.info("This is a learning prototype, not a property valuation or a live neighborhood assessment.")

with st.sidebar:
    st.header("Data source")
    mode = st.radio("Choose mode", ["Live Census API", "Illustrative sample data"])
    st.markdown(f"[ACS documentation]({SOURCE_URL})")
    st.caption("Live mode uses ACS 2024 five-year county estimates. These are survey estimates, not current property-level facts.")

st.subheader("Select a geographic area")
state = st.text_input("State FIPS code", value="17", max_chars=2, disabled=mode != "Live Census API")
county = st.text_input("County FIPS code", value="031", max_chars=3, disabled=mode != "Live Census API")
st.caption("Example: Illinois = 17; Cook County = 031. Keep leading zeros.")

if st.button("Generate verified facts", type="primary", use_container_width=True):
    if mode == "Illustrative sample data":
        record = SAMPLE_RECORD
        st.warning("SAMPLE MODE: The values below are invented for demonstration, not Census results.")
    else:
        try:
            with st.spinner("Retrieving Census statistics…"):
                record = fetch_county(state.strip(), county.strip())
        except (ValueError, CensusDataError) as exc:
            st.error(str(exc))
            st.stop()
    try:
        facts = generate_facts(record)
    except ValueError as exc:
        st.error(str(exc))
        st.stop()
    if not facts:
        st.warning("No valid statistics were available. The system will not invent missing values.")
    else:
        st.subheader("Generated facts")
        for fact in facts:
            with st.container(border=True):
                st.write(fact.statement)
                st.caption(f"Source: {fact.source} · Geography: {fact.geography} · Variable(s): {fact.variable}")
        st.success(f"Generated {len(facts)} reproducible facts without an LLM.")
        st.download_button(
            "Download statements",
            data="\n\n".join(f.statement + f"\nSource: {f.source}; Variables: {f.variable}" for f in facts),
            file_name="neighborhood_facts.txt",
            mime="text/plain",
        )

st.divider()
with st.expander("How this prevents hallucinated facts"):
    st.markdown("""1. Retrieve numerical values from the Census API.\n2. Reject missing or invalid estimates.\n3. Populate fixed sentence templates.\n4. Display the source, geography, reporting year, and variables.\n\n**Important:** Deterministic generation prevents the application from inventing numbers, but it does not guarantee the underlying source is error-free. ACS values are estimates and have margins of error.""")
