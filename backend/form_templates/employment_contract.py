EMPLOYMENT_CONTRACT = {
    "name": "TERMS AND CONDITIONS OF EMPLOYMENT",
    "key": "employment_contract",
    "category": "Contracts & Letters",
    "description": "Full employment contract with terms and conditions (TPO Uganda).",
    "fields": [
        {"name": "honorific", "label": "Honorific (Mr/Mrs/Ms/Dr)", "type": "select", "options": ["Mr.", "Mrs.", "Ms.", "Dr.", "Prof."], "required": False},
        {"name": "employee_name", "label": "Employee Full Name", "type": "text", "required": True},
        {"name": "nin", "label": "National ID / NIN", "type": "text", "required": False},
        {"name": "phone", "label": "Registered Tel. No.", "type": "text", "required": False},
        {"name": "po_box", "label": "P.O. Box", "type": "text", "required": False},
        {"name": "job_title", "label": "Job Title", "type": "text", "required": True},
        {"name": "grade", "label": "Grade", "type": "text", "required": False},
        {"name": "supervisor", "label": "Overall Supervisor", "type": "text", "required": False},
        {"name": "duty_station", "label": "Duty Station", "type": "text", "required": False},
        {"name": "report_to", "label": "Reports To", "type": "text", "required": False},
        {"name": "contract_start", "label": "Appointment Start", "type": "date", "required": True},
        {"name": "contract_end", "label": "Contract End", "type": "date", "required": True},
        {"name": "project_name", "label": "Project Name", "type": "text", "required": False},
        {"name": "salary_gross", "label": "Gross Monthly Salary (UGX)", "type": "number", "required": True},
        {"name": "director_name", "label": "Signatory Name", "type": "text", "required": False, "default": "Peter Okwi"},
    ],
    "template": """
<h1>THE REPUBLIC OF UGANDA</h1>
<h2>TPO UGANDA</h2>
<h1>TERMS AND CONDITIONS OF EMPLOYMENT</h1>
<h3>Preamble</h3>
<p>We consider ourselves to be an equal-opportunities employer. We shall at all times strive to create a work environment that encourages innovation and professionalism, whilst promoting transparency in all our dealings, and compassion in our interactions. We shall build a gender-sensitive workplace that gives equal opportunities for growth to all qualified candidates seeking employment with us irrespective of gender, race, ethnicity, religion and other lawful affiliations.</p>
<p>All our employees will be given opportunity to discover their potentials and to grow on the job. Our employment strategy will entail a mix of age, experience, young talent and skill, hence retaining experienced staff whilst tapping into young potential. Where new opportunities arise, we shall give priority to qualified existing staff.</p>
<h3>TPO Uganda VISION and MISSION</h3>
<p>Vision: &ldquo;A Society where individuals enjoy mental health and socio-economic wellbeing.&rdquo;</p>
<p>Mission: &ldquo;To empower communities, improve their mental health and socio-economic wellbeing.&rdquo;</p>
<p>Core Values: Professional, Accountable, Dependable, Inclusive, Innovative, Compassionate</p>
<h3>Contract of Employment</h3>
<p>This contract of employment is made between TPO Uganda of P.O. Box 21646, Plot 652, Wamala Close, Munyonyo, Kampala as the employer on one hand, and <span class="bold">{h(honorific)}</span> <span class="bold ul">{h(employee_name)}</span>, NIN: {h(nin)} &nbsp; Registered Tel. No. {h(phone)} &nbsp; P.O. Box {h(po_box)} as the employee on the other hand.</p>
<p>Job Title and Grade: {h(job_title)}, Grade {h(grade)}</p>
<p>Overall Supervisor: <span class="bold">{h(supervisor)}</span></p>
<p>Duty Station: {h(duty_station)}</p>
<p>Duties: Please read carefully the description of your duties in the job description/terms of reference and competence profile which is applicable and is attached.</p>
<h3>Appointment and Duration of Contract</h3>
<p>TPO hereby appoints the Employee into the position of {h(job_title)}, subject to the following:</p>
<ul>
<li>That the Employee by entering into this agreement shall not be in breach of any laws of the Republic of Uganda or any express or implied terms of a contract or other obligation binding upon him/her.</li>
<li>That the Employee has not been the subject of any criminal investigation or on-going judicial inquiry, or convicted of a criminal offence involving moral turpitude or financial impropriety;</li>
<li>That the Employee is medically fit to carry out the duties of the position;</li>
<li>That the Employee possesses the requisite professional and academic qualifications;</li>
<li>That the Employee has not made any misrepresentations or omissions in regard to his/her academic qualifications or past record of employment.</li>
</ul>
<p>The Appointment shall commence on <span class="bold">{h(contract_start)}</span> and unless otherwise terminated earlier in accordance with this contract, shall continue for a period ending on <span class="bold">{h(contract_end)}</span>. This contract may, subject to satisfactory performance and availability of funds, be renewed on terms agreed by both parties in writing.</p>
<p>Name of project if recruitment is for a specific project: <span class="bold">{h(project_name)}</span></p>
<h3>Background and references</h3>
<p>This employment is subject to satisfactory background and reference checks, including a Certificate of Good Conduct where applicable, in line with TPO's Anti-Fraud and PSEAH Policies.</p>
<h3>Terms and Conditions of Employment</h3>
<p>In carrying out his/her duties, the Employee shall:</p>
<ul>
<li>report directly to {h(report_to)}.</li>
<li>devote all his/her time, attention and abilities to the performance of his/her duties and shall not take any assignment or employment outside his/her employment with TPO unless otherwise authorized by the Executive Director;</li>
<li>faithfully and diligently perform his/her duties;</li>
<li>obey all lawful and reasonable directions of the Supervisor(s) as issued from time to time.</li>
</ul>
<p>During the Appointment the Appointee shall not:</p>
<ul>
<li>be engaged or interested either directly or indirectly in any trade, business or occupation whatsoever which puts him/her in a conflict of interest situation with TPO;</li>
<li>take up political office or an active role in a political party or organization.</li>
</ul>
<h3>Hours of Work &amp; Working Arrangements</h3>
<p>Your normal working time is forty (40) hours per week. For the Kampala office, hours are 8:00 a.m.&ndash;5:30 p.m. Monday&ndash;Thursday and 8:00 a.m.&ndash;1:00 p.m. on Friday. For field offices, hours are 8:00 a.m.&ndash;5:00 p.m., with a half day on the last Friday of each month, per the People &amp; Culture Management Manual (PCMM).</p>
<p>Total weekly hours shall not exceed forty-eight (48) hours unless specifically authorised by the Executive Director in accordance with policy.</p>
<h3>Overtime</h3>
<p>Overtime is discouraged and no extra pay shall be provided; and where approved, compensation is by time-in-lieu with prior supervisor approval.</p>
<h3>Salary</h3>
<p>Salary payments shall be made according to the grade of the position, and all employees shall submit timesheets approved by their respective supervisors by the stipulated date.</p>
<p>TPO shall pay to the Employee a gross monthly salary of UGX <span class="bold">{hm(salary_gross)}</span> subject to monthly statutory deductions including NSSF, PAYE, Local Service Tax (LST) and any other statutory deductions that may be applicable as set by the related laws and regulations.</p>
<p>The Salary shall be deemed to accrue evenly from day to day and shall be payable in arrears by equal monthly instalments in accordance with TPO's pay policy, into a bank account nominated by the Employee.</p>
<h3>Notice</h3>
<p>Notice periods shall follow the Employment Act and PCMM:</p>
<ul>
<li>Two (2) weeks (&gt;6 months &lt;1 year);</li>
<li>One (1) month (&gt;1 &lt;5 years);</li>
<li>Two (2) months (&gt;5 &lt;10 years);</li>
<li>Three (3) months (&ge;10 years).</li>
</ul>
<p>Payment-in-lieu of notice may be applied. TPO reserves the right to summarily dismiss an employee without notice in cases of gross misconduct, following due process.</p>
<h3>Final Dues</h3>
<p>Upon termination in any manner, final wages and accrued benefits shall be paid within seven (7) days of the termination date, in accordance with Section 42(6) of the Employment Act. The employee shall ensure compliance with exit procedures.</p>
<h3>Funding-Cessation / Project Frustration</h3>
<p>If donor funding or project financing directly supporting the position is withdrawn, suspended, or materially reduced, TPO may terminate this contract with immediate effect (without prior notice). In that event, TPO shall: (i) pay all earned wages and accrued benefits to the termination date; (ii) pay payment-in-lieu of notice equal to the statutory/contractual entitlement; (iii) consider redeployment to suitable and available vacancies; (iv) where multiple roles are affected, comply with applicable collective-termination procedures; and (v) pay final dues within seven (7) days.</p>
<p><span class="bold">Force Majeure / Funding Interruption:</span> TPO Uganda shall not be liable for delays or failure to pay salaries caused by events beyond its reasonable control, including sudden donor funding withdrawal, natural disasters, or government restrictions.</p>
<h3>Disciplinary Procedures</h3>
<p>TPO's Disciplinary Code and Procedures are set out in the People &amp; Culture Management Manual (PCMM). The employee is required to observe and familiarise him/herself with the standards, policies, and procedures.</p>
<h3>Security and Safety</h3>
<p>All employees are required to take reasonable steps to ensure their own safety and that of colleagues, volunteers, service users and visitors.</p>
<h3>Confidentiality</h3>
<p>The employee's personal data shall be processed in accordance with TPO's Data Protection Policy and the Data Protection and Privacy Act (2019). No staff is permitted to divulge material, literature, information pertaining to the work of TPO Uganda with any external agencies, individuals or entity without the express authorization of the Executive Director.</p>
<h3>Certificate of Service</h3>
<p>Upon termination or expiry of this contract, the employee is entitled to a certificate of service, in accordance with the Employment Act.</p>
<h3>Other Relevant TPO Uganda Policies governing this Contract</h3>
<p>This contract will be enforced in tandem with the TPO Policies and Operations Manuals, specifically the People &amp; Culture Management Manual (PCMM) and the Finance Manual. Other relevant policy guidelines include the Procurement Manual, Staff Code of Conduct, Anti-fraud, safeguarding policies and the staff travel guide.</p>
<h3>Entire Agreement &amp; Variation</h3>
<p>This contract, together with the PCMM and referenced policies, constitutes the terms of employment. Any change to these terms must be in writing and signed by TPO Uganda.</p>
<h3>Approval:</h3>
<p>SIGNED FOR TPO UGANDA &nbsp;&nbsp; DATE:&nbsp;{sign_dots}</p>
<p class="spacer-md"></p>
<p>{sign_dots}</p>
<p><span class="bold">{h(director_name)}</span></p>
<p><span class="bold">Executive Director, TPO Uganda</span></p>
<p class="spacer-lg"></p>
<p>EMPLOYEE: &nbsp; DATE:&nbsp;{sign_dots}</p>
<p class="spacer-md"></p>
<p>{sign_dots} &nbsp; ({h(employee_name)})</p>
<p>{sign_dots} &nbsp; (Signature)</p>
""",
}