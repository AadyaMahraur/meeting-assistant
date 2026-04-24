from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import date, datetime
from uuid import UUID

class MeetingRequest(BaseModel):
    title: str
    meeting_date: date
    text: str = Field(min_length=20)

class MeetingResponse(BaseModel):
    meeting_id: UUID
    status: str
    message: str

class ActionItem(BaseModel):
    description: str
    owner: str
    deadline: str
    priority: str
    status: str
    model_config = ConfigDict(from_attributes=True)

class Decision(BaseModel):
    description: str
    decided_by: str
    model_config = ConfigDict(from_attributes=True)

class Blocker(BaseModel):
    description: str
    type: str
    raised_by: str
    model_config = ConfigDict(from_attributes=True)

class MeetingDetailedResponse(BaseModel):
    id: UUID
    title: str
    meeting_date: date
    status: str
    input_type: str
    # word_count: int
    short_summary: str
    detailed_summary: str
    # action_item_count: int
    # decision_count: int
    created_at: datetime
    followup_email: str

    action_items: List[ActionItem] = []
    decisions: List[Decision] = []
    blockers: List[Blocker] = []

    model_config = ConfigDict(from_attributes=True)


class MeetingStatusResponse(BaseModel):
    status: str

# for meeting history: individual, list
class MeetingHistoryCard(BaseModel):
    id: UUID
    title: str
    meeting_date: date
    status: str
    input_type: str
    # word_count: int
    short_summary: str
    # action_item_count: int
    # decision_count: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MeetingListResponse(BaseModel):
    meetings: List[MeetingHistoryCard]
    total: int
    page: int
    per_page:int