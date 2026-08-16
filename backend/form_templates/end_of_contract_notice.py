END_OF_CONTRACT_NOTICE = {
    "name": "NOTICE OF CONTRACT COMPLETION",
    "key": "end_of_contract_notice",
    "category": "Contracts & Letters",
    "description": "Formal notification that a fixed-term contract has reached its end.",
    "fields": [
        {"name": "date", "label": "Date", "type": "date", "required": True},
        {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "employee_title", "label": "Employee Position", "type": "text", "required": True},
        {"name": "end_date", "label": "Contract End Date", "type": "date", "required": True},
        {"name": "contract_clause", "label": "Contract Clause", "type": "text", "required": False, "default": "3"},
        {"name": "director_name", "label": "Signatory Name", "type": "text", "required": False, "default": "Peter Okwi"},
        {"name": "director_title", "label": "Signatory Title", "type": "text", "required": False, "default": "Country Director"},
    ],
    "template": """
<h1>NOTICE OF CONTRACT COMPLETION</h1>
<p>{h(date)}</p>
<div class="spacer-sm"></div>
<p><span class="bold">{h(employee_name)}</span></p>
<p><span class="bold">{h(employee_title)}</span></p>
<p>Dear {first_name(employee_name)},</p>
<p><span class="bold">RE:</span>&nbsp; <span class="bold ul">NOTICE OF CONTRACT &amp; COMPLETION</span></p>
<p>On behalf of TPO Uganda, I wish to express our appreciation for your dedicated service over the past years. Your professionalism, integrity, and commitment have significantly contributed to our mission and the wellbeing of the communities we serve.</p>
<p>We take this opportunity to formally acknowledge the completion of your contract in accordance with Clause {h(contract_clause, '3')} of your employment contract and Section 6.7.1 of the People and Culture Management Manual. This process is in accordance with the Employment Act Cap 226 and internal policies.</p>
<p>This letter serves as formal notification that your contract will end on <span class="bold">{h(end_date)}</span>.</p>
<p>To ensure a smooth transition and proper closure of responsibilities, and in line with Sections 6.7.4 and 6.7.5 of the Manual, we kindly request that you complete all exit and handover processes prior to your departure (and with guidance from your supervisor). These include:</p>
<ul>
<li>Submission of all handover documentation and project files.</li>
<li>Clearance of any outstanding liabilities.</li>
<li>Return of all organizational property (e.g., ID card, laptop, manuals, etc.).</li>
<li>Completion of the TPO Uganda exit interview and clearance form.</li>
</ul>
<p>Your final payment and Certificate of Service will be processed within 30 calendar days from the date of contract expiry, subject to completion of the clearance process.</p>
<p>We thank you once again for your years of service and dedication. Should future opportunities arise, you are welcome to apply through our recruitment process, where your experience will be valued.</p>
<p>Please accept our best wishes for continued success in your future endeavors.</p>
<div class="spacer-md"></div>
<p><span class="bold">Yours sincerely,</span></p>
<div class="spacer-md"></div>
<p>{sign_dots}</p>
<p><span class="bold">{h(director_name)}</span></p>
<p><span class="bold">{h(director_title)}</span></p>
""",
}