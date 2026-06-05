from datetime import datetime
from loguru import logger
from schemas.models import OptimizationRequest, OptimizationResponse
from services.ai_service import generate_content
from services.prompts import OPTIMIZATION_SYSTEM_PROMPT


def generate_optimization_tips(
    request: OptimizationRequest
) -> OptimizationResponse:

    logger.info(
        f"Optimization tips generation "
        f"started for: {request.name}"
    )

    user_prompt = f"""
Review this portfolio and provide optimization tips:

Name: {request.name}
Role: {request.role}
Total Projects: {request.projects_count}
Experience Entries: {request.experience_count or 0}
Skills Listed: {len(request.skills)}
Skills: {', '.join(request.skills)}
Bio Provided: {'Yes' if request.bio and len(request.bio) > 50 else 'No'}

Give 6 to 8 specific actionable tips to make
this portfolio stand out.

Focus on:
- Content quality and storytelling
- Technical depth
- Achievements with metrics
- Missing sections or improvements
- Overall impact and professionalism

Return as a clear numbered list.
"""

    tips_text = generate_content(
        system_prompt=OPTIMIZATION_SYSTEM_PROMPT,
        user_prompt=user_prompt.strip(),
        max_tokens=700,
        temperature=0.65
    )

    tips_list = [
        line.strip()
        for line in tips_text.split('\n')
        if line.strip() and len(line.strip()) > 10
    ]

    overall_score = min(
        98,
        35 +
        (request.projects_count * 10) +
        (len(request.skills) * 4)
    )

    logger.info(
        f"Optimization tips generated for {request.name} "
        f"| Score: {overall_score}/100"
    )

    return OptimizationResponse(
        success=True,
        tips=tips_list[:8],
        overall_score=overall_score,
        generated_at=datetime.utcnow()
    )