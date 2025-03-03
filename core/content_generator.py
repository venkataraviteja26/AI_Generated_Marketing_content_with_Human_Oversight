import asyncio
import logging
import requests
import sys
import os
import json
from config import config


logger = logging.getLogger("content_generator")
api_key = config["development"].API_KEY

async def generate_content(prompt: str) -> str:
    """
    Generate marketing content based on the given prompt using AI.
    This function simulates an asynchronous call to an AI content generation service.
    
    Args:
        prompt (str): The input prompt for generating content.
    
    Returns:
        str: The AI-generated marketing content.
    """
    try:
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
                        "content": prompt
                    }
                ],
            })
        )

        # Check if the API call was successful
        if response.status_code == 200:
            response_data = response.json()
            generated_content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return generated_content
        else:
            logger.error(f"API call failed with status code {response.status_code}: {response.text}")
            return f"Failed to generate content: {response.text}"

    except Exception as e:
        logger.error(f"Content generation error: {e}")
        raise e

# Example usage
# if __name__ == "__main__":
#     prompt = "What is the meaning of life?"
#     content = asyncio.run(generate_content(prompt))
#     print(content)
