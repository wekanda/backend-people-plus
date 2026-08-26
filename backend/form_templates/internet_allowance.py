INTERNET_ALLOWANCE = {
    "name": "INTERNET BUNDLES / DATA ALLOWANCE REQUEST",
    "key": "internet_allowance",
    "category": "Payroll & Benefits",
    "description": "Staff internet / data bundles allowance for official remote work & research.",
    "fields": [
        {"name": "date", "label": "Date", "type": "date", "required": True},
        {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "employee_no", "label": "Employee No.", "type": "text", "required": False},
        {"name": "position", "label": "Position", "type": "text", "required": False},
        {"name": "department", "label": "Department / Project", "type": "text", "required": False},
        {"name": "period", "label": "Claim Period (Month/Year)", "type": "text", "required": True},
        {"name": "provider", "label": "Provider", "type": "select",
         "options": ["MTN", "Airtel", "Africell", "Liquid Home", "Other"], "required": True, "default": "MTN"},
        {"name": "bundle_size", "label": "Bundle Size (GB)", "type": "text", "required": False},
        {"name": "amount", "label": "Amount (UGX)", "type": "number", "required": True},
        {"name": "purpose", "label": "Purpose / Justification", "type": "longtext", "required": False},
        {"name": "approved_by", "label": "Approved By", "type": "text", "required": False, "default": "Program Manager"},
    ],
    "template": """
<h1>INTERNET BUNDLES ALLOWANCE REQUEST</h1>
<p class="right">{h(date)}</p>
<div class="spacer-sm"></div>
<table class="info">
<tr><td class="k">Employee Name</td><td>{h(employee_name)}</td><td class="k">Employee No.</td><td>{h(employee_no)}</td></tr>
<tr><td class="k">Position</td><td>{h(position)}</td><td class="k">Department / Project</td><td>{h(department)}</td></tr>
<tr><td class="k">Provider</td><td><span class="bold">{h(provider)}</span></td><td class="k">Claim Period</td><td>{h(period)}</td></tr>
</table>
<div class="spacer-sm"></div>
<h3>INTERNET BUNDLE DETAILS</h3>
<table class="bordered">
<tr><th>Bundle Size</th><th style="width:30%">Amount (UGX)</th></tr>
<tr><td>{h(bundle_size)} &mdash; {h(purpose)}</td><td class="right"><span class="bold">{hm(amount)}</span></td></tr>
</table>
<div class="spacer-md"></div>
<p>I request the above internet bundle allowance in line with the TPO Uganda staff benefits policy for official work (remote work, research, reporting).</p>
<p class="spacer-sm"> </p>
<p>Requested by: {h(employee_name)} &nbsp; Signature: {sign_dots} &nbsp; Date: {h(date)}</p>
<p>Approved by: {h(approved_by)} &nbsp; Signature: {sign_dots} &nbsp; Date: {sign_dots}</p>
""",
}