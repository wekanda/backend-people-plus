SLA_AGREEMENT = {
    "name": "SERVICE LEVEL AGREEMENT",
    "key": "sla",
    "category": "Contracts & Letters",
    "description": "Service Level Agreement between TPO Uganda and an independent contractor.",
    "fields": [
        {"name": "day", "label": "Day (e.g. 1st)", "type": "text", "required": False},
        {"name": "month", "label": "Month", "type": "text", "required": False},
        {"name": "contractor_name", "label": "Name of Contractor", "type": "text", "required": True},
        {"name": "contractor_title", "label": "Contractor's Title", "type": "text", "required": True},
        {"name": "title_acronym", "label": "Title Acronym", "type": "text", "required": False},
        {"name": "project_name", "label": "Project Name", "type": "text", "required": False},
        {"name": "project_location", "label": "Project Location", "type": "text", "required": False},
        {"name": "start_date", "label": "Start Date", "type": "date", "required": True},
        {"name": "end_date", "label": "End Date", "type": "date", "required": True},
        {"name": "duration", "label": "Duration (Years/Months)", "type": "text", "required": False},
        {"name": "amount_words", "label": "Monthly Fee (Words)", "type": "text", "required": False},
        {"name": "amount_figures", "label": "Monthly Fee (Figures)", "type": "number", "required": True},
        {"name": "duties", "label": "Duties / Responsibilities", "type": "longtext", "required": False},
    ],
    "template": """
<div class="center"><span class="bold">THE REPUBLIC OF UGANDA</span></div>
<h1>SERVICE LEVEL AGREEMENT</h1>
<p class="center"><span class="bold">THIS AGREEMENT</span> is made this <span class="bold">__{h(day, '____')}__</span> of <span class="bold">__{h(month, '______')}__</span> 2026.</p>
<div class="spacer-sm"></div>
<p class="center"><span class="bold">BETWEEN</span></p>
<p class="center">TPO Uganda (hereinafter referred to as &ldquo;<span class="bold">the CLIENT</span>&rdquo;)</p>
<div class="spacer-sm"></div>
<p class="center"><span class="bold">AND</span></p>
<p class="center"><span class="bold">{h(contractor_name)}</span> hereinafter referred to as [<span class="bold">&ldquo;{h(contractor_title)}&rdquo;</span>] under the <span class="bold">[{h(project_name)}]</span> in <span class="bold">[{h(project_location)}].</span></p>
<div class="spacer-sm"></div>
<p>Whereas TPO Uganda is desirous to engage the services of a <span class="bold">[{h(contractor_title)}]</span> on the terms and conditions hereinafter set forth and</p>
<p>Whereas the <span class="bold">[{h(contractor_title)}]</span> is ready and willing to accept the engagement of services with TPO Uganda on the said terms and conditions</p>
<p><span class="bold">NOW, THEREFORE,</span> the parties hereto agree as follows:</p>
<p><span class="bold">1. STATUS OF THE SUBSCRIBER</span></p>
<p>The <span class="bold">[{h(contractor_title)}]</span> will be considered as an independent practitioner. He/she shall not be considered as a staff member of TPO Uganda.</p>
<p>Please note that this offer of employment is made to you with the understanding that you do not have a history of fraud and sexual offences. In accordance with the <span class="bold">TPO Uganda's Anti-Fraud and PSHEA Policies 2021</span>, you are expected to abide and comply with the terms and conditions therein at all times. Any violation of this and other policies is highly punishable as per guidelines indicated in the various policies and laws of Uganda.</p>
<p><span class="bold">2. NATURE OF SERVICES</span></p>
<p>The <span class="bold">[{h(contractor_title)}]</span> ({h(title_acronym)}) shall perform the services described in the duties scheduled below. TPO will avail all the relevant information and documents important for this assignment including personnel, all relevant publications, reports, photos and other information as may be required for this task.</p>
<p><span class="bold">3. DUTIES AND RESPONSIBILITIES</span></p>
<p>{h(duties)}</p>
<p><span class="bold">4. DURATION OF AGREEMENT AND TERMS OF PAYMENT</span></p>
<p>The contract shall commence from <span class="bold">[{h(start_date)}]</span> to <span class="bold">[{h(end_date)}]</span> ({h(duration)}). Termination can be made in writing without notice based on operational needs, poor performance, disciplinary problems or any other extenuating circumstances.</p>
<p class="spacer-sm"> </p>
<p><span class="bold">5. PAYMENT</span></p>
<p>The monthly contract fee will be <span class="bold">[{h(amount_words)}]</span> <span class="bold">[{hm(amount_figures)}]</span> payable monthly subject to 6% withholding tax. It is the responsibility of the <span class="bold">[{h(contractor_title)}]</span> to meet his/her necessity, housing, health and insurable needs. TPO Uganda will not deal with a proxy; where the <span class="bold">[{h(contractor_title)}]</span> is unable to perform their assignment, payment equivalent to non-performance time will be forfeited.</p>
<p><span class="bold">6. GOVERNING LAW AND RESOLUTION OF DISPUTES</span></p>
<p>This contract, including any disputes related thereto shall be governed by the laws of Uganda. Any claims arising out of performance of this contract that is related to any decision of the government must be resolved in accordance with Uganda laws.</p>
<p>The following procedures shall govern the resolution of any disputes, controversy or claims between or among the parties arising out of interpretation, performance, breach or alleged breach of contract.</p>
<p><span class="bold">Negotiation.</span> The parties shall promptly attempt to resolve any disputes by negotiation in the normal course of business. If after good faith efforts the dispute is not resolved, either party may request in writing that the dispute be resolved via executive consultation.</p>
<p><span class="bold">Executive consultation.</span> For disputes submitted for executive consultation each party shall designate a person in position of authority and responsibility.</p>
<p><span class="bold">Arbitration.</span> Any controversy or claim between the parties arising out of or relating to this contract, or breach thereof that has not been resolved by executive consultation shall be settled by arbitration administered by an approved legal representative.</p>
<p>The <span class="bold">[{h(contractor_title)}]</span> shall diligently proceed with the performance of work pending final resolution.</p>
<div class="spacer-md"></div>
<p><span class="bold">SIGNATURES</span></p>
<p>I have read and understood and hereby agree to the terms and conditions herein</p>
<p>Name: {sign_dots}</p>
<p>Signed: {sign_dots} &nbsp; Date: {sign_dots}</p>
<div class="spacer-sm"></div>
<p><span class="bold">Signed on behalf of TPO Uganda</span></p>
<p>{sign_dots} &nbsp; Date: {sign_dots}</p>
<p><span class="bold">Peter Okwi</span></p>
<p><span class="bold">Executive Director</span></p>
<p class="spacer-sm"> </p>
<p><span class="bold">Witnessed By</span></p>
<p>Name: {sign_dots} &nbsp; Signature: {sign_dots}</p>
<p>Date: {sign_dots}</p>
""",
}