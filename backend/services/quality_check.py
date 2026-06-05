from loguru import logger
from services.ai_service import generate_content
from services.prompts import QUALITY_SYSTEM_PROMPT

# Generic words to avoid in portfolios
GENERIC_WORDS = {
    "passionate", "hardworking", "dedicated",
    "motivated", "innovative", "team player",
    "hard worker", "dynamic", "results-driven",
    "self-motivated", "go-getter", "synergistic"
}


def quality_check(text: str, content_type: str = "bio") -> dict:

    issues = []
    score = 100

    # Empty check
    if not text or len(text.strip()) < 50:
        issues.append("Content is too short or empty")
        score -= 40

    text_lower = text.lower()

    # Generic buzzwords check
    found_generic = [
        word for word in GENERIC_WORDS
        if word in text_lower
    ]
    for word in found_generic:
        issues.append(f"Contains generic buzzword: '{word}'")
        score -= 10

    # Length check
    word_count = len(text.split())

    if content_type == "bio":
        if word_count < 150:
            issues.append(
                "Bio is too short — should be 180 to 250 words"
            )
            score -= 20
        elif word_count > 320:
            issues.append("Bio is too long")
            score -= 10
    else:
        if word_count < 80:
            issues.append("Project description is too short")
            score -= 20

    # Metrics check
    if not any(char.isdigit() for char in text):
        issues.append(
            "Consider adding metrics with numbers"
        )
        score -= 10

    # Technical depth check
    tech_keywords = [
        "python", "fastapi", "machine learning",
        "react", "mongodb", "api", "groq",
        "docker", "ai", "ml", "yolo"
    ]
    if not any(word in text_lower for word in tech_keywords):
        issues.append(
            "Low technical depth — add specific technologies"
        )
        score -= 10

    # AI review
    try:
        ai_review = generate_content(
            system_prompt=QUALITY_SYSTEM_PROMPT,
            user_prompt=(
                f"Review this {content_type} "
                f"for a professional portfolio:\n\n{text}"
            ),
            max_tokens=150,
            temperature=0.5
        )

        if any(word in ai_review.lower()
               for word in ["improve", "add", "avoid", "missing"]):
            issues.append(f"AI Suggestion: {ai_review[:120]}")
            score -= 5

    except Exception:
        logger.warning("AI quality check skipped")
        ai_review = "Manual review recommended"

    return {
        "passed": max(0, score) >= 70,
        "quality_score": max(0, min(100, score)),
        "issues": issues,
        "word_count": word_count
    }