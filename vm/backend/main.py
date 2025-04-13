from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import Database, Speech
from recognizer import Recognizer
app = FastAPI()

# Configure CORS to allow cross-origin requests
# This is important for enabling frontend applications to communicate with our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (in production, specify exact origins)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Counters for monitoring and analytics purposes
# Track how many times each processing method is used
usedDBCounter = 0      # Tracks database cache hits
usedRecognizerCounter = 0  # Tracks speech recognition usage

# Endpoint for monitoring dashboard to retrieve usage statistics
# Returns counts of database vs. recognizer usage
@app.get("/origins")
def get_origins():
    return {
        "DB": usedDBCounter,
        "Recognizer": usedRecognizerCounter
    }

# Root endpoint for API health check
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Main transcription endpoint
# Handles uploading audio files, processing, and returning transcribed text
@app.post("/transcribe/")
async def transcribe_audio(audio_file: UploadFile):
    global usedDBCounter
    global usedRecognizerCounter
    
    # Validate file format - only accept WAV files
    ending = audio_file.filename.lower().split(".")[-1]
    valid_types = ["wav"]
    if not ending in valid_types:
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    # Create database connection
    database = Database()
    
    # Calculate hash from audio file content to use as unique identifier
    file_hash = database.create_audio_hash(await audio_file.read())
    
    # Check if this audio has been processed before
    speech = database.get_speech_if_hash_exists(file_hash)
    if speech:
        # If hash exists, retrieve cached transcription from database
        print("Hash exists in database")
        text = speech.content
        origin = "database"
        usedDBCounter += 1  # Increment database usage counter
    else:
        # If hash doesn't exist, process the audio with speech recognition
        print("Hash does not exist in database")
        recognizer = Recognizer()
        
        # Convert uploaded file to a path the recognizer can process
        file_path = await recognizer.convert_audio_file_to_path(audio_file)
        
        # Perform speech recognition
        text = recognizer.handleSpeech(file_path)
        
        # Store the new transcription in the database for future requests
        new_speech = Speech(file_hash=file_hash, content=text)
        database.add_to_database(new_speech)
        
        origin = "speech recognizer"
        usedRecognizerCounter += 1  # Increment recognizer usage counter
    
    print(text)  # Log the transcription result
    
    # Return response with transcription data and metadata
    return {
        "filename": audio_file.filename,
        "content": text,
        "origin": origin,
    }