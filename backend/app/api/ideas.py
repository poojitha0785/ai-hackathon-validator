from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import db
from ..models import Idea,IdeaVersion
from ..schemas import CreateIdea,VersionIn
from ..security import user
r=APIRouter(prefix="/ideas")
async def owned(i,s,u):
    x=await s.scalar(select(Idea).options(selectinload(Idea.versions)).where(Idea.id==i,Idea.user_id==u.id))
    if not x: raise HTTPException(404,"Idea not found")
    return x
@r.post("")
async def create(x:CreateIdea,s:AsyncSession=Depends(db),u=Depends(user)):
    i=Idea(user_id=u.id,title=x.title.strip());s.add(i);await s.flush();s.add(IdeaVersion(idea_id=i.id,version_number=1,**x.version.model_dump()));await s.commit();return {"id":i.id,"title":i.title,"latest_version":1}
@r.get("")
async def listing(s:AsyncSession=Depends(db),u=Depends(user)):
    xs=(await s.execute(select(Idea).where(Idea.user_id==u.id).order_by(Idea.updated_at.desc()))).scalars().all();return [{"id":i.id,"title":i.title,"latest_version":await s.scalar(select(IdeaVersion.version_number).where(IdeaVersion.idea_id==i.id).order_by(IdeaVersion.version_number.desc()).limit(1))} for i in xs]
@r.get("/{idea_id}")
async def get(idea_id:int,s:AsyncSession=Depends(db),u=Depends(user)):
    i=await owned(idea_id,s,u);return {"id":i.id,"title":i.title,"versions":[{"id":v.id,"version_number":v.version_number,"problem":v.problem,"solution":v.solution,"features":v.features} for v in sorted(i.versions,key=lambda z:z.version_number)]}
@r.post("/{idea_id}/versions")
async def version(idea_id:int,x:VersionIn,s:AsyncSession=Depends(db),u=Depends(user)):
    i=await owned(idea_id,s,u);n=max([v.version_number for v in i.versions],default=0)+1;v=IdeaVersion(idea_id=i.id,version_number=n,**x.model_dump());s.add(v);await s.commit();return {"version_id":v.id,"version_number":n}
