from fastapi import FastAPI
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import Database, Speech
from recognizer import Recognizer
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (in production, specify exact origins)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

usedDBCounter = 0
usedRecognizerCounter = 0

#value for grafana dashboard
@app.get("/origins")
def get_origins():
    return {
        "DB": usedDBCounter,
        "Recognizer": usedRecognizerCounter
    }


@app.get("/")
def read_root():
    return {"Hello": "World"}


 
@app.post("/transcribe/")
async def transcribe_audio(audio_file: UploadFile):
    global usedDBCounter
    global usedRecognizerCounter
    
    ending = audio_file.filename.lower().split(".")[-1]
    valid_types = ["wav"]
    if not ending in valid_types:
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    database = Database()
    file_hash = database.create_audio_hash(await audio_file.read())
    
    speech = database.get_speech_if_hash_exists(file_hash)
    if speech:
        print("Hash exists in database")
        text = speech.content
        origin = "database"
        usedDBCounter += 1
    else:
        
        print("Hash does not exist in database")
        recognizer = Recognizer()
        file_path = await recognizer.convert_audio_file_to_path(audio_file)
        text = recognizer.handleSpeech(file_path)
        new_speech = Speech(file_hash=file_hash, content=text)
        database.add_to_database(new_speech)
        origin = "speech recognizer"
        usedRecognizerCounter += 1
    print(text)
    
    return {
        "filename": audio_file.filename,
        "content": text,
        "origin": origin,
    }