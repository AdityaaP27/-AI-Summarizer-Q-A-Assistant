
## Overview

**AI Summarizer & Q\&A Assistant** is a two‐part web application that lets users:

* **Summarize** any webpage by URL into a concise 5-10 sentence summary plus key bullet points
* **Index** that content in Pinecone and **ask questions** interactively via a Retrieval-Augmented-Generation (RAG) pipeline using MistralAI embeddings

The backend is built with **FastAPI**, **LangChain**, **MistralAI**, and **Pinecone**, while the frontend uses **Streamlit**.

---

## Live-Demo

> Because Render’s free tier sleeps inactive services, please start the backend first:
> **Backend (starts slowly on cold start):**
> [https://ai-summarizer-qa-assistant.onrender.com/](https://ai-summarizer-qa-assistant.onrender.com/)
>
> Then open the main UI:
> **Streamlit Frontend:**
> [https://ai-summarizer-qa-assistant-ui.onrender.com/](https://ai-summarizer-qa-assistant-ui.onrender.com/)

---

## Features

* **URL Summarization**

  * Fetches page HTML, cleans boilerplate, and summarizes in 5-10 sentences
  * Extracts 5–10 key bullet points
* **Interactive Q\&A**

  * Chunks page text and indexes in Pinecone with MistralAI embeddings
  * Allows natural-language questions against the indexed content
* **Modular Architecture**

  * Clear separation of scraping, summarization, indexing, and Q\&A
  * Easily swap in different LLMs, embeddings, or vector stores

---

## Architecture

```
┌────────────┐    ┌───────────┐    ┌────────────┐    ┌───────────┐
│ Streamlit  │──▶│ FastAPI   │──▶│ LangChain  │──▶│ MistralAI │
│ Frontend   │   │ (Backend) │   │ Pipelines  │   │  LLM &     │
│ (UI)       │◀──│           │◀──│ & Pinecone │◀──│ Embeddings │
└────────────┘    └───────────┘    └────────────┘    └───────────┘
```

1. **Scraper**: `requests` + BeautifulSoup
2. **Summarizer**: LangChain LLMChain with MistralAI
3. **Vector Store**: Pinecone + `langchain_pinecone`
4. **Q\&A Chain**: LangChain RetrievalQA
5. **UI**: Streamlit

---

## Getting Started

### Prerequisites

* Python 3.10+
* [Pinecone API Key](https://www.pinecone.io/)
* [MistralAI API Key](https://mistral.ai/)

### Repository Structure

```
ai_summarizer/
├── backend/
│   ├── app/
│     ├── config.py        # env var loader
│     ├── embed.py         # MistralAI embeddings wrapper
│     ├── main.py          # FastAPI endpoints
│     ├── scraper.py       # HTML fetch & cleaning
│     ├── summarizer.py    # LangChain summarization chains
│     └── vectorstore.py   # Pinecone init & connection
│   
└── frontend/
│    └── app.py               # Streamlit UI
│    
└── requirements.txt
```

### Environment Variables

Create `backend/.env`:

```dotenv
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=your_pinecone_env
PINECONE_INDEX_NAME=your_index_name

MISTRAL_API_KEY=your_mistralai_key
API_BASE=your_api
```

### Installation & Run

1. **Backend**

   ```bash
   cd ai_summarizer
   python -m venv .venv
   source .venv/bin/activate      # macOS/Linux
   .venv\Scripts\activate         # Windows
   pip install -r requirements.txt
   uvicorn backend.app.main:app --reload --app-dir .
   ```

2. **Frontend**

   ```bash
   cd ai_summarizer
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   streamlit run frontend/app.py
   ```

---

## Usage

1. **Summarize**

   * Enter a URL and click **Summarize**
   * View the summary and key points
2. **Index for Q\&A**

   * Click **Index for Q\&A** to store embeddings in Pinecone
3. **Ask Questions**

   * Type a question and click **Ask** to get answers sourced from the page

---


