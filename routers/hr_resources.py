"""
HR Resources - exposes the real reference documents, fillable forms and Excel HR
tools stored in the project folders so users can browse and download them from
the reorganized HR Tools / Documents hubs.

Also manages the ORGANIZATION BRANDING feature:
  * organization name / motto / address / contacts
  * company logo upload (appears on generated documents)
  * document header image upload (organizational letterhead)
  * branded downloads of the built-in Excel HR tools (organisation name + logo
    are pre-filled into a copy of the workbook)
"""
import io
import os
import re
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
from database import get_db
from auth import get_current_user
from sqlalchemy.orm import Session
import models

router = APIRouter(prefix="/api/hr-resources", tags=["hr-resources"])

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "")

FOLDERS = {
    "hr_tools": ("the HR tools", "Excel HR Tools"),
    "excel_tools": ("new excels", "Built-in Excel HR Tools"),
    "fillable_forms": ("documents to be filled", "Fillable Forms"),
    "reference_docs": ("only documents", "Reference Documents"),
    "pdfs": ("new pdfs", "PDF Reference Files"),
    "word_documents": ("word documents", "Word Master Documents"),
}

BRAND_UPLOAD_DIR = os.path.join(BASE, "uploads", "company")
os.makedirs(BRAND_UPLOAD_DIR, exist_ok=True)

ALLOWED_ROLES = ("hr_admin", "project_manager", "finance", "staff")
ALLOWED_IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
# Organisation names that mean "no branding configured" (default TPO templates).
_DEFAULT_ORG_NAMES = {"", "tpo uganda", "tpo", "people plus", "peoplepluse", "people plus uganda"}


def _folder_abs(key):
    folder, _ = FOLDERS[key]
    path = os.path.join(BASE, folder)
    return path if os.path.isdir(path) else None


def _company_profile(db: Session):
    """Return the single CompanySettings row (create it if missing)."""
    profile = db.query(models.CompanySettings).order_by(models.CompanySettings.id.desc()).first()
    if not profile:
        profile = models.CompanySettings(company_name="")
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


def _is_default_org(name):
    return (name or "").strip().lower() in _DEFAULT_ORG_NAMES


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


###############################################################################
# Branded downloads of the built-in Excel HR tools ("new excels")
###############################################################################

def _rebrand_workbook(workbook, company_name: str, logo_path=None):
    """Replace the default organisation name in every cell and drop the logo into
    the first sheet's heading row (at a blank anchor cell) when supplied."""
    name = (company_name or "").strip()
    replacements = {
        "tpo uganda's": f"{name}'s",
        "tpo uganda’s": f"{name}’s",
        "on behalf of tpo uganda": f"on behalf of {name}",
        "signed on behalf of tpo uganda": f"signed on behalf of {name}",
        "tpo uganda": name,
    }
    for ws in workbook.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                if cell.value is None or not isinstance(cell.value, str):
                    continue
                val = cell.value
                lowered = val.lower()
                changed = False
                for src, dst in replacements.items():
                    idx = 0
                    while True:
                        pos = lowered.find(src, idx)
                        if pos == -1:
                            break
                        val = val[:pos] + dst + val[pos + len(src):]
                        lowered = val.lower()
                        idx = pos + len(dst)
                        changed = True
                if changed:
                    cell.value = val
        # Also swap remaining standalone 'TPO' tokens for consistency with generated docs.
        if name:
            for row in ws.iter_rows():
                for cell in row:
                    if cell.value is None or not isinstance(cell.value, str) or "TPO" not in cell.value:
                        continue
                    cell.value = re.sub(r"\bTPO\b", name, cell.value)

    if logo_path and os.path.isfile(logo_path) and workbook.worksheets:
        try:
            from openpyxl.drawing.image import Image as XLImage
            from openpyxl.utils import get_column_letter
            img = XLImage(logo_path)
            ratio = img.height / img.width if img.width else 1.0
            img.width = int(3.2 * 118)  # px for ~3.2 cm at 96dpi
            img.height = int(img.width * ratio)
            ws = workbook.worksheets[0]
            anchor = "A1"
            placed = False
            for col in range(1, 30):
                cell = ws.cell(row=1, column=col)
                if cell.value in (None, ""):
                    anchor = f"{get_column_letter(col)}1"
                    placed = True
                    break
            if not placed:
                for col in range(1, 4):
                    cell = ws.cell(row=2, column=col)
                    if cell.value in (None, ""):
                        anchor = f"{get_column_letter(col)}2"
                        placed = True
                        break
            if placed:
                ws.add_image(img, anchor)
        except Exception:
            pass  # Logo insertion is best-effort - never break the download.
    return workbook


