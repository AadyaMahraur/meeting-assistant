# Project Architecture & Design Decisions

### Decision: FastAPI as the Backend Framework
**Date:** 2026-04-10  
**Meeting-to-Execution Assistant — Internship Charter**

**Decision:** Use FastAPI for the core API development.

**Alternatives Considered:**
1. **Flask** — While flexible, it lacks native asynchronous support and built-in data validation.
2. **Django** — Too "heavyweight" for this project; the built-in Admin and ORM complexity would have slowed down the rapid development of a focused AI microservice.

**Why Chosen:** FastAPI provides native support for `async/await`, which is essential for non-blocking AI API calls. Its automatic Swagger documentation and Pydantic-based data validation ensure the AI response matches the database schema perfectly.

**Downsides:** Requires a bit more manual setup for certain features (like authentication) compared to Django’s "batteries-included" approach.

**Revisit If:** The project grows into a massive monolithic enterprise application requiring complex built-in administrative tools.

---

### Decision: PostgreSQL for Data Storage
**Date:** 2026-04-12  
**Meeting-to-Execution Assistant — Internship Charter**

**Decision:** Use PostgreSQL as the primary relational database.

**Alternatives Considered:**
1. **MongoDB** — While good for unstructured JSON, it makes complex relational queries (like joining Meetings, Action Items, and Decisions for search) much more difficult to manage as the data grows.

**Why Chosen:** The meeting data is inherently relational. A single meeting has many action items, decisions, and blockers. SQL allows for strict data integrity and efficient searching across these related tables.

**Downsides:** Schema changes require database migrations, which are slightly more rigid than MongoDB's document-based approach.

**Revisit If:** The application pivots to storing entirely unstructured, non-relational "blobs" of data with no clear connections.

---

### Decision: Google Gemini 2.5 Flash for AI Extraction
**Date:** 2026-04-14  
**Meeting-to-Execution Assistant — Internship Charter**

**Decision:** Use the Gemini 2.5 Flash model for transcript processing.

**Alternatives Considered:**
1. **GPT-4o / GPT-3.5** — High cost and lower rate limits for the expected volume of transcript data.
2. **Llama 3 (Self-hosted)** — High infrastructure overhead and latency for an MVP.

**Why Chosen:** Gemini 2.5 Flash offers a massive context window (allowing for long transcripts) and high speed at a lower cost. Its native support for `response_mime_type: "application/json"` ensures reliable structured data extraction.

**Downsides:** Requires consistent internet connectivity and reliance on a third-party API provider.

**Revisit If:** Strict data privacy regulations mandate local, on-premise model hosting.

---

### Decision: Synchronous-Response Polling over Async Message Queues
**Date:** 2026-04-16  
**Meeting-to-Execution Assistant — Internship Charter**

**Decision:** Return a "Pending" status immediately and use frontend polling instead of a background worker.

**Alternatives Considered:**
1. **Celery + Redis** — The standard for long-running tasks, but significantly increases the complexity of the deployment and infrastructure for an MVP.

**Why Chosen:** For an MVP, keeping the infrastructure simple is a priority. Using FastAPI’s `async` capabilities to handle the API call while the database tracks status allows the frontend to poll for updates without needing a complex message broker.

**Downsides:** Not as scalable for thousands of simultaneous users as a dedicated worker queue.

**Revisit If:** User volume increases to the point where API workers are consistently blocked by long-running AI requests.

---

### Decision: Strict JSON Grounding in Prompt Engineering
**Date:** 2026-04-18  
**Meeting-to-Execution Assistant — Internship Charter**

**Decision:** Structured the prompt to enforce "Strict Grounding" and a mandatory JSON schema.

**Alternatives Considered:**
1. **Natural Language Output** — Letting the AI write a free-form summary. This was rejected because the output cannot be cleanly saved into relational database tables.

**Why Chosen:** By providing a sample JSON schema in the prompt and using the `response_mime_type` config, we ensure the backend can immediately parse the output into `ActionItem` and `Decision` database models.

**Downsides:** Strict grounding can sometimes make summaries feel "dry" as it prevents the AI from adding helpful outside context that wasn't explicitly stated.

**Revisit If:** The UI moves toward a conversational/chat-based interface rather than a structured dashboard.

---

### Decision: Dynamic Summary Scaling for Long Transcripts
**Date:** 2026-04-20  
**Meeting-to-Execution Assistant — Internship Charter**

**Decision:** Implement prompt instructions that change length requirements based on input word count.

**Alternatives Considered:**
1. **Recursive Summarization** — Breaking the meeting into chunks and summarizing each separately. Rejected for the MVP due to high token cost and latency.

**Why Chosen:** Instructing the AI to increase paragraph counts (1-3 for short, 5-7 for long) ensures that important details in an hour-long meeting aren't compressed into a single generic paragraph.

**Downsides:** Very long meetings may still hit token limits or cause the AI to "lose the thread" of earlier discussion points.

**Revisit If:** Meetings regularly exceed 2+ hours, requiring a "Map-Reduce" chunking summarization approach.

---

