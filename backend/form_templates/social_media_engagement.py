SOCIAL_MEDIA_ENGAGEMENT = {
    "name": "STAFF WELLNESS & SOCIAL MEDIA ENGAGEMENT PLAN",
    "key": "social_media_engagement",
    "category": "Communications & Engagement",
    "description": "Staff wellness activities and social media content plan (TPO Uganda).",
    "fields": [
        {"name": "date", "label": "Plan Date", "type": "date", "required": False},
        {"name": "team", "label": "Department / Team", "type": "text", "required": False},
        {"name": "prepared_by", "label": "Prepared By", "type": "text", "required": False},
        {"name": "notes", "label": "Additional Notes", "type": "longtext", "required": False},
    ],
    "template": """
<h1>STAFF WELLNESS &amp; SOCIAL MEDIA<br/>ENGAGEMENT PLAN</h1>
<table class="info">
<tr><td class="k">Date</td><td>{h(date)}</td><td class="k">Department / Team</td><td>{h(team)}</td></tr>
<tr><td class="k">Prepared By</td><td>{h(prepared_by)}</td></tr>
</table>
<p><span class="bold">1. Wellness Wednesdays</span></p>
<p><span class="bold">Internal Activity:</span> 15-minute staff wellness sessions (stretching, mindfulness, breathing exercises, or desk yoga). Invite wellness experts for short talks.</p>
<p><span class="bold">Social Media Content:</span> Share wellness tips every Wednesday. Post short videos from experts. Create graphics on stress management, self-care, and mental health.</p>
<p><span class="bold">2. Step Challenge or Fitness Challenge</span></p>
<p><span class="bold">Internal Activity:</span> Monthly walking or fitness challenge among staff. Recognize top participants.</p>
<p><span class="bold">Social Media Content:</span> Share challenge updates and milestones. Encourage followers to participate and share their progress using a campaign hashtag.</p>
<p><span class="bold">3. Mental Health Awareness Campaign</span></p>
<p><span class="bold">Internal Activity:</span> Mental health check-in sessions. Peer support discussions. Employee wellness surveys.</p>
<p><span class="bold">Social Media Content:</span> Weekly mental health facts and myth-busting posts. Stories of resilience and coping strategies. Expert interviews.</p>
<p><span class="bold">4. Healthy Living Month</span></p>
<p><span class="bold">Internal Activity:</span> Healthy eating demonstrations. Nutrition talks. Fruit days at the office.</p>
<p><span class="bold">Social Media Content:</span> Healthy recipe features. Nutrition tips. &ldquo;Healthy Habit of the Week&rdquo; series.</p>
<p><span class="bold">5. Staff Spotlight Series</span></p>
<p><span class="bold">Internal Activity:</span> Recognize staff members who promote wellness and positive workplace culture.</p>
<p><span class="bold">Social Media Content:</span> Share employee wellness journeys. Feature staff hobbies, fitness routines, or self-care practices.</p>
<p><span class="bold">6. Mindfulness Mondays</span></p>
<p><span class="bold">Internal Activity:</span> Five-minute guided meditation sessions before work.</p>
<p><span class="bold">Social Media Content:</span> Weekly mindfulness tips. Reflection prompts. Guided breathing exercise videos.</p>
<p><span class="bold">7. Community Wellness Outreach</span></p>
<p><span class="bold">Internal Activity:</span> Wellness events with beneficiaries and community members. Mental health awareness activities in communities.</p>
<p><span class="bold">Social Media Content:</span> Event highlights and impact stories. Beneficiary testimonials. Photos and videos from outreach activities.</p>
<p><span class="bold">8. Wellness Webinars and Live Sessions</span></p>
<p><span class="bold">Internal Activity:</span> Host webinars on burnout prevention, work-life balance, and resilience.</p>
<p><span class="bold">Social Media Content:</span> Stream sessions live on social platforms. Share key takeaways and recordings afterward.</p>
<p><span class="bold">9. Monthly Wellness Themes</span></p>
<p><span class="bold">Examples:</span> January: Mental Health Awareness &middot; February: Self-Care and Relationships &middot; March: Physical Fitness &middot; April: Stress Management &middot; May: Work-Life Balance &middot; June: Men's Mental Health &middot; October: Mental Health Month.</p>
<p><span class="bold">Social Media Content:</span> Align all posts and activities with the monthly theme.</p>
<p><span class="bold">10. Wellness Champions Program</span></p>
<p><span class="bold">Internal Activity:</span> Identify staff wellness ambassadors across departments.</p>
<p><span class="bold">Social Media Content:</span> Feature Wellness Champions sharing tips and experiences. Encourage followers to adopt healthy habits.</p>
<div class="spacer-sm"></div>
<p><span class="bold">Suggested Social Media Hashtags</span></p>
<p>#WellnessAtTPO &middot; #HealthyMindsHealthyLives &middot; #TPOCares &middot; #MentalHealthMatters &middot; #WellnessWednesday &middot; #ThriveWithTPO &middot; #SelfCareEveryDay</p>
<p class="spacer-sm"></p>
<p><span class="bold">Additional Notes:</span></p>
<p>{h(notes)}</p>
""",
}