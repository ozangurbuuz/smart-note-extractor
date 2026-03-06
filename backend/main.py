from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as summarize_router


app = FastAPI(
    title="Smart Note Extractor API",
    version="0.1.0",
    description="Extractive NLP summarization for PDF/TXT files.",
)

# Allow local frontend access during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summarize_router)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