@router.get("/builtin-excel/{filename}")
def download_builtin_excel(filename: str, branded: str = "1",
                           db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Download one of the built-in Excel HR tools, optionally pre-filled with the
    organization's name and logo (branded=1 default)."""
    if user.role not in ALLOWED_ROLES:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    folder_key, _ = FOLDERS["excel_tools"]
    path = os.path.join(BASE, folder_key)
    if not os.path.isdir(path):
        raise HTTPException(status_code=404, detail="Built-in Excel tools folder not found")
    base_name = os.path.basename(filename)
    full = os.path.join(path, base_name)
    if not os.path.isfile(full):
        raise HTTPException(status_code=404, detail="File not found")

    if branded != "1":
        return FileResponse(full, filename=base_name)

    profile = db.query(models.CompanySettings).order_by(models.CompanySettings.id.desc()).first()
    company_name = (profile.company_name if profile else "") or ""
    # When the org has not configured a custom name yet, use a neutral placeholder so
    # the default 'TPO Uganda' wording never appears on the built-in tools either.
    if _is_default_org(company_name):
        company_name = "The Organization"

    try:
        import openpyxl
        wb = openpyxl.load_workbook(full)
        logo_path = None
        if profile and profile.logo_url and profile.logo_url.startswith("/uploads/company/"):
            candidate = os.path.join(BRAND_UPLOAD_DIR, os.path.basename(profile.logo_url))
            if os.path.isfile(candidate):
                logo_path = candidate
        _rebrand_workbook(wb, company_name, logo_path)
        out = io.BytesIO()
        wb.save(out)
        out.seek(0)
        return StreamingResponse(
            out,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="{base_name}"'},
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not brand the workbook: {exc}")


@router.get("/company")
def get_company_profile(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Company logo, document header, email, phone and address used across the app."""
    if user.role not in ALLOWED_ROLES:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    profile = db.query(models.CompanySettings).order_by(models.CompanySettings.id.desc()).first()
    if not profile:
        return {
            "company_name": "",
            "motto": "",
            "logo_url": "",
            "header_url": "",
            "contact_email": "",
            "contact_phone": "",
            "address": "",
            "country": "Uganda",
        }
    return {
        "company_name": profile.company_name or "",
        "motto": profile.motto or "",
        "logo_url": profile.logo_url or "",
        "header_url": profile.header_url or "",
        "contact_email": profile.contact_email or "",
        "contact_phone": profile.contact_phone or "",
        "address": profile.address or "",
        "country": profile.country or "Uganda",
    }


@router.put("/company")
def update_company_profile(payload: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Admin-only settings for company name, motto, logo/header URLs and contacts."""
    if user.role not in ("hr_admin",):
        raise HTTPException(status_code=403, detail="Only HR Admin can update company profile")
    profile = _company_profile(db)
    for field in ("company_name", "motto", "logo_url", "header_url", "contact_email", "contact_phone", "address", "country"):
        if field in payload:
            value = payload[field]
            setattr(profile, field, (value or "").strip() if isinstance(value, str) else value)
    profile.updated_by = user.id
    db.commit()
    db.refresh(profile)
    return {
        "ok": True,
        "company_name": profile.company_name,
        "motto": profile.motto or "",
        "logo_url": profile.logo_url or "",
        "header_url": profile.header_url or "",
    }


def _save_brand_image(kind: str, file: UploadFile) -> str:
    """Persist an uploaded brand image (logo or header) and return its public URL."""
    original = file.filename or f"{kind}.png"
    ext = os.path.splitext(original)[1].lower()
    if ext not in ALLOWED_IMG_EXT:
        raise HTTPException(status_code=400, detail="Only image files are allowed (PNG, JPG, GIF, WEBP, SVG)")
    contents = file.file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image is too large (max 10 MB)")
    # Remove previous files of the same brand kind so only the newest stays active.
    for old in os.listdir(BRAND_UPLOAD_DIR):
        if old.startswith(kind + "."):
            try:
                os.remove(os.path.join(BRAND_UPLOAD_DIR, old))
            except OSError:
                pass
    safe_ext = ext if ext in {".jpg", ".jpeg", ".gif", ".webp", ".svg"} else ".png"
    fname = f"{kind}_{str(uuid.uuid4())[:8]}{safe_ext}"
    with open(os.path.join(BRAND_UPLOAD_DIR, fname), "wb") as f:
        f.write(contents)
    return f"/uploads/company/{fname}"


@router.post("/company/logo")
def upload_company_logo(file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Upload the company logo shown on generated documents."""
    if user.role not in ("hr_admin",):
        raise HTTPException(status_code=403, detail="Only HR Admin can upload the company logo")
    url = _save_brand_image("logo", file)
    profile = _company_profile(db)
    profile.logo_url = url
    profile.updated_by = user.id
    db.commit()
    return {"ok": True, "logo_url": url}


@router.post("/company/header")
def upload_company_header(file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Upload the organizational letterhead / document header image."""
    if user.role not in ("hr_admin",):
        raise HTTPException(status_code=403, detail="Only HR Admin can upload the document header")
    url = _save_brand_image("header", file)
    profile = _company_profile(db)
    profile.header_url = url
    profile.updated_by = user.id
    db.commit()
    return {"ok": True, "header_url": url}


@router.delete("/company/brand")
def reset_company_brand(which: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Remove the uploaded logo / header image ('logo' or 'header')."""
    if user.role not in ("hr_admin",):
        raise HTTPException(status_code=403, detail="Only HR Admin can manage brand assets")
    if which not in ("logo", "header"):
        raise HTTPException(status_code=400, detail="which must be 'logo' or 'header'")
    for old in os.listdir(BRAND_UPLOAD_DIR):
        if old.startswith(which + "."):
            try:
                os.remove(os.path.join(BRAND_UPLOAD_DIR, old))
            except OSError:
                pass
    profile = _company_profile(db)
    if which == "logo":
        profile.logo_url = None
    else:
        profile.header_url = None
    db.commit()
    return {"ok": True}