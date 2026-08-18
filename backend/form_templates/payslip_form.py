PAYSLIP_FORM = {
    "name": "PAYSLIP",
    "key": "payslip",
    "category": "Payroll",
    "description": "Monthly payslip aligned with PAYSLIP.xlsx - earnings, deductions and net pay.",
    "fields": [
        {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "employee_no", "label": "Employee No.", "type": "text", "required": True},
        {"name": "position", "label": "Position", "type": "text", "required": False},
        {"name": "department", "label": "Department", "type": "text", "required": False},
        {"name": "pay_period", "label": "Pay Period (e.g. June 2026)", "type": "text", "required": True},
        {"name": "tin", "label": "TIN", "type": "text", "required": False},
        {"name": "nssf_no", "label": "NSSF No.", "type": "text", "required": False},
        {"name": "basic_salary", "label": "Basic Salary", "type": "number", "required": True},
        {"name": "allowances", "label": "Allowances", "type": "number", "required": False},
        {"name": "overtime", "label": "Overtime / Bonuses", "type": "number", "required": False},
        {"name": "gross", "label": "Gross Pay", "type": "number", "required": False},
        {"name": "paye", "label": "PAYE (Tax)", "type": "number", "required": True},
        {"name": "nssf_employee", "label": "NSSF 5% (Employee)", "type": "number", "required": False},
        {"name": "provident_employee", "label": "Provident Fund 4% (Employee)", "type": "number", "required": False},
        {"name": "advances", "label": "Advances / Loans", "type": "number", "required": False},
        {"name": "other_deductions", "label": "Other Deductions", "type": "number", "required": False},
        {"name": "total_deductions", "label": "Total Deductions", "type": "number", "required": False},
        {"name": "net_pay", "label": "Net Pay", "type": "number", "required": True},
        {"name": "employer_nssf", "label": "Employer NSSF 10%", "type": "number", "required": False},
        {"name": "employer_provident", "label": "Employer Provident 8%", "type": "number", "required": False},
    ],
    "template": """
<h1>PAYSLIP</h1>
<p class="center">PEOPLE PULSE &mdash; PAYROLL</p>
<p class="center">Pay Period: <span class="bold">{h(pay_period)}</span></p>
<div class="spacer-sm"></div>
<table class="info">
<tr><td class="k">Employee Name</td><td><span class="bold">{h(employee_name)}</span></td><td class="k">Employee No.</td><td>{h(employee_no)}</td></tr>
<tr><td class="k">Position</td><td>{h(position)}</td><td class="k">Department</td><td>{h(department)}</td></tr>
<tr><td class="k">TIN</td><td>{h(tin)}</td><td class="k">NSSF No.</td><td>{h(nssf_no)}</td></tr>
</table>
<h3>EARNINGS</h3>
<table class="bordered">
<tr><td>Basic Salary</td><td class="right">{hm(basic_salary)}</td></tr>
<tr><td>Allowances</td><td class="right">{hm(allowances)}</td></tr>
<tr><td>Overtime / Bonuses</td><td class="right">{hm(overtime)}</td></tr>
<tr><td><span class="bold">Gross Pay</span></td><td class="right"><span class="bold">{hm(gross)}</span></td></tr>
</table>
<h3>DEDUCTIONS</h3>
<table class="bordered">
<tr><td>PAYE (Tax)</td><td class="right">{hm(paye)}</td></tr>
<tr><td>NSSF 5% (Employee)</td><td class="right">{hm(nssf_employee)}</td></tr>
<tr><td>Provident Fund 4% (Employee)</td><td class="right">{hm(provident_employee)}</td></tr>
<tr><td>Advances / Loans</td><td class="right">{hm(advances)}</td></tr>
<tr><td>Other Deductions</td><td class="right">{hm(other_deductions)}</td></tr>
<tr><td><span class="bold">Total Deductions</span></td><td class="right"><span class="bold">{hm(total_deductions)}</span></td></tr>
</table>
<table class="info">
<tr><td class="k"><span class="bold">NET PAY</span></td><td><span class="bold">{hm(net_pay)}</span></td></tr>
</table>
<h3>EMPLOYER CONTRIBUTIONS</h3>
<table class="bordered">
<tr><td>NSSF 10% (Employer)</td><td class="right">{hm(employer_nssf)}</td></tr>
<tr><td>Provident Fund 8% (Employer)</td><td class="right">{hm(employer_provident)}</td></tr>
</table>
<div class="spacer-md"></div>
<p>Prepared by: {sign_dots} &nbsp;&nbsp; Approved by: {sign_dots}</p>
<p class="center"><i>This payslip is system-generated. Do not alter.</i></p>
""",
}