import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from dotenv import load_dotenv

from schemas.models import (
    ChatRequest,
    BioGenerateRequest,
    ProjectDescRequest,
    OptimizationRequest
)
from chatbot import get_response
from controllers.bio_controller import generate_bio
from controllers.project_controller import (
    generate_project_description
)
from controllers.optimization_controller import (
    generate_optimization_tips
)
from data.portfolio_data import portfolio_data

load_dotenv()

app = FastAPI(
    title="Portfolio AI System",
    description=(
        "Combined AI Portfolio System — "
        "Chatbot + Bio Generator + "
        "Project Description + Optimization Tips"
    ),
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://portfolio-website-up2p.vercel.app"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────
# Health Check
# ─────────────────────────────────
@app.get("/")
def home():
    return {
        "message": "Portfolio AI System is running!",
        "version": "3.0.0",
        "owner": portfolio_data["name"],
        "role": portfolio_data["role"],
        "ai_model": "Groq - LLaMA 3.1 8B",
        "developers": {
            "chatbot": "Rehman Ahmad",
            "content_generation": "Ayesha"
        },
        "endpoints": {
            "portfolio": "GET /portfolio",
            "chatbot": "POST /ai/chat",
            "skill_suggestions": "GET /ai/skill-suggestions",
            "generate_bio": "POST /ai/generate-bio",
            "generate_description": "POST /ai/generate-description",
            "portfolio_tips": "POST /ai/portfolio-tips"
        }
    }


# ─────────────────────────────────
# Portfolio Data
# ─────────────────────────────────
@app.get("/portfolio")
def get_portfolio():
    return {
        "status": "success",
        "data": portfolio_data
    }


# ─────────────────────────────────
# AI Chatbot — Stateless
# ─────────────────────────────────
@app.post("/ai/chat")
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    response = get_response(
        request.message,
        request.history
    )

    return {
        "status": "success",
        "user_message": request.message,
        "bot_response": response,
        "model": "Groq - LLaMA 3.1 8B"
    }


# ─────────────────────────────────
# Skill Suggestions
# ─────────────────────────────────
@app.get("/ai/skill-suggestions")
def skill_suggestions():

    current_skills = [
        skill["name"].lower()
        for skill in portfolio_data["skills"]
    ]

    project_tech = []
    for project in portfolio_data["projects"]:
        for tech in project["tech_stack"]:
            project_tech.append(tech.lower())

    suggestions = []

    if "python" in current_skills:
        if "docker" not in current_skills:
            suggestions.append({
                "skill": "Docker",
                "reason": (
                    "You use FastAPI — Docker will "
                    "help you deploy professionally"
                )
            })
        if "langchain" not in current_skills:
            suggestions.append({
                "skill": "LangChain",
                "reason": (
                    "As an AI developer, LangChain "
                    "will help you build advanced AI apps"
                )
            })

    if "machine learning" in current_skills:
        if "deep learning" not in current_skills:
            suggestions.append({
                "skill": "Deep Learning",
                "reason": (
                    "Natural next step after "
                    "Machine Learning"
                )
            })

    if "mongodb" in current_skills:
        if "redis" not in current_skills:
            suggestions.append({
                "skill": "Redis",
                "reason": (
                    "Redis caching will make "
                    "your APIs much faster"
                )
            })

    if "yolov8" in project_tech:
        if "opencv" not in current_skills:
            suggestions.append({
                "skill": "OpenCV",
                "reason": (
                    "You use YOLOv8 — OpenCV is "
                    "the natural companion"
                )
            })

    if not suggestions:
        suggestions.append({
            "skill": "System Design",
            "reason": (
                "Will help you build "
                "scalable AI systems"
            )
        })

    return {
        "status": "success",
        "owner": portfolio_data["name"],
        "current_skills": [
            s["name"] for s in portfolio_data["skills"]
        ],
        "suggestions": suggestions,
        "total_suggestions": len(suggestions)
    }


# ─────────────────────────────────
# Bio Generator
# ─────────────────────────────────
@app.post("/ai/generate-bio")
def bio_generator(request: BioGenerateRequest):
    try:
        result = generate_bio(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ─────────────────────────────────
# Project Description Generator
# ─────────────────────────────────
@app.post("/ai/generate-description")
def description_generator(request: ProjectDescRequest):
    try:
        result = generate_project_description(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ─────────────────────────────────
# Portfolio Optimization Tips
# ─────────────────────────────────
@app.post("/ai/portfolio-tips")
def optimization_tips(request: OptimizationRequest):
    try:
        result = generate_optimization_tips(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
