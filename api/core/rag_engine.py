import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from .config import settings

DB_PATH = settings.DB_PATH

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'})

def get_retriever():
    vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 8})

def get_rag_chain():
    llm = ChatGoogleGenerativeAI(
        model=settings.MODEL_NAME,
        temperature=0.1,
        api_key=settings.GEMINI_API_KEY
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful and cautious medical assistant.
Answer the user's question clearly, thoroughly, and accurately using the context provided below.
If the context does not contain sufficient information to answer the question, clearly state that you do not have enough information in the provided documents.
Always conclude your response with: "Please consult a qualified doctor."

Context:
{context}"""),
        ("human", "{input}")
    ])

    question_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(get_retriever(), question_chain)
    return rag_chain

_rag_chain = None
def get_chain():
    global _rag_chain
    if _rag_chain is None:
        _rag_chain = get_rag_chain()
    return _rag_chain