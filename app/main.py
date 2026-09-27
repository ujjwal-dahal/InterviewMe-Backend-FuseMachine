from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.config import get_settings
from app.routers.resume import router as resume_router
from app.routers.roadmap import router as roadmap_router

settings = get_settings()
app = FastAPI(title="InterviewMe Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(resume_router)
app.include_router(roadmap_router)


@app.get("/", include_in_schema=False)
def homepage():
    homepage_file = Path(__file__).with_name("homepage.html")
    return FileResponse(homepage_file, media_type="text/html")


@app.get("/health")
def health_check():
    return {"status": "ok"}