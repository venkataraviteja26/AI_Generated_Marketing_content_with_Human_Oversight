import asyncio
from datetime import datetime
import logging
from db import GeneratedContent, Review, SessionLocal, Prompt, init_db, User

logger = logging.getLogger("review_manager")

def _process_review(content_id: int, updated_content: str, comment: str, reviewer_username: str, reviewer_email: str):
    """
    Synchronously process the review: verify the generated content exists,
    create a review entry (creating reviewer if necessary), and return review details.
    """
    session = SessionLocal()
    try:
        # Check if the generated content exists
        generated = session.query(GeneratedContent).filter(GeneratedContent.id == content_id).first()
        if not generated:
            raise ValueError("Generated content not found")

        # Ensure reviewer exists; create if not
        reviewer = session.query(User).filter(User.email == reviewer_email).first()
        if not reviewer:
            reviewer = User(username=reviewer_username, email=reviewer_email)
            session.add(reviewer)
            session.commit()
            session.refresh(reviewer)
            print(f"Created new reviewer: {reviewer.username} (ID: {reviewer.id})")

        # Create and append a new review
        review = Review(
            content_id=content_id,
            reviewer_id=reviewer.id,  # Associate with the reviewer
            updated_content=updated_content,
            comment=comment
        )
        session.add(review)
        session.commit()
        session.refresh(review)

        # Append review to the generated content's review list
        generated.reviews.append(review)
        session.commit()

        result = {
            "review_id": review.id,
            "content_id": content_id,
            "reviewer_id": reviewer.id,
            "reviewer_username": reviewer.username,
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

async def process_review(content_id: int, updated_content: str, comment: str, reviewer_username: str, reviewer_email: str):
    """
    Asynchronously process a review submission, ensuring reviewer existence and handling database operations.
    """
    return await asyncio.to_thread(_process_review, content_id, updated_content, comment, reviewer_username, reviewer_email)


if __name__ == "__main__":
    # Initialize the test database
    # init_db()

    session = SessionLocal()
    try:
        # Insert a dummy user (content creator)
        user = User(username="test3_user", email="test3_user@example.com")
        session.add(user)
        session.commit()

        # Insert a dummy reviewer user
        reviewer1 = User(username="reviewer1_user", email="reviewer1_user@example.com")
        reviewer2 = User(username="reviewer2_user", email="reviewer2_user@example.com")
        session.add_all([reviewer1, reviewer2])
        session.commit()

        # Insert a dummy prompt
        prompt = Prompt(prompt_text="What is the meaning of life?")
        session.add(prompt)
        session.commit()

        # Insert dummy generated content with user_id
        generated_content = GeneratedContent(
            prompt_id=prompt.id,
            user_id=user.id,  # Associate with the dummy user
            content_text="The meaning of life is subjective and varies by individual."
        )
        session.add(generated_content)
        session.commit()

        print(f"Inserted test user (ID: {user.id}), reviewers (ID: {reviewer1.id}, {reviewer2.id}), prompt (ID: {prompt.id}), and content (ID: {generated_content.id})")

        # Call the async function to add multiple reviews for the generated content
        updated_text1 = "Life has different meanings for everyone."
        comment1 = "This is a well-written response but could be more philosophical."
        review_result1 = asyncio.run(process_review(generated_content.id, updated_text1, comment1, reviewer1.username, reviewer1.email))

        updated_text2 = "Life's meaning is a complex philosophical question."
        comment2 = "Consider adding perspectives from various philosophies."
        review_result2 = asyncio.run(process_review(generated_content.id, updated_text2, comment2, reviewer2.username, reviewer2.email))

        # Display results
        print("Reviews created successfully:")
        print(review_result1)
        print(review_result2)

        # Verify multiple reviews are linked to the generated content
        stored_reviews = session.query(Review).filter(Review.content_id == generated_content.id).all()
        print(f"Total reviews for content ID {generated_content.id}: {len(stored_reviews)}")

        # Cleanup
        session.query(Review).delete()
        session.commit()
        session.query(GeneratedContent).delete()
        session.commit()
        session.query(Prompt).delete()
        session.commit()
        session.query(User).delete()
        session.commit()

    finally:
        session.close()
