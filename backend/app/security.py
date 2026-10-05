from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from pwdlib import PasswordHash
from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .config import settings
from .db import db
from .models import User
ph=PasswordHash.recommended(); bearer=HTTPBearer(); s=settings()
def hash_pw(p): return ph.hash(p)
def verify_pw(p,h): return ph.verify(p,h)
def token(uid): return jwt.encode({"sub":str(uid),"exp":datetime.now(timezone.utc)+timedelta(minutes=s.access_token_minutes)},s.secret_key,algorithm="HS256")
async def user(c:HTTPAuthorizationCredentials=Depends(bearer),session:AsyncSession=Depends(db)):
    try: uid=int(jwt.decode(c.credentials,s.secret_key,algorithms=["HS256"])["sub"])
    except (JWTError,KeyError,ValueError): raise HTTPException(401,"Invalid or expired token")
    u=await session.scalar(select(User).where(User.id==uid))
    if not u: raise HTTPException(401,"User not found")
    return u
