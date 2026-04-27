# Project Scope: Meeting-to-Execution Assistant

This document defines the boundaries of the Minimum Viable Product (MVP) for the Meeting-to-Execution Assistant. It outlines what will be delivered, what is intentionally excluded, and the assumptions and risks associated with the build.

---

## In Scope (MVP Features)

The MVP is focused on delivering a core, end-to-end pipeline for text-based meeting extraction and management. 

### 1. Data Ingestion
* **Text Input:** A UI component allowing users to copy and paste raw transcript text directly.
* **File Upload:** Support for uploading standard document formats (`.txt`, `.pdf`, `.docx`) and extracting their raw text.
* **Pre-processing Validation:** Backend and Pydantic validation to ensure inputs meet minimum length requirements before AI processing.

### 2. AI Extraction Pipeline (Gemini 2.5 Flash)
* **Summarization:** Generation of both a Short Summary (3-5 sentences) and a length-scaled Detailed Summary (1-7 paragraphs).
* **Action Item Tracking:** Extraction of specific tasks, assigning "owners," "deadlines," and calculating "priority."
* **Decision Logging:** Extraction of explicitly confirmed decisions and the parties responsible for making them.
* **Blocker Identification:** Extraction of issues categorized strictly as `blocker`, `risk`, or `open_question`.
* **Automated Drafting:** Generation of a ready-to-send follow-up email summarizing the meeting.

### 3. User Interface & Experience
* **Asynchronous Polling:** A real-time loading UI that polls the backend (`/status`) so users aren't left waiting on a frozen screen during the 20-60 second AI processing time.
* **Result Dashboard:** A clean, tabbed or card-based UI to display the extracted JSON data.
* **Meeting History:** A fully paginated dashboard displaying past meetings.
* **Deep Search:** A search bar capable of querying meeting titles, summaries, action items, and decisions.

### 4. Backend & Infrastructure
* **Relational Database:** A PostgreSQL database utilizing a One-to-Many schema (`Meetings`, `ActionItems`, `Decisions`, `Blockers`, `ProcessingLogs`).
* **Error Handling:** Graceful API fallbacks, custom `PipelineError` classes, and database rollbacks to prevent corrupted data if the AI fails.

---

## Out of Scope

To ensure the MVP is delivered on time, the following features are strictly excluded from this phase of development:

* **Native Audio/Video Transcription:** The system will not accept `.mp3` or `.mp4` files. Users must provide pre-transcribed text.
* **User Authentication & Workspaces:** The MVP will act as a single-tenant application. There are no logins, roles, or private user accounts.
* **External Integrations:** No direct integration with external task managers (e.g., Jira, Asana, Trello, or Slack).
* **Document Export:** Downloading results as `.pdf`, `.docx`, or `.md` files is not supported in the UI.
* **Cross-Meeting Analytics:** The AI processes each meeting in a vacuum; it cannot track an action item's progress across multiple sequential meetings.
* **Live Collaborative Editing:** The extracted results dashboard is read-only (aside from deleting the entire meeting). Users cannot manually edit the AI's output in the UI.

---

## Assumptions

The success of the project relies on the following assumptions being true:

1. **Transcript Quality:** Users will input reasonably coherent, pre-generated transcripts. The AI can handle conversational tangents, but it cannot invent data from completely garbled or incomplete text.
2. **Explicit Mentions:** For the AI to extract an owner or a decision, it must be explicitly mentioned in the text. (e.g., The AI will not know who "I" or "we" refers to unless names are used).
3. **API Stability:** The Google Gemini 2.5 Flash API will remain available, with latency and cost parameters suitable for a synchronous polling architecture.
4. **Database Resilience:** The chosen serverless PostgreSQL provider will support connection pre-pinging to prevent idle disconnects during long AI processing windows.

---

## Risks

| Risk | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **API Timeout / Rate Limiting** | High | Implemented `tenacity` exponential backoff retries and a strict 60-second `asyncio.wait_for` timeout. |
| **JSON Hallucinations** | High | Using `response_mime_type="application/json"` and strict post-extraction dictionary validation before database insertion. |
| **Token Limit Exceeded** | Medium | Built dynamic paragraph scaling into the prompt and established a known limitation for transcripts >15,000 words. |
| **Database Connection Drops** | Medium | Configured SQLAlchemy engine with `pool_pre_ping=True` and `pool_recycle=300` to silently rebuild severed connections. |

---

## Success Criteria

The MVP will be considered complete and successful when:

1. **End-to-End Execution:** A user can upload a 3,000-word transcript and view the fully populated results dashboard within 60 seconds without errors.
2. **Data Integrity:** The database correctly associates Action Items, Decisions, and Blockers with their parent Meeting ID 100% of the time, with no orphaned records.
3. **Searchability:** A user can successfully retrieve a past meeting by searching for a keyword that exists only inside one of its Action Items.
4. **Resiliency:** If the Gemini API goes down or returns garbage data, the backend successfully catches the error, saves the failure metadata to the `ProcessingLogs`, rolls back the database, and displays a friendly error message to the user instead of crashing the server.