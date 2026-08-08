#!/usr/bin/env python3
"""
Seed document templates into the database.
This script creates predefined document templates that can be used with the document generator.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import json
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from database import SessionLocal
from backend import models

def create_employment_contract_template():
    """Create Employment Contract template"""
    content = """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; margin: 40px;">
<h1 style="text-align: center;">EMPLOYMENT AGREEMENT</h1>

<p>This Employment Agreement is entered into on {{ date }} between:</p>

<p><strong>PEOPLE PLUS HR SYSTEMS</strong> (hereinafter "Employer")</p>

<p>AND</p>

<p><strong>{{ employee_name }}</strong> (hereinafter "Employee")</p>

<h2>WHEREAS</h2>
<p>The Employer wishes to employ the Employee and the Employee wishes to be employed by the Employer on the terms and conditions set forth herein:</p>

<h2>1. POSITION</h2>
<p>The Employee shall be employed as a <strong>{{ position }}</strong> in the <strong>{{ department }}</strong> department.</p>

<h2>2. EMPLOYMENT START DATE</h2>
<p>Employment shall commence on <strong>{{ date_of_appointment }}</strong> and shall continue until terminated as per the provisions herein.</p>

<h2>3. COMPENSATION</h2>
<p>The Employee shall receive an annual salary of <strong>{{ currency }} {{ salary }}</strong>, payable in monthly installments.</p>

<h2>4. BENEFITS</h2>
<p>The Employee shall be entitled to:
<ul>
<li>Annual leave of 21 days</li>
<li>Health insurance coverage</li>
<li>Pension contributions</li>
<li>Other benefits as per company policy</li>
</ul>
</p>

<h2>5. DUTIES AND RESPONSIBILITIES</h2>
<p>The Employee shall perform duties as assigned by management consistent with the position of {{ position }}.</p>

<h2>6. CONFIDENTIALITY</h2>
<p>The Employee agrees to maintain confidentiality of all company information and proprietary data.</p>

<h2>7. TERMINATION</h2>
<p>Either party may terminate this agreement by giving 30 days written notice, or as per statutory requirements.</p>

<h2>8. GOVERNING LAW</h2>
<p>This agreement is governed by the laws of Uganda.</p>

<p style="margin-top: 50px;">
IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.
</p>

<table style="width: 100%; border-collapse: collapse;">
<tr>
<td style="width: 50%; text-align: center; padding: 30px 10px 10px 10px;">
<strong>EMPLOYER</strong><br/><br/>
_____________________<br/>
HR Director<br/>
People Plus HR Systems<br/><br/>
Date: _______________
</td>
<td style="width: 50%; text-align: center; padding: 30px 10px 10px 10px;">
<strong>EMPLOYEE</strong><br/><br/>
_____________________<br/>
{{ employee_name }}<br/><br/>
Date: _______________
</td>
</tr>
</table>

</body>
</html>
"""
    
    fields = [
        {"name": "date", "label": "Contract Date", "type": "date", "required": True},
        {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "position", "label": "Job Position", "type": "text", "required": True},
        {"name": "department", "label": "Department", "type": "text", "required": True},
        {"name": "date_of_appointment", "label": "Date of Appointment", "type": "date", "required": True},
        {"name": "salary", "label": "Annual Salary", "type": "number", "required": True},
        {"name": "currency", "label": "Currency", "type": "text", "required": True},
    ]
    
    return {
        "name": "Employment Contract",
        "description": "Full employment contract with terms and conditions",
        "category": "contract",
        "template_type": "html",
        "content": content,
        "fields": fields
    }


def create_appointment_letter_template():
    """Create Appointment Letter template"""
    content = """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; margin: 40px;">
<h1>APPOINTMENT LETTER</h1>

<p>Date: {{ date }}</p>

<p>To:<br/>
{{ employee_name }}<br/>
{{ employee_email }}<br/>
{{ employee_address }}
</p>

<p>Dear {{ employee_name }},</p>

