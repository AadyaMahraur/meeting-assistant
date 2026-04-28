from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import desc

from app.db.models import Meeting
# Updated Imports
from app.schemas.meeting import (
    TextMeetingUpload, 
    MeetingUploadAck, 
    MeetingDetailResult, 
    MeetingStatusResult, 
    PaginatedMeetingHistory
)
from app.db.database import get_db

from app.services.extraction import process_meeting_extraction
from app.services.ingestion import ingest_meeting_results, save_processing_log
from app.services.ai_pipeline import PipelineError

from app.utils.file_handling import validate_file, extract_text_from_file, validate_text_content

router = APIRouter()   

@router.post('/text', response_model=MeetingUploadAck, status_code=status.HTTP_202_ACCEPTED)
async def meetings_text(request_meeting: TextMeetingUpload, db: Session = Depends(get_db)):
    validated_text, word_count = validate_text_content(request_meeting.text)

    final_title = request_meeting.title if request_meeting.title else f"New Meeting - {datetime.now().strftime(('%b %d, %H:%M'))}"
    final_date = request_meeting.meeting_date if request_meeting.meeting_date else datetime.now().date()

    new_meeting = Meeting(
        title=final_title, 
        meeting_date=final_date, 
        raw_input_text=validated_text, 
        status="pending",
        input_type="text",
        word_count = word_count
    )

    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)

    try: 
        ai_results, metadata = await process_meeting_extraction(new_meeting.raw_input_text)
        ingest_meeting_results(new_meeting.id, ai_results, db)
        
        new_meeting.status = "completed"
        db.commit()
        save_processing_log(new_meeting.id, metadata, db)
        
    except PipelineError as pe:
        db.rollback() 
        new_meeting.status = "failed"
        new_meeting.error_message = str(pe)
        db.commit()
        save_processing_log(new_meeting.id, pe.metadata, db)
        print(f"AI PIPELINE FAILED: {str(pe)}")
        
    except Exception as e:
        db.rollback()
        new_meeting.status = "failed"
        new_meeting.error_message = f"System error: {str(e)}"
        db.commit()
        
        fallback_meta = {
            "started_at": datetime.now(timezone.utc),
            "completed_at": datetime.now(timezone.utc),
            "success": False,
            "error_details": f"System error: {str(e)}"
        }
        save_processing_log(new_meeting.id, fallback_meta, db)
        
    return MeetingUploadAck(
        meeting_id=new_meeting.id, 
        status=new_meeting.status,
        message="Meeting processed successfully." if new_meeting.status == "completed" else "Meeting submission failed during AI extraction."
    )


@router.post('/upload', response_model=MeetingUploadAck, status_code=status.HTTP_202_ACCEPTED)
async def meetings_upload(
    file: UploadFile = File(...), 
    title: Optional[str] = Form(None), 
    meeting_date: Optional[str] = Form(None), 
    db: Session = Depends(get_db)
):
    new_meeting = None
    try: 
        if validate_file(file):
            validated_text, word_count = extract_text_from_file(file)
            final_title = title if title else file.filename
            final_date = meeting_date if meeting_date else datetime.now().date()

            new_meeting = Meeting(
                title=final_title, 
                meeting_date=final_date, 
                raw_input_text=validated_text, 
                status="pending",
                input_type="transcript file",
                word_count = word_count
            )

            db.add(new_meeting)
            db.commit()
            db.refresh(new_meeting)
            
            try:
                ai_results, metadata = await process_meeting_extraction(new_meeting.raw_input_text)
                ingest_meeting_results(new_meeting.id, ai_results, db)
                
                new_meeting.status = "completed"
                db.commit()
                save_processing_log(new_meeting.id, metadata, db)
                
            except PipelineError as pe:
                db.rollback() 
                new_meeting.status = "failed"
                new_meeting.error_message = str(pe)
                db.commit()
                save_processing_log(new_meeting.id, pe.metadata, db)
                print(f"AI PIPELINE FAILED: {str(pe)}")
                
            except Exception as e:
                db.rollback()
                new_meeting.status = "failed"
                new_meeting.error_message = f"System error: {str(e)}"
                db.commit()
                
                fallback_meta = {
                    "started_at": datetime.now(timezone.utc),
                    "completed_at": datetime.now(timezone.utc),
                    "success": False,
                    "error_details": f"System error: {str(e)}"
                }
                save_processing_log(new_meeting.id, fallback_meta, db)

            return MeetingUploadAck(
                meeting_id=new_meeting.id, 
                status=new_meeting.status,
                message="Meeting processed successfully." if new_meeting.status == "completed" else "Meeting submission failed during AI extraction."
            )
            
    except Exception as e:
        if not new_meeting:
            raise e
        return MeetingUploadAck(
            meeting_id=str(new_meeting.id), 
            status="failed",
            message="File upload successful but processing crashed."
        )


@router.get('/{meeting_id}/status', response_model=MeetingStatusResult, status_code=status.HTTP_200_OK)
async def get_meeting_status(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting: 
        raise HTTPException(status_code=404, detail="Meeting Not Found")
    
    return meeting


@router.get('/{meeting_id}', response_model=MeetingDetailResult, status_code=status.HTTP_200_OK)
async def get_meeting(meeting_id: str, db : Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting Not Found")
    
    return meeting


@router.delete('/{meeting_id}', status_code=status.HTTP_200_OK)
async def delete_meeting(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting Not Found")

    try:
        db.delete(meeting)
        db.commit()
        
        return {"message": "Meeting deleted successfully."}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete meeting: {str(e)}")


@router.get('/', response_model=PaginatedMeetingHistory, status_code=status.HTTP_200_OK)
async def get_all_meetings(
    page: int = 1,
    per_page: int = 9,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    
    if status:
        query = db.query(Meeting).filter(Meeting.status == status)
    else:
        query = db.query(Meeting).filter(Meeting.status == "completed")

    total_count = query.count()
    offset = (page - 1) * per_page
    meetings = query.order_by(desc(Meeting.created_at)).offset(offset).limit(per_page).all()
    
    return {
        "meetings": meetings, 
        "total": total_count,
        "page": page,
        "per_page": per_page
    }