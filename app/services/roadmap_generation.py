from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from urllib.parse import quote_plus

from app.schemas.resume import ResumeInfo
from app.schemas.roadmap import (
    InterviewType,
    RoadmapItem,
    RoadmapLlmResource,
    RoadmapResource,
    RoadmapResult,
    Priority,
)
from app.services.llm import get_llm


class RoadmapLlmItem(BaseModel):
    topic: str
    priority: Priority
    why_it_matters: str
    what_to_improve: str
    how_to_study: str
    resources: list[RoadmapLlmResource] = Field(default_factory=list, min_length=2, max_length=4)


class RoadmapLlmAnswer(BaseModel):
    roadmap: list[RoadmapLlmItem] = Field(default_factory=list)
    overall_focus: str = ""


ROADMAP_SYSTEM_MESSAGE = """
You are a practical interview preparation coach. Create a personalized study
roadmap using the candidate's actual resume information, target role, and
interview type. Do not give generic advice.

For every roadmap item, return:
- topic and priority (high, medium, or low)
- why_it_matters: one short sentence connected to the role or interview
- what_to_improve: a specific weakness or missing evidence from the resume
- how_to_study: one concise, concrete action, such as solving practice
    problems and explaining the solution aloud
- resources: exactly two real, well-known resources, each with title,
    platform, and type

Return three or four high-value roadmap items. Keep every text field to one
or two sentences so the response stays focused and easy to follow.

Resources must be real and relevant. Use official documentation, well-known
courses, books, videos, articles, or practice sites. Do not return a url field.
The backend will create a safe search link from the title and platform.
The resource type must be exactly one of: course, documentation, video,
article, or practice. Do not use book or any other resource type.
"""


ROADMAP_PROMPT = """
Build the study roadmap for this candidate.

Target role: {target_role}
Interview type: {interview_type}
Resume information:
{resume_info}
"""


def generate_roadmap(
    resume_info: ResumeInfo,
    target_role: str,
    interview_type: InterviewType,
) -> RoadmapResult:
    prompt = ChatPromptTemplate.from_messages([
        ("system", ROADMAP_SYSTEM_MESSAGE),
        ("human", ROADMAP_PROMPT),
    ])
    structured_llm = get_llm().with_structured_output(RoadmapLlmAnswer).with_retry(
        stop_after_attempt=2,
    )
    answer = (prompt | structured_llm).invoke({
        "target_role": target_role,
        "interview_type": interview_type,
        "resume_info": resume_info.model_dump_json(),
    })

    roadmap = []
    for item in answer.roadmap:
        resources = []
        for resource in item.resources:
            resources.append(RoadmapResource(
                title=resource.title,
                platform=resource.platform,
                type=resource.type,
                url=build_resource_link(resource.title, resource.platform, resource.type),
            ))
        roadmap.append(RoadmapItem(
            topic=item.topic,
            priority=item.priority,
            why_it_matters=item.why_it_matters,
            what_to_improve=item.what_to_improve,
            how_to_study=item.how_to_study,
            resources=resources,
        ))

    return RoadmapResult(
        resume_info=resume_info,
        roadmap=roadmap,
        overall_focus=answer.overall_focus,
    )


def build_resource_link(title: str, platform: str, resource_type: str) -> str:
    search_text = quote_plus(f"{title} {platform}")
    if platform.lower() == "youtube" or resource_type == "video":
        return f"https://www.youtube.com/results?search_query={search_text}"
    return f"https://www.google.com/search?q={search_text}"