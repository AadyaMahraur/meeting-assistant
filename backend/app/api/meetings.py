from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status, File, Form, UploadFile
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import desc, or_
import langdetect

from app.db.models import Meeting, ActionItem, Decision
from app.schemas.meeting import MeetingRequest, MeetingResponse, MeetingDetailedResponse, MeetingStatusResponse, MeetingListResponse
from app.db.database import get_db

# Imported from your newly separated modules
from app.services.extraction import process_meeting_extraction
from app.services.ingestion import ingest_meeting_results, save_processing_log
from app.services.ai_pipeline import PipelineError
from app.utils.file_handling import validate_file, extract_text_from_file, check_filler_words

router = APIRouter()   

@router.post('/text', response_model=MeetingResponse, status_code=status.HTTP_202_ACCEPTED)
async def meetings_text(request_meeting: MeetingRequest, db: Session = Depends(get_db)):
    text = request_meeting.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty Text")

    word_count = len(text.split())

    if word_count < 50:
        raise HTTPException(status_code=400, detail="Input too short. Please provide at least 50 words.")
    if word_count > 10000:
        raise HTTPException(status_code=400, detail="Input too long. Max limit is 10,000 words.")

    try:
        if langdetect.detect(text) != 'en':
            raise HTTPException(status_code=400, detail="Only English text is supported.")
    except:
        raise HTTPException(status_code=400, detail="Could not determine language.")

    if check_filler_words(text):
        raise HTTPException(status_code=400, detail="Only conversational filler words present. Lacks substance.")

    final_date = request_meeting.meeting_date if request_meeting.meeting_date else datetime.now().date()

    new_meeting = Meeting(
        title=request_meeting.title, 
        meeting_date=final_date, 
        raw_input_text=text, 
        status="pending",
        input_type="text"
    )

    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)

    # --- NEW ROBUST PIPELINE INTEGRATION ---
    try: 
        # 1. Run the Async AI Pipeline
        ai_results, metadata = await process_meeting_extraction(new_meeting.raw_input_text)
        
        # 2. Ingest the structured data
        ingest_meeting_results(new_meeting.id, ai_results, db)
        
        # 3. Mark complete
        new_meeting.status = "completed"
        db.commit()
        
        # 4. Save success metrics to ProcessingLog
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
        
    return MeetingResponse(
        meeting_id=str(new_meeting.id), 
        status=new_meeting.status,
        message="Meeting processed successfully." if new_meeting.status == "completed" else "Meeting submission failed during AI extraction."
    )


@router.post('/upload', response_model=MeetingResponse, status_code=status.HTTP_202_ACCEPTED)
async def meetings_upload(
    file: UploadFile = File(...), 
    title: Optional[str] = Form(None), 
    meeting_date: Optional[str] = Form(None), 
    db: Session = Depends(get_db)
):
    new_meeting = None
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
            
            # --- NEW ROBUST PIPELINE INTEGRATION ---
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

            return MeetingResponse(
                meeting_id=str(new_meeting.id), 
                status=new_meeting.status,
                message="Meeting processed successfully." if new_meeting.status == "completed" else "Meeting submission failed during AI extraction."
            )
            
    except Exception as e:
        if not new_meeting:
            raise e
        return MeetingResponse(
            meeting_id=str(new_meeting.id), 
            status="failed",
            message="File upload successful but processing crashed."
        )


@router.get('/search', response_model=MeetingListResponse, status_code=status.HTTP_200_OK)
async def meeting_search(
    q: str,
    page: int = 1,
    per_page: int = 9,
    db: Session = Depends(get_db)
):
    query = db.query(Meeting).outerjoin(ActionItem).outerjoin(Decision)
    search_filter = or_(
        Meeting.title.ilike(f"%{q}%"),
        Meeting.raw_input_text.ilike(f"%{q}%"),
        Meeting.short_summary.ilike(f"%{q}%"),
        ActionItem.description.ilike(f"%{q}%"),
        Decision.description.ilike(f"%{q}%")
    )

    query = query.filter(search_filter).group_by(Meeting.id) 

    total_count = query.count()
    offset = (page - 1) * per_page

    meetings = (
        query.order_by(desc(Meeting.created_at)) 
        .offset(offset)
        .limit(per_page)
        .all()
    )   

    return {
        "meetings": meetings,
        "total": total_count,
        "page": page,
        "per_page": per_page
    }


@router.get('/{meeting_id}/status', response_model=MeetingStatusResponse, status_code=status.HTTP_200_OK)
async def get_meeting_status(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting: 
        raise HTTPException(status_code=404, detail="Meeting Not Found")
    
    return meeting


@router.get('/{meeting_id}', response_model=MeetingDetailedResponse, status_code=status.HTTP_200_OK)
async def get_meeting(meeting_id: str, db : Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting Not Found")
    
    return meeting


@router.get('/', response_model=MeetingListResponse, status_code=status.HTTP_200_OK)
async def get_all_meetings(
    page: int = 1,
    per_page: int = 9,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Meeting)

    if status:
        query = query.filter(Meeting.status == status)

    total_count = query.count()
    offset = (page - 1) * per_page
    meetings = query.order_by(desc(Meeting.created_at)).offset(offset).limit(per_page).all()
    
    formatted_meetings = []
    for m in meetings:
        m_dict = {
            "id": str(m.id), 
            "title": m.title,
            "meeting_date": m.meeting_date,
            "status": m.status,
            "input_type": m.input_type,
            "short_summary": m.short_summary,
            "created_at": m.created_at
        }
        formatted_meetings.append(m_dict)

    return {
        "meetings": formatted_meetings,
        "total": total_count,
        "page": page,
        "per_page": per_page
    }