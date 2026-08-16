"""
Document Generation Engine Router
Handles document template management and document generation from templates.
"""

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from pathlib import Path
import json
import os
from jinja2 import Template
import io

from database import get_db
from auth import get_current_user
from models import (
    User, Employee, DocumentTemplate, GeneratedDocument, 
    DocumentFieldValue, Notification
)
from schemas import UserBase

router = APIRouter(prefix="/api/documents", tags=["documents"])

UPLOAD_DIR = Path("./uploads/generated_documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ==================== TEMPLATE MANAGEMENT ====================

@router.get("/templates")
async def list_document_templates(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    current_user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all active document templates."""
    query = db.query(DocumentTemplate).filter(DocumentTemplate.is_active == True)
    
    if category:
        query = query.filter(DocumentTemplate.category == category)
    
    templates = query.offset(skip).limit(limit).all()
    
    return {
        "count": len(templates),
        "templates": [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "category": t.category,
                "template_type": t.template_type,
                "fields": json.loads(t.fields_json) if t.fields_json else [],
                "created_at": t.created_at
            }
            for t in templates
        ]
    }


@router.get("/templates/{template_id}")
async def get_template_details(
    template_id: int,
    current_user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed template information with field definitions."""
    template = db.query(DocumentTemplate).filter(
        DocumentTemplate.id == template_id,
        DocumentTemplate.is_active == True
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return {
        "id": template.id,
        "name": template.name,
        "description": template.description,
        "category": template.category,
        "template_type": template.template_type,
        "content": template.content,
        "fields": json.loads(template.fields_json) if template.fields_json else [],
        "created_at": template.created_at
    }


@router.post("/templates")
async def create_document_template(
    name: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    template_type: str = Form(...),
    fields_json: str = Form(...),
    content: str = Form(...),
    current_user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new document template."""
    # Check authorization - only admins can create templates
    current_user_obj = db.query(User).filter(User.id == current_user.id).first()
    if current_user_obj.role not in ["hr_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Only admins can create templates")
    
    # Check if template with same name exists
    existing = db.query(DocumentTemplate).filter(
        DocumentTemplate.name == name
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Template with this name already exists")
    
    # Validate fields_json is valid JSON
    try:
        json.loads(fields_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid fields_json format")
    
    template = DocumentTemplate(
        name=name,
        description=description,
        category=category,
        template_type=template_type,
        fields_json=fields_json,
        content=content,
        created_by=current_user.id
    )
    
    db.add(template)
    db.commit()
    db.refresh(template)
    
    return {
        "id": template.id,
        "name": template.name,
        "message": "Template created successfully"
    }


# ==================== DOCUMENT GENERATION ====================

@router.post("/generate")
async def start_document_generation(
    template_id: int,
    employee_id: int,
    document_name: str = None,
    current_user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new generated document from a template."""
    # Verify template exists
    template = db.query(DocumentTemplate).filter(
        DocumentTemplate.id == template_id
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Verify employee exists
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Create generated document record
    generated_doc = GeneratedDocument(
        template_id=template_id,
        employee_id=employee_id,
        document_name=document_name or f"{template.name}_{employee.file_code}",
        file_format="html",  # Start as HTML, can export to PDF/DOCX
        created_by=current_user.id,
        status="draft"
    )
    
    db.add(generated_doc)
    db.commit()
    db.refresh(generated_doc)
    
    return {
        "document_id": generated_doc.id,
        "template_id": template_id,
        "employee_id": employee_id,
        "template_name": template.name,
        "fields": json.loads(template.fields_json) if template.fields_json else [],
        "status": "draft"
    }


@router.post("/generated/{document_id}/fill-field")
async def fill_document_field(
    document_id: int,
    field_name: str,
    field_value: str,
    field_type: str = "text",
    current_user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fill a single field in a generated document."""
    # Verify document exists
    doc = db.query(GeneratedDocument).filter(
        GeneratedDocument.id == document_id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check if field already exists, update or create
    existing_field = db.query(DocumentFieldValue).filter(
        DocumentFieldValue.generated_document_id == document_id,
        DocumentFieldValue.field_name == field_name
    ).first()
    
    if existing_field:
        existing_field.field_value = field_value
        existing_field.field_type = field_type
        existing_field.updated_at = datetime.now(timezone.utc)
    else:
        new_field = DocumentFieldValue(
            generated_document_id=document_id,
            field_name=field_name,
            field_value=field_value,
            field_type=field_type
        )
        db.add(new_field)
    
    db.commit()
    
    return {
        "document_id": document_id,
        "field_name": field_name,
        "field_value": field_value,
        "status": "saved"
    }


@router.post("/generated/{document_id}/fill-multiple")
async def fill_multiple_fields(
    document_id: int,
    fields: dict,
    current_user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fill multiple fields in a document at once."""
    # Verify document exists
    doc = db.query(GeneratedDocument).filter(
        GeneratedDocument.id == document_id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Process each field
    for field_name, field_data in fields.items():
        field_value = field_data.get("value", "")
        field_type = field_data.get("type", "text")
        
        existing_field = db.query(DocumentFieldValue).filter(
            DocumentFieldValue.generated_document_id == document_id,
            DocumentFieldValue.field_name == field_name
        ).first()
        
        if existing_field:
            existing_field.field_value = field_value
            existing_field.field_type = field_type
            existing_field.updated_at = datetime.now(timezone.utc)
        else:
            new_field = DocumentFieldValue(
                generated_document_id=document_id,
                field_name=field_name,
                field_value=field_value,
                field_type=field_type
            )
            db.add(new_field)
    
    db.commit()
    
    return {
        "document_id": document_id,
        "fields_filled": len(fields),
        "status": "updated"
    }


@router.get("/generated/{document_id}/preview")
async def preview_generated_document(
    document_id: int,
    current_user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get HTML preview of a generated document with current field values."""
    # Get document and template
    doc = db.query(GeneratedDocument).filter(
        GeneratedDocument.id == document_id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    template = doc.template
    employee = doc.employee
    
    # Get all filled field values
    field_values = db.query(DocumentFieldValue).filter(
        DocumentFieldValue.generated_document_id == document_id
    ).all()
    
    # Build context dictionary
    context = {
        "employee_name": employee.full_name,
        "employee_file_code": employee.file_code,
        "employee_position": employee.position,
        "employee_email": employee.personal_email,
        "employee_phone": employee.contact_number,
        "employee_bank": employee.bank_name,
        "employee_account": employee.bank_account_number,
        "date": datetime.now().strftime("%d %B %Y"),
    }
    
    # Add filled field values
    for fv in field_values:
        context[fv.field_name] = fv.field_value
    
    # Render template
    try:
        jinja_template = Template(template.content)
        html_content = jinja_template.render(**context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Template rendering error: {str(e)}")
    
    return {
        "document_id": document_id,
        "template_name": template.name,
        "employee_name": employee.full_name,
        "html_preview": html_content,
        "field_values": {fv.field_name: fv.field_value for fv in field_values}
    }


@router.post("/generated/{document_id}/generate-pdf")
async def generate_pdf_document(
    document_id: int,
    current_user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate PDF from document template with filled values."""
    try:
        from weasyprint import HTML, CSS
    except ImportError:
        raise HTTPException(
            status_code=500, 
            detail="PDF generation not available. Install weasyprint: pip install weasyprint"
        )
    
    # Get document
    doc = db.query(GeneratedDocument).filter(
        GeneratedDocument.id == document_id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    template = doc.template
    employee = doc.employee
    
    # Get field values
    field_values = db.query(DocumentFieldValue).filter(
        DocumentFieldValue.generated_document_id == document_id
    ).all()
    
    # Build context
    context = {
        "employee_name": employee.full_name,
        "employee_file_code": employee.file_code,
        "employee_position": employee.position,
        "employee_email": employee.personal_email,
        "employee_phone": employee.contact_number,
        "date": datetime.now().strftime("%d %B %Y"),
    }
    
    for fv in field_values:
        context[fv.field_name] = fv.field_value
    
    # Render HTML
    try:
        jinja_template = Template(template.content)
        html_content = jinja_template.render(**context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Template rendering error: {str(e)}")
    
    # Generate PDF
    try:
        pdf_file = HTML(string=html_content).write_pdf()
        
        # Save to file
        filename = f"{doc.document_name}_{document_id}.pdf"
        filepath = UPLOAD_DIR / filename
        
        with open(filepath, "wb") as f:
            f.write(pdf_file)
        
        # Update document record
        doc.file_path = str(filepath)
        doc.file_format = "pdf"
        doc.status = "generated"
        doc.generated_at = datetime.now(timezone.utc)
        db.commit()
        
        return {
            "document_id": document_id,
            "filename": filename,
            "status": "generated",
            "file_path": str(filepath)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")


@router.get("/generated/{document_id}/download")
async def download_generated_document(
    document_id: int,
    current_user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download a generated document."""
    doc = db.query(GeneratedDocument).filter(
        GeneratedDocument.id == document_id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not doc.file_path or not os.path.exists(doc.file_path):
        raise HTTPException(status_code=400, detail="Document not yet generated")
    
    # Update download timestamp
    doc.downloaded_at = datetime.now(timezone.utc)
    db.commit()
    
    return FileResponse(
        path=doc.file_path,
        filename=f"{doc.document_name}.{doc.file_format}"
    )


@router.get("/generated/{document_id}/list")
async def list_generated_documents(
    employee_id: int = None,
    template_id: int = None,
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    current_user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List generated documents with optional filters."""
    query = db.query(GeneratedDocument)
    
    if employee_id:
        query = query.filter(GeneratedDocument.employee_id == employee_id)
    
    if template_id:
        query = query.filter(GeneratedDocument.template_id == template_id)
    
    if status:
        query = query.filter(GeneratedDocument.status == status)
    
    documents = query.offset(skip).limit(limit).all()
    
    return {
        "count": len(documents),
        "documents": [
            {
                "id": d.id,
                "template_id": d.template_id,
                "template_name": d.template.name,
                "employee_id": d.employee_id,
                "employee_name": d.employee.full_name,
                "document_name": d.document_name,
                "status": d.status,
                "file_format": d.file_format,
                "created_at": d.created_at,
                "generated_at": d.generated_at
            }
            for d in documents
        ]
    }


@router.post("/generated/{document_id}/send")
async def send_generated_document(
    document_id: int,
    recipient_email: str,
    message: str = "",
    current_user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send generated document via email."""
    doc = db.query(GeneratedDocument).filter(
        GeneratedDocument.id == document_id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # TODO: Implement actual email sending with SMTP
    # For now, just update the record
    doc.sent_at = datetime.now(timezone.utc)
    doc.sent_to = recipient_email
    doc.status = "sent"
    
    # Create notification
    notification = Notification(
        user_id=doc.employee.user_id if hasattr(doc.employee, 'user_id') else None,
        message=f"Document '{doc.document_name}' has been sent to {recipient_email}",
        type="document_sent",
        read=False
    )
    
    db.add(notification)
    db.commit()
    
    return {
        "document_id": document_id,
        "sent_to": recipient_email,
        "status": "sent",
        "sent_at": doc.sent_at
    }
