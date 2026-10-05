from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase
from .config import settings
s=settings(); engine=create_async_engine(s.database_url,pool_pre_ping=True,pool_recycle=1800); Session=async_sessionmaker(engine,expire_on_commit=False,class_=AsyncSession)
class Base(DeclarativeBase): pass
async def db():
    async with Session() as session: yield session
