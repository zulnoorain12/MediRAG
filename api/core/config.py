# api/core/config.py   ← FIXED PATH VERSION
from dotenv import load_dotenv
import os

# Load .env from project root (not inside api folder)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
env_path = os.path.join(project_root, ".env")
load_dotenv(env_path)

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in .env at project root!")

    PROJECT_NAME = "MediRAG API"
    VERSION = "2.0"
    # CORRECTED PATH — points to data/vector_db from project root
    DB_PATH = os.path.join(project_root, "data", "vector_db", "medi_chromadb")

settings = Settings()