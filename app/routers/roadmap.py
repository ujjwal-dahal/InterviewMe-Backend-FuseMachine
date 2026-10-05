import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.roadmap import InterviewType, RoadmapResult
from app.services.resume_analysis import analyze_resume
from app.services.resume_reader import read_resume
from app.services.roadmap_generation import generate_roadmap


router = APIRouter(prefix="/roadmap", tags=["roadmap"])
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=RoadmapResult)
async def generate_roadmap_for_resume(
    file: UploadFile = File(...),
    target_role: str = Form(...),
    interview_type: InterviewType = Form(...),
):
    if not target_role.strip():
        raise HTTPException(status_code=422, detail="target_role cannot be empty.")

    try:
        resume_text = await read_resume(file)
        resume_info = analyze_resume(resume_text)
        return generate_roadmap(resume_info, target_role, interview_type)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except Exception as error:
        logger.exception("Roadmap generation failed")
        raise HTTPException(status_code=502, detail="Roadmap generation failed.") from error