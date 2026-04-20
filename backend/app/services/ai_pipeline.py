import os, json
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# env_path = Path(__file__).resolve().parent.parent / 'backend' / '.env'
load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


def process_meeting_text(text: str) -> dict:
    prompt = '''
        You are an expert meeting analyst. Your job is to extract
        structured information from meeting notes or transcripts.
        Analyze the following meeting content and extract:
        1. SHORT_SUMMARY: A concise summary in 3-5 sentences.
        2. DETAILED_SUMMARY: A detailed summary in 1-3 paragraphs.
        3. DECISIONS: A list of decisions that were made during the meeting. For each decision, include:
        -description: what was decided
        -decided_by: who made or announced the decision (use "Not identified" if unclear)
        4. ACTION_ITEMS: A list of tasks or action items. For each, include:
        -description: what needs to be done
        -owner: who is responsible (use "Not identified" if unclear)
        -deadline: when it is due (use "Not specified" if not mentioned)
        -priority: high, medium, or low (use "not specified" if not inferable)
        5. BLOCKERS: A list of blockers, risks, or open questions. For each, include:
        -description: what the issue is
        -type: "blocker", "risk", or "open_question"
        -raised_by: who raised it (use "Not identified" if unclear)
        6. FOLLOWUP_EMAIL: A professional follow-up email summarizing the meeting, including key 
        decisions, action items, and next steps

        IMPORTANT RULES:
        1. Only extract information that is explicitly present in the input. Do NOT invent or assume information.
        2. If something is unclear or ambiguous, mark it as such.
        3. If the input is too short or vague, say so in the summary and return empty lists for items you cannot identify.
        4. Return your response as valid JSON matching this exact schema:
        { "short_summary": "string", "detailed_summary": "string", "decisions": [ { "description": "string", 
        "decided_by": "string" } ], "action_items": [ { "description": "string", "owner": "string", "deadline": "string", 
        "priority": "string" } ], "blockers": [ { "description": "string", "type": "string", "raised_by": "string" } ], 
        "followup_email": "string" }

        MEETING CONTENT:
        %s
    '''% (text)

    try: 
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1
            )
        )
        print(response)
        json_text = response.text.replace("```json", "").replace("```", "").strip()
        results = json.loads(json_text)
        print(results)
        required_keys = {"short_summary", "detailed_summary", "decisions", "action_items", "blockers", "followup_email"}
        if not required_keys.issubset(results.keys()):
            raise ValueError("AI Response missing required JSON keys")
        return results
    except json.JSONDecodeError:
        print("Failed to parse AI response as JSON")
        raise
    except Exception as e:
        print("AI Pipeline error at: {}".format(e))
        raise