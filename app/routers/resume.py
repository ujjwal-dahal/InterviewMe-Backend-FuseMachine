import logging

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.resume import ResumeInfo
from app.services.resume_analysis import analyze_resume
from app.services.resume_reader import read_resume


router = APIRouter(prefix="/resume", tags=["resume"])
logger = logging.getLogger(__name__)


@router.post("/analyze", response_model=ResumeInfo)
async def analyze_uploaded_resume(file: UploadFile = File(...)):
    try:
        resume_text = await read_resume(file)
        return analyze_resume(resume_text)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except Exception as error:
        logger.exception("Resume analysis failed")
        raise HTTPException(status_code=502, detail="Resume analysis failed.") from error