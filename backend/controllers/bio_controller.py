from datetime import datetime
from loguru import logger
from schemas.models import BioGenerateRequest, BioResponse
from services.ai_service import generate_content
from services.prompts import BIO_SYSTEM_PROMPT
from services.quality_check import quality_check


def generate_bio(request: BioGenerateRequest) -> BioResponse:

    logger.info(
        f"Bio generation started for: "
        f"{request.name} ({request.role})"
    )

    user_prompt = f"""
Write a professional, engaging, and natural bio
for a portfolio website.

Full Name: {request.name}
Current Role: {request.role}
Tagline: {request.tagline or 'Not provided'}
Key Skills: {', '.join(request.skills) if request.skills else 'Not provided'}
Experience: {', '.join(request.experience) if request.experience else 'Not provided'}
Education: {request.education or 'Not provided'}
Tone: {request.tone}

Instructions:
- Write between 180 to 250 words
- Use confident, modern, and natural tone
- Highlight technical expertise
- Avoid generic buzzwords completely
- End with a forward-looking professional statement
- Return ONLY the bio text
"""

    generated_bio = generate_content(
        system_prompt=BIO_SYSTEM_PROMPT,
        user_prompt=user_prompt.strip(),
        max_tokens=500,
        temperature=0.68
    )

    quality = quality_check(generated_bio, content_type="bio")

    logger.info(
        f"Bio generated for {request.name} "
        f"| Score: {quality['quality_score']}/100"
    )

    return BioResponse(
        success=True,
        bio=generated_bio,
        word_count=quality["word_count"],
        quality_score=quality["quality_score"],
        issues=quality["issues"],
        generated_at=datetime.utcnow()
    )