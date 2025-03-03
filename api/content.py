from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

from core import generate_content

router = APIRouter()
logger = logging.getLogger("content_api")

class ContentRequest(BaseModel):
    prompt: str
    user_name: str
    user_email: str

class ContentResponse(BaseModel):
    content: str

@router.post("/generate", response_model=ContentResponse)
async def generate_marketing_content(request: ContentRequest):
    """
    Generate marketing content using AI based on the provided prompt.
    The generated content is logged along with the original prompt.
    """
    try:
        # Call the content generator service (assumed to be async)
        result = await generate_content(request.prompt, request.user_name, request.user_email)
        # Log the prompt and the generated content
        logger.info(f"Prompt: {request.prompt}")
        logger.info(f"User Name: {request.user_name}")
        logger.info(f"User email: {request.user_email}")
        logger.info(f"Generated Content: {result}")
        return ContentResponse(content=result)
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        raise HTTPException(status_code=500, detail="Error generating content")
