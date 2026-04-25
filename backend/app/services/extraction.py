from app.services.ai_pipeline import generate_json_with_gemini, PipelineError
from datetime import datetime, timezone

async def process_meeting_extraction(text: str) -> tuple[dict, dict]:

    prompt = '''
        You are an expert meeting analyst. Your task is to extract strictly grounded, structured information from meeting notes or transcripts.
        Analyze the following meeting content and extract:
        1. SHORT_SUMMARY: A concise summary in 3-5 sentences. It should include the purpose of meeting, major discussion themes and any explicit decisions or outcomes (only if stated in the input). 
        2. DETAILED_SUMMARY: Provide a comprehensive narrative summary. Length requirements: 1–3 paragraphs for short meetings (<500 words), 3–5 paragraphs for medium meetings (500–2000 words), 5–7 paragraphs for long meetings (2000–5000 words). Include all major discussion points, viewpoints raised, alternatives considered, constraints or factors discussed, conclusions or next steps (only if explicitly stated).
        3. DECISIONS: A list of decisions that were made during the meeting. Extract only confirmed decisions (i.e., items where a clear conclusion or consensus is stated). For each decision, include:
        -description: what was decided
        -decided_by: who made or announced the decision (use "Not identified" if unclear)
        4. ACTION_ITEMS: A list of tasks or follow-ups. For each, include:
        -description: what needs to be done
        -owner: responsible team or team lead (use "Not identified" if unclear)
        -deadline: when it is due (use "Not specified" if not mentioned)
        -priority: high, medium, or low (use "not specified" if not inferable)
        5. BLOCKERS: A list of blockers, risks, or open questions. For each, include:
        -description: what the issue is
        -type: "blocker" (things that are preventing progress), "risk" (things that could go wrong), or "open_question" (things that were raised but not resolved)
        -raised_by: who raised it (use "Not identified" if unclear)
        6. FOLLOWUP_EMAIL: A professional follow-up email summarizing the meeting, including key decisions, action items, and next steps

        IMPORTANT RULES:
        1. Only extract information that is explicitly present in the input. Do NOT invent or assume information.
        2. List every decision, action item, blocker which can be confidently inferred from the text.
        3. If something is unclear or ambiguous, mark it as such.
        4. If the input is too short or vague, say so in the summary and return empty lists for items you cannot identify.
        5. Return your response as valid JSON matching this exact schema:
        { "short_summary": "string", "detailed_summary": "string", "decisions": [ { "description": "string", 
        "decided_by": "string" } ], "action_items": [ { "description": "string", "owner": "string", "deadline": "string", 
        "priority": "string" } ], "blockers": [ { "description": "string", "type": "string", "raised_by": "string" } ], 
        "followup_email": "string" }
        6. Write in past tense and third person in a clear, neutral tone.

        MEETING CONTENT:
        %s
    '''% (text)

    # Returns the structured data AND the logging metadata
    results, metadata = await generate_json_with_gemini(prompt)
    
    required_keys = {"short_summary", "detailed_summary", "decisions", "action_items", "blockers", "followup_email"}
    if not required_keys.issubset(results.keys()):
        metadata["success"] = False
        metadata["completed_at"] = datetime.now(timezone.utc)
        metadata["error_details"] = "AI Response missing required JSON keys."
        raise PipelineError("Missing required keys for extraction.", metadata)
        
    return results, metadata