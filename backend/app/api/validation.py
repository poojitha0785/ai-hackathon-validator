from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import db
from ..models import Evaluation
from ..security import user
from ..ai import analyze
from ..scoring import calc
from .ideas import owned
r=APIRouter(prefix="/ideas")
@r.post("/{idea_id}/validate")
async def validate(idea_id:int,s:AsyncSession=Depends(db),u=Depends(user)):
    i=await owned(idea_id,s,u);v=max(i.versions,key=lambda z:z.version_number);payload={"title":i.title,**{k:getattr(v,k) for k in ["problem","solution","target_users","features","impact","technology_preference","team_size","team_skill_level","hackathon_duration_hours","prototype","constraints"]}};a=await analyze(payload);scores=calc(a);s.add(Evaluation(idea_version_id=v.id,analysis_json=a,**scores));await s.commit();return {"version":v.version_number,"scores":scores,"analysis":a}
@r.get("/{idea_id}/evaluations")
async def evaluations(idea_id:int,s:AsyncSession=Depends(db),u=Depends(user)):
    i=await owned(idea_id,s,u);ids=[v.id for v in i.versions];rows=(await s.execute(__import__('sqlalchemy').select(Evaluation).where(Evaluation.idea_version_id.in_(ids)).order_by(Evaluation.created_at.desc()))).scalars().all();return [{"id":e.id,"idea_version_id":e.idea_version_id,"idea_quality_score":e.idea_quality_score,"build_feasibility_score":e.build_feasibility_score,"hackathon_readiness_score":e.hackathon_readiness_score,"analysis":e.analysis_json} for e in rows]
