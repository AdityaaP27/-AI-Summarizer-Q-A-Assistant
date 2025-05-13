# backend/app/summarizer.py

import os
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_mistralai import ChatMistralAI
from .config import MISTRAL_API_KEY


os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY

def build_documents(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.create_documents([text])

def load_llm():
    return ChatMistralAI(
            model="mistral-large-latest",
            temperature=0,
            max_retries=2,
            )

def summarize_text(docs: list[Document]) -> tuple[str, list[str]]:
    llm = load_llm()

    summary_prompt = PromptTemplate.from_template(
        "Summarize the following content in 5-10 sentences:\n{text}"
    )
    keypoints_prompt = PromptTemplate.from_template(
        "Extract 5-10 key points from this text as bullet points:\n{text}"
    )

    summary_chain = LLMChain(llm=llm, prompt=summary_prompt)
    keypoints_chain = LLMChain(llm=llm, prompt=keypoints_prompt)

    combined_text = "\n".join([doc.page_content for doc in docs])

    summary = summary_chain.run(text=combined_text)
    keypoints = keypoints_chain.run(text=combined_text)

    return summary.strip(), keypoints.strip().split("\n")
