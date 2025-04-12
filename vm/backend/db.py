from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()
Base = declarative_base()

class Speech(Base):
    __tablename__ = 'speeches'
    
    id = Column(Integer, primary_key=True)
    file_hash = Column(String(64), unique=True, index=True)  # SHA-256 produces 64 character hashes
    content = Column(Text)

class Database:

    def __init__(self):
        db_connection_string = os.getenv("db_connection_string")
        if not db_connection_string:
            raise ValueError("Database connection string not found in environment variables")
        
        self.engine = create_engine(db_connection_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_audio_hash(self, audio_data):
        
        if not audio_data:
            raise ValueError("No audio data provided")
        
        hasher = hashlib.sha256()
        hasher.update(audio_data)
        file_hash = hasher.hexdigest()
        
        return file_hash

    def add_to_database(self, speech):
        
        session = self.Session()
        try:
            session.add(speech)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    def get_speech_if_hash_exists(self, file_hash)->Speech|None:
        session = self.Session()
        try:
            speech = session.query(Speech).filter_by(file_hash=file_hash).first()
            return speech
        finally:
            session.close()
        