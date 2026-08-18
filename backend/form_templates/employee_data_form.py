EMPLOYEE_DATA = {
    "name": "EMPLOYEE DATA FORM / PERSONNEL FILE",
    "key": "employee_data_form",
    "category": "Employee Records",
    "description": "Master employee/personnel record aligned with EMPLOYEE DATA FORM & STAFF PERSONNEL FILE.",
    "fields": [
        {"name": "full_name", "label": "Full Name", "type": "text", "required": True},
        {"name": "employee_no", "label": "Employee No.", "type": "text", "required": True},
        {"name": "dob", "label": "Date of Birth", "type": "date", "required": False},
        {"name": "gender", "label": "Gender", "type": "select", "options": ["Male", "Female"], "required": False},
        {"name": "nationality", "label": "Nationality", "type": "text", "required": False},
        {"name": "nin", "label": "National ID / NIN", "type": "text", "required": False},
        {"name": "tin", "label": "TIN", "type": "text", "required": False},
        {"name": "nssf_no", "label": "NSSF No.", "type": "text", "required": False},
        {"name": "phone", "label": "Phone", "type": "text", "required": False},
        {"name": "email", "label": "Email (Outlook)", "type": "text", "required": False},
        {"name": "address", "label": "Residential Address", "type": "text", "required": False},
        {"name": "district", "label": "District", "type": "text", "required": False},
        {"name": "position", "label": "Position", "type": "text", "required": True},
        {"name": "project", "label": "Project / Department", "type": "text", "required": False},
        {"name": "duty_station", "label": "Duty Station", "type": "text", "required": False},
        {"name": "supervisor", "label": "Supervisor", "type": "text", "required": False},
        {"name": "grade", "label": "Grade", "type": "text", "required": False},
        {"name": "salary", "label": "Gross Monthly Salary (UGX)", "type": "number", "required": False},
        {"name": "appointment_date", "label": "Date of Appointment", "type": "date", "required": False},
        {"name": "contract_start", "label": "Contract Start", "type": "date", "required": False},
        {"name": "contract_end", "label": "Contract Expiry", "type": "date", "required": False},
        {"name": "employment_type", "label": "Employment Type", "type": "select", "options": ["Full-time", "Part-time", "Contract", "Internship", "Temporary"], "required": False},
        {"name": "notice_period", "label": "Notice Period", "type": "text", "required": False},
        {"name": "status", "label": "Status", "type": "select", "options": ["Active", "On Leave", "Probation", "Inactive", "Terminated"], "required": False},
        {"name": "spouse_name", "label": "Spouse Name", "type": "text", "required": False},
        {"name": "child1_name", "label": "Child 1 Name", "type": "text", "required": False},
        {"name": "child2_name", "label": "Child 2 Name", "type": "text", "required": False},
        {"name": "next_of_kin", "label": "Next of Kin", "type": "text", "required": False},
        {"name": "next_of_kin_contact", "label": "Next of Kin Contact", "type": "text", "required": False},
        {"name": "bank_name", "label": "Bank Name", "type": "text", "required": False},
        {"name": "account_number", "label": "Account No.", "type": "text", "required": False},
    ],
    "template": """
<h1>EMPLOYEE DATA FORM / STAFF PERSONNEL FILE</h1>
<table class="info">
<tr><td class="k">Employee No.</td><td>{h(employee_no)}</td><td class="k">Status</td><td>{h(status)}</td></tr>
<tr><td class="k">Full Name</td><td><span class="bold">{h(full_name)}</span></td><td class="k">Gender</td><td>{h(gender)}</td></tr>
<tr><td class="k">Date of Birth</td><td>{h(dob)}</td><td class="k">Nationality</td><td>{h(nationality)}</td></tr>
<tr><td class="k">National ID / NIN</td><td>{h(nin)}</td><td class="k">TIN</td><td>{h(tin)}</td></tr>
<tr><td class="k">NSSF No.</td><td>{h(nssf_no)}</td></tr>
</table>
<h3>2. CONTACT</h3>
<table class="info">
<tr><td class="k">Phone</td><td>{h(phone)}</td><td class="k">Email (Outlook)</td><td>{h(email)}</td></tr>
<tr><td class="k">Residential Address</td><td>{h(address)}</td><td class="k">District</td><td>{h(district)}</td></tr>
</table>
<h3>3. EMPLOYMENT</h3>
<table class="info">
<tr><td class="k">Position</td><td>{h(position)}</td><td class="k">Project / Department</td><td>{h(project)}</td></tr>
<tr><td class="k">Duty Station</td><td>{h(duty_station)}</td><td class="k">Supervisor</td><td>{h(supervisor)}</td></tr>
<tr><td class="k">Grade</td><td>{h(grade)}</td><td class="k">Gross Monthly Salary</td><td><span class="bold">{hm(salary)}</span></td></tr>
<tr><td class="k">Date of Appointment</td><td>{h(appointment_date)}</td><td class="k">Employment Type</td><td>{h(employment_type)}</td></tr>
<tr><td class="k">Contract Start</td><td>{h(contract_start)}</td><td class="k">Contract Expiry</td><td>{h(contract_end)}</td></tr>
<tr><td class="k">Notice Period</td><td>{h(notice_period)}</td></tr>
</table>
<h3>4. DEPENDANTS (&le; 2)</h3>
<table class="bordered">
<tr><th>Spouse</th><th>Child 1</th><th>Child 2</th></tr>
<tr><td>{h(spouse_name)}</td><td>{h(child1_name)}</td><td>{h(child2_name)}</td></tr>
</table>
<h3>5. NEXT OF KIN</h3>
<table class="info">
<tr><td class="k">Name</td><td>{h(next_of_kin)}</td><td class="k">Contact</td><td>{h(next_of_kin_contact)}</td></tr>
</table>
<h3>6. BANK DETAILS</h3>
<table class="info">
<tr><td class="k">Bank Name</td><td>{h(bank_name)}</td><td class="k">Account No.</td><td>{h(account_number)}</td></tr>
</table>
<div class="spacer-sm"></div>
<p><span class="bold">Missing Documents Tracker:</span> Complete / Action Required &nbsp; <i>(auto-flagged from personnel file)</i></p>
<p class="spacer-sm"> </p>
<p>Prepared by: {sign_dots} &nbsp; Date: {sign_dots} &nbsp;&nbsp; HRM Sign-off: {sign_dots} &nbsp; Date: {sign_dots}</p>
""",
}