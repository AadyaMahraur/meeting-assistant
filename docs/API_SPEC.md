| Endpoint                    | Method | Frontend Component      | Backend Logic (FastAPI)                         | Database Action  |
|-----------------------------|--------|-------------------------|-------------------------------------------------|------------------|
| /api/meetings/text          | POST   | TextInputForm           | Validates text; triggers background task        | INSERT           |
| /api/meetings/upload        | POST   | FileUploadForm          | Extracts text via file_handling.py              | INSERT           |
| /api/meetings/{id}/status   | GET    | ProcessingIndicator     | Checks if background task is finished           | SELECT           |
| /api/meetings/{id}          | GET    | ResultView              | Fetches full processed object                   | SELECT           |
| /api/meetings               | GET    | HistoryPage             | Handles pagination & sorting                    | SELECT           |
| /api/meetings/search        | GET    | SearchBar               | Passes query string q to backend                | SELECT           |
| /api/meetings/{id}          | DELETE | MeetingCard             | Verifies ID existence                           | DELETE           |
| /api/health                 | GET    | (System Monitor)        | Runs SELECT 1 to check connection               | SELECT           |



1 POST /api/meetings/text
Submit meeting notes as text.

    Request body:
        JSON
        {
        "title": "Sprint Planning - June 12",
        "meeting_date": "2025-06-12",
        "text": "We discussed the new feature timeline..."
        }

    Response (202 Accepted):
        JSON
        {
        "meeting_id": "uuid-here",
        "status": "processing",
        "message": "Meeting submitted. Processing started."
        }


2 POST /api/meetings/upload
Upload a transcript file.

    Request: multipart/form-data
        file: the transcript file (.txt, .md, .docx) title: string (optional) meeting_date: string (optional) 

    Response (202 Accepted):
        JSON
        {
        "meeting_id": "uuid-here",
        "status": "processing",
        "message": "File uploaded. Processing started."
        }


3 GET /api/meetings/{meeting_id}
Get full details of a processed meeting.

    Response (200 OK):
        JSON
        {
        "id": "uuid",
        "title": "Sprint Planning - June 12",
        "meeting_date": "2025-06-12",
        "status": "completed",
        "input_type": "text",
        "word_count": 847,
        "short_summary": "...",
        "detailed_summary": "...",
        "followup_email": "...",
        "action_items": [
            {
            }
        ],
            "id": "uuid",
            "description": "Update the API documentation",
            "owner": "Rahul",
            "deadline": "June 15",
            "priority": "high",
            "status": "pending"
        "decisions": [
            {
            "id": "uuid",
            "description": "Use PostgreSQL instead of MongoDB",
            "decided_by": "Tech Lead"
            }
            ],
        "blockers": [
            {
            "id": "uuid",
            "description": "Waiting for design approval from client",
            "type": "blocker",
            "raised_by": "Priya"
            }
        ],
        "created_at": "2025-06-12T10:30:00Z"
        }


4 GET /api/meetings
List all meetings with pagination.

    Query parameters:
        page: integer (default 1) per_page: integer (default 10) status: string (optional filter) sort_by: string 
        (default "created_at") sort_order: string (default "desc") 
        
    Response (200 OK):
        JSON
        {
        "meetings": [
            {
            "id": "uuid",
            "title": "Sprint Planning - June 12",
            "meeting_date": "2025-06-12",
            "status": "completed",
            "input_type": "text",
            "word_count": 847,
            "short_summary": "...",
            "action_item_count": 5,
            "decision_count": 3,
            "created_at": "2025-06-12T10:30:00Z"
            }
        ],
        "total": 25,
        "page": 1,
        "per_page": 10
        }



5 GET /api/meetings/search
Search meetings by keyword.

    Query parameters:
        q: string (search query) page: integer per_page: integer This searches across: title, raw_input_text, 
        short_summary, action item descriptions, decision descriptions.

    Response: 
        same format as GET /api/meetings



6 GET /api/meetings/{meeting_id}/status
Check processing status of a meeting.

    Response (200 OK):
        JSON
        {
        "meeting_id": "uuid",
        "status": "processing",
        "started_at": "2025-06-12T10:30:00Z"
        }


7 DELETE /api/meetings/{meeting_id}
Delete a meeting and all associated data.

Response (200 OK):
    JSON
    {
    "message": "Meeting deleted successfully"
    }

8 GET /api/health
Health check endpoint.

    Response (200 OK):
        JSON
        {
        "status": "healthy",
        "database": "connected",
        "timestamp": "2025-06-12T10:30:00Z"
        }