from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import GeneratedContent, Review, User, SessionLocal
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
    Helper function to format generated content with user and review details.
    """
    return {
        "id": entry.id,
        "prompt_id": entry.prompt_id,
        "content_text": entry.content_text,
        "generated_at": entry.generated_at,
        "user": {
            "user_id": entry.user.id,
            "username": entry.user.username,
            "email": entry.user.email
        } if entry.user else None,
        "reviews": [  # Now correctly handles multiple reviews
            {
                "id": review.id,
                "updated_content": review.updated_content,
                "comment": review.comment,
                "reviewed_at": review.reviewed_at,
                "reviewer": {
                    "reviewer_id": review.reviewer.id,
                    "reviewer_username": review.reviewer.username,
                    "reviewer_email": review.reviewer.email
                } if review.reviewer else None
            }
            for review in entry.reviews  # Iterate over multiple reviews
        ]
    }

@router.get("/generated_content/", response_model=list[dict])
async def get_generated_content(db: Session = Depends(get_db)):
    """
    Fetch all generated content along with their related user and review info.
    """
    content_entries = db.query(GeneratedContent).all()
    return [format_generated_content(entry) for entry in content_entries]

@router.get("/generated_content/{content_id}", response_model=dict)
async def get_generated_content_by_id(content_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single generated content entry by ID, including its user and review details.
    """
    content = db.query(GeneratedContent).filter(GeneratedContent.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Generated content not found")
    
    return format_generated_content(content)
