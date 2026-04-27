# API Specification

## Endpoint Overview

| Endpoint | Method | Frontend Component | Backend Logic (FastAPI) | Database Action |
| :--- | :--- | :--- | :--- | :--- |
| `/api/meetings/text` | POST | `TextInputForm` | Validates text; triggers background task | INSERT |
| `/api/meetings/upload` | POST | `FileUploadForm` | Extracts text via `file_handling.py` | INSERT |
| `/api/meetings/{id}/status` | GET | `ProcessingIndicator` | Checks if background task is finished | SELECT |
| `/api/meetings/{id}` | GET | `ResultView` | Fetches full processed object | SELECT |
| `/api/meetings` | GET | `HistoryPage` | Handles pagination & sorting | SELECT |
| `/api/meetings/search` | GET | `SearchBar` | Passes query string `q` to backend | SELECT |
| `/api/meetings/{id}` | DELETE | `MeetingCard` | Verifies ID existence and removes record | DELETE |
| `/api/health` | GET | (System Monitor) | Runs `SELECT 1` to check connection | SELECT |

---

## Endpoint Details

### 1. `POST /api/meetings/text`
Submit meeting notes as plain text for AI processing.

**Request Body:** `application/json`
```json
{
  "title": "Sprint Planning - June 12",
  "meeting_date": "2025-06-12",
  "text": "We discussed the new feature timeline..."
}
```

**Response:** `202 Accepted`
```json
{
  "meeting_id": "uuid-here",
  "status": "processing",
  "message": "Meeting submitted. Processing started."
}
```

---

### 2. `POST /api/meetings/upload`
Upload a transcript file for text extraction and AI processing.

**Request Body:** `multipart/form-data`
* `file`: The transcript file (`.txt`, `.md`, `.docx`)
* `title`: string *(optional)*
* `meeting_date`: string *(optional)*

**Response:** `202 Accepted`
```json
{
  "meeting_id": "uuid-here",
  "status": "processing",
  "message": "File uploaded. Processing started."
}
```

---

### 3. `GET /api/meetings/{meeting_id}`
Get the full, detailed results of a processed meeting.

**Response:** `200 OK`
```json
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
      "id": "uuid",
      "description": "Update the API documentation",
      "owner": "Rahul",
      "deadline": "June 15",
      "priority": "high",
      "status": "pending"
    }
  ],
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
```

---

### 4. `GET /api/meetings`
List all historical meetings with pagination support.

**Query Parameters:**
* `page`: integer *(default: 1)*
* `per_page`: integer *(default: 10)*
* `status`: string *(optional filter)*
* `sort_by`: string *(default: "created_at")*
* `sort_order`: string *(default: "desc")*

**Response:** `200 OK`
```json
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
```

---

### 5. `GET /api/meetings/search`
Search all meetings by a specific keyword or phrase.

**Query Parameters:**
* `q`: string *(the search query)*
* `page`: integer *(default: 1)*
* `per_page`: integer *(default: 10)*

*Note: This endpoint searches across `title`, `raw_input_text`, `short_summary`, action item `description`, and decision `description`.*

**Response:** `200 OK`
*(Returns the same paginated format as `GET /api/meetings`)*

---

### 6. `GET /api/meetings/{meeting_id}/status`
Check the background processing status of a submitted meeting.

**Response:** `200 OK`
```json
{
  "meeting_id": "uuid",
  "status": "processing",
  "started_at": "2025-06-12T10:30:00Z"
}
```

---

### 7. `DELETE /api/meetings/{meeting_id}`
Delete a meeting and all of its associated cascade data (Action Items, Decisions, Blockers, Logs).

**Response:** `200 OK`
```json
{
  "message": "Meeting deleted successfully"
}
```

---

### 8. `GET /api/health`
System health check endpoint used by deployment monitors.

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-06-12T10:30:00Z"
}
```