TRANSPORT_CLAIM = {
    "name": "TRANSPORT CLAIM FORM",
    "key": "transport_claim",
    "category": "Payroll & Benefits",
    "description": "Reimbursement claim for staff travel & transport costs incurred on duty.",
    "fields": [
        {"name": "date", "label": "Date", "type": "date", "required": True},
        {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "employee_no", "label": "Employee No.", "type": "text", "required": False},
        {"name": "position", "label": "Position", "type": "text", "required": False},
        {"name": "department", "label": "Department / Project", "type": "text", "required": False},
        {"name": "duty_station", "label": "Duty Station", "type": "text", "required": False},
        {"name": "period", "label": "Claim Period", "type": "text", "required": False},
        {"name": "from_place", "label": "From (Place)", "type": "text", "required": True},
        {"name": "to_place", "label": "To (Place)", "type": "text", "required": True},
        {"name": "travel_date", "label": "Travel Date", "type": "date", "required": True},
        {"name": "transport_mode", "label": "Mode", "type": "select",
         "options": ["Boda boda", "Taxi / Matatu", "Bus / Coach", "Airport transfer", "Own vehicle (fuel)", "Boat / Ferry"],
         "required": True},
        {"name": "fare_amount", "label": "Fare Amount (UGX)", "type": "number", "required": True},
        {"name": "purpose", "label": "Purpose of Trip", "type": "longtext", "required": False},
        {"name": "approved_by", "label": "Approved By", "type": "text", "required": False, "default": "Finance Officer"},
    ],
    "template": """
<h1>TRANSPORT CLAIM FORM</h1>
<p class="right">{h(date)}</p>
<div class="spacer-sm"></div>
<table class="info">
<tr><td class="k">Employee Name</td><td>{h(employee_name)}</td><td class="k">Employee No.</td><td>{h(employee_no)}</td></tr>
<tr><td class="k">Position</td><td>{h(position)}</td><td class="k">Department / Project</td><td>{h(department)}</td></tr>
<tr><td class="k">Duty Station</td><td>{h(duty_station)}</td><td class="k">Claim Period</td><td>{h(period)}</td></tr>
</table>
<div class="spacer-sm"></div>
<h3>JOURNEY DETAILS</h3>
<table class="bordered">
<tr><th>Date</th><th>From</th><th>To</th><th>Mode</th></tr>
<tr><td>{hd(travel_date)}</td><td>{h(from_place)}</td><td>{h(to_place)}</td><td>{h(transport_mode)}</td></tr>
</table>
<table class="info">
<tr><td class="k">Fare / Amount (UGX)</td><td><span class="bold">{hm(fare_amount)}</span></td></tr>
<tr><td class="k">Purpose of Trip</td><td>{h(purpose)}</td></tr>
</table>
<div class="spacer-md"></div>
<p>I certify that the above journey was undertaken on official duty and the amount claimed has not been received from any other source.</p>
<p class="spacer-sm"> </p>
<p>Claimant: {h(employee_name)} &nbsp; Signature: {sign_dots} &nbsp; Date: {h(date)}</p>
<p>Approved by: {h(approved_by)} &nbsp; Signature: {sign_dots} &nbsp; Date: {sign_dots}</p>
""",
}