LEAVE_TRACKER = {
    "name": "LEAVE TRACKER",
    "key": "leave_tracker",
    "category": "Leave",
    "description": "Staff leave entitlement tracker aligned with LEAVE TRACKER.xlsx.",
    "fields": [
        {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "employee_id", "label": "Employee No.", "type": "text", "required": True},
        {"name": "designation", "label": "Designation", "type": "text", "required": False},
        {"name": "project", "label": "Department / Project", "type": "text", "required": False},
        {"name": "year", "label": "Year", "type": "text", "required": True, "default": "2026"},
        {"name": "annual_entitled", "label": "Annual Leave Entitled (days)", "type": "number", "required": False, "default": "21"},
        {"name": "annual_taken", "label": "Annual Leave Taken (days)", "type": "number", "required": False},
        {"name": "sick_entitled", "label": "Sick Leave Entitled (days)", "type": "number", "required": False},
        {"name": "sick_taken", "label": "Sick Leave Taken (days)", "type": "number", "required": False},
        {"name": "maternity_entitled", "label": "Maternity Leave Entitled (days)", "type": "number", "required": False, "default": "60"},
        {"name": "maternity_taken", "label": "Maternity Leave Taken (days)", "type": "number", "required": False},
        {"name": "paternity_entitled", "label": "Paternity Leave Entitled (days)", "type": "number", "required": False, "default": "4"},
        {"name": "paternity_taken", "label": "Paternity Leave Taken (days)", "type": "number", "required": False},
        {"name": "compassionate_taken", "label": "Compassionate / Study / Other Taken (days)", "type": "number", "required": False},
        {"name": "remarks", "label": "Remarks", "type": "longtext", "required": False},
    ],
    "template": """
<h1>LEAVE TRACKER</h1>
<p class="center">Financial Year {h(year)}</p>
<table class="info">
<tr><td class="k">Employee Name</td><td>{h(employee_name)}</td><td class="k">Employee No.</td><td>{h(employee_id)}</td></tr>
<tr><td class="k">Designation</td><td>{h(designation)}</td><td class="k">Department / Project</td><td>{h(project)}</td></tr>
</table>
<div class="spacer-sm"></div>
<table class="bordered">
<tr><th>Leave Type</th><th style="width:18%">Entitled (days)</th><th style="width:18%">Taken (days)</th><th style="width:18%">Balance</th></tr>
<tr><td>Annual Leave</td><td>{h(annual_entitled)}</td><td>{h(annual_taken)}</td><td><span class="bold">{h(annual_balance)}</span></td></tr>
<tr><td>Sick Leave</td><td>{h(sick_entitled)}</td><td>{h(sick_taken)}</td><td><span class="bold">{h(sick_balance)}</span></td></tr>
<tr><td>Maternity Leave</td><td>{h(maternity_entitled)}</td><td>{h(maternity_taken)}</td><td><span class="bold">{h(maternity_balance)}</span></td></tr>
<tr><td>Paternity Leave</td><td>{h(paternity_entitled)}</td><td>{h(paternity_taken)}</td><td><span class="bold">{h(paternity_balance)}</span></td></tr>
<tr><td>Compassionate / Study / Other</td><td></td><td>{h(compassionate_taken)}</td><td></td></tr>
</table>
<div class="spacer-sm"></div>
<p><span class="bold">Remarks:</span></p>
<p>{h(remarks)}</p>
<p class="spacer-sm"> </p>
<p>Prepared by: {sign_dots} &nbsp; Date: {sign_dots} &nbsp;&nbsp;&nbsp; Approved by: {sign_dots} &nbsp; Date: {sign_dots}</p>
""",
}