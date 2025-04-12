from typing import Union

from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import Database, Speech
import tempfile
import os
from recognizer import Recognizer
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (in production, specify exact origins)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/transcribe/")
async def transcribe_audio(audio_file: UploadFile):
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
    else:
        
        print("Hash does not exist in database")
        recognizer = Recognizer()
        file_path = await recognizer.convert_audio_file_to_path(audio_file)
        text = recognizer.handleSpeech(file_path)
        new_speech = Speech(file_hash=file_hash, content=text)
        database.add_to_database(new_speech)
        origin = "speech recognizer"
    print(text)
    
    return {
        "filename": audio_file.filename,
        "content": text,
        "origin": origin,
    }