<p>We are pleased to confirm your appointment as <strong>{{ position }}</strong> at People Plus HR Systems.</p>

<h2>Position Details:</h2>
<ul>
<li><strong>Position:</strong> {{ position }}</li>
<li><strong>Department:</strong> {{ department }}</li>
<li><strong>Start Date:</strong> {{ start_date }}</li>
<li><strong>Employment Type:</strong> {{ employment_type }}</li>
<li><strong>Reporting To:</strong> {{ manager_name }}</li>
<li><strong>Office Location:</strong> {{ location }}</li>
</ul>

<h2>Compensation Package:</h2>
<ul>
<li><strong>Annual Salary:</strong> {{ currency }} {{ salary }}</li>
<li><strong>Benefits:</strong> {{ benefits }}</li>
</ul>

<h2>Terms of Employment:</h2>
<ol>
<li>This is an employment relationship subject to the laws of Uganda.</li>
<li>Your employment is subject to satisfactory completion of background checks and verification.</li>
<li>You will be subject to our company policies as per the employee handbook.</li>
<li>You are required to provide all necessary employment documents before your start date.</li>
</ol>

<p>We look forward to welcoming you to our team and working together towards our shared goals.</p>

<p>Best regards,</p>

<p>
Human Resources Department<br/>
People Plus HR Systems
</p>

</body>
</html>
"""
    
    fields = [
        {"name": "date", "label": "Letter Date", "type": "date", "required": True},
        {"name": "employee_name", "label": "Employee Name", "type": "text", "required": True},
        {"name": "employee_email", "label": "Email Address", "type": "email", "required": True},
        {"name": "employee_address", "label": "Address", "type": "text", "required": False},
        {"name": "position", "label": "Job Position", "type": "text", "required": True},
        {"name": "department", "label": "Department", "type": "text", "required": True},
        {"name": "start_date", "label": "Start Date", "type": "date", "required": True},
        {"name": "employment_type", "label": "Employment Type", "type": "select", "required": True, "options": ["Full-time", "Part-time", "Contract"]},
        {"name": "manager_name", "label": "Reporting Manager", "type": "text", "required": False},
        {"name": "location", "label": "Office Location", "type": "text", "required": False},
        {"name": "salary", "label": "Annual Salary", "type": "number", "required": True},
        {"name": "currency", "label": "Currency", "type": "text", "required": True},
        {"name": "benefits", "label": "Benefits", "type": "textarea", "required": False},
    ]
    
    return {
        "name": "Appointment Letter",
        "description": "Letter confirming employee appointment with details",
        "category": "letter",
        "template_type": "html",
        "content": content,
        "fields": fields
    }


def create_offer_letter_template():
    """Create Offer Letter template"""
    content = """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; margin: 40px;">
<h1>OFFER OF EMPLOYMENT</h1>

<p>Date: {{ date }}</p>

<p>Dear {{ applicant_name }},</p>

<p>We are pleased to make you a formal offer of employment for the position of <strong>{{ position }}</strong> at People Plus HR Systems.</p>

<h2>Position Details:</h2>
<ul>
<li><strong>Job Title:</strong> {{ position }}</li>
<li><strong>Department:</strong> {{ department }}</li>
<li><strong>Location:</strong> {{ location }}</li>
<li><strong>Proposed Start Date:</strong> {{ start_date }}</li>
<li><strong>Employment Type:</strong> {{ employment_type }}</li>
</ul>

<h2>Compensation Package:</h2>
<ul>
<li><strong>Base Salary:</strong> {{ currency }} {{ base_salary }} per annum</li>
<li><strong>Additional Benefits:</strong> {{ benefits }}</li>
<li><strong>Annual Leave:</strong> 21 working days</li>
</ul>

<h2>Your Responsibilities Will Include:</h2>
<p>{{ responsibilities }}</p>

