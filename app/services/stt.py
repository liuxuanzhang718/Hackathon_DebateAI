from google.cloud import speech
import io
from pathlib import Path
import logging
import os
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class STTService:
    def __init__(self):
        try:
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            logger.info(f"Initializing STT service with credentials from: {credentials_path}")
            
            if not credentials_path or not os.path.exists(credentials_path):
                logger.warning(f"Credentials file not found at: {credentials_path}")
                self.client = None
                return
                
            self.client = speech.SpeechClient()
            logger.info("Successfully initialized STT service")
        except Exception as e:
            logger.error(f"Failed to initialize STT service: {str(e)}\n{traceback.format_exc()}")
            self.client = None

    async def transcribe_audio(self, audio_file_path: Path) -> str:
        """
        Transcribe audio file to text using Google Cloud Speech-to-Text
        """
        if not self.client:
            raise RuntimeError("STT service not properly initialized")
            
        try:
            logger.info(f"Starting transcription of file: {audio_file_path}")
            
            # Verify file exists and is readable
            if not audio_file_path.exists():
                logger.error(f"Audio file not found: {audio_file_path}")
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
            if not os.access(audio_file_path, os.R_OK):
                logger.error(f"Audio file not readable: {audio_file_path}")
                raise PermissionError(f"Audio file not readable: {audio_file_path}")
            
            # Read the audio file
            try:
                with io.open(audio_file_path, "rb") as audio_file:
                    content = audio_file.read()
                logger.info(f"Successfully read audio file, size: {len(content)} bytes")
                
                if len(content) == 0:
                    logger.error("Audio file is empty")
                    raise ValueError("Audio file is empty")
                    
            except IOError as io_error:
                logger.error(f"Failed to read audio file: {str(io_error)}")
                raise IOError(f"Failed to read audio file: {str(io_error)}")

            # Configure the recognition settings
            try:
                config = speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=int(os.getenv('STT_SAMPLE_RATE', '22050')),
                    language_code=os.getenv('STT_LANGUAGE', 'en-US'),
                    enable_automatic_punctuation=True,
                    model="latest_long",
                    use_enhanced=True,
                    audio_channel_count=1,
                    enable_word_time_offsets=True,
                    profanity_filter=False
                )
                logger.info("Recognition config created")

                # Create the audio object
                audio = speech.RecognitionAudio(content=content)
                logger.info("Audio object created")
            except Exception as config_error:
                logger.error(f"Failed to create recognition config: {str(config_error)}")
                raise Exception(f"Failed to create recognition config: {str(config_error)}")

            # Perform the transcription
            logger.info("Starting recognition request")
            try:
                response = self.client.recognize(config=config, audio=audio)
                logger.info(f"Recognition completed, results: {response.results}")
            except Exception as recognition_error:
                logger.error(f"Recognition request failed: {str(recognition_error)}\n{traceback.format_exc()}")
                raise Exception(f"Speech recognition failed: {str(recognition_error)}")

            if not response.results:
                logger.error("No speech content detected in the audio")
                raise ValueError("No speech content detected in the audio")

            # Combine all transcripts from the results
            try:
                transcripts = []
                for result in response.results:
                    alternative = result.alternatives[0]
                    transcripts.append(alternative.transcript)
                    logger.info(f"Transcript confidence: {alternative.confidence}")
                
                final_text = " ".join(transcripts)
                if not final_text.strip():
                    logger.error("Empty transcript generated")
                    raise ValueError("Empty transcript generated")
                    
                logger.info(f"Transcription successful: {final_text}")
                return final_text
            except Exception as processing_error:
                logger.error(f"Failed to process transcription results: {str(processing_error)}")
                raise Exception(f"Failed to process transcription results: {str(processing_error)}")

        except Exception as e:
            logger.error(f"Error in transcribing audio: {str(e)}\n{traceback.format_exc()}")
            raise

# Initialize the STT service
stt_service = STTService() 