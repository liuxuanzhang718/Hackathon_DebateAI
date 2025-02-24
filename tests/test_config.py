import pytest
import os
from app.config import Settings
from dotenv import load_dotenv

def test_settings_from_env():
    # Set test environment variables
    os.environ["OPENAI_API_KEY"] = "test_openai_key"
    os.environ["ELEVENLABS_API_KEY"] = "test_elevenlabs_key"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "test_credentials_path"
    
    # Initialize settings
    settings = Settings()
    
    # Verify settings are loaded correctly
    assert settings.OPENAI_API_KEY == "test_openai_key"
    assert settings.ELEVENLABS_API_KEY == "test_elevenlabs_key"
    assert settings.GOOGLE_APPLICATION_CREDENTIALS == "test_credentials_path"
    assert os.getenv("GOOGLE_APPLICATION_CREDENTIALS") == "test_credentials_path"

def test_settings_missing_env():
    # Clear relevant environment variables
    for key in ["OPENAI_API_KEY", "ELEVENLABS_API_KEY", "GOOGLE_APPLICATION_CREDENTIALS"]:
        if key in os.environ:
            del os.environ[key]
    
    # Verify that exception is raised when required environment variables are missing
    with pytest.raises(Exception):
        settings = Settings() 