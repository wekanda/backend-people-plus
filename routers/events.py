"""
Organization Calendar - meetings, interviews, trainings, check-ins.

Events can carry an optional meeting link which can be broadcast to everyone in
the organization (a notification is created for every user).
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from auth import get_current_user
import models

router = APIRouter(prefix="/api/calendar", tags=["calendar"])

EVENT_TYPES = ("meeting", "interview", "training", "checkin", "leave", "other")
MANAGE_ROLES = ("hr_admin", "it_officer", "ceo", "ceo_assistant", "project_manager")


def _public(ev: models.CalendarEvent, can_manage: bool):
    return {
        "id": ev.id,
        "title": ev.title,
        "event_type": ev.event_type,
        "description": ev.description or "",
        "meeting_link": ev.meeting_link or "",
        "start_at": ev.start_at.isoformat() if ev.start_at else None,
        "end_at": ev.end_at.isoformat() if ev.end_at else None,
        "location": ev.location or "",
        "created_by": ev.created_by,
        "can_manage": can_manage,
    }


def _parse_dt(value):
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid date/time: {value}")


@router.get("/events")
def list_events(upcoming: bool = False, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """List calendar events (all authenticated users)."""
    query = db.query(models.CalendarEvent)
    if upcoming:
        query = query.filter(models.CalendarEvent.start_at >= datetime.now(timezone.utc))
    events = query.order_by(models.CalendarEvent.start_at.asc()).all()
    return {"events": [_public(ev, current_user.role in MANAGE_ROLES or ev.created_by == current_user.id) for ev in events]}


@router.post("/events")
def create_event(payload: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Create a calendar event (any authenticated user can schedule)."""
    title = (payload.get("title") or "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")
    start = _parse_dt(payload.get("start_at"))
    ev = models.CalendarEvent(
        title=title,
        event_type=payload.get("event_type") if payload.get("event_type") in EVENT_TYPES else "meeting",
        description=(payload.get("description") or ""),
        meeting_link=(payload.get("meeting_link") or ""),
        start_at=start,
        end_at=_parse_dt(payload["end_at"]) if payload.get("end_at") else None,
        location=(payload.get("location") or ""),
        created_by=current_user.id,
    )
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return _public(ev, True)


@router.put("/events/{event_id}")
def update_event(event_id: int, payload: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    ev = db.query(models.CalendarEvent).filter(models.CalendarEvent.id == event_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")
    if not (current_user.role in MANAGE_ROLES or ev.created_by == current_user.id):
        raise HTTPException(status_code=403, detail="You can only edit your own events")
    for field in ("title", "event_type", "description", "meeting_link", "location"):
        if field in payload:
            setattr(ev, field, payload[field])
    if "start_at" in payload:
        ev.start_at = _parse_dt(payload["start_at"])
    if "end_at" in payload and payload["end_at"]:
        ev.end_at = _parse_dt(payload["end_at"])
    db.commit()
    db.refresh(ev)
    return _public(ev, True)


@router.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    ev = db.query(models.CalendarEvent).filter(models.CalendarEvent.id == event_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")
    if not (current_user.role in MANAGE_ROLES or ev.created_by == current_user.id):
        raise HTTPException(status_code=403, detail="You can only delete your own events")
    db.delete(ev)
    db.commit()
    return {"ok": True}


@router.post("/events/{event_id}/broadcast")
def broadcast_event(event_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Share the event meeting link with everyone - creates a notification for each user."""
    ev = db.query(models.CalendarEvent).filter(models.CalendarEvent.id == event_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")
    link = ev.meeting_link or ""
    message = f"📅 {ev.title} ({ev.event_type})"
    if ev.start_at:
        message += f" • {ev.start_at.strftime('%d %b %Y %H:%M')}"
    if link:
        message += f" • Join: {link}"
    users = db.query(models.User).all()
    for u in users:
        db.add(models.Notification(user_id=u.id, message=message, type="calendar_event", read=False))
    db.commit()
    return {"ok": True, "shared_to": len(users)}