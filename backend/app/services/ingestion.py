from app.db.models import Meeting, ActionItem, Decision, Blocker, ProcessingLog

def save_processing_log(meeting_id: str, metadata: dict, db):
    """Saves the tracking metrics to the processing_logs table."""
    log_record = ProcessingLog(
        meeting_id=meeting_id,
        started_at=metadata.get("started_at"),
        completed_at=metadata.get("completed_at"),
        model_used=metadata.get("model_used", "gemini-3-flash-preview"),
        prompt_tokens=metadata.get("prompt_tokens"),
        response_tokens=metadata.get("response_tokens"),
        success=metadata.get("success", False),
        error_details=metadata.get("error_details"),
        retry_count=metadata.get("retry_count", 0)
    )
    db.add(log_record)
    db.commit()

def ingest_meeting_results(meeting_id: str, results: dict, db): 
    """Takes extracted dictionary results and stages them for the database."""
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting:
        raise ValueError(f"Meeting {meeting_id} not found")
    
    meeting.short_summary = results.get("short_summary")
    meeting.detailed_summary = results.get("detailed_summary")
    meeting.followup_email = results.get("followup_email")

    for action in results.get("action_items", []):
        db.add(ActionItem(
            meeting_id=meeting_id,
            description=action.get("description"),
            owner=action.get("owner"),
            deadline=action.get("deadline"),
            priority=action.get("priority"),
            status="pending"
        ))

    for decision in results.get("decisions", []):
        db.add(Decision(
            meeting_id=meeting_id,
            description=decision.get("description"),
            decided_by=decision.get("decided_by")
        ))

    for blocker in results.get("blockers", []):
        db.add(Blocker(
            meeting_id=meeting_id,
            description=blocker.get("description"),
            type=blocker.get("type"),
            raised_by=blocker.get("raised_by")
        ))
    
    # flush instead of commit so the API route can manage the final transaction
    db.flush()