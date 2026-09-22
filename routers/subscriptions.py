"""
Subscription & Billing - organisation plan (quarterly / yearly).

Payments and online billing will be ACTIVATED once the app is fully built.
Until then this module records the plan and status (inactive / trial / active /
expired) so that activation is a one-switch operation. No payments are collected
yet and the app does not block any feature based on subscription status.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta

from database import get_db
from auth import get_current_user, user_role_matches
import models

router = APIRouter(prefix="/api/subscription", tags=["subscription"])

VIEW_ROLES = ("hr_admin", "project_manager", "finance", "staff", "it_officer", "ceo", "ceo_assistant")
MANAGE_ROLES = ("hr_admin", "it_officer")


def _get_or_create(db: Session):
    sub = db.query(models.Subscription).order_by(models.Subscription.id.desc()).first()
    if not sub:
        sub = models.Subscription(
            plan="yearly",
            status="inactive",
            currency="UGX",
            notes="Payments & subscriptions will be activated once the app is fully built.",
        )
        db.add(sub)
        db.commit()
        db.refresh(sub)
    return sub


def _public(sub: models.Subscription):
    return {
        "id": sub.id,
        "plan": sub.plan,
        "status": sub.status,
        "amount": sub.amount,
        "currency": sub.currency,
        "start_date": sub.start_date.isoformat() if sub.start_date else None,
        "end_date": sub.end_date.isoformat() if sub.end_date else None,
        "trial_end_date": sub.trial_end_date.isoformat() if sub.trial_end_date else None,
        "auto_renew": bool(sub.auto_renew),
        "notes": sub.notes or "",
        "updated_at": sub.updated_at.isoformat() if sub.updated_at else None,
        "payments_active": False,  # switched on at full launch
    }


@router.get("")
@router.get("/")
def get_subscription(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Return the organization's current subscription plan and status."""
    if current_user.role not in VIEW_ROLES:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return _public(_get_or_create(db))


@router.put("")
@router.put("/")
def update_subscription(payload: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Admin/IT Officer: set the plan (quarterly/yearly), status and dates.

    This prepares the subscription for when payments are activated - no billing
    happens here yet.
    """
    if current_user.role not in MANAGE_ROLES:
        raise HTTPException(status_code=403, detail="Only HR Admin or IT Officer can manage the subscription")
    sub = _get_or_create(db)
    for field in ("plan", "status", "amount", "currency", "auto_renew", "notes"):
        if field in payload:
            setattr(sub, field, payload[field])
    for field in ("start_date", "end_date", "trial_end_date"):
        if field in payload and payload[field]:
            try:
                setattr(sub, field, date.fromisoformat(str(payload[field])[:10]))
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid date for {field}: {payload[field]}")
    sub.updated_by = current_user.id
    db.commit()
    db.refresh(sub)
    return _public(sub)


@router.post("/simulate-plan")
def simulate_plan(payload: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Preview helper: set a trial period for the chosen plan (no payment).

    plan: 'quarterly' (3 months) or 'yearly' (12 months). Marks status 'trial'.
    """
    if current_user.role not in MANAGE_ROLES:
        raise HTTPException(status_code=403, detail="Only HR Admin or IT Officer can manage the subscription")
    plan = (payload.get("plan") or "yearly").lower()
    if plan not in ("quarterly", "yearly"):
        raise HTTPException(status_code=400, detail="plan must be 'quarterly' or 'yearly'")
    sub = _get_or_create(db)
    months = 3 if plan == "quarterly" else 12
    today = date.today()
    sub.plan = plan
    sub.status = "trial"
    sub.start_date = today
    sub.end_date = today + timedelta(days=30 * months)
    sub.trial_end_date = today + timedelta(days=14)
    sub.updated_by = current_user.id
    db.commit()
    db.refresh(sub)
    return _public(sub)