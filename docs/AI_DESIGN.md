Model: gemini-2.5-flash

## How the prompt works?
The prompt mentions all the required headings(short summary, long summary, action items etc) with descriptions and specifications. It explicitly define rules regarding AI hallucination, ambiguity, and corner cases. It also provides the output format (json object). Finally, it provides the meeting content.



## Output

The extraction pipeline is designed to return a **strictly structured JSON object**. This ensures that the frontend can reliably map data to UI components like summary cards, action item tables, and decision logs.

###  Data Structure Overview
The final output is a single JSON object containing six primary keys. Each key serves a specific functional purpose:

| Key | Type | Description |
| :--- | :--- | :--- |
| `short_summary` | `string` | A 3-5 sentence overview focusing on the meeting's purpose and primary outcomes. |
| `detailed_summary` | `string` | A comprehensive narrative (1–7 paragraphs) detailing discussion themes and alternatives. |
| `decisions` | `list[object]` | Structured logs of confirmed conclusions and the parties responsible. |
| `action_items` | `list[object]` | A task list including descriptions, owners, deadlines, and priority levels. |
| `blockers` | `list[object]` | A breakdown of progress-impeding issues, risks, or unresolved questions. |
| `followup_email` | `string` | A pre-written, professional email draft summarizing the entire meeting. |

---

### Validation Criteria
For an output to be considered "successful," it must meet these logic requirements:

* **Decision Grounding:** Only items with a clear conclusion or consensus are included.
* **Action Item Specificity:** The `owner` field must identify specific teams or individuals (e.g., "Dev Team") instead of generic terms like "the team."
* **Blocker Taxonomy:** Categorized as `blocker` (immediate stop), `risk` (future issue), or `open_question` (unresolved).
* **Summary Scaling:** The `detailed_summary` length scales proportionally to the transcript word count (e.g., 5-7 paragraphs for >2000 words).



## Initial Challenges & Observations

During early testing with the baseline prompt, several structural and logical issues were identified:

### 1. Decision Dilution
* **Issue:** For short meetings, the AI mentioned "areas of discussion" but missed the actual finalized decision.
* **Issue:** In long meetings, the AI only identified explicit instructions as decisions, ignoring implicit consensus.

### 2. Entity & Role Confusion
* **Issue:** The model struggled to distinguish between who *raised* a blocker versus who was assigned to *fix* it.
* **Issue:** Generic terms like "the team" were used instead of identifying specific departments or individuals mentioned in the text.

### 3. Classification Overlap
* **Issue:** Misclassification of "Open Questions." The AI would categorize items as open questions even after a decision had clearly been made regarding them later in the meeting.
* **Issue:** A tendency to cap results at 5-6 points per category rather than exhaustive extraction.

---

## Prompt Refinement Strategy

To resolve these issues, the system prompt was rebuilt with strict logical constraints and improved definitions.

### Key Adjustments
* **Dynamic Length Scaling:** Introduced paragraph requirements based on word count (e.g., 5-7 paragraphs for meetings >2000 words) to prevent the "Detailed Summary" from being too brief.
* **Strict Grounding:** Explicitly forbade the AI from inventing information, while simultaneously commanding it to look outside of provided headings for hidden action items.
* **Entity Specificity:** Instructed the AI to distinguish between managerial tasks (assigned to team leads) and execution tasks (assigned to teams).
* **Blocker Definitions:** Defined the specific taxonomy for "Blocker" (progress-stopping), "Risk" (potential issue), and "Open Question" (unresolved).

---

## Prompt Evolution

### Version 1 (Baseline)
> *Focus: Basic categorization and JSON formatting.*
> 
> "You are an expert meeting analyst... extract SHORT_SUMMARY, DETAILED_SUMMARY, DECISIONS, ACTION_ITEMS..."

### Version 2 (Refined & Grounded) - *Current*
> *Focus: Contextual intelligence and strict data integrity.*
>
> **Major Additions:**
> * **confirmed decisions only:** Explicitly filter for "clear conclusion or consensus."
> * **Role-Based Ownership:** Differentiates between team leads and team members.
> * **Discussion Context:** Requires explicit mention of "alternatives considered" and "prioritized factors" for medium/long meetings.
> * **Tense & Tone:** Enforces past tense and third-person neutral tone for professional documentation.

---

## Handling Extraction Failures

The pipeline includes a "Self-Correction" logic at the code level:
1. **JSON Verification:** The system checks if all required keys (`short_summary`, `action_items`, etc.) are present in the AI response.
2. **Fallback Defaults:** If an owner or deadline is missing in an otherwise valid extraction, the system defaults to "Not identified" or "Not specified" rather than failing the entire process.
3. **PipelineError:** If the JSON is malformed or keys are missing, a custom `PipelineError` triggers a retry or logs the failure metadata for debugging.