from io import BytesIO
from pathlib import Path

from docx import Document
from fastapi import UploadFile
from pypdf import PdfReader


def get_file_extension(file: UploadFile) -> str:
    return Path(file.filename or "").suffix.lower()


async def read_resume(file: UploadFile) -> str:
    extension = get_file_extension(file)
    if extension not in {".pdf", ".docx"}:
        raise ValueError("Only PDF and DOCX files are supported.")

    contents = await file.read()
    if not contents:
        raise ValueError("The uploaded file is empty.")

    try:
        if extension == ".pdf":
            reader = PdfReader(BytesIO(contents))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        else:
            document = Document(BytesIO(contents))
            text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    except Exception as error:
        raise ValueError("Could not read text from the uploaded file.") from error

    if not text.strip():
        raise ValueError("No readable text was found in the uploaded file.")
    return text.strip()