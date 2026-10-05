import logging,time
from collections import defaultdict,deque
from contextlib import asynccontextmanager
from fastapi import FastAPI,Request,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import settings
from .db import engine,Base
from .api import auth,ideas,validation
from . import models
logging.basicConfig(level=logging.INFO);log=logging.getLogger("validator");s=settings();buckets=defaultdict(deque)
@asynccontextmanager
async def life(app):
    async with engine.begin() as c: await c.run_sync(Base.metadata.create_all)
    yield;await engine.dispose()
app=FastAPI(title="AI Hackathon Idea Validator API",version="1.0.0",lifespan=life)
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in s.cors_origins.split(",")],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.middleware("http")
async def cross(request:Request,call_next):
    if request.url.path not in ["/health","/docs","/openapi.json","/redoc"]:
        key=request.client.host if request.client else "unknown";now=time.monotonic();q=buckets[key]
        while q and now-q[0]>60:q.popleft()
        if len(q)>=s.rate_limit_per_minute: raise HTTPException(429,"Rate limit exceeded")
        q.append(now)
    resp=await call_next(request);resp.headers["X-Content-Type-Options"]="nosniff";resp.headers["X-Frame-Options"]="DENY";resp.headers["Referrer-Policy"]="strict-origin-when-cross-origin";return resp
@app.exception_handler(Exception)
async def errors(request,exc): log.exception("Unhandled error");return JSONResponse(500,{"detail":"Internal server error"})
app.include_router(auth.r,prefix="/api");app.include_router(ideas.r,prefix="/api");app.include_router(validation.r,prefix="/api")
@app.get("/health")
async def health(): return {"status":"ok"}
