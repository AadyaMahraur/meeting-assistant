import os, json, logging, asyncio
from datetime import datetime, timezone
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tenacity import retry, wait_exponential, stop_after_attempt

load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
logger = logging.getLogger(__name__)

# Custom error that carries our log data back to the database
class PipelineError(Exception):
    def __init__(self, message, metadata):
        super().__init__(message)
        self.metadata = metadata

# 1. Retry Logic: 1 initial attempt + 2 retries = 3 attempts total.
@retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3),
    reraise=True
)
async def _call_gemini_with_retry(prompt: str, model_name: str, config: types.GenerateContentConfig):
    # We use the async client (client.aio) so asyncio.wait_for can accurately track time
    return await client.aio.models.generate_content(
        model=model_name,
        contents=prompt,
        config=config
    )

async def generate_json_with_gemini(prompt: str) -> tuple[dict, dict]:
    model_name = "gemini-2.5-flash"
    
    # Initialize the log data
    metadata = {
        "started_at": datetime.now(timezone.utc),
        "model_used": model_name,
        "prompt_tokens": 0,
        "response_tokens": 0,
        "retry_count": 0,
        "success": False,
        "error_details": None,
        "completed_at": None
    }

    try:
        config = types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json"
        )

        # 2. Timeout Logic: 60 seconds maximum
        response = await asyncio.wait_for(
            _call_gemini_with_retry(prompt, model_name, config),
            timeout=60.0
        )

        # Extract Token Usage
        if response.usage_metadata:
            metadata["prompt_tokens"] = response.usage_metadata.prompt_token_count
            metadata["response_tokens"] = response.usage_metadata.candidates_token_count

        # Tenacity attempt_number starts at 1, so we subtract 1 for retry_count
        attempts = _call_gemini_with_retry.retry.statistics.get("attempt_number", 1)
        metadata["retry_count"] = attempts - 1

        json_text = response.text.replace("```json", "").replace("```", "").strip()
        results = json.loads(json_text)

        metadata["success"] = True
        metadata["completed_at"] = datetime.now(timezone.utc)
        return results, metadata

    except asyncio.TimeoutError:
        metadata["error_details"] = "Processing timed out (exceeded 60 seconds)."
        metadata["completed_at"] = datetime.now(timezone.utc)
        metadata["retry_count"] = _call_gemini_with_retry.retry.statistics.get("attempt_number", 1) - 1
        raise PipelineError(metadata["error_details"], metadata)

    except json.JSONDecodeError as e:
        metadata["error_details"] = f"Invalid JSON format returned: {str(e)}"
        metadata["completed_at"] = datetime.now(timezone.utc)
        metadata["retry_count"] = _call_gemini_with_retry.retry.statistics.get("attempt_number", 1) - 1
        raise PipelineError("The AI generated an invalid data format.", metadata)

    except Exception as e:
        metadata["error_details"] = str(e)
        metadata["completed_at"] = datetime.now(timezone.utc)
        metadata["retry_count"] = _call_gemini_with_retry.retry.statistics.get("attempt_number", 1) - 1
        raise PipelineError(f"AI Pipeline failed: {str(e)}", metadata)