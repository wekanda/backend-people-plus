"""Interview scheduling CRUD backed by the `interviews` table."""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from auth import get_current_user

router = APIRouter(prefix="/hr", tags=["hr"])


def _serialize(interview) -> dict:
    """Return the interview in the shape the frontend expects (date/time separately)."""
    scheduled = interview.scheduled_at
    return {
        "id": interview.id,
        "application_id": interview.application_id,
        "candidate_name": interview.candidate_name or "",
        "position": interview.position or "",
        "interviewer": interview.interviewer or "",
        "notes": interview.notes or "",
        "status": interview.status or "Scheduled",
        "scheduled_at": scheduled.isoformat() if scheduled else None,
        "date": scheduled.strftime("%Y-%m-%d") if scheduled else "",
        "time": scheduled.strftime("%H:%M") if scheduled else "",
        "duration_minutes": interview.duration_minutes or 60,
        "location": interview.location,
    }


@router.get("/interviews")
def list_interviews(db: Session = Depends(get_db), user=Depends(get_current_user)):
    interviews = db.query(models.Interview).order_by(models.Interview.id.desc()).all()
    return [_serialize(i) for i in interviews]


@router.post("/interviews")
def create_interview(payload: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    date_str = str(payload.get("date") or "").strip()
    time_str = str(payload.get("time") or "").strip() or "09:00"
    scheduled_at = None
    try:
        scheduled_at = datetime.fromisoformat(f"{date_str}T{time_str}")
    except ValueError:
        scheduled_at = datetime.now()

    interview = models.Interview(
        candidate_name=str(payload.get("candidate_name") or "").strip(),
        position=str(payload.get("position") or "").strip(),
        interviewer=str(payload.get("interviewer") or "").strip(),
        notes=str(payload.get("notes") or "").strip(),
        status=str(payload.get("status") or "Scheduled"),
        scheduled_at=scheduled_at,
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)
    return _serialize(interview)


@router.delete("/interviews/{interview_id}")
def delete_interview(interview_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    interview = db.query(models.Interview).filter(models.Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    db.delete(interview)
    db.commit()
    return {"ok": True, "id": interview_id}