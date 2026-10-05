from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import db
from ..models import User
from ..schemas import Register,Login
from ..security import hash_pw,verify_pw,token
r=APIRouter(prefix="/auth")
@r.post("/register")
async def register(x:Register,s:AsyncSession=Depends(db)):
    if await s.scalar(select(User).where(User.email==x.email.lower())): raise HTTPException(409,"Email already registered")
    u=User(name=x.name.strip(),email=x.email.lower(),password_hash=hash_pw(x.password)); s.add(u); await s.commit(); await s.refresh(u); return {"access_token":token(u.id),"user":{"id":u.id,"name":u.name,"email":u.email,"role":u.role}}
@r.post("/login")
async def login(x:Login,s:AsyncSession=Depends(db)):
    u=await s.scalar(select(User).where(User.email==x.email.lower()))
    if not u or not verify_pw(x.password,u.password_hash): raise HTTPException(401,"Invalid email or password")
    return {"access_token":token(u.id),"user":{"id":u.id,"name":u.name,"email":u.email,"role":u.role}}
