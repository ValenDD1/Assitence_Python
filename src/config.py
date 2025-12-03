import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv("GEMINI_API_KEY")
    ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Asistente")
    
    VOICE_RATE = 170
    VOICE_VOLUME = 1.0

if not Config.API_KEY:
    raise ValueError("FATAL: No se encontró la GEMINI_API_KEY en el archivo .env")