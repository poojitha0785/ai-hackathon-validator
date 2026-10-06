import json
import httpx

from fastapi import HTTPException

from .config import settings


PROMPT = """You evaluate a student hackathon idea.

Return ONLY valid JSON with these dimensions:
problem_clarity,
innovation,
impact,
solution_quality,
user_value,
ethics,
technical_feasibility,
mvp_feasibility,
time_feasibility,
team_skill_match,
dependency_risk.

Each dimension must contain:
- score: 0-100
- confidence: High, Medium, or Low
- explanation
- evidence: array
- improvement

Also return:
- strengths
- weaknesses
- recommendations
- risks
- assumptions
- mvp_features
- remove_from_first_demo
- effort_min_hours
- effort_max_hours
- recommended_stack object
- pitch object

Do not invent facts.

dependency_risk is higher-is-worse.

The system's aggregate scores are calculated by the backend.
"""


def fallback():
    def d(text):
        return {
            "score": 50,
            "confidence": "Low",
            "explanation": text,
            "evidence": ["LLM key not configured"],
            "improvement": "Clarify this dimension with concrete evidence."
        }

    return {
        k: d("Conservative fallback assessment.")
        for k in [
            "problem_clarity",
            "innovation",
            "impact",
            "solution_quality",
            "user_value",
            "ethics",
            "technical_feasibility",
            "mvp_feasibility",
            "time_feasibility",
            "team_skill_match",
            "dependency_risk"
        ]
    } | {
        "strengths": [
            "Idea is ready for structured review."
        ],
        "weaknesses": [
            "Needs deeper evidence."
        ],
        "recommendations": [
            "Reduce first-demo scope.",
            "Clarify user value."
        ],
        "risks": [
            "Scope risk."
        ],
        "assumptions": [
            "No hackathon rules supplied."
        ],
        "mvp_features": [
            "Core end-to-end workflow"
        ],
        "remove_from_first_demo": [
            "Non-essential advanced features"
        ],
        "effort_min_hours": 30,
        "effort_max_hours": 42,
        "recommended_stack": {
            "frontend": "React + Vite + Tailwind",
            "backend": "FastAPI",
            "database": "PostgreSQL",
            "ai": "OpenAI-compatible API"
        },
        "pitch": {
            "one_line_pitch": "An AI-assisted hackathon preparation platform.",
            "demo_flow": [
                "Submit idea",
                "Validate",
                "Improve"
            ]
        }
    }


async def analyze(payload):
    s = settings()

    # Temporary debugging information.
    # API key is intentionally NOT printed.
    print("LLM BASE URL:", s.llm_base_url)
    print("LLM MODEL:", s.llm_model)
    print("LLM KEY LOADED:", bool(s.llm_api_key))

    if not s.llm_api_key:
        return fallback()

    try:
        url = s.llm_base_url.rstrip("/") + "/chat/completions"

        print("LLM URL:", url)

        async with httpx.AsyncClient(timeout=120) as c:
            r = await c.post(
                url,
                headers={
                    "Authorization": f"Bearer {s.llm_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": s.llm_model,
                    "messages": [
                        {
                            "role": "system",
                            "content": PROMPT
                        },
                        {
                            "role": "user",
                            "content": json.dumps(payload)
                        }
                    ],
                    "temperature": 0.2,
                    "top_p": 0.95,
                    "max_tokens": 8000,
                    "reasoning_effort": "low",
                    "response_format": {
                        "type": "json_object"
                    }
                }
            )

            r.raise_for_status()

            result = r.json()

            print("AI RESPONSE STATUS:", r.status_code)

            content = result["choices"][0]["message"].get("content")

            print("AI CONTENT:", content)
            print(
                "AI REASONING:",
                bool(
                    result["choices"][0]["message"].get(
                        "reasoning_content"
                    )
                )
            )

            if not content:
                raise HTTPException(
                    status_code=502,
                    detail="AI provider returned empty content"
                )

            try:
                return json.loads(content)

            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=502,
                    detail=f"AI provider returned invalid JSON: {str(e)}"
                )

    except httpx.HTTPStatusError as e:
        detail = e.response.text

        raise HTTPException(
            status_code=502,
            detail=(
                f"AI provider error: HTTP "
                f"{e.response.status_code} - {detail}"
            )
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=(
                f"AI provider error: "
                f"{type(e).__name__} - {str(e)}"
            )
        )