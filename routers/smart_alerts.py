"""
Smart Alerts - birthdays, work anniversaries, contract/project expiry and
probation/review reminders computed from the employee database.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from auth import get_current_user
from datetime import date, timedelta

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


def _next_occurrence(ref: date, target: date, within: int) -> int:
    """Days until the next annual occurrence of target from ref (or None)."""
    try:
        nxt = ref.replace(month=target.month, day=target.day)
    except ValueError:
        # handle Feb 29 gracefully
        nxt = ref.replace(month=2, day=28)
    if nxt < ref:
        nxt = nxt.replace(year=ref.year + 1)
    return (nxt - ref).days


@router.get("")
def smart_alerts(days: int = 30, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Compute upcoming birthdays, anniversaries, contract ends and reminders."""
    today = date.today()
    employees = db.query(models.Employee).all()

    birthdays = []
    anniversaries = []
    contract_expiry = []
    project_end = []
    probation_end = []
    review_due = []

    for emp in employees:
        # Birthdays (next within N days)
        if emp.date_of_birth:
            d = _next_occurrence(today, emp.date_of_birth, days)
            if d <= days and d >= 0:
                age = today.year - emp.date_of_birth.year if (today.month, today.day) >= (emp.date_of_birth.month, emp.date_of_birth.day) else today.year - emp.date_of_birth.year - 1
                birthdays.append({
                    "employee_id": emp.id, "name": emp.full_name, "file_code": emp.file_code,
                    "date": emp.date_of_birth.isoformat(), "days": d,
                    "detail": f"turns {age + 1}",
                })

        # Work anniversaries (contract_start preferred, fallback date_of_appointment)
        anchor = emp.contract_start or emp.date_of_appointment
        if anchor:
            d = _next_occurrence(today, anchor, days)
            if d <= days and d >= 0:
                years = today.year - anchor.year if (today.month, today.day) >= (anchor.month, anchor.day) else today.year - anchor.year - 1
                anniversaries.append({
                    "employee_id": emp.id, "name": emp.full_name, "file_code": emp.file_code,
                    "date": anchor.isoformat(), "days": d, "years": years,
                    "detail": f"{years + 1} year{'s' if years != 0 else ''} with TPO",
                })

        # Contract expiry (within N days)
        if emp.contract_end:
            d = (emp.contract_end - today).days
            if 0 <= d <= days:
                contract_expiry.append({
                    "employee_id": emp.id, "name": emp.full_name, "file_code": emp.file_code,
                    "date": emp.contract_end.isoformat(), "days": d,
                    "detail": f"contract {'expires' if d > 0 else 'expired'} today",
                })

        # Project end (use contract_end for now; explicit project-level date can be added later)
        if emp.contract_end and emp.project:
            d = (emp.contract_end - today).days
            if 0 <= d <= days:
                project_end.append({
                    "employee_id": emp.id, "name": emp.full_name, "project": emp.project,
                    "date": emp.contract_end.isoformat(), "days": d,
                    "detail": f"'{emp.project}' {d} day{'s' if d != 1 else ''} to completion",
                })

        # Probation ends
        if emp.probation_end:
            d = (emp.probation_end - today).days
            if 0 <= d <= days:
                probation_end.append({
                    "employee_id": emp.id, "name": emp.full_name, "file_code": emp.file_code,
                    "date": emp.probation_end.isoformat(), "days": d,
                    "detail": "probation period is ending",
                })

        # Contract review due
        if emp.contract_review_date:
            d = (emp.contract_review_date - today).days
            if 0 <= d <= days:
                review_due.append({
                    "employee_id": emp.id, "name": emp.full_name, "file_code": emp.file_code,
                    "date": emp.contract_review_date.isoformat(), "days": d,
                    "detail": "contract review is due",
                })

    # Counters
    counts = {
        "birthdays": len(birthdays),
        "anniversaries": len(anniversaries),
        "contract_expiry": len(contract_expiry),
        "project_end": len(project_end),
        "probation_end": len(probation_end),
        "review_due": len(review_due),
    }

    sorted_ = lambda items: sorted(items, key=lambda x: x["days"])
    return {
        "as_of": today.isoformat(),
        "window_days": days,
        "counts": counts,
        "total": sum(counts.values()),
        "alerts": {
            "birthdays": sorted_(birthdays),
            "anniversaries": sorted_(anniversaries),
            "contract_expiry": sorted_(contract_expiry),
            "project_end": sorted_(project_end),
            "probation_end": sorted_(probation_end),
            "review_due": sorted_(review_due),
        },
    }