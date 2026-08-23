FUEL_ALLOWANCE = {
    "name": "FUEL ALLOWANCE REQUEST",
    "key": "fuel_allowance",
    "category": "Payroll & Benefits",
    "description": "Monthly fuel/transport allowance claim for staff & field officers.",
    "fields": [
        {"name": "date", "label": "Date", "type": "date", "required": True},
        {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "employee_no", "label": "Employee No.", "type": "text", "required": False},
        {"name": "position", "label": "Position", "type": "text", "required": False},
        {"name": "department", "label": "Department / Project", "type": "text", "required": False},
        {"name": "duty_station", "label": "Duty Station", "type": "text", "required": False},
        {"name": "period", "label": "Claim Period (Month/Year)", "type": "text", "required": True},
        {"name": "litres", "label": "Litres Requested", "type": "number", "required": False},
        {"name": "unit_price", "label": "Unit Price (UGX/L)", "type": "number", "required": False},
        {"name": "total_amount", "label": "Total Amount (UGX)", "type": "number", "required": True},
        {"name": "vehicle_reg", "label": "Vehicle / Motorcycle Reg. No.", "type": "text", "required": False},
        {"name": "purpose", "label": "Purpose / Route", "type": "longtext", "required": False},
        {"name": "approved_by", "label": "Approved By", "type": "text", "required": False, "default": "Program Manager"},
    ],
    "template": """
<h1>FUEL ALLOWANCE REQUEST</h1>
<p class="right">{h(date)}</p>
<div class="spacer-sm"></div>
<table class="info">
<tr><td class="k">Employee Name</td><td>{h(employee_name)}</td><td class="k">Employee No.</td><td>{h(employee_no)}</td></tr>
<tr><td class="k">Position</td><td>{h(position)}</td><td class="k">Department / Project</td><td>{h(department)}</td></tr>
<tr><td class="k">Duty Station</td><td>{h(duty_station)}</td><td class="k">Claim Period</td><td><span class="bold">{h(period)}</span></td></tr>
<tr><td class="k">Vehicle / M/Cycle Reg.</td><td>{h(vehicle_reg)}</td></tr>
</table>
<div class="spacer-sm"></div>
<h3>FUEL REQUEST DETAILS</h3>
<table class="bordered">
<tr><th style="width:40%">Description</th><th style="width:22%">Litres</th><th style="width:18%">Unit Price</th><th style="width:20%">Amount (UGX)</th></tr>
<tr><td>Fuel for field / official duty &mdash; <span class="bold">{h(purpose)}</span></td><td class="center">{h(litres)}</td><td class="center">{hm(unit_price)}</td><td class="right"><span class="bold">{hm(total_amount)}</span></td></tr>
</table>
<div class="spacer-sm"></div>
<p>I request payment of the above fuel allowance in line with the TPO Uganda staff benefits policy.</p>
<p class="spacer-md"> </p>
<p>Requested by: {h(employee_name)} &nbsp; Signature: {sign_dots} &nbsp; Date: {h(date)}</p>
<p>Approved by: {h(approved_by)} &nbsp; Signature: {sign_dots} &nbsp; Date: {sign_dots}</p>
""",
}