from langchain_core.prompts import ChatPromptTemplate

from app.schemas.resume import ResumeInfo
from app.services.llm import get_llm


RESUME_PROMPT = """
Read the resume below and return the information in the requested structure.
Only include information that appears in the resume. Use empty lists when a
section is missing. Keep the summary short and factual.

Resume:
{resume_text}
"""


def analyze_resume(resume_text: str) -> ResumeInfo:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You extract useful, factual information from resumes."),
        ("human", RESUME_PROMPT),
    ])
    structured_llm = get_llm().with_structured_output(ResumeInfo)
    result = (prompt | structured_llm).invoke({"resume_text": resume_text})
    return result