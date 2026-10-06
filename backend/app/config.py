from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
BASE_DIR=Path(__file__).resolve().parents[1]
class Settings(BaseSettings):
    secret_key:str
    database_url:str
    llm_base_url:str="https://integrate.api.nvidia.com/v1"
    llm_api_key:str="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"
    llm_model:str="nemotron-3-super-120b-a12b"

    cors_origins:str="http://localhost:5173"
    rate_limit_per_minute:int=60
    access_token_minutes:int=120
    model_config=SettingsConfigDict(env_file=BASE_DIR / ".env",extra="ignore")
@lru_cache
def settings(): return Settings()
