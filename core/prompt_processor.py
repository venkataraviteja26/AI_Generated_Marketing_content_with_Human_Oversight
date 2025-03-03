import re
import logging

logger = logging.getLogger("prompt_processor")

def process_prompt(prompt: str) -> str:
    """
    Processing the prompt to ensure it meets formatting and security standards.
    
    This function performs basic sanitization by:
    - Trimming leading and trailing whitespace.
    - Replacing multiple whitespace characters with a single space.
    
    
    Args:
        prompt (str): The original prompt submitted by the user.
    
    Returns:
        str: The sanitized prompt.
    """
    try:
        # Remove leading/trailing whitespace
        cleaned_prompt = prompt.strip()
        # Replace multiple whitespace with a single space
        cleaned_prompt = re.sub(r'\s+', ' ', cleaned_prompt)
        logger.info("Prompt processed successfully.")
        return cleaned_prompt
    except Exception as e:
        logger.error(f"Error processing prompt: {e}")
        raise e
