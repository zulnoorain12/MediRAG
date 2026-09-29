# utils/document_processor.py   ← FINAL 100% WORKING VERSION (Dec 2025)
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from loguru import logger
import shutil
import streamlit as st  # Only for warning inside function

# Local, free, unlimited embeddings (no internet, no quota)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}  # change to 'cuda' if you have GPU
)

def get_vectorstore():
    db_path = "data/vector_db/medi_chromadb"
    if os.path.exists(db_path) and os.listdir(db_path):
        return Chroma(persist_directory=db_path, embedding_function=embeddings)
    else:
        os.makedirs(db_path, exist_ok=True)
        return Chroma(persist_directory=db_path, embedding_function=embeddings)

def process_uploaded_files(uploaded_files):
    if not uploaded_files:
        return 0

    docs = []
    temp_dir = "data/raw_docs/temp"
    os.makedirs(temp_dir, exist_ok=True)

    for file in uploaded_files:
        file_path = os.path.join(temp_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        try:
            if file.name.lower().endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            else:
                loader = TextLoader(file_path, encoding="utf-8")
            docs.extend(loader.load())
        except Exception as e:
            logger.error(f"Failed to load {file.name}: {e}")

    if not docs:
        st.warning("No readable text found in uploaded files.")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return 0

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Index with FREE local embeddings → auto-saves, no .persist() needed
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory="data/vector_db/medi_chromadb"
    )
    # .persist() REMOVED — not needed in Chroma 0.5+

    logger.success(f"Successfully indexed {len(splits)} chunks from {len(uploaded_files)} file(s)")
    st.success(f"Indexed {len(splits)} chunks into knowledge base!")
    st.balloons()

    shutil.rmtree(temp_dir, ignore_errors=True)
    return len(splits)