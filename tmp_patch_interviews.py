from pathlib import Path

block = """

def interview_to_dict(interview: models.Interview):
    return {
        'id': interview.id,
        'application_id': interview.application_id,
        'candidate_name': getattr(interview, 'candidate_name', None),
        'position': getattr(interview, 'position', None),
        'interviewer': getattr(interview, 'interviewer', None),
        'notes': getattr(interview, 'notes', None),
        'status': getattr(interview, 'status', None),
        'date': interview.scheduled_at.date().isoformat() if interview.scheduled_at else None,
        'time': interview.scheduled_at.strftime('%H:%M') if interview.scheduled_at else None,
        'duration_minutes': getattr(interview, 'duration_minutes', None),
        'location': getattr(interview, 'location', None),
        'panel': getattr(interview, 'panel', None),
    }


@router.get('/interviews')
def list_interviews(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role not in ('hr_admin','project_manager'):
        raise HTTPException(status_code=403)
    interviews = db.query(models.Interview).order_by(models.Interview.scheduled_at.desc()).all()
    return [interview_to_dict(i) for i in interviews]


@router.post('/interviews')
def create_interview(payload: dict, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role not in ('hr_admin','project_manager'):
        raise HTTPException(status_code=403)

    scheduled_at = None
    if payload.get('date'):
        date_value = payload.get('date')
        time_value = payload.get('time')
        try:
            scheduled_at = datetime.fromisoformat(f"{date_value}T{time_value}") if time_value else datetime.fromisoformat(date_value)
        except Exception:
            scheduled_at = datetime.utcnow()
    else:
        scheduled_at = datetime.utcnow()

    interview = models.Interview(
        application_id=payload.get('application_id'),
        candidate_name=payload.get('candidate_name'),
        position=payload.get('position'),
        interviewer=payload.get('interviewer'),
        notes=payload.get('notes'),
        scheduled_at=scheduled_at,
        duration_minutes=payload.get('duration_minutes', 60),
        panel=','.join(map(str, payload.get('panel', []))) if payload.get('panel') else None,
        location=payload.get('location'),
        status=payload.get('status', 'scheduled')
    )
    db.add(interview); db.commit(); db.refresh(interview)
    return interview_to_dict(interview)


@router.delete('/interviews/{interview_id}')
def delete_interview(interview_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role not in ('hr_admin','project_manager'):
        raise HTTPException(status_code=403)
    interview = db.query(models.Interview).filter(models.Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail='Interview not found')
    db.delete(interview)
    db.commit()
    return {'status': 'deleted', 'id': interview_id}
"""

for relative in ['backend/hr_tools.py', 'people-pluse-backend/backend/hr_tools.py']:
    path = Path(relative)
    text = path.read_text(encoding='utf-8')
    if 'def list_interviews' in text:
        print(relative, 'already has interviews endpoints')
        continue
    marker = "@router.get('/analytics/recruitment')"
    idx = text.find(marker)
    if idx == -1:
        raise SystemExit(f"Marker not found in {relative}")
    new_text = text[:idx] + block + '\n\n' + text[idx:]
    path.write_text(new_text, encoding='utf-8')
    print('patched', relative)
