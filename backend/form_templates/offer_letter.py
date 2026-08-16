OFFER_LETTER = {
    "name": "OFFER / APPOINTMENT LETTER",
    "key": "offer_letter",
    "category": "Contracts & Letters",
    "description": "Appointment/offer letter with salary table (TPO Uganda).",
    "fields": [
        {"name": "date", "label": "Letter Date", "type": "date", "required": True},
        {"name": "to_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "to_title", "label": "Employee Position", "type": "text", "required": True},
        {"name": "appointment_role", "label": "Appointment As", "type": "text", "required": True},
        {"name": "effective_date", "label": "Effective Date", "type": "date", "required": True},
        {"name": "contract_start", "label": "Contract Start", "type": "date", "required": True},
        {"name": "contract_end", "label": "Contract End", "type": "date", "required": True},
        {"name": "project", "label": "Project Name", "type": "text", "required": False},
        {"name": "supervisor", "label": "Reporting To", "type": "text", "required": False},
        {"name": "grade", "label": "TPO Grade", "type": "text", "required": False},
        {"name": "gross_pay", "label": "Gross Pay (SHS)", "type": "number", "required": True},
        {"name": "nssf", "label": "5% NSSF", "type": "number", "required": True},
        {"name": "provident", "label": "4% Provident Fund", "type": "number", "required": True},
        {"name": "paye", "label": "PAYE", "type": "number", "required": True},
        {"name": "net_pay", "label": "Net Pay (SHS)", "type": "number", "required": True},
        {"name": "duty_station", "label": "Duty Station", "type": "text", "required": False},
        {"name": "director_name", "label": "Signatory Name", "type": "text", "required": False, "default": "Peter Okwi"},
        {"name": "director_title", "label": "Signatory Title", "type": "text", "required": False, "default": "Executive Director"},
    ],
    "template": """
<h1>OFFER / APPOINTMENT LETTER</h1>
<p>{h(date)}</p>
<p class="spacer-sm"> </p>
<p><span class="bold">TO:</span></p>
<p>{h(to_name)}</p>
<p>{h(to_title)}</p>
<p class="spacer-sm"> </p>
<p><span class="bold">RE:</span>&nbsp; <span class="bold ul">APPOINTMENT AS {h(appointment_role)}</span></p>
<p>Following expiry of your current contract, TPO Uganda is pleased to offer you employment under its new structure, effective <span class="bold">{h(effective_date)}</span> as <span class="bold">{h(to_title)}</span>, for its <span class="bold">{h(project)}</span> Project reporting to <span class="bold">{h(supervisor)}</span>, under the following terms:</p>
<p><span class="bold">1) Contract Duration</span></p>
<p>This is a fixed-term appointment from <span class="bold">{h(contract_start)}</span> to <span class="bold">{h(contract_end)}</span>, subject to satisfactory performance and availability of funds. Unless renewed in writing, the contract shall end automatically on its expiry date and no notice is required upon such expiry.</p>
<p><span class="bold">Salary Payment:</span> Salary payments are in Ugandan Shillings made monthly based on your Grade in the organization and calculated as follows:</p>
<div class="spacer-sm"></div>
<p>Your position within the organization's salary scale is <span class="bold">TPO Grade {h(grade)}</span></p>
<table class="info">
<tr><td class="k">Position</td><td>{h(to_title)}</td></tr>
<tr><td class="k">Supervisor</td><td>{h(supervisor)}</td></tr>
<tr><td class="k">Gross Pay (SHS)</td><td><span class="bold">{hm(gross_pay)}</span></td></tr>
<tr><td class="k"><span class="bold">Less:</span></td><td></td></tr>
<tr><td class="k">5% NSSF</td><td><span class="bold">{hm(nssf)}</span></td></tr>
<tr><td class="k">4% Provident Fund</td><td><span class="bold">{hm(provident)}</span></td></tr>
<tr><td class="k">PAYE</td><td><span class="bold">{hm(paye)}</span></td></tr>
<tr><td class="k">Net Pay (SHS)</td><td><span class="bold">{hm(net_pay)}</span></td></tr>
<tr><td class="k">Duty Station</td><td>{h(duty_station)}</td></tr>
</table>
<p><span class="bold">2) Governing Terms and Conditions</span></p>
<p>Your employment will be governed by:</p>
<ul>
<li>The <span class="bold">Employment Act, 2006 (Uganda)</span>;</li>
<li>TPO Uganda's <span class="bold">People &amp; Culture Management Manual (2025)</span> and associated policies; and</li>
<li>The <span class="bold">Employment Contract</span> issued with this letter, which sets out the particulars required under the law.</li>
</ul>
<p>Please review the contract together with this letter.</p>
<p><span class="bold">3) Conditions Precedent &amp; Acknowledgement</span></p>
<p>This offer is subject to satisfactory background and reference checks, including a Certificate of Good Conduct where applicable, in line with TPO's Anti-Fraud and PSEAH Policies. You are required to comply with these policies and all applicable Ugandan laws.</p>
<p><span class="bold">Acceptance</span></p>
<p>Please confirm your acceptance or rejection by circling and signing below within two weeks from the date of this letter.</p>
<p>We look forward to working with you.</p>
<p><span class="bold">Yours faithfully,</span></p>
<div class="spacer-md"></div>
<p>{sign_dots} &nbsp; Date:&nbsp;…………………………………</p>
<p><span class="bold">{h(director_name)}</span></p>
<p>{h(director_title)}</p>
<div class="spacer-lg"></div>
<p>I accept / decline this offer <i>(circle as applicable)</i></p>
<div class="spacer-lg"></div>
<p>{sign_dots} &nbsp; Date:&nbsp;……………………………</p>
<p><span class="bold">{h(to_name)}</span></p>
<p>{h(to_title)}</p>
""",
}