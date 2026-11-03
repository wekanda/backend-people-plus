import json
import re
import sys
import unicodedata
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "People_Pulse_Unified_Master_Specification ..docx"
OUTPUT = ROOT / "people-pluse-frontend" / "src" / "data" / "specificationCatalog.json"
BACKEND_OUTPUT = ROOT / "specification" / "catalog.json"

MODULES = {
    "people": "People & Culture",
    "procurement": "Procurement & Supply Chain",
    "finance": "Finance & Administration",
    "assets": "Asset Management",
    "shared": "Shared Platform",
}

FORM_EXCLUSIONS = (
    "recommended ", "dashboard kpi", "key workflow integration", "ai data sources",
    "example ai", "example questions", "end-to-end workflow", "core treasury formula",
)


def slug(value):
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", normalized).strip("_") or "record"


def module_for(text, fallback):
    value = text.lower()
    if any(word in value for word in ("asset", "depreciation", "maintenance reminder", "disposal approval")):
        return "assets"
    if any(word in value for word in ("procurement", "purchase requisition", "purchase order", "quotation", "tender", "rfq", "vendor onboarding")):
        return "procurement"
    if any(word in value for word in ("finance", "invoice", "payment", "payroll", "budget", "tax", "treasury", "cash", "audit", "account payable", "account receivable", "expense claim")):
        return "finance"
    if any(word in value for word in ("people & culture", "human resource", "employee", "staff", "recruitment", "leave", "attendance", "performance", "training", "hr ")):
        return "people"
    return fallback


def field_type(label):
    value = label.lower()
    if any(word in value for word in ("date", "time", "timestamp", "period start", "period end")):
        return "date" if "time" not in value and "timestamp" not in value else "datetime-local"
    if "email" in value:
        return "email"
    if "phone" in value or "mobile" in value:
        return "tel"
    if any(word in value for word in ("yes/no", "indicator", "is active", "is approved", "is required", "duplicate check")):
        return "boolean"
    if any(word in value for word in ("amount", "balance", "quantity", "count", "number of", "total", "rate", "score", "percentage", "percent", "cost", "value", "salary", "tax", "days overdue", "exchange rate", "variance", "utilisation", "utilization", "age in days")):
        return "number"
    if any(word in value for word in ("description", "comments", "notes", "reason", "justification", "summary", "address", "recommendation", "explanation", "details", "narrative", "action plan")):
        return "textarea"
    return "text"


def is_form_heading(paragraph, text, depth):
    style = paragraph.style.name if paragraph.style else ""
    lowered = text.lower()
    if any(token in lowered for token in FORM_EXCLUSIONS):
        return False
    if text.startswith("#"):
        return depth <= 2
    if style == "Heading 1":
        return True
    if style in ("Heading 2", "Heading 3"):
        return True
    if text == text.upper() and any(character.isalpha() for character in text) and len(text) >= 12:
        return True
    if re.match(r"^\d{1,2}(?:\.\d{1,2})+\s+[A-Z]", text) and len(text) < 120:
        return True
    if re.match(r"^\d{1,2}\.\s+[A-Z]", text) and len(text) < 100:
        return True
    return False


def is_section_heading(paragraph, text, depth):
    style = paragraph.style.name if paragraph.style else ""
    return (text.startswith("#") and depth > 2) or style in ("Heading 2", "Heading 3")


def is_field_label(paragraph, text):
    if not text or len(text) > 140 or text.endswith((".", "!", "?", ":")):
        return False
    if text.startswith(("http://", "https://", "→", "↓")):
        return False
    if text.count(" ") > 18:
        return False
    return True


