import asyncio
import logging
import requests
import sys
import os
import json
from sqlalchemy.orm import Session
from config import config
from db import SessionLocal
from db import GeneratedContent, Prompt

logger = logging.getLogger("content_generator")
api_key = config["development"].API_KEY

async def generate_content(prompt_text: str) -> str:
    """
    Generate marketing content based on the given prompt using AI.
    The generated content is stored in the database.
    
    Args:
        prompt_text (str): The input prompt for generating content.
    
    Returns:
        str: The AI-generated marketing content.
    """
    session = SessionLocal()  # Create a new database session

    try:
        # Ensure the prompt exists in the database
        prompt = session.query(Prompt).filter_by(prompt_text=prompt_text).first()
        if not prompt:
            prompt = Prompt(prompt_text=prompt_text)
            session.add(prompt)
            session.commit()  # Commit to get prompt.id

        # Simulate network/API delay
        await asyncio.sleep(1)

        # Call the LLM API to generate content
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",  
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "cognitivecomputations/dolphin3.0-r1-mistral-24b:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt_text
                    }
                ],
            })
        )

        # Check if the API call was successful
        if response.status_code == 200:
            response_data = response.json()
            generated_text = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")

            # Store the generated content in the database
            generated_content = GeneratedContent(
                prompt_id=prompt.id,
                content_text=generated_text
            )
            session.add(generated_content)
            session.commit()

            logger.info(f"Generated content stored with ID: {generated_content.id}")
            return generated_text
        else:
            logger.error(f"API call failed with status code {response.status_code}: {response.text}")
            return f"Failed to generate content: {response.text}"

    except Exception as e:
        logger.error(f"Content generation error: {e}")
        session.rollback()
        raise e

    finally:
        session.close()  # Close the database session

# Example usage for testing
if __name__ == "__main__":
    test_prompt = "What is the purpose of life?"
    generated_content = asyncio.run(generate_content(test_prompt))
    print(f"Generated Content: {generated_content}")
