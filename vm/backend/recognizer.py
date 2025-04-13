import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import tempfile

class Recognizer:
    """
    A class that handles speech recognition using Azure Cognitive Services.
    Processes audio files and converts speech to text.
    """
    def __init__(self):
        # Load environment variables and initialize Azure credentials
        load_dotenv()
        self.region = os.getenv("region")  # Azure service region
        self.api_key = os.getenv("api_key")  # Azure subscription key
        
    async def convert_audio_file_to_path(self, audio_file):
        """
        Converts an uploaded file to a temporary file on disk.
        
        Args:
            audio_file: FastAPI UploadFile object containing the audio data
            
        Returns:
            str: Path to the temporary file
            
        Raises:
            Exception: If file processing fails
        """
        # Create a temporary file with the correct extension
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_file.filename.split('.')[-1]}")
        try:
            await audio_file.seek(0)  # Reset file pointer to beginning
            # Write uploaded content to the temporary file
            content = await audio_file.read()
            temp_file.write(content)
            temp_file.close()
            return temp_file.name
        except Exception as e:
            # Clean up the temporary file in case of error
            os.unlink(temp_file.name)
            raise e
    
    def handleSpeech(self, file_path):
        """
        Processes an audio file using Azure Speech recognition.
        
        Args:
            file_path (str): Path to the audio file
            
        Returns:
            str: Transcribed text or error message
        """
        # Configure Azure Speech service
        region = self.region
        api_key = self.api_key
        speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
        
        # Configure automatic language detection for German and English
        auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
            languages=["de-DE", "en-US"]
        )
        
        # Create audio configuration from file
        audio_config = speechsdk.audio.AudioConfig(filename=file_path)
        
        # Initialize speech recognizer with configurations
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, 
            audio_config=audio_config, 
            auto_detect_source_language_config=auto_detect_source_language_config
        )
        
        # Perform synchronous speech recognition
        result = speech_recognizer.recognize_once()
        
        # Clean up the temporary file after processing
        try:
            os.unlink(file_path)
        except:
            pass  # Ignore errors during cleanup
            
        # Handle different recognition results
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            # Successful speech recognition
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            # No speech detected or recognized
            return f"No speech could be recognized: {result.no_match_details}"
        elif result.reason == speechsdk.ResultReason.Canceled:
            # Recognition was canceled
            cancellation = result.cancellation_details
            return f"Speech recognition canceled: {cancellation.reason}. Error details: {cancellation.error_details}"