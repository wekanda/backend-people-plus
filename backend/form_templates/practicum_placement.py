PRACTICUM_PLACEMENT = {
    "name": "ACCEPTANCE LETTER FOR PRACTICUM PLACEMENT",
    "key": "practicum_placement",
    "category": "Internships",
    "description": "Internship placement acceptance letter (TPO Uganda).",
    "fields": [
        {"name": "date", "label": "Date", "type": "date", "required": True},
        {"name": "intern_name", "label": "Name of Intern", "type": "text", "required": True},
        {"name": "location", "label": "Field Office Location", "type": "text", "required": True},
        {"name": "duration", "label": "Duration (e.g. six (6) weeks)", "type": "text", "required": True},
        {"name": "start_date", "label": "Start Date", "type": "date", "required": True},
        {"name": "end_date", "label": "End Date", "type": "date", "required": True},
        {"name": "director_name", "label": "Signatory Name", "type": "text", "required": False, "default": "Peter Okwi"},
    ],
    "template": """
<h1>ACCEPTANCE LETTER FOR<br/>PRACTICUM PLACEMENT</h1>
<p class="right"><span class="bold">({h(date)})</span></p>
<div class="spacer-sm"></div>
<p>To: <span class="bold">({h(intern_name)})</span></p>
<div class="spacer-sm"></div>
<p><span class="bold">RE:</span>&nbsp; <span class="bold ul">ACCEPTANCE LETTER FOR PRACTICUM PLACEMENT</span></p>
<p>TPO Uganda is a National Humanitarian and Development Non-Governmental Organization (NGO) that has been delivering services to vulnerable communities in Uganda since 1994. Our work covers; Mental, Neurological and Substance Use Disorders (MNS); Child Care and Protection; Gender-Based Violence Prevention and Mitigation; HIV/AIDS Prevention, Care and Support; Disaster Risk Prevention and Response; livelihood support; and Organizational Development and Sustainability. Over the years, TPO Uganda has grown into a respectable National NGO with a demonstrable track record in up to 45 Districts spread across seven sub-regions as of December 2024.</p>
<div class="spacer-sm"></div>
<p>Following your application for Practicum placement with TPO Uganda, I am delighted to inform you that you have been considered for an internship placement at our Field Office in <span class="bold">({h(location)})</span> for <span class="bold">({h(duration)})</span>, starting <span class="bold">({h(start_date)})</span> and ending <span class="bold">({h(end_date)})</span>. Your reporting line is directly to the Regional Manager. This position is non-paid; thus, it's the responsibility of the intern to meet his/her own safety, housing, health, and insurable needs.</p>
<div class="spacer-sm"></div>
<p>Please do not hesitate to contact the undersigned, should you have any questions or require further communications.</p>
<div class="spacer-md"></div>
<p><span class="bold">Yours sincerely,</span></p>
<div class="spacer-md"></div>
<p>{sign_dots}</p>
<p><span class="bold">{h(director_name)}</span></p>
<p><span class="bold">Executive Director.</span></p>
<div class="spacer-lg"></div>
<p><span class="bold">I accept/decline this offer by signing <i>(Circle as applicable)</i></span></p>
<div class="spacer-lg"></div>
<p>{sign_dots} &nbsp; &nbsp; &nbsp; Date:&nbsp;…………………………………</p>
<p class="center"><span class="bold">({h(intern_name)})</span></p>
<p class="center"><span class="bold">Internship Student</span></p>
<div class="spacer-md"></div>
<p><span class="bold">Please Note:</span> This offer of employment is made to you with the understanding that you do not have a history of fraud and sexual offences. In accordance with the TPO Uganda's Anti-Fraud and PSHEA Policies 2021, you are expected to abide and comply with the terms and conditions therein at all times. Any violation of this and other policies is highly punishable as per guidelines indicated in the various policies and laws of Uganda.</p>
""",
}