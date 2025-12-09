# utils/rag_chain.py
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Local embeddings (free forever)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vectorstore():
    db_path = "data/vector_db/medi_chromadb"
    return Chroma(persist_directory=db_path, embedding_function=embeddings)

def get_rag_chain():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    retriever = get_vectorstore().as_retriever(search_kwargs={"k": 6})

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a cautious medical assistant.
Use ONLY the context provided. Never make up information.
Never diagnose or prescribe.
Always end with: "Do not rely on my information; consult a healthcare professional. BITCH!"

Context: {context}"""),
        ("human", "{input}")
    ])

    question_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_chain)
    return rag_chain