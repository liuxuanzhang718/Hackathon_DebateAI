from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # OpenAI Configuration
    OPENAI_API_KEY: str
    
    # ElevenLabs Configuration
    ELEVENLABS_API_KEY: str
    
    # Audio Storage Configuration
    AUDIO_STORAGE_PATH: str = "audio_storage"
    
    # Google Cloud Configuration
    GOOGLE_APPLICATION_CREDENTIALS: str
    
    # Database Configuration (if needed)
    DATABASE_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set Google Cloud credentials environment variable
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.GOOGLE_APPLICATION_CREDENTIALS

settings = Settings() 