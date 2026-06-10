"""
Configuration management for ARIA system
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # Groq Configuration
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
    
    # Tavily Configuration
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    
    # System Configuration
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Paths
    project_root: Path = Path(__file__).parent.parent
    data_dir: Path = project_root / "data"
    chroma_db_path: Path = Path(os.getenv("CHROMA_DB_PATH", "./data/memories"))
    metrics_db_path: Path = Path(os.getenv("METRICS_DB_PATH", "./data/metrics.db"))
    
    # Feature Flags
    enable_web_search: bool = os.getenv("ENABLE_WEB_SEARCH", "True").lower() == "true"
    enable_code_execution: bool = os.getenv("ENABLE_CODE_EXECUTION", "True").lower() == "true"
    enable_memory: bool = os.getenv("ENABLE_MEMORY", "True").lower() == "true"
    
    # Agent Configuration
    agent_timeout: int = 60
    max_retries: int = 3
    retry_delay: float = 1.0
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

def ensure_directories():
    """Create necessary directories"""
    settings.data_dir.mkdir(exist_ok=True)
    settings.chroma_db_path.mkdir(parents=True, exist_ok=True)