<h2>Conditions of Employment:</h2>
<ol>
<li>This offer is conditional upon successful background verification.</li>
<li>You are required to provide proof of educational qualifications.</li>
<li>A medical examination may be required.</li>
<li>You will be required to sign our standard employment contract.</li>
<li>You must provide all necessary employment documents as per company requirements.</li>
</ol>

<p><strong>Acceptance Deadline:</strong> {{ acceptance_deadline }}</p>

<p>If you accept this offer, please confirm your acceptance by the deadline above.</p>

<p>We look forward to your response and welcoming you to our team.</p>

<p>
Sincerely,<br/><br/>
Human Resources Department<br/>
People Plus HR Systems
</p>

</body>
</html>
"""
    
    fields = [
        {"name": "date", "label": "Offer Date", "type": "date", "required": True},
        {"name": "applicant_name", "label": "Applicant Name", "type": "text", "required": True},
        {"name": "position", "label": "Position", "type": "text", "required": True},
        {"name": "department", "label": "Department", "type": "text", "required": True},
        {"name": "location", "label": "Location", "type": "text", "required": False},
        {"name": "start_date", "label": "Proposed Start Date", "type": "date", "required": True},
        {"name": "employment_type", "label": "Employment Type", "type": "select", "required": True, "options": ["Full-time", "Part-time", "Contract"]},
        {"name": "base_salary", "label": "Base Salary", "type": "number", "required": True},
        {"name": "currency", "label": "Currency", "type": "text", "required": True},
        {"name": "benefits", "label": "Additional Benefits", "type": "textarea", "required": False},
        {"name": "responsibilities", "label": "Key Responsibilities", "type": "textarea", "required": False},
        {"name": "acceptance_deadline", "label": "Acceptance Deadline", "type": "date", "required": True},
    ]
    
    return {
        "name": "Offer Letter",
        "description": "Formal job offer letter to candidates",
        "category": "letter",
        "template_type": "html",
        "content": content,
        "fields": fields
    }


def create_payslip_template():
    """Create Payslip template"""
    content = """
<html>
<body style="font-family: Arial, sans-serif; font-size: 12px; margin: 30px;">

<div style="text-align: center; margin-bottom: 30px;">
<h1 style="margin: 0;">PAYSLIP</h1>
<p style="margin: 5px 0;">People Plus HR Systems</p>
</div>

<table style="width: 100%; margin-bottom: 20px; border-collapse: collapse;">
<tr>
<td style="width: 50%; padding: 10px; border: 1px solid #ddd;">
<strong>Employee Information</strong><br/>
Name: {{ employee_name }}<br/>
Employee ID: {{ employee_file_code }}<br/>
Position: {{ employee_position }}<br/>
Department: {{ department }}
</td>
<td style="width: 50%; padding: 10px; border: 1px solid #ddd;">
<strong>Pay Period</strong><br/>
From: {{ period_start }}<br/>
To: {{ period_end }}<br/>
Generated: {{ date }}
</td>
</tr>
</table>

<table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
<tr style="background-color: #f0f0f0; font-weight: bold;">
<td style="padding: 10px; border: 1px solid #ddd; width: 60%;">EARNINGS</td>
<td style="padding: 10px; border: 1px solid #ddd; width: 40%; text-align: right;">Amount</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">Basic Salary</td>
<td style="padding: 10px; border: 1px solid #ddd; text-align: right;">{{ currency }} {{ basic_salary }}</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">Gross Salary</td>
<td style="padding: 10px; border: 1px solid #ddd; text-align: right; font-weight: bold;">{{ currency }} {{ gross_salary }}</td>
</tr>
</table>

