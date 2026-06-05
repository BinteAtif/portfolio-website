import os
from groq import Groq
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# Single Groq client for all AI features
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_content(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 600,
    temperature: float = 0.7
) -> str:

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logger.error(f"Groq API Error: {e}")
        raise Exception(f"Failed to generate content: {str(e)}")