# AI Portfolio – Complete Setup & Deployment Guide

**Team Members**  
- Saqib Javaid – React Developer  
- Muhammad Umer – Full Stack Developer  
- Aasiyah Syed – AI Developer  

This document covers everything from installing prerequisites to deploying your AI-powered portfolio on Render (backend) and Vercel (frontend). Follow the steps in order.

---

## Table of Contents

1. [Prerequisites (Accounts & Tools)](#1-prerequisites-accounts--tools)
2. [Getting Groq API Key](#2-getting-groq-api-key)
3. [Changing Portfolio Data (Your Name, Skills, Projects)](#3-changing-portfolio-data-your-name-skills-projects)
4. [Future Updates Without Coding (via GitHub)](#4-future-updates-without-coding-via-github)
5. [Local Installation & Testing (Frontend + Backend)](#5-local-installation--testing-frontend--backend)
6. [Testing the AI Chatbot](#6-testing-the-ai-chatbot)
7. [Environment Variables Explained (Frontend & Backend)](#7-environment-variables-explained-frontend--backend)
8. [Deploy Backend on Render (Free)](#8-deploy-backend-on-render-free)
9. [Deploy Frontend on Vercel (Free)](#9-deploy-frontend-on-vercel-free)
10. [Final Testing After Deployment](#10-final-testing-after-deployment)
11. [Troubleshooting Common Issues](#11-troubleshooting-common-issues)

---

## 1. Prerequisites (Accounts & Tools)

Each team member must have the following installed on their laptop:

- **Node.js** (v18 or higher) – [Download](https://nodejs.org/)
- **Python** (3.10 or higher) – [Download](https://python.org/)
- **Git** – [Download](https://git-scm.com/)
- **GitHub Account** (free) – [Sign up](https://github.com/)
- **Vercel Account** (free, login with GitHub) – [vercel.com](https://vercel.com)
- **Render Account** (free, login with GitHub) – [render.com](https://render.com)
- **Groq Account** (free, sign up with email) – [console.groq.com](https://console.groq.com)

> **Note:** You will need **two terminal windows** to run backend and frontend simultaneously.

---

## 2. Getting Groq API Key (Required for AI Chatbot)

1. Go to [Groq Console](https://console.groq.com) and **Sign Up** (Google or email).
2. After login, go to **API Keys** menu.
3. Click **Create API Key**, give it a name (e.g., `portfolio-ai`).
4. **Copy the key** (it will be shown only once).
5. Inside your project folder, go to the `backend` folder and create a file named **`.env`** (exact name).
6. Write the following in that file (replace with your actual key):
   ```
   GROQ_API_KEY=your_copied_key_here
   ```
7. **Important:** Do NOT push this `.env` file to GitHub. We will add it to `.gitignore`.

---

## 3. Changing Portfolio Data (Your Name, Skills, Projects)

All portfolio content is stored in `backend/data/portfolio_data.py`. Open this file and replace the example data with your own.

### Example structure of `portfolio_data.py`

```python
portfolio_data = {
    "name": "Saqib Javaid",
    "title": "React Developer",
    "bio": "I am a frontend specialist with 2 years of experience...",
    "skills": ["React", "Tailwind CSS", "JavaScript", "Vite"],
    "projects": [
        {
            "name": "AI Chatbot Portfolio",
            "description": "A full-stack portfolio with LLM integration...",
            "technologies": ["React", "FastAPI", "Groq"],
            "link": "https://github.com/..."
        },
        # Add more projects here
    ],
    "contact": {
        "email": "saqib@example.com",
        "github": "https://github.com/saqib",
        "linkedin": "https://linkedin.com/in/saqib"
    }
}

etc.
```

### How to change each field:

- **name** – your full name  
- **title** – your role (e.g., React Developer, Full Stack Developer, AI Developer)  
- **bio** – 2–3 lines about yourself  
- **skills** – list of your skills (comma separated inside brackets)  
- **projects** – copy the `{ }` block for each new project and fill in `name`, `description`, `technologies`, `link`  
- **contact** – your real email, GitHub, and LinkedIn URLs  

Save the file. Now when you run the project locally, your data will appear.

---

## 4. Future Updates Without Coding (via GitHub)

If you want to add a new project or skill later **without writing code**, follow this method:

1. Go to your **GitHub repository**.
2. Navigate to `backend/data/portfolio_data.py`.
3. Click the **Edit button** (pencil icon).
4. Make your changes directly (e.g., add a new project block).
5. Scroll down, write a commit message like `"added new project"`.
6. Click **Commit changes**.
7. After committing, **Render** and **Vercel** will automatically redeploy (2–3 minutes). Your live portfolio will show the new data.

> This method requires **no coding knowledge** – only a GitHub account and a browser.

**Alternative easy method:** Use GitHub’s **Dev editor** – same process: open file, edit, commit.

---

## 5. Local Installation & Testing (Run on Your Laptop)

First, download the project (ZIP file or `git clone`).

### Step 5.1: Backend Setup (FastAPI + AI)

Open **Terminal #1**

```bash
cd backend
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make sure your .env file (with GROQ_API_KEY) exists in the backend folder

# Run backend server
python -m uvicorn main:app --reload --port 8000
```

If successful, you will see:  
`Uvicorn running on http://127.0.0.1:8000`

**Test:** Open `http://localhost:8000/docs` in your browser – Swagger UI should appear.

### Step 5.2: Frontend Setup (React + Vite)

Open **Terminal #2** (new window)

```bash
cd frontend
npm install
npm run dev
```

You will see: `Vite running on http://localhost:5173`

### Step 5.3: Run Both Together

- Backend is on port `8000`
- Frontend is on port `5173`
- Open `http://localhost:5173` in your browser – the portfolio should load.

> **Note:** The frontend is configured to call `http://localhost:8000` by default (see `frontend/src/services/chatApi.js`). If needed, create `frontend/.env` and add:  
> `VITE_API_URL=http://localhost:8000`

---

## 6. Testing the AI Chatbot (Every Team Member Should Do This)

**Goal:** Ask questions to the chatbot and verify that it answers correctly based on the portfolio data.

### Test Cases (copy and paste into the AI Chat widget)

| Test Question | Expected Answer |
|---------------|------------------|
| `"What is my name?"` | Should return the name from `portfolio_data.py` |
| `"List my skills"` | Should list the skills from the data |
| `"Tell me about my projects"` | Should show project names and descriptions |
| `"How can someone contact me?"` | Should show email and social links |
| `"Suggest a new project idea"` | AI should generate a creative suggestion |
| `"What technologies does this portfolio use?"` | Should mention React, FastAPI, Groq, etc. |

### Expected Behaviour

- The chatbot must answer based on the actual content of `portfolio_data.py`.
- If it gives wrong answers, check the system prompts in `backend/chatbot.py` or `backend/services/prompts.py` and adjust them.

### Testing Frontend–Backend Integration

- Type a message in the chat widget and press Enter.
- A typing indicator should appear.
- The bot response should come within 2–3 seconds.
- If an error occurs, open browser console (F12) – common issues are CORS or invalid API key.

---

## 7. Environment Variables Explained (Frontend & Backend)

### Backend `.env` (inside `backend/` folder)

- `GROQ_API_KEY` – your secret Groq key. **Never share it publicly**.
- On Render, you will set this same key as an environment variable.

### Frontend `.env` (inside `frontend/` folder – optional)

- `VITE_API_URL` – the URL of your backend.  
  - Local: `http://localhost:8000`  
  - Production: `https://your-backend.onrender.com`

> **Important for React/Vite:** All environment variables must start with `VITE_`.

### How it works in production

- Render gives your backend a URL like `https://ai-portfolio-backend.onrender.com`
- Vercel gives your frontend a URL like `https://ai-portfolio.vercel.app`
- The frontend needs to know the backend URL – so you set `VITE_API_URL` in Vercel’s environment variables.

---

## 8. Deploy Backend on Render (Free)

1. **Push your project to GitHub** (make sure `.env` is in `.gitignore` and not uploaded).
2. Log in to [Render.com](https://render.com) with GitHub.
3. On the dashboard, click **New +** → **Web Service**.
4. Connect your GitHub repository.
5. Fill in the settings:

| Field | Value |
|-------|-------|
| **Name** | `ai-portfolio-backend` (any name) |
| **Environment** | `Python` |
| **Build Command** | `pip install -r backend/requirements.txt` |
| **Start Command** | `cd backend && uvicorn main:app --host 0.0.0.0 --port 10000` |
| **Root Directory** | `backend` |

> **Alternative (cleaner):** Set Root Directory = `backend` and Start Command = `uvicorn main:app --host 0.0.0.0 --port 10000` (without `cd backend`).

6. In the **Environment Variables** section, add:
   - Key: `GROQ_API_KEY`  
     Value: (your actual Groq API key)
7. Select **Free tier**.
8. Click **Create Web Service**. Deployment will take 2–3 minutes.
9. Once status becomes `Live`, copy the URL (e.g., `https://ai-portfolio-backend.onrender.com`).

**Test backend:** Open `https://your-backend.onrender.com/docs` – Swagger UI should load.

---

## 9. Deploy Frontend on Vercel (Free)

1. Log in to [Vercel.com](https://vercel.com) with GitHub.
2. Click **Add New** → **Project**.
3. Select your GitHub repository.
4. Configure the project:

| Field | Value |
|-------|-------|
| **Framework Preset** | `Vite` |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |

5. In **Environment Variables**, add:
   - Key: `VITE_API_URL`  
     Value: `https://your-backend.onrender.com` (the URL from Render)
6. Click **Deploy**.
7. Within seconds, Vercel will give you a URL (e.g., `https://ai-portfolio.vercel.app`).

**Test frontend:** Open that URL – your portfolio should appear and the AI chatbot must work (connected to the backend).

> **Important:** If the chatbot doesn’t work, check that `VITE_API_URL` is correct. Open browser console (F12) to see any `Failed to fetch` errors.

---

## 10. Final Testing After Deployment

- Open the Vercel frontend URL.
- Ask the chatbot: `"What is my name?"` – it should answer correctly.
- Check that your name, skills, projects are displayed on the portfolio page.
- Test on mobile view – the design should be responsive.

If everything works → **Congratulations! Your team’s AI portfolio is live.**

---

## 11. Troubleshooting Common Issues

| Problem | Solution |
|---------|----------|
| Backend deploy fails (Module not found) | Check that `requirements.txt` contains all libraries. Ensure build command uses `backend/requirements.txt`. |
| Chatbot does not respond on live site | Open browser console (F12). If `Failed to fetch`, your `VITE_API_URL` is wrong. Update it in Vercel and redeploy. |
| Groq API key invalid | No extra spaces in the key. On Render, re-enter the exact key and redeploy. |
| CORS error | Backend `main.py` already has CORS middleware with `allow_origins=["*"]`. If missing, add it. |
| Frontend build fails | Run `npm run build` locally. If it fails, fix missing imports or syntax errors. |
| Portfolio data not updating after GitHub edit | Render and Vercel auto-deploy on push. Wait 2–3 minutes, then do a hard refresh (Ctrl+Shift+R). |

---
---
---
---

**Good luck! Your AI portfolio will be live and professional.**


