### Table: meetings
 
| Column            | Type         | Notes                                             |
| :---------------- | :----------- | :------------------------------------------------ |
| id                | UUID         | Primary key, auto-generated                       |
| title             | VARCHAR(500) | User-provided or auto-generated                   |
| meeting_date      | DATE         | Date of the meeting                               |
| created_at        | TIMESTAMP    | When record was created                           |
| updated_at        | TIMESTAMP    | When record was last updated                      |
| input_type        | VARCHAR(50)  | "text" or "transcript-file" or "audio"            |
| raw_input_text    | TEXT         | The original input text                           |
| original_filename | VARCHAR(500) | If file was uploaded, the filename                |
| status            | VARCHAR(50)  | "pending" / "processing" / "completed" / "failed" |
| error_message     | TEXT         | If processing failed, the error                   |
| word_count        | INTEGER      | Word count of input                               |
| short_summary     | TEXT         | Generated short summary                           |
| detailed_summary  | TEXT         | Generated detailed summary                        |
| followup_email    | TEXT         | Generated follow-up email draft                   |


### Table: action_items

| Column      | Type         | Notes                                                                           |
| :---------- | :----------- | :-------------------------------------------------------------------------------|
| id          | UUID         | Primary key                                                                     |
| meeting_id  | UUID         | Foreign key to meetings                                                         |
| description | TEXT         | What needs to be done                                                           |
| owner       | VARCHAR(200) | Who is responsible (nullable)                                                   |
| deadline    | VARCHAR(200) | When it is due (nullable, text: input may say "next Friday" or "end of sprint") |
| priority    | VARCHAR(50)  | "high" / "medium" / "low" / "not specified"                                     |
| status      | VARCHAR(50)  | "pending" / "in-progress" / "done"                                              |
| created_at  | TIMESTAMP    |                                                                                 |


### Table: decisions

| Column      | Type         | Notes                           |
| :---------- | :----------- | :------------------------------ |
| id          | UUID         | Primary key                     |
| meeting_id  | UUID         | Foreign key to meetings         |
| description | TEXT         | What was decided                |
| decided_by  | VARCHAR(200) | Who made the decision (nullable)|
| created_at  | TIMESTAMP    |                                 |



### Table: blockers

| Column      | Type         | Notes                                   |
| :---------- | :----------- | :-------------------------------------- |
| id          | UUID         | Primary key                             |
| meeting_id  | UUID         | Foreign key to meetings                 |
| description | TEXT         | Description of blocker/risk/question    |
| type        | VARCHAR(50)  | "blocker" / "risk" / "open-question"    |
| raised_by   | VARCHAR(200) | Who raised it (nullable)                |
| created_at  | TIMESTAMP    |                                         |


### Table: processing_logs

| Column          | Type         | Notes                                |
| :-------------- | :----------- | :----------------------------------- |
| id              | UUID         | Primary key                          |
| meeting_id      | UUID         | Foreign key to meetings              |
| started_at      | TIMESTAMP    | When processing started              |
| completed_at    | TIMESTAMP    | When processing finished             |
| model_used      | VARCHAR(100) | e.g., "gemini-1.5-flash"             |
| prompt_tokens   | INTEGER      | Tokens used in prompt (if available) |
| response_tokens | INTEGER      | Tokens in response (if available)    |
| success         | BOOLEAN      | Whether processing succeeded         |
| error_details   | TEXT         | Error details if failed              |
| retry_count     | INTEGER      | Number of retries attempted          |

Relationships:
1 One meeting has many action_items
2 One meeting has many decisions
3 One meeting has many blockers
4 One meeting has many processing_logs

Indexes:
1 Index on meetings.status
2 Index on meetings.created_at
3 Index on meetings.title (for search)
4 Full-text search index on meetings.raw_input_text (for keyword search)
5 Index on action_items.meeting_id
6 Index on decisions.meeting_id
7 Index on blockers.meeting_id