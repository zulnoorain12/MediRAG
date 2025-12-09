import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
import shutil

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})

embeddings = get_embeddings()

def process_uploaded_files(uploaded_files):
    if not uploaded_files:
        st.warning("No files uploaded.")
        return 0

    docs = []
    temp_dir = "data/raw_docs/temp"
    os.makedirs(temp_dir, exist_ok=True)

    for file in uploaded_files:
        file_path = os.path.join(temp_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        st.info(f"Processing: {file.name}")

        try:
            if file.name.lower().endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            else:
                loader = TextLoader(file_path, encoding="utf-8")

            loaded_docs = loader.load()
            st.success(f"Extracted {len(loaded_docs)} pages from {file.name}")

            if loaded_docs:
                with st.expander(f"Preview {file.name}"):
                    st.text(loaded_docs[0].page_content[:500] + "...")

            docs.extend(loaded_docs)
        except Exception as e:
            st.error(f"Failed to read {file.name}: {e}")

    if not docs:
        st.error("No text extracted!")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return 0

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    st.info(f"Created {len(chunks)} chunks")

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="data/vector_db/medi_chromadb"
    )

    st.success(f"Indexed {len(chunks)} chunks!")
    st.balloons()
    shutil.rmtree(temp_dir, ignore_errors=True)
    return len(chunks)

st.title("Upload Medical Documents")
st.write("Upload PDF/TXT files (e.g., COVID, diabetes)")

uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=["pdf", "txt"])

if uploaded_files and st.button("Process & Index"):
    with st.spinner("Indexing..."):
        process_uploaded_files(uploaded_files)