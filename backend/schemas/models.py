from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime


class ChatRequest(BaseModel):
    message: str
    history: List[dict] = Field(default_factory=list)

class BioGenerateRequest(BaseModel):
    name: str
    role: str
    tagline: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    experience: List[str] = Field(default_factory=list)
    education: Optional[str] = None
    tone: str = "professional"


class BioResponse(BaseModel):
    success: bool
    bio: str
    word_count: int
    quality_score: int
    issues: List[str]
    generated_at: datetime = Field(
        default_factory=datetime.utcnow
    )


class ProjectDescRequest(BaseModel):
    title: str
    category: str = "AI/Python"
    tech_stack: List[str]
    key_features: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    challenge: Optional[str] = None


class ProjectDescResponse(BaseModel):
    success: bool
    description: str
    word_count: int
    quality_score: int
    issues: List[str]
    generated_at: datetime = Field(
        default_factory=datetime.utcnow
    )


class OptimizationRequest(BaseModel):
    name: str
    role: str
    skills: List[str]
    projects_count: int
    bio: Optional[str] = None
    experience_count: Optional[int] = 0


class OptimizationResponse(BaseModel):
    success: bool
    tips: List[str]
    overall_score: int
    generated_at: datetime = Field(
        default_factory=datetime.utcnow
    )