from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from typing import Optional
from app.db.models import Meeting
from app.schemas.meeting import MeetingRequest, MeetingResponse, MeetingDetailedResponse, MeetingStatusResponse
from app.db.database import get_db
from app.services.ai_pipeline import process_meeting_text
from app.services.extraction import save_extraction_results
from app.utils.file_handling import validate_file, extract_text_from_file
from datetime import datetime

router = APIRouter()   

@router.post('/text', response_model=MeetingResponse, status_code=status.HTTP_202_ACCEPTED)
async def meetings_text(request_meeting: MeetingRequest, db: Session = Depends(get_db)):
    if not request_meeting.text.strip():
        raise HTTPException(status_code=400, detail="Empty Text")

    new_meeting = Meeting(
        title=request_meeting.title, 
        meeting_date=request_meeting.meeting_date, 
        raw_input_text=request_meeting.text, 
        status="pending",
        input_type="text"
    )

    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)
    try: 
        ai_results = process_meeting_text(new_meeting.raw_input_text)
        save_extraction_results(new_meeting.id, ai_results, db)
        db.refresh(new_meeting)
    except Exception as e:
        # print("Pipeline failed: {}".format(e))
        pass


    return MeetingResponse(
        meeting_id=str(new_meeting.id), 
        status=new_meeting.status,
        message="Meeting submitted. Processing started." if new_meeting.status == "completed" else "Meeting submission failed during AI extraction"
    )


@router.post('/upload', response_model=MeetingResponse, status_code=status.HTTP_202_ACCEPTED)
async def meetings_upload(
    file: UploadFile = File(...), 
    title: Optional[str] = Form(None), 
    meeting_date: Optional[str] = Form(None), 
    db: Session = Depends(get_db)
):
    new_meeting=None
    try: 
        if validate_file(file):
            text = extract_text_from_file(file)
            final_title = title if title else file.filename
            final_date = meeting_date if meeting_date else datetime.now().date()

            new_meeting = Meeting(
                title=final_title, 
                meeting_date=final_date, 
                raw_input_text=text, 
                status="pending",
                input_type="transcript file"
            )

            db.add(new_meeting)
            db.commit()
            db.refresh(new_meeting)
            ai_results = process_meeting_text(new_meeting.raw_input_text)
            save_extraction_results(new_meeting.id, ai_results, db)
            db.refresh(new_meeting)
            return MeetingResponse(
                meeting_id=str(new_meeting.id), 
                status=new_meeting.status,
                message="Meeting submitted. Processing started." if new_meeting.status == "completed" else "Meeting submission failed during AI extraction"
            )
    except Exception as e:
        print("File upload failed at: {}".format(e))

        if not new_meeting:
            raise e
        
        return MeetingResponse(
            meeting_id=str(new_meeting.id), 
            status="failed",
            message="File upload successful but AI processing failed"
        )


    
@router.get('/{meeting_id}', response_model=MeetingDetailedResponse, status_code=status.HTTP_200_OK)
async def get_meeting(meeting_id: str, db : Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting Not Found")
    
    meeting.id = str(meeting.id)
    
    return meeting
    

@router.get('/{meeting_id}/status', response_model=MeetingStatusResponse, status_code=status.HTTP_200_OK)
async def get_meeting_status(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting: 
        raise HTTPException(status_code=404, detail="Meeting Not Found")
    
    return meeting