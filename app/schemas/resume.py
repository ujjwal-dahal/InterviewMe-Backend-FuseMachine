from pydantic import BaseModel, Field


class ResumeInfo(BaseModel):
    skills: list[str] = Field(default_factory=list, description="Skills found in the resume")
    projects: list[str] = Field(default_factory=list, description="Projects found in the resume")
    experience: list[str] = Field(default_factory=list, description="Work experience entries from the resume")
    education: list[str] = Field(default_factory=list, description="Education entries from the resume")
    summary: str = Field(default="", description="A short summary of the candidate")