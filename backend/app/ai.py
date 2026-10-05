import json,httpx
from fastapi import HTTPException
from .config import settings
PROMPT="""You evaluate a student hackathon idea. Return ONLY JSON with dimensions problem_clarity, innovation, impact, solution_quality, user_value, ethics, technical_feasibility, mvp_feasibility, time_feasibility, team_skill_match, dependency_risk. Each dimension must contain score 0-100, confidence High/Medium/Low, explanation, evidence array, improvement. Also return strengths, weaknesses, recommendations, risks, assumptions, mvp_features, remove_from_first_demo, effort_min_hours, effort_max_hours, recommended_stack object, and pitch object. Do not invent facts. dependency_risk is higher-is-worse. The system's aggregate scores are calculated by the backend."""
def fallback():
    def d(text): return {"score":50,"confidence":"Low","explanation":text,"evidence":["LLM key not configured"],"improvement":"Clarify this dimension with concrete evidence."}
    return {k:d("Conservative fallback assessment.") for k in ["problem_clarity","innovation","impact","solution_quality","user_value","ethics","technical_feasibility","mvp_feasibility","time_feasibility","team_skill_match","dependency_risk"]}|{"strengths":["Idea is ready for structured review."],"weaknesses":["Needs deeper evidence."],"recommendations":["Reduce first-demo scope.","Clarify user value."],"risks":["Scope risk."],"assumptions":["No hackathon rules supplied."],"mvp_features":["Core end-to-end workflow"],"remove_from_first_demo":["Non-essential advanced features"],"effort_min_hours":30,"effort_max_hours":42,"recommended_stack":{"frontend":"React + Vite + Tailwind","backend":"FastAPI","database":"PostgreSQL","ai":"OpenAI-compatible API"},"pitch":{"one_line_pitch":"An AI-assisted hackathon preparation platform.","demo_flow":["Submit idea","Validate","Improve"]}}
async def analyze(payload):
    s=settings()
    if not s.llm_api_key: return fallback()
    try:
        async with httpx.AsyncClient(timeout=90) as c:
            r=await c.post(s.llm_base_url.rstrip("/")+"/chat/completions",headers={"Authorization":f"Bearer {s.llm_api_key}"},json={"model":s.llm_model,"temperature":.1,"response_format":{"type":"json_object"},"messages":[{"role":"system","content":PROMPT},{"role":"user","content":json.dumps(payload)}]})
            r.raise_for_status(); return json.loads(r.json()["choices"][0]["message"]["content"])
    except Exception as e: raise HTTPException(502,f"AI provider error: {type(e).__name__}")
