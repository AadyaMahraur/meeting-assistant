from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status
from app.db.models import Meeting
from app.schemas.meeting import MeetingRequest, MeetingResponse
from app.db.database import get_db

router = APIRouter()   

@router.post('/text', response_model=MeetingResponse, status_code=status.HTTP_202_ACCEPTED)
async def meetings_text(request_meeting: MeetingRequest, db: Session = Depends(get_db)):
    if not request_meeting.text.strip():
        raise HTTPException(status_code=400, detail="Empty Text")

    new_meeting = Meeting(
        title=request_meeting.title, 
        meeting_date=request_meeting.meeting_date, 
        raw_input_text=request_meeting.text, 
        status="pending"
    )

    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)

    return MeetingResponse(
        meeting_id=str(new_meeting.id), 
        status=new_meeting.status,
        message="Meeting submitted. Processing started."
    )



