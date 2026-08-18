CONTRACT_RENEWAL = {
    "name": "CONTRACT RENEWAL LETTER",
    "key": "contract_renewal",
    "category": "Contracts & Letters",
    "description": "Renewal of a fixed-term employment contract (TPO Uganda / People Pulse).",
    "fields": [
        {"name": "date", "label": "Date", "type": "date", "required": True},
        {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "position", "label": "Position", "type": "text", "required": True},
        {"name": "duty_station", "label": "Duty Station", "type": "text", "required": False},
        {"name": "department", "label": "Department", "type": "text", "required": False},
        {"name": "project_name", "label": "Project", "type": "text", "required": False},
        {"name": "old_contract_dates", "label": "Previous Contract Period (e.g. 1st Feb 2024 - 31st Jan 2026)", "type": "text", "required": True},
        {"name": "new_start", "label": "New Contract Start", "type": "date", "required": True},
        {"name": "new_end", "label": "New Contract End", "type": "date", "required": True},
        {"name": "duration", "label": "Renewal Duration (e.g. one (1) year)", "type": "text", "required": True},
        {"name": "grade", "label": "Grade", "type": "text", "required": False},
        {"name": "salary", "label": "Gross Monthly Salary (UGX)", "type": "number", "required": False},
        {"name": "supervisor", "label": "Supervisor", "type": "text", "required": False},
        {"name": "director_name", "label": "Signatory Name", "type": "text", "required": False, "default": "Peter Okwi"},
    ],
    "template": """
<h1>CONTRACT RENEWAL</h1>
<p>{h(date)}</p>
<div class="spacer-sm"></div>
<p><span class="bold">To:</span></p>
<p>{h(employee_name)}</p>
<p>{h(position)} &mdash; {h(department)}</p>
<div class="spacer-sm"></div>
<p><span class="bold">RE:</span>&nbsp; <span class="bold ul">RENEWAL OF EMPLOYMENT CONTRACT</span></p>
<p>We refer to your fixed-term employment contract with TPO Uganda for the period <span class="bold">{h(old_contract_dates)}</span>.</p>
<p>Following a review of programme needs and your satisfactory performance, we are pleased to inform you that your contract of employment with TPO Uganda has been <span class="bold">renewed for a further period of {h(duration)}</span>, effective <span class="bold">{h(new_start)}</span> and ending on <span class="bold">{h(new_end)}</span>.</p>
<p>Your appointment details upon renewal are as follows:</p>
<table class="info">
<tr><td class="k">Position</td><td>{h(position)}</td></tr>
<tr><td class="k">Department / Project</td><td>{h(department)} &mdash; {h(project_name)}</td></tr>
<tr><td class="k">Duty Station</td><td>{h(duty_station)}</td></tr>
<tr><td class="k">Supervisor</td><td>{h(supervisor)}</td></tr>
<tr><td class="k">Grade</td><td>{h(grade)}</td></tr>
<tr><td class="k">Gross Monthly Salary</td><td><span class="bold">{hm(salary)}</span></td></tr>
</table>
<p>This renewal is subject to the following:</p>
<p>(a) Your continued satisfactory performance.</p>
<p>(b) Availability of project funding and/or donor approval.</p>
<p>(c) Continued compliance with TPO Uganda policies, procedures, safeguarding standards and the Code of Conduct.</p>
<p>All other terms and conditions of your contract remain as per the original terms, unless otherwise communicated in writing.</p>
<p>Kindly sign and return a copy of this letter to confirm your acceptance of this renewal.</p>
<div class="spacer-md"></div>
<p><span class="bold">Yours sincerely,</span></p>
<p>{h(director_name)}</p>
<p><span class="bold">Executive Director</span></p>
<div class="spacer-md"></div>
<p><span class="bold">Acknowledgement:</span></p>
<p>I {h(employee_name, '.....................')}, accept / reject the renewal of my employment contract as set out above. <i>(Circle where applicable)</i></p>
<p>Signature: {sign_dots} &nbsp;&nbsp; Date: {sign_dots}</p>
""",
}