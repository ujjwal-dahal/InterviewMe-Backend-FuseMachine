from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.resume import ResumeInfo


InterviewType = Literal["technical", "behavioral", "mixed"]
Priority = Literal["high", "medium", "low"]
ResourceType = Literal["course", "documentation", "video", "article", "practice"]


class RoadmapLlmResource(BaseModel):
    title: str = Field(description="Name of the course, documentation, video, article, or practice resource")
    platform: str = Field(description="Platform or source, such as MDN, YouTube, or official documentation")
    type: ResourceType = Field(description="Kind of learning resource")


class RoadmapResource(RoadmapLlmResource):
    url: str = Field(description="Working search URL created by the backend")


class RoadmapItem(BaseModel):
    topic: str = Field(description="The interview topic to prepare")
    priority: Priority = Field(description="How important this topic is")
    why_it_matters: str = Field(description="Why this topic matters for the target role and interview")
    what_to_improve: str = Field(description="What is weak or missing in the resume for this topic")
    how_to_study: str = Field(description="A specific and practical way to study this topic")
    resources: list[RoadmapResource] = Field(
        default_factory=list,
        min_length=2,
        max_length=4,
        description="Two to four specific learning resources for this topic",
    )


class RoadmapResult(BaseModel):
    resume_info: ResumeInfo = Field(description="Structured information extracted from the resume")
    roadmap: list[RoadmapItem] = Field(default_factory=list, description="Personalized interview preparation topics")
    overall_focus: str = Field(default="", description="A short description of the main preparation focus")