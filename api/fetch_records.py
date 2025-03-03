from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import SessionLocal
from db.models import GeneratedContent, Review
import logging

router = APIRouter()
logger = logging.getLogger("generated_content_api")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def format_generated_content(entry: GeneratedContent) -> dict:
    """
    Helper function to format generated content with review details.
    """
    return {
        "id": entry.id,
        "prompt_id": entry.prompt_id,
        "content_text": entry.content_text,
        "generated_at": entry.generated_at,
        "review": {
            "id": entry.review.id,
            "updated_content": entry.review.updated_content,
            "comment": entry.review.comment,
            "reviewed_at": entry.review.reviewed_at
        } if entry.review else None
    }

@router.get("/generated_content/", response_model=list[dict])
async def get_generated_content(db: Session = Depends(get_db)):
    """
    Fetch all generated content along with their related review info.
    """
    content_entries = db.query(GeneratedContent).all()
    return [format_generated_content(entry) for entry in content_entries]

@router.get("/generated_content/{content_id}", response_model=dict)
async def get_generated_content_by_id(content_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single generated content entry by ID, including its review (if available).
    """
    content = db.query(GeneratedContent).filter(GeneratedContent.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Generated content not found")
    
    return format_generated_content(content)
