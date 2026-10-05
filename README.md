# InterviewMe Backend

FastAPI backend for resume analysis and personalized interview roadmaps. It accepts PDF or DOCX resumes, extracts their text, and uses Groq through LangChain for structured responses.

```powershell
Copy-Item .env.example .env
# Put your Groq key in .env
uv sync
uv run uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. FastAPI's API reference is at `http://127.0.0.1:8000/docs`.

The Next.js frontend can call the API from `http://localhost:3000`. CORS is already enabled for that origin.

## Vercel deployment

The local `.env` file is not deployed to Vercel. In the Vercel project settings, add
`GROQ_API_KEY` under **Settings > Environment Variables** for the **Production**
environment, then redeploy the `master` branch. Keep `GROQ_MODEL` set to
`openai/gpt-oss-20b` unless you intentionally choose another Groq-supported model.

## API contract

### POST `/resume/analyze`

Request: `multipart/form-data` with one field:

| Field  | Type             | Description           |
| ------ | ---------------- | --------------------- |
| `file` | PDF or DOCX file | The resume to analyze |

Successful response: `200 OK`

```json
{
  "skills": ["Python", "FastAPI"],
  "projects": ["InterviewMe backend"],
  "experience": ["Backend developer at Example Company"],
  "education": ["BSc in Computer Science"],
  "summary": "Backend developer with experience building Python APIs."
}
```

All five fields are always present. The list fields are `string[]` and may be empty. `summary` is a string and may be empty when the resume does not contain enough information.

### POST `/roadmap/generate`

Request: `multipart/form-data` with these fields:

| Field            | Type                                  | Description                                 |
| ---------------- | ------------------------------------- | ------------------------------------------- |
| `file`           | PDF or DOCX file                      | The resume to analyze                       |
| `target_role`    | string                                | The job role the candidate is preparing for |
| `interview_type` | `technical`, `behavioral`, or `mixed` | The type of interview                       |

Successful response: `200 OK`

```json
{
  "resume_info": {
    "skills": ["Python", "FastAPI"],
    "projects": ["InterviewMe backend"],
    "experience": ["Backend developer at Example Company"],
    "education": ["BSc in Computer Science"],
    "summary": "Backend developer with experience building Python APIs."
  },
  "roadmap": [
    {
      "topic": "FastAPI fundamentals",
      "priority": "high",
      "why_it_matters": "FastAPI is central to the target backend role and will likely be discussed in a technical interview.",
      "what_to_improve": "The resume shows FastAPI experience but does not clearly demonstrate dependency management or testing.",
      "how_to_study": "Build a small API with validation and dependencies, add tests, and explain the request flow out loud.",
      "resources": [
        {
          "title": "FastAPI Official Documentation",
          "platform": "official documentation",
          "type": "documentation",
          "url": "https://www.google.com/search?q=FastAPI+Official+Documentation+official+documentation"
        },
        {
          "title": "REST API Practice",
          "platform": "roadmap.sh",
          "type": "practice",
          "url": "https://www.google.com/search?q=REST+API+Practice+roadmap.sh"
        }
      ]
    }
  ],
  "overall_focus": "Strengthen backend API design and system fundamentals."
}
```

`priority` is always one of `high`, `medium`, or `low`.

### Errors

Errors use the same shape so the frontend can display `detail`:

```json
{
  "detail": "Only PDF and DOCX files are supported."
}
```

- `422`: unsupported file, empty file, unreadable resume, or invalid form data
- `502`: resume analysis or roadmap generation failed while calling the LLM

## Curl examples

Analyze a resume:

```bash
curl -X POST http://127.0.0.1:8000/resume/analyze \
	-F "file=@./resume.pdf"
```

Generate a technical roadmap:

```bash
curl -X POST http://127.0.0.1:8000/roadmap/generate \
	-F "file=@./resume.pdf" \
	-F "target_role=Backend Software Engineer" \
	-F "interview_type=technical"
```

Generate a mixed roadmap from a DOCX file:

```bash
curl -X POST http://127.0.0.1:8000/roadmap/generate \
	-F "file=@./resume.docx" \
	-F "target_role=Full Stack Developer" \
	-F "interview_type=mixed"
```
