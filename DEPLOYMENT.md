# Deployment Guide

## Quick Start (Local)

1. **Activate venv and install dependencies:**
```powershell
cd "c:\Users\Prateek Batra\Downloads\paraphraser"
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. **Set OpenAI key (optional, enables AI features):**
```powershell
# Create .env file
notepad .env
# Add: OPENAI_API_KEY=sk-...
```

3. **Run the app:**
```powershell
uvicorn fastapi_study_buddy.main:app --reload --host 0.0.0.0 --port 8000
```
Open http://localhost:8000

4. **Run tests:**
```powershell
pytest -v
```

---

## Deploy to Railway

1. **Prepare repo for GitHub:**
   - Create `.gitignore` at project root:
   ```
   .env
   .venv
   __pycache__
   *.pyc
   *.db
   conversations.db
   ```
   - Push to GitHub: `git init`, `git add .`, `git commit -m "initial"`, `git push origin main`

2. **Create Railway project:**
   - Go to https://railway.app/dashboard
   - Click "New Project" → "Deploy from GitHub"
   - Select your repo

3. **Configure environment:**
   - In Railway dashboard, go to Variables
   - Add: `OPENAI_API_KEY` = your-api-key (do NOT commit this)
   - Build command: (leave as auto-detect or set `pip install -r requirements.txt`)
   - Start command: `uvicorn fastapi_study_buddy.main:app --host 0.0.0.0 --port $PORT`

4. **Deploy:**
   - Railway auto-deploys on git push. Monitor logs in the dashboard.
   - URL will be shown as `https://<your-railway-url>.app`

---

## Deploy to Render

1. **Prepare repo (same as Railway step 1)**

2. **Create Render service:**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repo

3. **Configure:**
   - Name: `study-buddy`
   - Region: choose closest
   - Runtime: `python 3.11`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn fastapi_study_buddy.main:app --host 0.0.0.0 --port $PORT`
   - Environment variables: add `OPENAI_API_KEY`

4. **Deploy:**
   - Render auto-deploys. Your URL: `https://<your-service>.onrender.com`

---

## Notes
- Conversations are persisted in SQLite (`conversations.db`). On Railway/Render, data is ephemeral unless you add a persistent volume.
- For production, consider adding a PostgreSQL database on Railway/Render instead of SQLite.
- Always set API keys in the deployment platform's environment settings, never in code.
