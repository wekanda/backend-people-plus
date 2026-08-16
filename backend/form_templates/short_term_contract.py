SHORT_TERM_CONTRACT = {
    "name": "SHORT TERM CONTRACT / SERVICE AGREEMENT",
    "key": "short_term_contract",
    "category": "Contracts & Letters",
    "description": "Short-term service agreement for a Volunteer Psychosocial Assistant (VPA).",
    "fields": [
        {"name": "made_on", "label": "Made On (date)", "type": "date", "required": True},
        {"name": "contractor_name", "label": "Contractor Name", "type": "text", "required": True},
        {"name": "contractor_title", "label": "Contractor Title", "type": "text", "required": True},
        {"name": "project_location", "label": "Project Location", "type": "text", "required": False},
        {"name": "project_name", "label": "Project Name", "type": "text", "required": False},
        {"name": "start_date", "label": "Start Date", "type": "date", "required": True},
        {"name": "end_date", "label": "End Date", "type": "date", "required": True},
        {"name": "fee_figures", "label": "Contract Fee (Figures)", "type": "number", "required": True},
        {"name": "fee_words", "label": "Contract Fee (Words)", "type": "text", "required": False},
        {"name": "wht_rate", "label": "WHT Rate %", "type": "number", "required": False, "default": "6"},
        {"name": "tin_number", "label": "TIN Number", "type": "text", "required": False},
        {"name": "airtime_amount", "label": "Airtime Facilitation", "type": "number", "required": False, "default": "10000"},
        {"name": "momo_number", "label": "Mobile Money Number", "type": "text", "required": False},
        {"name": "director_name", "label": "Signatory Name", "type": "text", "required": False, "default": "Peter Okwi"},
        {"name": "duties", "label": "Duties & Responsibilities", "type": "longtext", "required": False},
    ],
    "template": """
<div class="center"><span class="bold">THE REPUBLIC OF UGANDA</span></div>
<h1>SERVICE AGREEMENT</h1>
<p><span class="bold">MADE ON</span> {hd(made_on)} between TPO Uganda (hereinafter referred as the &ldquo;contractor&rdquo;) and <span class="bold">{h(contractor_name)}</span>, (Hereinafter referred to as &ldquo;<span class="bold">{h(contractor_title)}</span>&rdquo;) for its Project in <span class="bold">{h(project_location)} - Refugee Settlement</span>. <span class="bold">{h(project_name)}</span> Project. Whereas TPO Uganda is desirous to engage the services of a {h(contractor_title)} on the terms and conditions hereinafter set forth and; Whereas <span class="bold">{h(contractor_name)}</span> is ready and willing to accept the engagement of services with TPO Uganda on the said terms and conditions. <span class="bold">NOW, THEREFORE,</span> the parties hereto agree as follows:</p>
<div class="spacer-sm"></div>
<p><span class="bold">1. STATUS OF THE SUBSCRIBER</span></p>
<p>The {h(contractor_title)} will be considered as an independent practitioner. He/she shall not be in any way/respect as being a staff member of TPO Uganda or organization affiliated to this.</p>
<p>Please note that this offer of employment is made to you with the understanding that you do not have a history of fraud and sexual offences. In accordance with the <span class="bold">TPO Uganda's Anti-Fraud and Prevention of Sexual Harassment, Exploitation and Abuse Policies 2021</span>, you are expected to abide and comply with the terms and conditions therein at all times. Any violation of this and other policies is highly punishable as per guidelines indicated in the various policies and laws of Uganda.</p>
<p><span class="bold">2. NATURE OF SERVICES</span></p>
<p>The {h(contractor_title)} shall perform the services described in the duties below. TPO will avail all relevant information and documents important for this assignment including personnel, all relevant publications, reports, photos and other information as may be required for this task.</p>
<p><span class="bold">3. DUTIES AND RESPONSIBILITIES</span></p>
<p>{h(duties)}</p>
<p><span class="bold">4. DURATION OF AGREEMENT AND TERMS OF PAYMENT</span></p>
<p>The contract shall commence <span class="bold">{hd(start_date)}</span> to <span class="bold">{hd(end_date)}</span>. Termination can be made in writing without notice based on operational needs, poor performance, disciplinary problems or other extenuating circumstances.</p>
<p><span class="bold">5. PAYMENT</span></p>
<p>The contract fee will be <span class="bold">{hm(fee_figures)}/= ({h(fee_words)})</span> Subject to {h(wht_rate)}% WHT in this Tin number <span class="bold">{h(tin_number)}</span>. This will be paid at the end of the month through your registered mobile money number {h(momo_number)} and you shall be required to sign the acknowledgement form confirming the money received.</p>
<p>You are also entitled to <span class="bold">{hm(airtime_amount)}/=</span> monthly airtime facilitation paid to the phone number of your choice. It is the responsibility of the {h(contractor_title)} to meet his/her necessity, housing, health and insurable needs. TPO Uganda will not deal with a proxy; where the {h(contractor_title)} is unable to perform their assignment, payment equivalent to non-performance time will be forfeited.</p>
<p><span class="bold">6. GOVERNING LAW AND RESOLUTION OF DISPUTES</span></p>
<p>This contract shall be governed by the laws of Uganda. The following procedures shall govern the resolution of any disputes between the parties:</p>
<p><span class="bold">Negotiation.</span> The parties shall promptly attempt to resolve any disputes by negotiation in the normal course of business. If after good faith efforts the dispute is not resolved, either party may request in writing that the dispute be resolved via executive consultation.</p>
<p><span class="bold">Executive consultation.</span> For disputes submitted for executive consultation each party shall designate a person in position of authority and responsibility.</p>
<p><span class="bold">Arbitration.</span> Any controversy or claim between the parties arising out of or relating to this contract, or breach thereof that has not been resolved by executive consultation shall be settled by arbitration administered by an approved legal representative. The {h(contractor_title)} shall diligently proceed with the performance of work pending final resolution. </p>
<p class="spacer-md"></p>
<p><span class="bold">Signatures</span></p>
<p>I have read and understood and hereby agree to the terms and conditions herein</p>
<p><span class="bold">Signed on behalf of TPO Uganda</span></p>
<p>Signature: {sign_dots} &nbsp; Date: {sign_dots}</p>
<p><span class="bold">{h(director_name)}</span></p>
<p><span class="bold">Executive Director</span></p>
<p class="spacer-md"></p>
<p>Name: {sign_dots}</p>
<p>Signed: {sign_dots} &nbsp; Date: {sign_dots}</p>
""",
}