<table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
<tr style="background-color: #f0f0f0; font-weight: bold;">
<td style="padding: 10px; border: 1px solid #ddd; width: 60%;">DEDUCTIONS</td>
<td style="padding: 10px; border: 1px solid #ddd; width: 40%; text-align: right;">Amount</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">Income Tax</td>
<td style="padding: 10px; border: 1px solid #ddd; text-align: right;">{{ currency }} {{ income_tax }}</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">NSSF Contribution</td>
<td style="padding: 10px; border: 1px solid #ddd; text-align: right;">{{ currency }} {{ nssf }}</td>
</tr>
<tr>
<td style="padding: 10px; border: 1px solid #ddd;">Other Deductions</td>
<td style="padding: 10px; border: 1px solid #ddd; text-align: right;">{{ currency }} {{ other_deductions }}</td>
</tr>
<tr style="background-color: #f0f0f0; font-weight: bold;">
<td style="padding: 10px; border: 1px solid #ddd;">TOTAL DEDUCTIONS</td>
<td style="padding: 10px; border: 1px solid #ddd; text-align: right;">{{ currency }} {{ total_deductions }}</td>
</tr>
</table>

<table style="width: 100%; border-collapse: collapse; margin-bottom: 30px;">
<tr style="background-color: #d4edda; font-weight: bold; font-size: 14px;">
<td style="padding: 15px; border: 2px solid #28a745; width: 60%;">NET PAY</td>
<td style="padding: 15px; border: 2px solid #28a745; width: 40%; text-align: right;">{{ currency }} {{ net_pay }}</td>
</tr>
</table>

<p style="font-size: 10px; color: #666; margin-top: 30px;">
This is a computer-generated payslip. No signature is required.
For queries, contact the HR Department.
</p>

</body>
</html>
"""
    
    fields = [
        {"name": "date", "label": "Generated Date", "type": "date", "required": True},
        {"name": "period_start", "label": "Pay Period Start", "type": "date", "required": True},
        {"name": "period_end", "label": "Pay Period End", "type": "date", "required": True},
        {"name": "department", "label": "Department", "type": "text", "required": False},
        {"name": "basic_salary", "label": "Basic Salary", "type": "number", "required": True},
        {"name": "gross_salary", "label": "Gross Salary", "type": "number", "required": True},
        {"name": "income_tax", "label": "Income Tax", "type": "number", "required": True},
        {"name": "nssf", "label": "NSSF Contribution", "type": "number", "required": True},
        {"name": "other_deductions", "label": "Other Deductions", "type": "number", "required": False},
        {"name": "total_deductions", "label": "Total Deductions", "type": "number", "required": True},
        {"name": "net_pay", "label": "Net Pay", "type": "number", "required": True},
        {"name": "currency", "label": "Currency", "type": "text", "required": True},
    ]
    
    return {
        "name": "Payslip",
        "description": "Employee monthly salary statement",
        "category": "payslip",
        "template_type": "html",
        "content": content,
        "fields": fields
    }


def seed_templates():
    """Seed all templates into database"""
    db = SessionLocal()
    
    try:
        # Create a default admin user for the created_by field
        admin = db.query(models.User).filter(models.User.email == "admin@peoplepluse.com").first()
        if not admin:
            print("ERROR: Admin user not found. Please run seed_hr_data.py first.")
            return False
        
        # Define all templates
        template_configs = [
            create_employment_contract_template(),
            create_appointment_letter_template(),
            create_offer_letter_template(),
            create_payslip_template(),
        ]
        
        # Create templates
        for config in template_configs:
            existing = db.query(models.DocumentTemplate).filter(
                models.DocumentTemplate.name == config["name"]
            ).first()
            
            if existing:
                print(f"✓ Template '{config['name']}' already exists. Skipping...")
                continue
            
            template = models.DocumentTemplate(
                name=config["name"],
                description=config["description"],
                category=config["category"],
                template_type=config["template_type"],
                content=config["content"],
                fields_json=json.dumps(config["fields"]),
                is_active=True,
                created_by=admin.id
            )
            
            db.add(template)
            print(f"✓ Created template: {config['name']}")
        
        db.commit()
        print("\n✅ All document templates seeded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error seeding templates: {e}")
        db.rollback()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding Document Templates...")
    success = seed_templates()
    sys.exit(0 if success else 1)
