from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import hashlib

# Load environment variables from .env file
load_dotenv()
Base = declarative_base()

class Speech(Base):
    """
    SQLAlchemy model representing audio transcription data.
    Stores the unique hash of audio files and their transcribed content.
    """
    __tablename__ = 'speeches'
    
    id = Column(Integer, primary_key=True)
    file_hash = Column(String(64), unique=True, index=True)  # SHA-256 produces 64 character hashes
    content = Column(Text)

class Database:
    """
    Database access layer for audio transcriptions.
    Handles connection management and CRUD operations for transcribed speech data.
    """

    def __init__(self):
        """
        Initialize database connection using environment variables.
        Creates tables if they don't exist.
        """
        db_connection_string = os.getenv("db_connection_string")
        if not db_connection_string:
            raise ValueError("Database connection string not found in environment variables")
        
        self.engine = create_engine(db_connection_string)
        Base.metadata.create_all(self.engine)  # Create tables if they don't exist
        self.Session = sessionmaker(bind=self.engine)

    def create_audio_hash(self, audio_data):
        """
        Generates a unique SHA-256 hash for audio data.
        Used to identify duplicate audio files without storing the actual audio.
        
        Args:
            audio_data (bytes): Binary audio data to hash
            
        Returns:
            str: Hexadecimal string representation of the SHA-256 hash
        """
        if not audio_data:
            raise ValueError("No audio data provided")
        
        hasher = hashlib.sha256()
        hasher.update(audio_data)
        file_hash = hasher.hexdigest()
        
        return file_hash

    def add_to_database(self, speech):
        """
        Adds a new Speech record to the database.
        
        Args:
            speech (Speech): Speech object to add to database
            
        Raises:
            Exception: If database operation fails
        """
        session = self.Session()
        try:
            session.add(speech)
            session.commit()
        except Exception as e:
            session.rollback()  # Undo changes if error occurs
            raise e
        finally:
            session.close()  # Ensure connection is closed
            
    def get_speech_if_hash_exists(self, file_hash) -> Speech|None:
        """
        Check if transcription for a specific audio file already exists.
        
        Args:
            file_hash (str): SHA-256 hash of the audio file
            
        Returns:
            Speech|None: Speech object if found, None if not in database
        """
        session = self.Session()
        try:
            speech = session.query(Speech).filter_by(file_hash=file_hash).first()
            return speech
        finally:
            session.close()  # Ensure connection is closed