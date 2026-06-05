from datetime import datetime
from loguru import logger
from schemas.models import ProjectDescRequest, ProjectDescResponse
from services.ai_service import generate_content
from services.prompts import PROJECT_SYSTEM_PROMPT
from services.quality_check import quality_check


def generate_project_description(
    request: ProjectDescRequest
) -> ProjectDescResponse:

    logger.info(
        f"Project description generation "
        f"started for: {request.title}"
    )

    user_prompt = f"""
Write a compelling professional project description
for a developer portfolio.

Project Title: {request.title}
Category: {request.category}
Tech Stack: {', '.join(request.tech_stack)}
Key Features: {', '.join(request.key_features) if request.key_features else 'Not specified'}
Achievements: {', '.join(request.achievements) if request.achievements else 'Not specified'}
Challenge: {request.challenge or 'Not specified'}

Instructions:
- Length: 120 to 180 words
- Start with a strong engaging hook
- Explain technical solution clearly
- Highlight impact and results
- Sound professional and impressive
- Return ONLY the description text
"""

    generated_desc = generate_content(
        system_prompt=PROJECT_SYSTEM_PROMPT,
        user_prompt=user_prompt.strip(),
        max_tokens=400,
        temperature=0.72
    )

    quality = quality_check(
        generated_desc,
        content_type="project"
    )

    logger.info(
        f"Description generated for {request.title} "
        f"| Score: {quality['quality_score']}/100"
    )

    return ProjectDescResponse(
        success=True,
        description=generated_desc,
        word_count=quality["word_count"],
        quality_score=quality["quality_score"],
        issues=quality["issues"],
        generated_at=datetime.utcnow()
    )