import os
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import settings

CHROMA_DIR = "db/"

if not os.path.exists(CHROMA_DIR):
    raise RuntimeError("Vector store not found. Please run `prepare_vectorstore.py` first.")

embeddings = GoogleGenerativeAIEmbeddings(
    model=settings.google_embeddings_model,
    google_api_key=settings.google_api_key,
)

vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
