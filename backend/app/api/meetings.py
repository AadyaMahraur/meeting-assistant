from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status
from app.db.models import Meeting
from app.schemas.meeting import MeetingRequest, MeetingResponse
from app.db.database import get_db
from app.services.ai_pipeline import process_meeting_text
from app.services.extraction import save_extraction_results

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
    try: 
        ai_results = process_meeting_text(new_meeting.raw_input_text)
        save_extraction_results(new_meeting.id, ai_results, db)
        db.refresh(new_meeting)
    except Exception as e:
        print("Pipeline failed: {}".format(e))


    return MeetingResponse(
        meeting_id=str(new_meeting.id), 
        status=new_meeting.status,
        message="Meeting submitted. Processing started." if new_meeting.status == "completed" else "Meeting submission failed during AI extraction"
    )