### Decision: Graceful Fallbacks for Missing Metadata
**Date:** 2026-04-22  
**Meeting-to-Execution Assistant — Internship Charter**

**Decision:** Programmatically inject "Not identified" or "Not specified" for missing owners and deadlines.

**Alternatives Considered:**
1. **AI "Best Guess"** — Forcing the AI to guess an owner. This leads to hallucinations and incorrect task assignments.

**Why Chosen:** It is better to show the user that information was missing from the transcript than to provide incorrect information. This maintains user trust in the system's accuracy.

**Downsides:** Requires the frontend to handle these "placeholder" strings gracefully in the UI.

**Revisit If:** The system integrates with a Company Directory to attempt "fuzzy matching" of speaker names to actual employees.

---

### Decision: Dual-Layer Input Validation
**Date:** 2026-04-24  
**Meeting-to-Execution Assistant — Internship Charter**

**Decision:** Maintain basic validation in Pydantic schemas while executing complex logic validation in the backend.

**Alternatives Considered:**
1. **Pydantic Only** — Writing complex regex or custom validators inside the schema.
2. **Backend Only** — Removing Pydantic rules and handling everything inside the API route.

**Why Chosen:** Pydantic acts as the "first line of defense," instantly rejecting empty or obviously useless payloads before they reach the route logic. The backend is then used for domain-specific logic, like counting words and cleaning the text, creating a highly resilient validation system.

**Downsides:** Slight logic duplication. If absolute minimum character limits change, both the schema and the backend text parser may need updates.

**Revisit If:** The validation logic becomes simple enough to consolidate entirely into Pydantic `@field_validator` decorators.

---

### Decision: Explicit Schema Naming Conventions
**Date:** 2026-04-25  
**Meeting-to-Execution Assistant — Internship Charter**

**Decision:** Rename Pydantic schemas to append `Schema` (e.g., `ActionItemSchema`) and use action-oriented names.

**Alternatives Considered:**
1. **Identical Naming** — Naming both the SQLAlchemy database model and the Pydantic data transfer object `ActionItem`.

**Why Chosen:** Prevents dangerous namespace collisions. Having two classes with the exact same name makes it incredibly easy to accidentally import the database model into the API route definition, causing silent failures. The suffixes create instant clarity on what type of object is being handled.

**Downsides:** Slightly more verbose class names.

**Revisit If:** The application folder structure is refactored into completely isolated vertical slices where cross-imports are impossible.

---

### Decision: Connection Pre-Pinging for Serverless Databases
**Date:** 2026-04-26  
**Meeting-to-Execution Assistant — Internship Charter**

**Decision:** Add `pool_pre_ping=True` and `pool_recycle=300` to the SQLAlchemy engine configuration.

**Alternatives Considered:**
1. **Default Settings** — Relying on the standard connection pool without health checks.

**Why Chosen:** Serverless databases aggressively sever idle connections to save resources. When SQLAlchemy attempts to send a payload down a dead connection, it throws an `OperationalError`. Pre-pinging forces SQLAlchemy to test the connection with a tiny `SELECT 1` before sending data, silently recreating the connection if it dropped.

**Downsides:** Adds a tiny microsecond overhead to every database transaction to perform the health check.

**Revisit If:** The database is migrated to a dedicated, always-on PostgreSQL instance where connection lifetimes are entirely under our control.

---

### Decision: Database Flushing vs. Committing in Services
**Date:** 2026-04-26  
**Meeting-to-Execution Assistant — Internship Charter**

**Decision:** Use `db.flush()` instead of `db.commit()` inside the `ingest_meeting_results` data mapping service.

**Alternatives Considered:**
1. **Commit in the Service** — Committing the data as soon as the `ActionItem` and `Decision` loops finish.

**Why Chosen:** Flushed data is sent to the database but the transaction remains open. This allows the parent API route to manage the final transaction. If saving the AI processing log fails *after* ingestion, the route can trigger a `db.rollback()`, wiping out the partially saved meeting and preventing corrupted or orphaned data.

**Downsides:** Developers must remember to call `db.commit()` at the route level, otherwise the data simply vanishes when the request ends.

**Revisit If:** We move to an Event-Driven architecture where ingestion steps are handled by fully isolated microservices.

---

### Decision: Strict Git Branching for UI vs. Logic
**Date:** 2026-04-27  
**Meeting-to-Execution Assistant — Internship Charter**

**Decision:** Isolate visual UI updates (`style/ui-polish`) from backend routing/logic fixes (`chore/code-cleanup-and-refining`).

**Alternatives Considered:**
1. **Single Branch Commits** — Pushing Tailwind CSS padding changes and API redirect logic into the same commit on the `main` branch.

**Why Chosen:** Keeps the Git history atomic. If a routing change breaks the application redirect flow, it can be reverted safely without accidentally undoing all the front-end styling and layout work. It mirrors professional CI/CD team environments.

**Downsides:** Requires more disciplined branch management and context switching during rapid solo development.

**Revisit If:** Working on an extremely tight deadline where rapid prototyping speed is strictly prioritized over a maintainable code history.