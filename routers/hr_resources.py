"""
HR Resources - exposes the real reference documents, fillable forms and Excel HR
tools stored in the project folders so users can browse and download them from
the reorganized HR Tools / Documents hubs.
"""
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from database import get_db
from auth import get_current_user
from sqlalchemy.orm import Session
import models

router = APIRouter(prefix="/api/hr-resources", tags=["hr-resources"])

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "")

FOLDERS = {
    "hr_tools": ("the HR tools", "Excel HR Tools"),
    "fillable_forms": ("documents to be filled", "Fillable Forms"),
    "reference_docs": ("only documents", "Reference Documents"),
    "pdfs": ("new pdfs", "PDF Reference Files"),
    "word_documents": ("word documents", "Word Master Documents"),
}


def _folder_abs(key):
    folder, _ = FOLDERS[key]
    path = os.path.join(BASE, folder)
    return path if os.path.isdir(path) else None


@router.get("")
@router.get("/")
def list_resources(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """List every downloadable HR file grouped by category folder."""
    if user.role not in ("hr_admin", "project_manager", "finance", "staff"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    groups = []
    for key, (folder, label) in FOLDERS.items():
        path = _folder_abs(key)
        files = []
        if path:
            for fn in sorted(os.listdir(path)):
                full = os.path.join(path, fn)
                if not os.path.isfile(full):
                    continue
                files.append({
                    "name": fn,
                    "path": f"{key}/{fn}",
                    "size": os.path.getsize(full),
                    "ext": os.path.splitext(fn)[1].lstrip(".").lower(),
                })
        groups.append({"key": key, "label": label, "files": files})
    return {"groups": groups, "total": sum(len(g["files"]) for g in groups)}


@router.get("/file")
def download_resource(folder: str, filename: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Download one real HR file from the categorized folders."""
    if user.role not in ("hr_admin", "project_manager", "finance", "staff"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    if folder not in FOLDERS:
        raise HTTPException(status_code=404, detail="Folder not found")
    path = _folder_abs(folder)
    if not path:
        raise HTTPException(status_code=404, detail="Folder not found")
    full = os.path.join(path, filename)
    if not os.path.isfile(full) or os.path.normpath(full) != os.path.normpath(os.path.join(path, os.path.basename(filename))):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(full, filename=filename)


@router.get("/company")
def get_company_profile(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Company logo, email, phone and address used by the HR Tools hub."""
    if user.role not in ("hr_admin", "project_manager", "finance", "staff"):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    profile = db.query(models.CompanySettings).order_by(models.CompanySettings.id.desc()).first()
    if not profile:
        return {
            "company_name": "TPO Uganda",
            "logo_url": "",
            "contact_email": "",
            "contact_phone": "",
            "address": "",
            "country": "Uganda",
        }
    return {
        "company_name": profile.company_name or "TPO Uganda",
        "logo_url": profile.logo_url or "",
        "contact_email": profile.contact_email or "",
        "contact_phone": profile.contact_phone or "",
        "address": profile.address or "",
        "country": profile.country or "Uganda",
    }


@router.put("/company")
def update_company_profile(payload: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Admin-only settings for company logo, email and phone."""
    if user.role not in ("hr_admin",):
        raise HTTPException(status_code=403, detail="Only HR Admin can update company profile")
    profile = db.query(models.CompanySettings).order_by(models.CompanySettings.id.desc()).first()
    if not profile:
        profile = models.CompanySettings()
        db.add(profile)
    for field in ("company_name", "logo_url", "contact_email", "contact_phone", "address", "country"):
        if field in payload:
            setattr(profile, field, payload[field])
    db.commit()
    db.refresh(profile)
    return {"ok": True, "company_name": profile.company_name}