# backend/app/schemas.py
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env in project root

def get_env(key: str) -> str:
    v = os.getenv(key)
    if not v:
        raise RuntimeError(f"Missing env var {key}")
    return v


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

