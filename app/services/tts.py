import os
import uuid
from pathlib import Path
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from ..config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        try:
            self.client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
            self.voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam pre-made voice
            logger.info("Successfully initialized TTS service")
        except Exception as e:
            logger.error(f"Failed to initialize TTS service: {str(e)}")
            raise

    async def text_to_speech(self, text: str) -> str:
        """
        Convert text to speech using ElevenLabs API and save the audio file
        Returns the relative path to the saved audio file as a string
        """
        try:
            logger.info("Starting text-to-speech conversion")
            
            # Create audio storage directory if it doesn't exist
            os.makedirs(settings.AUDIO_STORAGE_PATH, exist_ok=True)
            logger.info(f"Ensured audio storage directory exists: {settings.AUDIO_STORAGE_PATH}")

            # Generate a unique filename
            filename = f"{uuid.uuid4()}.mp3"
            output_path = Path(settings.AUDIO_STORAGE_PATH) / filename
            logger.info(f"Generated output path: {output_path}")

            # Convert text to speech
            logger.info("Calling ElevenLabs API")
            response = self.client.text_to_speech.convert(
                voice_id=self.voice_id,
                output_format="mp3_22050_32",
                text=text,
                model_id="eleven_turbo_v2_5",  # use the turbo model for low latency
                voice_settings=VoiceSettings(
                    stability=0.0,
                    similarity_boost=1.0,
                    style=0.0,
                    use_speaker_boost=True,
                )
            )
            logger.info("Received response from ElevenLabs API")

            # Save the audio file
            try:
                with open(output_path, "wb") as f:
                    for chunk in response:
                        if chunk:
                            f.write(chunk)
                logger.info(f"Successfully saved audio file to {output_path}")
            except Exception as save_error:
                logger.error(f"Failed to save audio file: {str(save_error)}")
                raise

            # Return the relative path as a string
            relative_path = str(Path("audio_storage") / filename)
            logger.info(f"Returning relative path: {relative_path}")
            return relative_path

        except Exception as e:
            logger.error(f"Error in text-to-speech conversion: {str(e)}")
            raise Exception(f"Error in text-to-speech conversion: {str(e)}")

# Initialize the TTS service
tts_service = TTSService() 