# Final Project Report: Meeting-to-Execution Assistant

## Project Summary
The Meeting-to-Execution Assistant is an AI-powered microservice and web application designed to transform unstructured meeting transcripts into actionable, relational data. By leveraging Google's Gemini 2.5 Flash model, the application automatically extracts executive summaries, decisions, action items, blockers, and drafts follow-up emails, saving teams hours of manual administrative work.

---

## What Was Built (MVP Scope)
1. **FastAPI Backend:** A robust, asynchronous API handling incoming transcripts, file uploads (.txt, .pdf, .docx), and background task processing.
2. **PostgreSQL Database:** A relational schema mapping single meetings to multiple action items, decisions, and blockers, alongside detailed AI processing logs.
3. **AI Pipeline:** A tightly controlled prompt engineering layer utilizing `tenacity` for retries and strict JSON schema enforcement to ensure predictable, structured data extraction.
4. **React/Vite Frontend:** A decoupled user interface featuring asynchronous status polling, a paginated history dashboard, and deep-search functionality.

---

## What Works Well
* **The Asynchronous Polling Architecture:** By returning a `202 Accepted` status immediately and having the UI poll for updates, the application successfully avoids HTTP 504 Gateway Timeouts, even when the AI takes up to 60 seconds to process a large transcript.
* **Strict Data Grounding:** The prompt engineering successfully forces the AI to output valid, parseable JSON that aligns perfectly with the backend Pydantic models. Data corruption from AI hallucinations is extremely low.
* **Database Resilience:** Implementing `pool_pre_ping=True` completely resolved the `OperationalError` bugs caused by serverless databases dropping idle connections.
* **Two-Tier Validation:** Using Pydantic for immediate lightweight validation and the backend service layer for heavy logic validation keeps the API secure and performant.

---

## What Does Not Work Well (Honest Assessment)
* **Speaker and Role Ambiguity:** The AI struggles if the transcript uses generic pronouns. If a transcript says, "We will handle that," the AI often defaults to "Not identified" for the owner. It requires explicit names to assign tasks accurately.
* **Context Isolation:** The application treats every meeting as an isolated event. It cannot link an action item from "Sprint Planning 1" to a blocker discussed in "Sprint Planning 2."
* **Processing Latency:** Processing long meetings (e.g., >5,000 words) can take upwards of 45–60 seconds. While the polling UI helps, it is still a long time for a user to stare at a loading screen.
* **Mobile Responsiveness on Tables:** While the overall UI is responsive, the Data Tables used for Action Items and Decisions require horizontal scrolling on small mobile screens, resulting in a suboptimal user experience.

---

## Technical Decisions and Trade-offs
* **FastAPI vs. Django:** Chose FastAPI for its native asynchronous capabilities, which are crucial for waiting on AI API calls. *Trade-off:* Had to manually configure features like CORS and project structure that Django handles out-of-the-box.
* **Sync Polling vs. Celery/Redis:** Chose to use FastAPI `BackgroundTasks` combined with database status flags instead of a dedicated message broker (Redis/Celery). *Trade-off:* Kept the deployment infrastructure simple and cheap for the MVP, but sacrificed the ability to easily scale to thousands of concurrent background tasks.
* **Structured Data vs. Creative Summaries:** Forced the AI into a strict JSON output. *Trade-off:* Made the data perfectly suited for a relational database and UI tables, but occasionally made the "Detailed Summary" feel a bit dry or rigidly formatted compared to a standard ChatGPT output.

---

## What I Learned
1. **Prompt Engineering is Software Engineering:** Writing a prompt isn't just about speaking English; it’s about establishing edge cases, defining variable constraints, and handling errors programmatically.
2. **Infrastructure Quirks:** Serverless databases operate differently than local databases. Learning to manage connection pooling and transaction states (`db.flush()` vs `db.commit()`) was a major leveling-up moment for backend stability.
3. **The Value of Decoupling:** Separating the frontend from the backend made testing infinitely easier. I could test the entire AI pipeline using a simple REST client without needing the UI to be finished.

---

## What I Would Do Differently
If starting this project over from day one:
* **Implement Authentication First:** I would build user logins (OAuth2) and attach a `user_id` to the `Meeting` table from the very beginning. Adding multi-tenancy *after* a database schema is heavily populated is difficult and requires complex migrations.
* **Adopt WebSockets:** Instead of having the frontend poll the backend every 3 seconds for a status update, I would use WebSockets for a true real-time push notification when the AI finishes processing.

---

## Future Improvements
1. **Audio/Video Ingestion:** Integrate an API like OpenAI Whisper to allow users to upload `.mp3` or `.mp4` files directly, bypassing the need for third-party transcription.
2. **Task Manager Integrations:** Build OAuth integrations to automatically push extracted Action Items into Jira, Asana, or Trello boards.
3. **Advanced Vector Search:** Upgrade the current standard PostgreSQL `ILIKE` search to use `tsvector` for full-text search, or integrate `pgvector` for semantic semantic similarity search across meetings.
4. **Cross-Meeting Analytics:** Create a dashboard that tracks the status of recurring Action Items and highlights long-term organizational blockers across multiple meeting sessions.
5. **Document Export:** Add functionality to allow users to export the final meeting breakdown as a formatted `.pdf` or a markdown-styled `.docx` file for easy sharing.
6. **User Authentication & Workspaces:** Implement secure user accounts so teams can have private, segmented meeting histories.

---

##  Time Spent Breakdown (Rough Estimate)
*Total Time: ~70 Hours*

* **15% (10 hrs) - Planning & Architecture:** System design, selecting the stack, defining the JSON schema, and setting up the Git repository.
* **30% (20 hrs) - Backend & Database:** Setting up FastAPI, building PostgreSQL models, creating CRUD endpoints, and managing connection pooling.
* **25% (18 hrs) - AI & Prompt Engineering:** Writing the extraction pipeline, refining the system prompt for strict JSON grounding, and implementing retry/timeout logic.
* **20% (15 hrs) - Frontend & UI:** Building the React dashboard, implementing the polling logic, and styling with Tailwind CSS.
* **10% (7 hrs) - Testing & Documentation:** Writing `pytest` backend tests, manual UI testing, and writing the README, Architecture, and API specification docs.