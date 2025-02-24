from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Server Configuration
    host: str
    port: int
    debug: bool

    # OpenAI Configuration
    OPENAI_API_KEY: str
    
    # ElevenLabs Configuration
    ELEVENLABS_API_KEY: str
    
    # Audio Storage Configuration
    AUDIO_STORAGE_PATH: str
    TEMP_STORAGE_PATH: str
    
    # Google Cloud Configuration
    GOOGLE_APPLICATION_CREDENTIALS: str
    
    # Logging Configuration
    LOG_LEVEL: str
    LOG_FILE: str

    # STT Configuration
    STT_LANGUAGE: str
    STT_SAMPLE_RATE: int

    # TTS Configuration
    TTS_VOICE_ID: str
    TTS_MODEL_ID: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.GOOGLE_APPLICATION_CREDENTIALS:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.GOOGLE_APPLICATION_CREDENTIALS

settings = Settings() 