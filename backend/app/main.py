# backend/app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain_mistralai import ChatMistralAI
import logging

logger = logging.getLogger(__name__)
from .scraper import fetch_and_clean_text
from .summarizer import build_documents, summarize_text
from .vectorstore import init_vector_store, get_vector_store
from .config import PINECONE_INDEX

# Schemas
class URLRequest(BaseModel):
    url: HttpUrl

class SummaryResponse(BaseModel):
    summary: str
    key_points: list[str]

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

app = FastAPI()

@app.post("/summarize", response_model=SummaryResponse)
def summarize(request: URLRequest):
    try:
        text = fetch_and_clean_text(request.url)
        docs = build_documents(text)
        summary, key_points = summarize_text(docs)
        return SummaryResponse(summary=summary, key_points=key_points)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/index", status_code=204)
def index_url(request: URLRequest):
    try:
        text = fetch_and_clean_text(request.url)
        docs = build_documents(text)
        init_vector_store(docs)  # now works without embed_documents error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
def query_qa(request: QueryRequest):
    try:
        store = get_vector_store()

        llm = ChatMistralAI(model="mistral-large-latest", temperature=0.0)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=store.as_retriever(search_kwargs={"k": 5}),
            return_source_documents=True
        )

        result = qa_chain(request.question)
        answer = result["result"]
        sources = [doc.metadata.get("source", "") for doc in result["source_documents"]]

        return QueryResponse(answer=answer, sources=sources)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Q&A failed: {e}")
