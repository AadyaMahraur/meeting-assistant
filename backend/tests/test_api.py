from fastapi.testclient import TestClient
from app.main import app  # Imports your actual FastAPI app

# Create a fake "client" to send requests to your app without needing a real server
client = TestClient(app)

def test_create_text_meeting_success():
    """Test 1: The 'Happy Path' where everything works perfectly."""
    
    # 1. Send the fake request
    response = client.post(
        "/api/meetings/text",
        json={
            "title": "Project Sync",
            "meeting_date": "2023-10-25",
            "text": "This is a completely valid, long enough meeting transcript."
        }
    )
    
    # 2. Check the results (Assert)
    assert response.status_code == 202
    
    data = response.json()
    assert "meeting_id" in data
    assert data["status"] == "pending"
    assert data["message"] == "Meeting submitted. Processing started."

def test_create_text_meeting_empty_text():
    """Test 2: Verifies your custom 400 error for empty strings."""
    
    response = client.post(
        "/api/meetings/text",
        json={
            "title": "Empty Sync",
            "meeting_date": "2023-10-25",
            "text": "     "  # Just spaces
        }
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Empty Text"

def test_create_text_meeting_short_text():
    """Test 3: Verifies Pydantic catches strings under 20 characters (422 Error)."""
    
    response = client.post(
        "/api/meetings/text",
        json={
            "title": "Short Sync",
            "meeting_date": "2023-10-25",
            "text": "Too short."  # Only 10 characters
        }
    )
    
    assert response.status_code == 422
    # Pydantic 422 errors return a list of "detail" dictionaries
    assert "detail" in response.json()