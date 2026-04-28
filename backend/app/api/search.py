from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_

from app.db.models import Meeting, ActionItem, Decision
# Updated Import
from app.schemas.meeting import PaginatedMeetingHistory
from app.db.database import get_db

router = APIRouter()

@router.get('/search', response_model=PaginatedMeetingHistory, status_code=status.HTTP_200_OK)
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

    query = query.filter(search_filter).filter(Meeting.status == "completed").group_by(Meeting.id) 

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
