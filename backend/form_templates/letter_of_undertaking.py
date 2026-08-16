LETTER_OF_UNDERTAKING = {
    "name": "LETTER OF UNDERTAKING (BANK LOAN)",
    "key": "letter_of_undertaking",
    "category": "HR & Finance",
    "description": "Employer undertaking to a bank regarding an employee loan.",
    "fields": [
        {"name": "date", "label": "Date", "type": "date", "required": True},
        {"name": "bank_name", "label": "Bank Name", "type": "text", "required": True},
        {"name": "applicant_name", "label": "Name of Applicant", "type": "text", "required": True},
        {"name": "amount_figures", "label": "Loan Amount (Figures)", "type": "number", "required": True},
        {"name": "amount_words", "label": "Loan Amount (Words)", "type": "text", "required": True},
        {"name": "loan_duration", "label": "Repayment Duration", "type": "text", "required": True},
        {"name": "monthly_installment", "label": "Monthly Instalment", "type": "number", "required": True},
        {"name": "gross_monthly_salary", "label": "Gross Monthly Salary", "type": "number", "required": True},
        {"name": "net_monthly_salary", "label": "Net Monthly Salary", "type": "number", "required": True},
        {"name": "employment_date", "label": "Employed Since (Date)", "type": "date", "required": True},
        {"name": "position", "label": "Position", "type": "text", "required": True},
        {"name": "contract_expiry", "label": "Contract Expiry Date", "type": "date", "required": True},
        {"name": "account_number", "label": "Bank Account Number", "type": "text", "required": True},
        {"name": "signer1_name", "label": "Signatory 1 Name", "type": "text", "required": False, "default": "Peter Okwi"},
        {"name": "signer1_title", "label": "Signatory 1 Title", "type": "text", "required": False, "default": "Executive Director"},
        {"name": "signer2_name", "label": "Signatory 2 Name", "type": "text", "required": False, "default": "Achola Mary"},
        {"name": "signer2_title", "label": "Signatory 2 Title", "type": "text", "required": False, "default": "People and Culture Manager"},
    ],
    "template": """
<h1>LETTER OF UNDERTAKING</h1>
<p class="right">({h(date)})</p>
<p class="right"><span class="bold">Attn To:</span></p>
<p><span class="bold">The Manager,</span></p>
<p><span class="bold">({h(bank_name)})</span></p>
<p class="spacer-sm"> </p>
<p><span class="bold">RE:</span>&nbsp;<span class="bold ul">LETTER OF UNDERTAKING</span></p>
<p>We refer to <span class="bold">({h(applicant_name)})</span> application to your bank for a staff loan of SHS. <span class="bold">({hm(amount_figures)})</span> (<span class="bold">({h(amount_words)})</span> Shillings) repayable over <span class="bold">({h(loan_duration)})</span> with a monthly instalment of SHS. <span class="bold">({hm(monthly_installment)})</span>. We recommend that the loan be granted.</p>
<p><span class="bold">({h(applicant_name)})</span> (the borrower) is an employee of this organization earning a gross monthly salary of Uganda SHS. <span class="bold">({hm(gross_monthly_salary)})</span>. After statutory deductions, his/her net monthly salary is UGX SHS <span class="bold">({hm(net_monthly_salary)})</span>. TPO Uganda has employed him/her since <span class="bold">({h(employment_date)})</span> and is presently employed as <span class="bold">({h(position)})</span> based in Kampala on a contract basis until <span class="bold">({h(contract_expiry)})</span>.</p>
<p><span class="bold">We undertake to do the following: -</span></p>
<p>1. Remit to the Bank the borrower's net monthly salary of UGX. SHS <span class="bold">({hm(net_monthly_salary)})</span> to the bank account no. <span class="bold">({h(account_number)})</span> held with your bank for the entire duration of his/her employment.</p>
<p>2. Advise the Bank in the event that the borrower's employment is terminated or if the borrower should cease to be employed by this organization.</p>
<p>3. Immediately remit to you the borrower's accrued terminal benefits as at the date of termination to settle any outstanding loan obligations and/or accrued interest. <span class="bold">NOT DETERMINED AT THE MOMENT</span>.</p>
<p>4. Should the borrower fail to meet any loan repayments and/or interest for any reason, TPO Uganda is not liable but shall provide the bank with all reasonable assistance to recover the outstanding balance of the loan and interest.</p>
<p class="spacer-sm"> </p>
<p>Sign (Employer): {sign_dots} &nbsp;&nbsp;&nbsp; Sign (Employer): {sign_dots}</p>
<p>Name: <span class="ul">{h(signer1_name)}</span> &nbsp;&nbsp; Name: <span class="ul">{h(signer2_name)}</span></p>
<p>Designation: <span class="ul">{h(signer1_title)}</span> &nbsp;&nbsp; Designation: <span class="ul">{h(signer2_title)}</span></p>
<p class="spacer-sm"> </p>
<p>I <span class="field-value">………………………………….</span> (the borrower) hereby consent for purposes of Clause 3 above, to the Organization/Company remitting my accrued terminal benefits to the Bank to settle my outstanding loan obligations with the Bank.</p>
<p class="spacer-md"> </p>
<p class="right">{sign_dots}</p>
<p class="right"><span class="bold">SIGNATURE (EMPLOYEE)</span></p>
""",
}