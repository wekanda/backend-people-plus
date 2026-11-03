from scripts.generate_specification_catalog import extract_catalog


def test_catalog_preserves_numbered_sections_and_source_tables():
    catalog = extract_catalog()
    forms = {form["title"]: form for form in catalog["forms"]}

    assert "19.1 Procurement Pipeline" in forms
    assert "19.6 Contract Status" in forms

    audit_table = forms["Finance Module Audit Requirements"]["reference_table"]
    assert audit_table["columns"] == ["Module", "Critical Audit Fields"]
    assert len(audit_table["rows"]) == 8
    assert audit_table["rows"][0] == [
        "Accounts Payable",
        "Who created, approved, modified, paid invoice",
    ]

    approval_table = forms["Approval Threshold Matrix"]["reference_table"]
    assert approval_table["columns"] == ["Transaction Value", "Approval Level"]
    assert len(approval_table["rows"]) == 5
    assert approval_table["rows"][-1][1] == "CEO / Board"