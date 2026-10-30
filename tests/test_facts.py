from fact_generator import SAMPLE_RECORD, generate_facts


def test_sample_is_deterministic():
    first = generate_facts(SAMPLE_RECORD)
    assert first == generate_facts(SAMPLE_RECORD)
    assert len(first) == 2
    assert "$92,500" in first[0].statement
    assert "62.0%" in first[1].statement


def test_missing_income_is_not_invented():
    record = {**SAMPLE_RECORD, "B19013_001E": "-666666666"}
    assert len(generate_facts(record)) == 1


def test_invalid_ownership_is_not_published():
    record = {**SAMPLE_RECORD, "B25003_002E": "20000"}
    assert len(generate_facts(record)) == 1
