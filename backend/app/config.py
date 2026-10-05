from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    secret_key:str
    database_url:str
    llm_base_url:str="https://api.openai.com/v1"
    llm_api_key:str=""
    llm_model:str="gpt-4o-mini"
    cors_origins:str="http://localhost:5173"
    rate_limit_per_minute:int=60
    access_token_minutes:int=120
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
@lru_cache
def settings(): return Settings()
