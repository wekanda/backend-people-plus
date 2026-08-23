STAFF_DEPENDANTS = {
    "name": "STAFF DEPENDANTS FORM",
    "key": "staff_dependants",
    "category": "Employee Records",
    "description": "Register of staff dependants (for benefits, next-of-kin and insurance).",
    "fields": [
        {"name": "date", "label": "Date", "type": "date", "required": True},
        {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "employee_no", "label": "Employee No.", "type": "text", "required": False},
        {"name": "position", "label": "Position", "type": "text", "required": False},
        {"name": "department", "label": "Department / Project", "type": "text", "required": False},
        {"name": "depend1_name", "label": "Dependant 1 - Name", "type": "text", "required": False},
        {"name": "depend1_relation", "label": "Dependant 1 - Relationship", "type": "text", "required": False},
        {"name": "depend1_dob", "label": "Dependant 1 - DOB", "type": "date", "required": False},
        {"name": "depend2_name", "label": "Dependant 2 - Name", "type": "text", "required": False},
        {"name": "depend2_relation", "label": "Dependant 2 - Relationship", "type": "text", "required": False},
        {"name": "depend2_dob", "label": "Dependant 2 - DOB", "type": "date", "required": False},
        {"name": "depend3_name", "label": "Dependant 3 - Name", "type": "text", "required": False},
        {"name": "depend3_relation", "label": "Dependant 3 - Relationship", "type": "text", "required": False},
        {"name": "depend3_dob", "label": "Dependant 3 - DOB", "type": "date", "required": False},
        {"name": "next_of_kin", "label": "Next of Kin (if not a dependant above)", "type": "text", "required": False},
        {"name": "next_of_kin_contact", "label": "Next of Kin Contact", "type": "text", "required": False},
        {"name": "prepared_by", "label": "Prepared By", "type": "text", "required": False, "default": "People & Culture Department"},
    ],
    "template": """
<h1>STAFF DEPENDANTS FORM</h1>
<p class="right">{h(date)}</p>
<div class="spacer-sm"></div>
<table class="info">
<tr><td class="k">Employee Name</td><td>{h(employee_name)}</td><td class="k">Employee No.</td><td>{h(employee_no)}</td></tr>
<tr><td class="k">Position</td><td>{h(position)}</td><td class="k">Department / Project</td><td>{h(department)}</td></tr>
</table>
<h3>DEPENDANTS</h3>
<table class="bordered">
<tr><th style="width:40%">Name</th><th style="width:30%">Relationship</th><th style="width:30%">Date of Birth</th></tr>
<tr><td>{h(depend1_name)}</td><td>{h(depend1_relation)}</td><td>{hd(depend1_dob)}</td></tr>
<tr><td>{h(depend2_name)}</td><td>{h(depend2_relation)}</td><td>{hd(depend2_dob)}</td></tr>
<tr><td>{h(depend3_name)}</td><td>{h(depend3_relation)}</td><td>{hd(depend3_dob)}</td></tr>
</table>
<h3>NEXT OF KIN</h3>
<table class="info">
<tr><td class="k">Next of Kin</td><td>{h(next_of_kin)}</td><td class="k">Contact</td><td>{h(next_of_kin_contact)}</td></tr>
</table>
<div class="spacer-md"></div>
<p>I confirm that the dependants listed above are accurate and will notify People &amp; Culture of any changes.</p>
<p class="spacer-sm"> </p>
<p>Employee: {h(employee_name)} &nbsp; Signature: {sign_dots} &nbsp; Date: {h(date)}</p>
<p>Prepared by: {h(prepared_by)} &nbsp; Date: {sign_dots}</p>
""",
}