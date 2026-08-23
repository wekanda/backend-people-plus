CONDOLENCE_BENEFIT = {
    "name": "CONDOLENCE / EMERGENCY SUPPORT FORM",
    "key": "condolence_benefit",
    "category": "Payroll & Benefits",
    "description": "Staff condolence & emergency welfare benefit request (bereavement / loss).",
    "fields": [
        {"name": "date", "label": "Date", "type": "date", "required": True},
        {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "employee_no", "label": "Employee No.", "type": "text", "required": False},
        {"name": "position", "label": "Position", "type": "text", "required": False},
        {"name": "department", "label": "Department / Project", "type": "text", "required": False},
        {"name": "duty_station", "label": "Duty Station", "type": "text", "required": False},
        {"name": "phone", "label": "Contact Number", "type": "text", "required": False},
        {"name": "reason", "label": "Reason (bereavement / emergency)", "type": "select",
         "options": ["Bereavement of immediate family", "Bereavement of extended family", "Emergency & medical support", "Other welfare support"],
         "required": True},
        {"name": "deceased_name", "label": "Deceased / Affected Person", "type": "text", "required": False},
        {"name": "relationship", "label": "Relationship", "type": "text", "required": False},
        {"name": "date_of_event", "label": "Date of Event", "type": "date", "required": True},
        {"name": "support_amount", "label": "Support Amount (UGX)", "type": "number", "required": True},
        {"name": "details", "label": "Brief Details", "type": "longtext", "required": False},
        {"name": "hr_approval", "label": "HR Approval", "type": "select", "options": ["Pending", "Approved", "Declined"], "required": False, "default": "Pending"},
    ],
    "template": """
<h1>CONDOLENCE / EMERGENCY SUPPORT FORM</h1>
<p class="right">{h(date)}</p>
<div class="spacer-sm"></div>
<table class="info">
<tr><td class="k">Employee Name</td><td>{h(employee_name)}</td><td class="k">Employee No.</td><td>{h(employee_no)}</td></tr>
<tr><td class="k">Position</td><td>{h(position)}</td><td class="k">Department / Project</td><td>{h(department)}</td></tr>
<tr><td class="k">Duty Station</td><td>{h(duty_station)}</td><td class="k">Contact</td><td>{h(phone)}</td></tr>
</table>
<div class="spacer-sm"></div>
<h3>WELFARE SUPPORT DETAILS</h3>
<table class="info">
<tr><td class="k">Nature of Support</td><td><span class="bold">{h(reason)}</span></td></tr>
<tr><td class="k">Deceased / Affected Person</td><td>{h(deceased_name)}</td><td class="k">Relationship</td><td>{h(relationship)}</td></tr>
<tr><td class="k">Date of Event</td><td>{hd(date_of_event)}</td><td class="k">Support Amount</td><td><span class="bold">{hm(support_amount)}</span></td></tr>
</table>
<h3>DETAILS</h3>
<p>{h(details)}</p>
<div class="spacer-sm"></div>
<table class="bordered">
<tr><th style="width:25%">Requested by</th><th style="width:25%">People &amp; Culture</th><th style="width:25%">Executive Director</th></tr>
<tr><td style="height:22mm">Signature: <span class="dots">{sign_dots}</span></td>
<td>Date: <span class="dots">{sign_dots}</span><br/>Approval: <span class="bold">{h(hr_approval)}</span></td>
<td>Date: <span class="dots">{sign_dots}</span></td></tr>
</table>
<p class="center"><i>This welfare benefit is governed by the TPO Uganda staff welfare policy.</i></p>
""",
}