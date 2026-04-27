from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import date, datetime
from uuid import UUID

#Input Schemas
class TextMeetingUpload(BaseModel):
    title: Optional[str]
    meeting_date: Optional[date] = None
    text: str = Field(min_length=20)

#Acknowledgment Schemas (Initial Submission)
class MeetingUploadAck(BaseModel):
    meeting_id: UUID
    status: str
    message: str

#Nested Entity Schemas (Suffix 'Schema' prevents DB model collision)
class ActionItemSchema(BaseModel):
    description: str
    owner: str
    deadline: str
    priority: str
    status: str
    model_config = ConfigDict(from_attributes=True)

class DecisionSchema(BaseModel):
    description: str
    decided_by: str
    model_config = ConfigDict(from_attributes=True)

class BlockerSchema(BaseModel):
    description: str
    type: str
    raised_by: str
    model_config = ConfigDict(from_attributes=True)

#Detail Schemas
class MeetingDetailResult(BaseModel):
    id: UUID
    title: str
    meeting_date: date
    status: str
    input_type: str
    word_count: int
    short_summary: Optional[str] = None     
    detailed_summary: Optional[str] = None  
    created_at: datetime
    followup_email: Optional[str] = None    

    action_items: List[ActionItemSchema] = []
    decisions: List[DecisionSchema] = []
    blockers: List[BlockerSchema] = []

    model_config = ConfigDict(from_attributes=True)

class MeetingStatusResult(BaseModel):
    status: str

#List/Pagination Schemas
class MeetingCardSchema(BaseModel):
    id: UUID
    title: str
    meeting_date: date
    status: str
    input_type: str
    word_count: int
    short_summary: Optional[str] = None     
    action_item_count: int
    decision_count: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PaginatedMeetingHistory(BaseModel):
    meetings: List[MeetingCardSchema]
    total: int
    page: int
    per_page: int