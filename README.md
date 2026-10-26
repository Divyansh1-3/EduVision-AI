# EduVision AI

EduVision AI is an interactive, multimodal AI study companion developed for a hackathon. It empowers students to understand complex textbook diagrams, science concepts, and study notes through structured explanations, high-yield revision summaries, and active-recall quizzes powered by **Gemma 4 (`gemma-4-26b-a4b-it`)** via the official Google `google-genai` SDK.

---

## Key Features

1. **Three Dedicated Study Modes:**
   - **💡 Explain Mode:** Delivers beginner-friendly conceptual overviews, step-by-step breakdowns, and concrete real-world examples.
   - **📝 Revision Notes Mode:** Produces concise, high-yield bullet summaries, key terms, definitions, and memory anchors for fast exam review.
   - **🎯 Quiz Mode:** Generates exactly 5 active-recall practice questions paired with an answer key and explanations clearly separated from the questions.

2. **Multimodal Image-to-Learning:**
   - Ingests study diagrams, textbook figures, charts, and handwritten notes.
   - Accepts an optional student question to focus the AI's visual analysis (or general analysis if left blank).
   - Provides live client-side image preview with file details and easy image clearing.

3. **Defensive Validation & Security:**
   - **True Binary Inspection:** Examines binary magic byte signatures (PNG, JPEG, WEBP) to prevent spoofed uploads; never trusts filename extensions alone.
   - **Size Safeguards:** Enforces a 5 MB maximum upload limit.
   - **Ephemeral In-Memory Handling:** Uploaded images are streamed transiently in memory for inference and immediately closed; zero permanent or unencrypted disk storage.
   - **Credential Protection:** Server-side API key resolution with strict exclusion from Git tracking (`.env` is gitignored).
   - **Safe UI Rendering:** Responses are rendered as text nodes with CSS whitespace preservation, eliminating raw HTML injection risks.

---

## Architecture

```text
Browser (React + Vite SPA on port 5173)
   │
   │  Proxy (/api/*)
   ▼
FastAPI Backend (port 8000)
   ├── GET  /api/health        ──> Health check status
   ├── POST /api/study         ──> Text query handling (JSON)
   └── POST /api/study/image   ──> Multimodal image handling (Multipart)
         │
         ▼
   GemmaService
         │  (Official google-genai Python SDK)
         ▼
   Hosted Gemma 4 Model (gemma-4-26b-a4b-it)
```

---

## Project Structure

```text
EduVision-AI/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx          # EduVision AI branding and mission badge
│   │   │   ├── ModeSelector.jsx    # Mode picker (Explain, Revision Notes, Quiz)
│   │   │   ├── QuestionForm.jsx    # Text input, image dropzone, and preview card
│   │   │   └── ResponsePanel.jsx   # Safe text rendering, loaders, and error states
│   │   ├── services/
│   │   │   └── studyApi.js         # API client for JSON and Multipart requests
│   │   ├── App.jsx                 # Top-level state coordinator and layout
│   │   ├── main.jsx                # React DOM root entrypoint
│   │   └── styles.css              # Custom dark glassmorphic design system
│   ├── index.html                  # HTML5 base template with Google Fonts
│   ├── package.json                # Frontend dependencies (React 18, Vite)
│   └── vite.config.js              # Vite server with /api proxy to FastAPI
├── backend/
│   ├── app/
│   │   ├── __init__.py             # Python package marker
│   │   ├── main.py                 # FastAPI application with CORS & routes
│   │   ├── schemas.py              # Pydantic models (HealthResponse, StudyRequest, StudyResponse)
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── health.py           # GET /api/health
│   │   │   └── study.py            # POST /api/study and POST /api/study/image
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── gemma_service.py    # Gemma 4 SDK integration & binary MIME validation
│   │       └── history_service.py  # Session history placeholder (for future database step)
│   ├── requirements.txt            # Backend dependencies (FastAPI, Uvicorn, google-genai, etc.)
│   ├── .env.example                # Template for environment variables (no real keys)
│   ├── test_gemma.py               # Standalone SDK verification script
│   ├── verify_study_api.py         # Automated test suite for text study API
│   └── verify_multimodal_api.py    # Automated test suite for multimodal image API
├── .gitignore                      # Excludes node_modules, .venv, caches, .env
└── README.md                       # Complete project documentation and guide
```

---

## Getting Started on Windows PowerShell

### Prerequisites
- Node.js (v18+) and npm
- Python (3.11+)
- A Gemini API key (from Google AI Studio)

---

### 1. Backend Setup & Run

Open a Windows PowerShell terminal in the repository root:

```powershell
# Navigate to backend
cd backend

# Create virtual environment (if not already created)
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Copy .env.example to .env and insert your real GEMINI_API_KEY:
Copy-Item .env.example .env
# Edit backend/.env to set: GEMINI_API_KEY=your_actual_key_here

# Start the FastAPI server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Verify backend:
- Health check: `http://127.0.0.1:8000/api/health`
- Interactive OpenAPI Docs: `http://127.0.0.1:8000/docs`

---

### 2. Frontend Setup & Run

Open a **separate** Windows PowerShell terminal:

```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```

Open your browser at **`http://localhost:5173`**.

---

## API Endpoints Reference

| Endpoint | Method | Format | Description |
| :--- | :---: | :--- | :--- |
| `/api/health` | `GET` | JSON | System status check (`{"status": "ok", "service": "eduvision-api"}`) |
| `/api/study` | `POST` | JSON | Text-based study request (`{"question": "...", "mode": "explain"}`) |
| `/api/study/image` | `POST` | Multipart | Image study request with fields `file`, `mode`, and optional `question` |
| `/` | `GET` | JSON | Root API discovery endpoint |

---

## Tested Capabilities & Verification Results

The test suite was run and validated:

1. **Frontend Production Build (`npm run build`):**
   - Transformed 36 modules, generated optimized distribution bundle with **0 errors**.
2. **Standalone Gemma 4 Connectivity (`backend/test_gemma.py`):**
   - Verified communication with `gemma-4-26b-a4b-it` using `google-genai` SDK.
3. **Text Study Endpoint (`backend/verify_study_api.py`):**
   - Verified `GET /api/health` (200 OK).
   - Verified `POST /api/study` in `explain` mode with live physics question (200 OK).
   - Verified validation rejections for whitespace-only question (422) and invalid mode (422).
4. **Multimodal Image API (`backend/verify_multimodal_api.py`):**
   - Verified real plant cell diagram visual understanding across all three modes:
     - `explain`: Visually recognized and explained chloroplasts and vacuole.
     - `revision`: Extracted structured organelle bullet notes.
     - `quiz`: Created 5 active-recall questions based on the diagram labels.
   - Verified rejection of spoofed/corrupted image file (400 Bad Request).
   - Verified rejection of oversized upload > 5 MB (400 Bad Request).

---

## Supported Image Specifications
- **Supported Formats:** JPG, JPEG, PNG, WEBP.
- **Maximum File Size:** 5 MB.
- **Validation:** Binary magic byte header analysis (file extensions alone are rejected as insufficient).

---

## Current Status & Known Limitations
- **Single Image Input:** Accepts one image per query (batch uploads not currently supported).
- **In-Memory Ephemeral Sessions:** Image inputs and AI responses are held transiently in memory for the request duration and are not persisted to a database (MongoDB history integration is stubbed in `history_service.py` for future database milestone).
- **Deployment Status:** Currently configured and tested for local execution (`http://localhost:5173` frontend with `http://127.0.0.1:8000` backend); remote cloud hosting has not yet occurred.
