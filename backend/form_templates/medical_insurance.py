MEDICAL_INSURANCE = {
    "name": "MEDICAL INSURANCE FORM",
    "key": "medical_insurance",
    "category": "Payroll & Benefits",
    "description": "Staff medical insurance registration - principal, spouse and up to two children.",
    "fields": [
        {"name": "date", "label": "Date", "type": "date", "required": True},
        {"name": "employee_name", "label": "Principal Name", "type": "text", "required": True},
        {"name": "employee_no", "label": "Employee No.", "type": "text", "required": False},
        {"name": "position", "label": "Position", "type": "text", "required": False},
        {"name": "department", "label": "Department / Project", "type": "text", "required": False},
        {"name": "duty_station", "label": "Duty Station / District", "type": "text", "required": False},
        {"name": "principal_dob", "label": "Principal DOB", "type": "date", "required": False},
        {"name": "principal_gender", "label": "Principal Gender", "type": "select", "options": ["Male", "Female"], "required": False},
        {"name": "principal_contact", "label": "Principal Contact", "type": "text", "required": False},
        {"name": "principal_email", "label": "Principal Email", "type": "text", "required": False},
        {"name": "spouse_name", "label": "Spouse Name", "type": "text", "required": False},
        {"name": "spouse_dob", "label": "Spouse DOB", "type": "date", "required": False},
        {"name": "spouse_gender", "label": "Spouse Gender", "type": "select", "options": ["Male", "Female"], "required": False},
        {"name": "child1_name", "label": "Child 1 Name", "type": "text", "required": False},
        {"name": "child1_dob", "label": "Child 1 DOB", "type": "date", "required": False},
        {"name": "child2_name", "label": "Child 2 Name", "type": "text", "required": False},
        {"name": "child2_dob", "label": "Child 2 DOB", "type": "date", "required": False},
        {"name": "insurance_category", "label": "Category", "type": "select",
         "options": ["Principal", "Principal + Spouse", "Family (Principal + Spouse + 2 Children)"],
         "required": False},
        {"name": "nin", "label": "National ID / NIN", "type": "text", "required": False},
        {"name": "prepared_by", "label": "Prepared By", "type": "text", "required": False, "default": "People & Culture Department"},
    ],
    "template": """
<h1>MEDICAL INSURANCE FORM</h1>
<p class="center">{h(date)}</p>
<div class="spacer-sm"></div>
<table class="info">
<tr><td class="k">Employee No.</td><td>{h(employee_no)}</td><td class="k">Insurance Category</td><td><span class="bold">{h(insurance_category)}</span></td></tr>
<tr><td class="k">Position</td><td>{h(position)}</td><td class="k">Department / Project</td><td>{h(department)}</td></tr>
<tr><td class="k">Duty Station / District</td><td>{h(duty_station)}</td></tr>
</table>
<h3>1. PRINCIPAL (Employee)</h3>
<table class="info">
<tr><td class="k">Full Name</td><td>{h(employee_name)}</td><td class="k">Gender</td><td>{h(principal_gender)}</td></tr>
<tr><td class="k">Date of Birth</td><td>{h(principal_dob)}</td><td class="k">National ID / NIN</td><td>{h(nin)}</td></tr>
<tr><td class="k">Contact No.</td><td>{h(principal_contact)}</td><td class="k">Email</td><td>{h(principal_email)}</td></tr>
</table>
<h3>2. SPOUSE</h3>
<table class="info">
<tr><td class="k">Full Name</td><td>{h(spouse_name)}</td><td class="k">Gender</td><td>{h(spouse_gender)}</td></tr>
<tr><td class="k">Date of Birth</td><td>{h(spouse_dob)}</td></tr>
</table>
<h3>3. CHILDREN (&le; 2)</h3>
<table class="bordered">
<tr><th>Name</th><th style="width:30%">Date of Birth</th></tr>
<tr><td>{h(child1_name)}</td><td>{h(child1_dob)}</td></tr>
<tr><td>{h(child2_name)}</td><td>{h(child2_dob)}</td></tr>
</table>
<div class="spacer-sm"></div>
<p>The above-listed members are hereby covered under the TPO Uganda staff medical insurance scheme. Declaration of any pre-existing conditions and documentation (IDs, birth certificates) shall be submitted with this form.</p>
<p class="spacer-sm"> </p>
<p>Prepared by: {h(prepared_by)} &nbsp; Signature: {sign_dots} &nbsp; Date: {sign_dots}</p>
<p>Approved by: {sign_dots} &nbsp; (People &amp; Culture Manager) &nbsp; Date: {sign_dots}</p>
""",
}