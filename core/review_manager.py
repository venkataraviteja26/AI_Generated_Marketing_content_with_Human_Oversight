import asyncio
from datetime import datetime
import logging
from db import GeneratedContent, Review, SessionLocal, Prompt, init_db

logger = logging.getLogger("review_manager")

def _process_review(content_id: int, updated_content: str, comment: str):
    """
    Synchronously process the review: verify the generated content exists,
    create a review entry, and return a dictionary with the review details.
    """
    session = SessionLocal()
    try:
        # Check if the generated content exists
        generated = session.query(GeneratedContent).filter(GeneratedContent.id == content_id).first()
        if not generated:
            raise ValueError("Generated content not found")
        
        # Create the review record
        review = Review(content_id=content_id, updated_content=updated_content, comment=comment)
        session.add(review)
        session.commit()
        session.refresh(review)
        
        result = {
            "review_id": review.id,
            "content_id": content_id,
            "updated_content": review.updated_content,
            "comment": review.comment,
            "reviewed_at": review.reviewed_at
        }
        return result
    except Exception as e:
        session.rollback()
        logger.error(f"Error processing review: {e}")
        raise e
    finally:
        session.close()

async def process_review(content_id: int, updated_content: str, comment: str):
    """
    Asynchronously process a review submission by wrapping synchronous
    database operations in a thread.
    """
    return await asyncio.to_thread(_process_review, content_id, updated_content, comment)


# # Example usage
# if __name__ == "__main__":
#     # Initialize the test database
#     init_db()

#     session = SessionLocal()
#     try:
#         # Insert a dummy prompt
#         prompt = Prompt(prompt_text="What is the meaning of life?")
#         session.add(prompt)
#         session.commit()

#         # Insert dummy generated content
#         generated_content = GeneratedContent(
#             prompt_id=prompt.id,
#             content_text="The meaning of life is subjective and varies by individual."
#         )
#         print("debug", generated_content.__dict__)
#         session.add(generated_content)
#         session.commit()

#         print(f"Inserted test prompt (ID: {prompt.id}) and content (ID: {generated_content.id})")

#         # Call the async function to review the generated content
#         updated_text = "Life has different meanings for everyone."
#         comment = "This is a well-written response but could be more philosophical."

#         review_result = asyncio.run(process_review(generated_content.id, updated_text, comment))

#         # Display results
#         print("Review created successfully:")
#         print(review_result)
#         session.query(GeneratedContent).delete()
#         session.commit()
#         session.query(Prompt).delete()
#         session.commit()

#     finally:
#         session.close()
