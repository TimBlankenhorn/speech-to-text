import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import tempfile

class Recognizer:
    def __init__(self):
        load_dotenv()
        self.region = os.getenv("region")
        self.api_key = os.getenv("api_key")
        
    async def convert_audio_file_to_path(self, audio_file):
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_file.filename.split('.')[-1]}")
        try:
            # Write content to the temporary file
            content = await audio_file.read()
            temp_file.write(content)
            temp_file.close()
            return temp_file.name
        except Exception as e:
            os.unlink(temp_file.name)
            raise e
    
    def handleSpeech(self, file_path):
        region = self.region
        api_key = self.api_key
        speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
        auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
            languages=["de-DE", "en-US"]
        )
        
        # Use file path directly instead of stream
        audio_config = speechsdk.audio.AudioConfig(filename=file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, 
            audio_config=audio_config, 
            auto_detect_source_language_config=auto_detect_source_language_config
        )
        
        # Process result as before
        result = speech_recognizer.recognize_once()
        
        # Clean up the temporary file
        try:
            os.unlink(file_path)
        except:
            pass
            
        # Check the result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return f"No speech could be recognized: {result.no_match_details}"
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            return f"Speech recognition canceled: {cancellation.reason}. Error details: {cancellation.error_details}"