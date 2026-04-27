# System Architecture

This document details the technical design and data flow of the Meeting-to-Execution Assistant.

## High-Level Overview

The application follows a decoupled client-server architecture. The frontend handles user interaction and real-time state management, while the backend manages long-running AI tasks, file processing, and relational data storage.

### The Tech Stack
* **Frontend:** React (Vite), Tailwind CSS, shadcn/ui, Lucide React.
* **Backend:** FastAPI (Python), SQLAlchemy (ORM).
* **Database:** PostgreSQL (via Neon/Railway).
* **AI Engine:** Google Gemini 2.5 Flash API.
* **Task Management:** Asynchronous polling logic.

---

## Data Flow Pipeline

### 1. Ingestion Phase
Users submit data via two primary paths:
* **Text Ingestion:** Raw text is validated for length and content safety before being stored as a `pending` meeting record.
* **File Ingestion:** Supported files (.txt, .md, .docx) are processed using specialized utility handlers to extract clean string data.

### 2. AI Processing Phase
The backend triggers the `process_meeting_extraction` service. 
* **Prompt Engineering:** A system prompt enforces a strict JSON schema and "grounding" rules (no hallucinations).
* **Resiliency:** The pipeline uses `tenacity` for exponential backoff retries and `asyncio.wait_for` to prevent hanging connections.
* **Observability:** Metadata (token count, latency, retries) is captured for every execution.

### 3. Ingestion & Relational Mapping
Once the AI returns valid JSON, the `ingest_meeting_results` service maps the data into a relational structure:
* **Meetings Table:** Stores summaries and follow-up emails.
* **ActionItems Table:** Stores tasks with owners, deadlines, and priorities.
* **Decisions/Blockers Tables:** Stores specific meeting outcomes.
* **ProcessingLogs Table:** Stores the AI performance metadata for that specific run.

---

## Database Schema

The database uses a relational one-to-many model centered around the `Meeting` entity.

* **Meeting (1) ⮕ (N) ActionItem**
* **Meeting (1) ⮕ (N) Decision**
* **Meeting (1) ⮕ (N) Blocker**
* **Meeting (1) ⮕ (1) ProcessingLog**



---

## Design Patterns & Principles

### Asynchronous Polling
Since AI extraction can take 20-60 seconds, the API returns a `202 ACCEPTED` status immediately with a `meeting_id`. The frontend then polls the `/{meeting_id}/status` endpoint. This prevents gateway timeouts and provides a better user experience.

### Repository Pattern (Service Layer)
Database logic is separated from API routes.
* `app/services/extraction.py`: Handles AI interaction.
* `app/services/ingestion.py`: Handles database staging and commits.

### Connection Resilience
The system uses SQLAlchemy connection pining (`pool_pre_ping=True`) to handle the aggressive idle-connection timeouts typical of serverless PostgreSQL providers.