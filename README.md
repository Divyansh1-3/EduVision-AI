# EduVision AI

EduVision AI is a multimodal study assistant built for a hackathon to help students learn through visual explanations, high-yield revision notes, and active-recall quizzes.

> **Status:** Step 1 complete — Project folder structure and minimal runnable skeleton.

---

## Tech Stack
- **Frontend:** React + Vite + JavaScript
- **Backend:** Python + FastAPI + Uvicorn
- **AI (Future Step):** Gemma 4 via official `google-genai` Python SDK
- **Database (Future Step):** MongoDB (handled by teammate)

---

## Project Structure

```text
EduVision-AI/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx          # EduVision AI branding and subtitle
│   │   │   ├── ModeSelector.jsx    # Study modes (Explain, Revision Notes, Quiz)
│   │   │   ├── QuestionForm.jsx    # Text input and image selection placeholder
│   │   │   └── ResponsePanel.jsx   # Visual response container placeholder
│   │   ├── App.jsx                 # Main application layout and UI state
│   │   ├── main.jsx                # React DOM root entrypoint
│   │   └── styles.css              # Glassmorphic dark theme stylesheet
│   ├── index.html                  # HTML5 template
│   ├── package.json                # Frontend dependencies and npm scripts
│   └── vite.config.js              # Vite server & React plugin configuration
├── backend/
│   ├── app/
│   │   ├── __init__.py             # Backend package marker
│   │   ├── main.py                 # FastAPI application and CORS setup
│   │   ├── schemas.py              # Pydantic models (health check & placeholders)
│   │   ├── routes/
│   │   │   ├── __init__.py         # Routes package marker
│   │   │   └── health.py           # GET /api/health endpoint
│   │   └── services/
│   │       ├── __init__.py         # Services package marker
│   │       ├── gemma_service.py    # Gemma AI service placeholder (google-genai)
│   │       └── history_service.py  # Session history placeholder (MongoDB)
│   ├── requirements.txt            # Minimal backend Python dependencies
│   └── .env.example                # Template for environment variables
├── .gitignore                      # Ignore patterns for node_modules, venv, caches, secrets
└── README.md                       # Project documentation and setup guide
```

---

## Getting Started on Windows PowerShell

### 1. Backend Setup & Run

Open a Windows PowerShell terminal in the repository root:

```powershell
# Navigate to the backend directory
cd backend

# Create a Python virtual environment
python -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Install minimal backend dependencies (FastAPI + Uvicorn)
pip install -r requirements.txt

# Run the FastAPI development server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Verify backend health in browser or PowerShell:
- Health Endpoint: `http://127.0.0.1:8000/api/health`
- Swagger Documentation: `http://127.0.0.1:8000/docs`

---

### 2. Frontend Setup & Run

Open a **separate** Windows PowerShell terminal:

```powershell
# Navigate to the frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
```

Open your browser at:
- Web App: `http://localhost:5173`

---

## Upcoming Implementation Steps
1. **Multimodal AI Integration:** Hook up Gemma 4 using the `google-genai` Python SDK in `gemma_service.py`.
2. **Database Integration:** Connect MongoDB in `history_service.py` to persist sessions, notes, and quiz history.
3. **Full Multimodal Pipeline:** Support direct image upload and analysis for diagrams, textbook pages, and study sheets.
