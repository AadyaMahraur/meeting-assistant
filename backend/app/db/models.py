import uuid
from sqlalchemy import Column, Boolean, Integer, String, Text, TIMESTAMP, Date, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(500))
    meeting_date = Column(Date)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    input_type = Column(String(50))
    raw_input_text = Column(Text, nullable=False)
    original_filename = Column(String(500)) 
    status = Column(String(50), index=True)
    error_message = Column(Text)
    word_count = Column(Integer)
    short_summary = Column(Text) 
    detailed_summary = Column(Text) 
    followup_email = Column(Text)

class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="cascade"), nullable=False, index=True)
    description = Column(Text, nullable=False)
    owner = Column(String(200))
    deadline = Column(String(200))
    priority = Column(String(50), nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Decision(Base):
    __tablename__ = "decisions"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="cascade"), nullable=False, index=True)
    description = Column(Text, nullable=False)
    decided_by = Column(String(200))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Blocker(Base):
    __tablename__ = "blockers"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="cascade"), nullable=False, index=True)
    description = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)
    raised_by = Column(String(200))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class ProcessingLog(Base):
    __tablename__ = "processing_logs"
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id", ondelete="cascade"), nullable=False, index=True)
    started_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    completed_at = Column(TIMESTAMP(timezone=True))
    model_used = Column(String(100), nullable=False)
    prompt_tokens = Column(Integer)
    response_tokens = Column(Integer)
    success = Column(Boolean)
    error_details = Column(Text)
    retry_count = Column(Integer, default=0)
