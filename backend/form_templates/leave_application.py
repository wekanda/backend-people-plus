LEAVE_APPLICATION = {
    "name": "LEAVE APPLICATION FORM",
    "key": "leave_application",
    "category": "Leave",
    "description": "Staff leave application with automatic day computation (TPO Uganda).",
    "fields": [
        {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "employee_id", "label": "Employee No.", "type": "text", "required": True},
        {"name": "designation", "label": "Designation", "type": "text", "required": True},
        {"name": "department", "label": "Department / Project", "type": "text", "required": False},
        {"name": "date_of_appointment", "label": "Date of Appointment", "type": "date", "required": False},
        {"name": "leave_type", "label": "Leave Type", "type": "select",
         "options": ["Annual Leave", "Sick Leave", "Maternity Leave", "Paternity Leave", "Compassionate Leave", "Study Leave", "Other"],
         "required": True},
        {"name": "days", "label": "Number of Days", "type": "number", "required": True},
        {"name": "from_date", "label": "From Date", "type": "date", "required": True},
        {"name": "to_date", "label": "To Date", "type": "date", "required": True},
        {"name": "return_date", "label": "Date of Return", "type": "date", "required": True},
        {"name": "computation_notes", "label": "Computation / Remarks", "type": "longtext", "required": False},
        {"name": "leave_balance", "label": "Leave Balance (days)", "type": "number", "required": False},
    ],
    "template": """
<h1>LEAVE APPLICATION</h1>
<table class="info">
<tr><td class="k">Employee Name</td><td>{h(employee_name)}</td><td class="k">Employee No.</td><td>{h(employee_id)}</td></tr>
<tr><td class="k">Designation</td><td>{h(designation)}</td><td class="k">Department / Project</td><td>{h(department)}</td></tr>
<tr><td class="k">Date of Appointment</td><td>{h(date_of_appointment)}</td></tr>
</table>
<div class="spacer-sm"></div>
<p>I, <span class="field-value">{h(employee_name, '...')}</span>, humbly request to be granted <span class="bold">{h(leave_type)}</span> of <span class="bold">{h(days)} day(s)</span> as indicated below:</p>
<table class="info">
<tr><td class="k">From</td><td>{h(from_date)}</td><td class="k">To</td><td>{h(to_date)}</td></tr>
<tr><td class="k">Date of Return</td><td>{h(return_date)}</td><td class="k">Leave Balance</td><td>{h(leave_balance)} days</td></tr>
</table>
<p><span class="bold">Computation / Remarks:</span></p>
<p>{h(computation_notes)}</p>
<div class="spacer-md"></div>
<p>Signature: {sign_dots}</p>
<p class="spacer-sm"> </p>
<p><span class="bold">Supervisor Recommendation:</span></p>
<p>Approved / Rejected &nbsp;&nbsp; <i>(circle where applicable)</i></p>
<p>Signature: {sign_dots} &nbsp; Date: {sign_dots}</p>
<p class="spacer-sm"> </p>
<p><span class="bold">People &amp; Culture / Admin Approval:</span></p>
<p>Approved / Rejected &nbsp;&nbsp; <i>(circle where applicable)</i></p>
<p>Signature: {sign_dots} &nbsp; Date: {sign_dots}</p>
""",
}