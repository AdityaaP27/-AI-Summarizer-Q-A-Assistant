# backend/app/vectorstore.py

import logging
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from .config import PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX
from .embed import get_embedder

logger = logging.getLogger(__name__)

def init_vector_store(documents):
    try:
        # 1) Init Pinecone client
        pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)  # :contentReference[oaicite:1]{index=1}

        # 2) Delete existing index if present
        existing = pc.list_indexes().names()
        if PINECONE_INDEX in existing:
            pc.delete_index(PINECONE_INDEX)

        # 3) Create new index
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=1024,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=PINECONE_ENV),
        )  # :contentReference[oaicite:2]{index=2}

        # 4) Connect to index
        index = pc.Index(PINECONE_INDEX)

        # 5) Embedder instance (not function)
        embedder = get_embedder()

        # 6) Wrap with LangChain store
        vector_store = PineconeVectorStore(
            index=index,
            embedding=embedder,          # pass the object, not embedder.embed_query :contentReference[oaicite:3]{index=3}
            text_key="page_content"
        )

        # 7) Upsert documents
        vector_store.add_documents(documents)  # now uses embedder.embed_documents under the hood :contentReference[oaicite:4]{index=4}

        return vector_store

    except Exception:
        logger.exception("Failed to init or upsert vector store")
        raise


def get_vector_store() -> PineconeVectorStore:
    """
    Connects to an existing Pinecone index and returns
    a LangChain PineconeVectorStore wrapper, without
    altering the index contents.
    """
    pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    index = pc.Index(PINECONE_INDEX)
    embedder = get_embedder()
    return PineconeVectorStore(
        index=index,
        embedding=embedder,
        text_key="page_content",
    )