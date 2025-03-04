from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import logging
from core import process_review

router = APIRouter()
logger = logging.getLogger("reviews_api")

class ReviewSubmission(BaseModel):
    content_id: int
    updated_content: str
    comment: str = None
    reviewer_username: str
    reviewer_email: str

class ReviewResponse(BaseModel):
    review_id: int
    content_id: int
    reviewer_id: int
    reviewer_username: str
    updated_content: str
    comment: str = None
    reviewed_at: datetime

@router.post("/", response_model=ReviewResponse)
async def submit_review(review: ReviewSubmission):
    """
    Submit a review for generated content.
    This endpoint processes the updated content and an optional comment.
    """
    try:
        # Process the review via core logic
        result = await process_review(
            review.content_id, 
            review.updated_content, 
            review.comment, 
            review.reviewer_username, 
            review.reviewer_email
        )

        return ReviewResponse(
            review_id=result["review_id"],
            content_id=result["content_id"],
            reviewer_id=result["reviewer_id"],
            reviewer_username=result["reviewer_username"],
            updated_content=result["updated_content"],
            comment=result["comment"],
            reviewed_at=result["reviewed_at"]
        )
    except Exception as e:
        logger.error(f"Error processing review: {e}")
        raise HTTPException(status_code=500, detail="Error processing review")
