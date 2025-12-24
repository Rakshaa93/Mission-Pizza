# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MCP_URL: str = "http://localhost:8001"
    CALENDAR_MCP_URL: str = "http://localhost:8002"
    UI_PORT: int = 9000
    
    class Config:
        env_file = ".env"