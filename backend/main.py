from typing import Union

from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile, HTTPException
import tempfile
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/transcribe/")
async def transcribe_audio(audio_file: UploadFile):
    ending = audio_file.filename.lower().split(".")[-1]
    valid_types = ["wav", "mp3"]
    if not ending in valid_types:
        raise HTTPException(status_code=400, detail="File must be an audio file")
    return {
        "filename": audio_file.filename,
        "content_type": audio_file.content_type
    }