from pathlib import Path
from fastapi import HTTPException
import os, io
from dotenv import load_dotenv
from docx import Document

load_dotenv()


def validate_file(file) -> bool:
    allowed_file_types = {".txt", ".md", ".docx"}
    filetype = Path(file.filename).suffix.lower()

    if filetype not in allowed_file_types:
        raise HTTPException(status_code=400, detail="Unsupported File Type")
    

    file_size = file.size

    max_limit = int(os.getenv('MAX_FILE_SIZE'))

    if file_size > max_limit:
        raise HTTPException(status_code=413, detail="File Too Large")
    

    return True


def extract_text_from_file(file) -> str:
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
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="No readable text")
        
    return text

    
    