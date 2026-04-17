from app.db.models import Meeting, ActionItem, Decision, Blocker


def save_extraction_results(meeting_id, results, db): #add data type?
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()

    if not meeting:
        print(f"Meeting {meeting_id} not found")
        return
    
    try: 
        meeting.short_summary = results["short_summary"]
        meeting.detailed_summary = results["detailed_summary"]
        meeting.followup_email = results["followup_email"]

        for action in results["action_items"]:
            action_record = ActionItem(
                meeting_id = meeting_id,
                description = action["description"],
                owner = action["owner"],
                deadline = action["deadline"],
                priority = action["priority"],
                status = "pending"
            )
            db.add(action_record)

        for decision in results["decisions"]:
            decision_record = Decision(
                meeting_id = meeting_id,
                description = decision["description"],
                decided_by = decision["decided_by"],
            )

            db.add(decision_record)

        for blocker in results["blockers"]:
            blocker_record = Blocker(
                meeting_id = meeting_id,
                description = blocker["description"],
                type = blocker["type"],
                raised_by = blocker["raised_by"],
            )

            db.add(blocker_record)
        
        meeting.status="completed"
        db.commit()
    except Exception as e:
        db.rollback()
        meeting.status = "failed"
        print(f"Error saving results: {e}")
        db.commit()


