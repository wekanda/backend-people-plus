CONTRACT_EXTENSION = {
    "name": "CONTRACT EXTENSION LETTER",
    "key": "contract_extension",
    "category": "Contracts & Letters",
    "description": "Extends a fixed-term employment contract (TPO Uganda).",
    "fields": [
        {"name": "date", "label": "Date", "type": "date", "required": True},
        {"name": "to_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "contract_date", "label": "Original Contract Date", "type": "date", "required": True},
        {"name": "expiry_date", "label": "Current Expiry Date", "type": "date", "required": True},
        {"name": "duration", "label": "Extension Duration", "type": "text", "required": True, "placeholder": "e.g. one (1) month"},
        {"name": "effective_date", "label": "Extension Effective Date", "type": "date", "required": True},
        {"name": "end_date", "label": "Extension End Date", "type": "date", "required": True},
        {"name": "director_name", "label": "Signatory Name", "type": "text", "required": False, "default": "Peter Okwi"},
    ],
    "template": """
<h1>CONTRACT EXTENSION</h1>
<p>{h(date)}</p>
<div class="spacer-sm"></div>
<p>To</p>
<p>{h(to_name, '.....................')}</p>
<div class="spacer-sm"></div>
<p>Dear,</p>
<p><span class="bold">RE:</span>&nbsp; <span class="bold ul">CONTRACT EXTENSION</span></p>
<p>We refer to your current fixed-term employment contract with TPO Uganda dated <span class="bold">[{h(contract_date)}]</span>, which is scheduled to expire on <span class="bold">[{h(expiry_date)}]</span>.</p>
<p>Following a review of programme needs and your performance, we are pleased to inform you that your contract has been extended for a further duration of <span class="bold">[{h(duration)}]</span>, effective <span class="bold">[{h(effective_date)}]</span> and ending on <span class="bold">[{h(end_date)}]</span>.</p>
<p>This extension is subject to the following:</p>
<p>(a) Your continued satisfactory performance.</p>
<p>(b) Availability of project funding and/or donor approval.</p>
<p>(c) Continued compliance with TPO Uganda policies, procedures, safeguarding standards and the Code of Conduct.</p>
<p>All other terms and conditions of your original contract remain unchanged unless otherwise communicated in writing.</p>
<p>Kindly sign and return a copy of this letter to confirm your acceptance of this extension.</p>
<p>TPO Uganda appreciates your continued contribution to the organization's mission and the communities we serve.</p>
<div class="spacer-sm"></div>
<p><span class="bold">Yours sincerely,</span></p>
<p><span class="bold">{h(director_name)}</span>,</p>
<p><span class="bold">Executive Director.</span></p>
<div class="spacer-md"></div>
<p><span class="bold">Acknowledgement:</span></p>
<p>I <span class="field-value">{h(to_name, '.....................')}</span>, accept / reject the terms of this contract extension. (<i>Circle where applicable</i>)</p>
<p>Signature: {sign_dots} &nbsp;&nbsp; Date: {sign_dots}</p>
""",
}