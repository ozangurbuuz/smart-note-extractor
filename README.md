# Smart Note Extractor

Smart Note Extractor is a full-stack NLP project where users upload a `PDF` or `TXT` file and receive:

1. A short summary
2. Bullet-point notes
3. Keywords

## Planning Docs

- MVP and RAG-ready implementation plan: `docs/MVP_RAG_READY_PLAN.md`

This MVP uses **traditional NLP only** (no OpenAI API, no paid AI services).

## Tech Stack

- Backend: FastAPI + Python
- Frontend: React + Vite + Tailwind CSS
- PDF Parsing: PyMuPDF
- NLP: nltk, scikit-learn, regex
- Database: none (MVP)

## Project Structure

```text
smart-note-extractor/
  backend/
    app/
      api/
        routes.py
      core/
        config.py
      schemas/
        response.py
      services/
        file_validation.py
        text_extraction.py
        text_cleaning.py
        sentence_splitter.py
        sentence_scoring.py
        summary_generation.py
        keyword_extraction.py
    main.py
    requirements.txt
  frontend/
    public/
    src/
      components/
        FileUploadForm.jsx
        ResultPanel.jsx
      services/
        api.js
      App.jsx
      main.jsx
      index.css
    index.html
    package.json
    vite.config.js
    tailwind.config.js
    postcss.config.js
  .gitignore
  README.md
```

## Backend Setup

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend runs on `http://localhost:8000`.

Health check endpoint:

```text
GET /health
```

Main endpoint:

```text
POST /summarize
```

Form-data fields:

- `file`: PDF or TXT
- `summary_type`: `balanced` or `keywords_first`
- `summary_length`: `short`, `medium`, or `long`

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`.

## Example API Response

```json
{
  "summary": "...",
  "notes": ["...", "..."],
  "keywords": ["...", "..."],
  "metadata": {
    "file_name": "example.pdf",
    "summary_type": "balanced",
    "summary_length": "medium",
    "sentence_count": 42
  }
}
```

## Suggested First Commits

1. `chore: initialize monorepo structure for smart-note-extractor`
2. `feat(backend): add modular NLP pipeline and /summarize endpoint`
3. `feat(frontend): add upload form, controls, and result panel`
4. `docs: add setup instructions and API usage examples`
