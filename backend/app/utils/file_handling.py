from pathlib import Path
from fastapi import HTTPException
import os, io
from dotenv import load_dotenv
from docx import Document
import langdetect

load_dotenv()

def validate_file(file) -> bool:
    allowed_file_types = {".txt", ".md", ".docx"}
    filetype = Path(file.filename).suffix.lower()

    if filetype not in allowed_file_types:
        raise HTTPException(status_code=400, detail="Unsupported File Type")
    
    file_size = file.size
    max_limit = int(os.getenv('MAX_FILE_SIZE', 5242880)) # Added fallback

    if file_size > max_limit:
        raise HTTPException(status_code=413, detail="File Too Large")
    
    return True

def check_filler_words(text: str) -> bool:
    words = text.split()
    
    # Count words that are longer than 5 characters 
    substantive_words = [w for w in words if len(w) > 5]
    
    if len(substantive_words) < (len(words) * 0.10):
        return True
        
    return False

def validate_text_content(text: str) -> tuple[str, int]:
    """Universal validation for both raw text and file uploads."""
    clean_text = text.strip()
    
    if not clean_text:
        raise HTTPException(status_code=400, detail="Empty text or no readable text found.")

    word_count = len(clean_text.split())

    if word_count < 50:
        raise HTTPException(status_code=400, detail="Input too short. Please provide at least 50 words.")
    if word_count > 10000:
        raise HTTPException(status_code=400, detail="Input too long. Max limit is 10,000 words.")

    try:
        if langdetect.detect(clean_text) != 'en':
            raise HTTPException(status_code=400, detail="Only English text is supported.")
    except:
        raise HTTPException(status_code=400, detail="Could not determine language.")
 
    if check_filler_words(clean_text):
        raise HTTPException(status_code=400, detail="Only conversational filler words present. Lacks substance.")
        
    return clean_text, word_count

def extract_text_from_file(file) -> tuple[str, int]:
    extension = Path(file.filename).suffix.lower()
    text = ""
    
    try:
        content = file.file.read()
        if extension in [".txt", ".md"]:
            text = content.decode("utf-8")
        elif extension == ".docx":
            doc = Document(io.BytesIO(content))
            text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise HTTPException(status_code=400, detail="Corrupted file")    
    finally:
        file.file.seek(0)
    
    # Run the extracted text through the universal validator
    validated_text, word_count = validate_text_content(text)
    
    return validated_text, word_count    