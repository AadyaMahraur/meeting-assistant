from pydantic import BaseModel, Field
from datetime import date

class MeetingRequest(BaseModel):
    title: str
    meeting_date: date
    text: str = Field(min_length=20)

class MeetingResponse(BaseModel):
    meeting_id: str
    status: str
    message: str