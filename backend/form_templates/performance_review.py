PERFORMANCE_REVIEW = {
    "name": "STAFF PERFORMANCE REVIEW RATING",
    "key": "performance_review",
    "category": "Performance",
    "description": "Performance review rating form using the TPO five-point rating scale.",
    "fields": [
        {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "position", "label": "Position", "type": "text", "required": False},
        {"name": "supervisor", "label": "Supervisor", "type": "text", "required": False},
        {"name": "review_period", "label": "Review Period (FY)", "type": "text", "required": False},
        {"name": "review_date", "label": "Review Meeting Date", "type": "date", "required": False},
        {"name": "overall_rating", "label": "Overall Rating", "type": "select",
         "options": ["Outstanding", "Commendable", "Fully Competent", "Needs Improvement", "Unsatisfactory", "TNR (too new to be rated)"],
         "required": True},
        {"name": "key_achievements", "label": "Key Achievements", "type": "longtext", "required": False},
        {"name": "development_areas", "label": "Development Areas", "type": "longtext", "required": False},
        {"name": "objectives_next_year", "label": "Objectives for Next Year", "type": "longtext", "required": False},
        {"name": "employee_comments", "label": "Employee Comments", "type": "longtext", "required": False},
        {"name": "supervisor_comments", "label": "Supervisor Comments", "type": "longtext", "required": False},
    ],
    "template": """
<h1>PERFORMANCE REVIEW RATING GUIDELINES</h1>
<p class="center"><span class="bold">Staff Performance Reviews</span></p>
<p>At the end of the financial year, all eligible staff will be expected to hold a formal performance review and evaluation meeting with their supervisors to appraise their performance during the year, discuss their individual development plan, start discussions on performance objectives for the upcoming year and provide opportunity for supervisors to receive feedback from their direct reports. A five-point rating scale for differentiating performance will be used. The categories are;</p>
<p>1) Outstanding. &nbsp; 2) Commendable. &nbsp; 3) Fully competent. &nbsp; 4) Needs improvement. &nbsp; 5) Unsatisfactory. &nbsp; 6) TNR (too new to be rated).</p>
<table class="bordered">
<tr><th style="width:10%">Rating</th><th>Scale</th><th>Description</th></tr>
<tr><td class="center"><span class="bold">O</span></td><td><span class="bold">Outstanding</span> &ndash; consistently and far exceeded the requirements of the role this year</td><td>Extraordinary, exemplary and exceptional accomplishments with significant contributions to the objectives of the department or the whole Organization. Performance clearly stands out from peers.</td></tr>
<tr><td class="center"><span class="bold">C</span></td><td><span class="bold">Commendable</span> &ndash; consistently exceeded many of the requirements of the role this year</td><td>Superior results above those expected; top 20% of performers in the organization; potential for added responsibility.</td></tr>
<tr><td class="center"><span class="bold">FC</span></td><td><span class="bold">Fully Competent</span> &ndash; successfully achieved the requirements of the role this year</td><td>Good, successful, effective performance; fulfilled all position requirements and sometimes more.</td></tr>
<tr><td class="center"><span class="bold">NI</span></td><td><span class="bold">Needs Improvement</span> &ndash; partially achieved the requirements of the role</td><td>Performance below the expected standard; improvement required; focused support and follow-up.</td></tr>
<tr><td class="center"><span class="bold">U</span></td><td><span class="bold">Unsatisfactory</span> &ndash; failed to meet the requirements of the role</td><td>Significant failure to meet expectations; formal performance improvement plan or disciplinary process.</td></tr>
<tr><td class="center"><span class="bold">TNR</span></td><td><span class="bold">Too New to be Rated</span></td><td>Staff in post for less than the qualifying period at end of the financial year.</td></tr>
</table>
<div class="spacer-sm"></div>
<h2>STAFF PERFORMANCE APPRAISAL FORM</h2>
<table class="info">
<tr><td class="k">Employee Name</td><td>{h(employee_name)}</td><td class="k">Position</td><td>{h(position)}</td></tr>
<tr><td class="k">Supervisor</td><td>{h(supervisor)}</td><td class="k">Review Period</td><td>{h(review_period)}</td></tr>
<tr><td class="k">Review Meeting Date</td><td>{h(review_date)}</td><td class="k">Overall Rating</td><td><span class="bold">{h(overall_rating)}</span></td></tr>
</table>
<p><span class="bold">Key Achievements this year:</span></p>
<p>{h(key_achievements)}</p>
<p><span class="bold">Development areas &amp; individual development plan:</span></p>
<p>{h(development_areas)}</p>
<p><span class="bold">Performance objectives for the upcoming year:</span></p>
<p>{h(objectives_next_year)}</p>
<p><span class="bold">Employee comments:</span></p>
<p>{h(employee_comments)}</p>
<p><span class="bold">Supervisor comments:</span></p>
<p>{h(supervisor_comments)}</p>
<div class="spacer-md"></div>
<p>Employee signature: <span class="field-value">{sign_dots}</span> &nbsp;&nbsp; Date: <span class="field-value">{sign_dots}</span></p>
<p>Supervisor signature: <span class="field-value">{sign_dots}</span> &nbsp;&nbsp; Date: <span class="field-value">{sign_dots}</span></p>
""",
}