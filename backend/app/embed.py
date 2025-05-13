# backend/app/embed.py

import os
from langchain_mistralai import MistralAIEmbeddings
from .config import MISTRAL_API_KEY

# Ensure the Mistral API key is set in the environment for the embeddings client
os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY

def get_embedder():
    """
    Returns a callable embedding function compatible with LangChainVectorStore.
    """
    return MistralAIEmbeddings()