def extract_catalog(source=SOURCE):
    document = Document(source)
    forms = []
    current_form = None
    current_module = "shared"
    current_section = "General"

    def finish_form():
        nonlocal current_form
        if current_form and current_form["fields"]:
            forms.append(current_form)
        current_form = None

    def begin_form(title, index):
        nonlocal current_form, current_module, current_section
        finish_form()
        module = module_for(title, current_module)
        current_module = module
        current_section = "General"
        current_form = {
            "key": f"spec_{module}_{slug(title)}_{index}",
            "module": module,
            "module_label": MODULES[module],
            "title": title.strip("# "),
            "source_paragraph": index,
            "fields": [],
        }

    for index, paragraph in enumerate(document.paragraphs):
        text = paragraph.text.strip()
        if not text:
            continue

        module = module_for(text, current_module)
        if module != current_module and any(
            marker in text.lower()
            for marker in ("people & culture department", "human resource", "finance department", "procurement department", "asset management")
        ):
            current_module = module

        depth = len(text) - len(text.lstrip("#")) if text.startswith("#") else 0
        if is_form_heading(paragraph, text, depth):
            begin_form(text.lstrip("# "), index)
            continue
        if is_section_heading(paragraph, text, depth):
            current_section = text.lstrip("# ")
            continue
        if not is_field_label(paragraph, text):
            continue
        if current_form is None:
            begin_form("Specification Data Points", index)

        field_name = slug(text)
        existing = {field["name"] for field in current_form["fields"]}
        suffix = 2
        unique_name = field_name
        while unique_name in existing:
            unique_name = f"{field_name}_{suffix}"
            suffix += 1
        current_form["fields"].append({
            "name": unique_name,
            "label": text,
            "type": field_type(text),
            "section": current_section,
            "source_paragraph": index,
        })

    finish_form()

    for table_index, table in enumerate(document.tables, start=1):
        headers = [cell.text.strip().replace("\n", " ") for cell in table.rows[0].cells]
        headers = [header for header in headers if header]
        if not headers:
            continue
        header_text = " ".join(headers).lower()
        if "critical audit" in header_text:
            title = "Finance Module Audit Requirements"
        elif "transaction value" in header_text and "approval level" in header_text:
            title = "Approval Threshold Matrix"
        else:
            title = f"Specification Table {table_index}"
        module = module_for(title, current_module)
        fields = []
        for label in headers:
            name = slug(label)
            suffix = 2
            while any(field["name"] == name for field in fields):
                name = f"{slug(label)}_{suffix}"
                suffix += 1
            fields.append({
                "name": name,
                "label": label,
                "type": field_type(label),
                "section": "General",
                "source_paragraph": len(document.paragraphs) + table_index,
            })
        rows = [
            [cell.text.strip().replace("\n", " ") for cell in row.cells]
            for row in table.rows[1:]
        ]
        source_index = len(document.paragraphs) + table_index
        forms.append({
            "key": f"spec_{module}_{slug(title)}_{source_index}",
            "module": module,
            "module_label": MODULES[module],
            "title": title,
            "source_paragraph": source_index,
            "fields": fields,
            "reference_table": {"columns": headers, "rows": rows},
        })

    forms = [form for form in forms if len(form["fields"]) > 0]
    payload = {
        "source": SOURCE.name,
        "modules": [{"key": key, "label": label} for key, label in MODULES.items()],
        "form_count": len(forms),
        "field_count": sum(len(form["fields"]) for form in forms),
        "forms": forms,
    }
    return payload


def main():
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else SOURCE
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else OUTPUT
    catalog = extract_catalog(source)
    serialized = json.dumps(catalog, ensure_ascii=False, indent=2)
    for target in {output, BACKEND_OUTPUT}:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(serialized, encoding="utf-8")
    print(f"Generated {catalog['form_count']} forms and {catalog['field_count']} data points from {source.name}")
    for module in catalog["modules"]:
        forms = [form for form in catalog["forms"] if form["module"] == module["key"]]
        print(f"{module['label']}: {len(forms)} forms, {sum(len(form['fields']) for form in forms)} fields")


if __name__ == "__main__":
    main()